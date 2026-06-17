#!/usr/bin/env python3
"""Verify structural completion of a Git conflict resolution.

Checks unresolved index entries, conflict markers in changed text files,
`git diff --check`, and optional project validation commands. It does not stage,
commit, reset, clean, or otherwise modify Git state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


START_RE = re.compile(r"^<<<<<<<(?:\s|$)")
BASE_RE = re.compile(r"^\|\|\|\|\|\|\|(?:\s|$)")
SEP_RE = re.compile(r"^=======$")
END_RE = re.compile(r"^>>>>>>>(?:\s|$)")


class GitError(RuntimeError):
    pass


def run(cmd: list[str] | str, *, cwd: Path, shell: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def git(args: list[str], *, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    proc = run(["git", *args], cwd=cwd)
    if check and proc.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc


def nul_paths(args: list[str], repo_root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [p.decode("utf-8", "surrogateescape") for p in proc.stdout.split(b"\0") if p]


def changed_paths(repo_root: Path) -> list[str]:
    paths: set[str] = set()
    for args in (
        ["diff", "--name-only", "-z"],
        ["diff", "--cached", "--name-only", "-z"],
        ["ls-files", "--others", "--exclude-standard", "-z"],
    ):
        paths.update(nul_paths(args, repo_root))
    return sorted(paths)


def scan_markers(repo_root: Path, rel_paths: list[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rel in rel_paths:
        path = repo_root / rel
        if not path.is_file():
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            findings.append({"path": rel, "kind": "read_error", "detail": str(exc)})
            continue
        if b"\x00" in data[:8192]:
            continue
        lines = data.decode("utf-8", "replace").splitlines()
        depth = 0
        for number, line in enumerate(lines, start=1):
            kind: str | None = None
            if START_RE.match(line):
                kind = "start"
                depth += 1
            elif BASE_RE.match(line):
                kind = "base"
            elif SEP_RE.match(line):
                kind = "separator"
            elif END_RE.match(line):
                kind = "end"
                depth = max(0, depth - 1)
            if kind:
                findings.append({"path": rel, "line": number, "kind": kind, "text": line[:200]})
        if depth:
            findings.append({"path": rel, "kind": "unclosed_conflict", "depth": depth})
    return findings


def diff_check(repo_root: Path, cached: bool) -> dict[str, Any]:
    args = ["diff"] + (["--cached"] if cached else []) + ["--check"]
    proc = git(args, cwd=repo_root, check=False)
    return {
        "name": "staged_diff_check" if cached else "worktree_diff_check",
        "command": "git " + " ".join(args),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "passed": proc.returncode == 0,
    }


def run_validation_commands(repo_root: Path, commands: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for command in commands:
        proc = run(command, cwd=repo_root, shell=True)
        results.append(
            {
                "command": command,
                "returncode": proc.returncode,
                "passed": proc.returncode == 0,
                "stdout": proc.stdout[-12000:],
                "stderr": proc.stderr[-12000:],
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Path inside the Git repository")
    parser.add_argument(
        "--command",
        action="append",
        default=[],
        help="Project validation command to run; repeat for multiple commands",
    )
    parser.add_argument("--json", dest="json_output", help="Write complete report to this JSON path")
    parser.add_argument("--no-marker-scan", action="store_true", help="Skip changed-file conflict marker scan")
    args = parser.parse_args()

    try:
        repo = Path(args.repo).resolve()
        repo_root = Path(git(["rev-parse", "--show-toplevel"], cwd=repo).stdout.strip()).resolve()
        unresolved = nul_paths(["diff", "--name-only", "--diff-filter=U", "-z"], repo_root)
        changed = changed_paths(repo_root)
        markers = [] if args.no_marker_scan else scan_markers(repo_root, changed)
        structural_checks = [diff_check(repo_root, cached=False), diff_check(repo_root, cached=True)]
        command_results = run_validation_commands(repo_root, args.command)

        report: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repository_root": str(repo_root),
            "unresolved_files": unresolved,
            "changed_files_scanned": changed,
            "marker_findings": markers,
            "structural_checks": structural_checks,
            "validation_commands": command_results,
        }
        passed = (
            not unresolved
            and not markers
            and all(item["passed"] for item in structural_checks)
            and all(item["passed"] for item in command_results)
        )
        report["passed"] = passed

        if args.json_output:
            out = Path(args.json_output).resolve()
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + os.linesep, encoding="utf-8")

        print(f"Repository: {repo_root}")
        print(f"Unresolved files: {len(unresolved)}")
        for path in unresolved:
            print(f"  - {path}")
        print(f"Conflict-marker findings: {len(markers)}")
        for item in markers[:30]:
            location = f":{item.get('line')}" if item.get("line") else ""
            print(f"  - {item['path']}{location} [{item['kind']}]")
        for check in structural_checks:
            print(f"{check['command']}: {'PASS' if check['passed'] else 'FAIL'}")
            if check["stdout"]:
                print(check["stdout"])
            if check["stderr"]:
                print(check["stderr"], file=sys.stderr)
        for result in command_results:
            print(f"{result['command']}: {'PASS' if result['passed'] else 'FAIL'}")
            if result["stdout"]:
                print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr)
        print(f"Overall: {'PASS' if passed else 'FAIL'}")
        return 0 if passed else 1
    except (GitError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
