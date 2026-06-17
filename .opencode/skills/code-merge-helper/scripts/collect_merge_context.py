#!/usr/bin/env python3
"""Collect read-only Git conflict context for semantic merge analysis.

The script does not modify the worktree or index. By default it stores a JSON
report under the repository's Git metadata directory so it does not dirty the
working tree.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class GitError(RuntimeError):
    pass


def run_git(args: list[str], *, cwd: Path, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
        errors="replace" if text else None,
        check=False,
    )
    if check and proc.returncode != 0:
        stderr = proc.stderr.strip() if isinstance(proc.stderr, str) else proc.stderr.decode("utf-8", "replace")
        raise GitError(f"git {' '.join(args)} failed: {stderr}")
    return proc


def git_text(args: list[str], *, cwd: Path, check: bool = True) -> str:
    return run_git(args, cwd=cwd, check=check, text=True).stdout.strip()


def resolve_git_path(repo_root: Path, name: str) -> Path:
    raw = git_text(["rev-parse", "--git-path", name], cwd=repo_root)
    path = Path(raw)
    return path if path.is_absolute() else (repo_root / path).resolve()


def detect_operation(repo_root: Path) -> dict[str, Any]:
    git_dir_raw = git_text(["rev-parse", "--git-dir"], cwd=repo_root)
    git_dir = Path(git_dir_raw)
    if not git_dir.is_absolute():
        git_dir = (repo_root / git_dir).resolve()

    candidates = [
        ("merge", resolve_git_path(repo_root, "MERGE_HEAD")),
        ("cherry-pick", resolve_git_path(repo_root, "CHERRY_PICK_HEAD")),
        ("revert", resolve_git_path(repo_root, "REVERT_HEAD")),
        ("rebase", git_dir / "rebase-merge"),
        ("rebase", git_dir / "rebase-apply"),
    ]
    operation = "none"
    marker: Path | None = None
    for name, path in candidates:
        if path.exists():
            operation = name
            marker = path
            break

    heads: dict[str, str] = {}
    for label, name in (
        ("merge_head", "MERGE_HEAD"),
        ("cherry_pick_head", "CHERRY_PICK_HEAD"),
        ("revert_head", "REVERT_HEAD"),
        ("orig_head", "ORIG_HEAD"),
    ):
        p = resolve_git_path(repo_root, name)
        if p.is_file():
            value = p.read_text(encoding="utf-8", errors="replace").strip().splitlines()
            if value:
                heads[label] = value[0]

    return {
        "type": operation,
        "marker": str(marker) if marker else None,
        "heads": heads,
        "git_dir": str(git_dir),
    }


def stage_entries(repo_root: Path, path: str) -> dict[str, dict[str, Any]]:
    raw = run_git(["ls-files", "-u", "-z", "--", path], cwd=repo_root, text=False).stdout
    result: dict[str, dict[str, Any]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, _, filename = record.partition(b"\t")
        parts = metadata.decode("ascii", "replace").split()
        if len(parts) != 3:
            continue
        mode, blob, stage = parts
        result[stage] = {
            "mode": mode,
            "blob": blob,
            "path": filename.decode("utf-8", "surrogateescape"),
        }
    return result


def stage_summary(repo_root: Path, path: str, stage: int, entry: dict[str, Any] | None) -> dict[str, Any] | None:
    if entry is None:
        return None
    proc = run_git(["show", f":{stage}:{path}"], cwd=repo_root, check=False, text=False)
    if proc.returncode != 0:
        return {**entry, "read_error": proc.stderr.decode("utf-8", "replace").strip()}
    data: bytes = proc.stdout
    binary = b"\x00" in data[:8192]
    summary: dict[str, Any] = {
        **entry,
        "bytes": len(data),
        "binary": binary,
    }
    if not binary:
        text = data.decode("utf-8", "replace")
        summary["lines"] = len(text.splitlines())
    return summary


def extract_conflict_hunks(path: Path, max_lines_per_hunk: int = 80) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    data = path.read_bytes()
    if b"\x00" in data[:8192]:
        return []
    lines = data.decode("utf-8", "replace").splitlines()
    hunks: list[dict[str, Any]] = []
    start: int | None = None
    for idx, line in enumerate(lines, start=1):
        if line.startswith("<<<<<<<") and start is None:
            start = idx
        elif line.startswith(">>>>>>>") and start is not None:
            end = idx
            snippet_end = min(end, start + max_lines_per_hunk - 1)
            snippet = lines[start - 1 : snippet_end]
            if snippet_end < end:
                snippet.append(f"... <truncated {end - snippet_end} lines> ...")
            hunks.append({"start_line": start, "end_line": end, "snippet": snippet})
            start = None
    if start is not None:
        hunks.append({"start_line": start, "end_line": None, "snippet": lines[start - 1 : start - 1 + max_lines_per_hunk]})
    return hunks


def format_log(repo_root: Path, revision_range: str | None, path: str, limit: int) -> list[dict[str, str]]:
    args = [
        "log",
        f"-n{limit}",
        "--date=iso-strict",
        "--format=%H%x1f%an%x1f%ae%x1f%ad%x1f%s",
    ]
    if revision_range:
        args.append(revision_range)
    else:
        args.append("--all")
    args.extend(["--", path])
    proc = run_git(args, cwd=repo_root, check=False)
    if proc.returncode != 0:
        return []
    commits: list[dict[str, str]] = []
    for line in proc.stdout.splitlines():
        parts = line.split("\x1f", 4)
        if len(parts) == 5:
            sha, author, email, date, subject = parts
            commits.append({"sha": sha, "author": author, "email": email, "date": date, "subject": subject})
    return commits


def merge_ranges(repo_root: Path, operation: dict[str, Any]) -> tuple[str | None, dict[str, str]]:
    head = git_text(["rev-parse", "HEAD"], cwd=repo_root)
    labels = {"head": head}
    merge_head = operation.get("heads", {}).get("merge_head")
    if operation.get("type") == "merge" and merge_head:
        proc = run_git(["merge-base", head, merge_head], cwd=repo_root, check=False)
        if proc.returncode == 0:
            base = proc.stdout.strip()
            labels.update({"common_base": base, "stage_2_revision": head, "stage_3_revision": merge_head})
            return base, labels
    return None, labels


def collect(repo: Path, log_limit: int) -> dict[str, Any]:
    repo_root = Path(git_text(["rev-parse", "--show-toplevel"], cwd=repo)).resolve()
    operation = detect_operation(repo_root)
    base, revisions = merge_ranges(repo_root, operation)
    branch = git_text(["symbolic-ref", "--short", "-q", "HEAD"], cwd=repo_root, check=False) or "DETACHED"
    status = git_text(["status", "--porcelain=v2", "--branch"], cwd=repo_root, check=False)
    conflicts_raw = run_git(["diff", "--name-only", "--diff-filter=U", "-z"], cwd=repo_root, text=False).stdout
    conflict_paths = [p.decode("utf-8", "surrogateescape") for p in conflicts_raw.split(b"\0") if p]

    files: list[dict[str, Any]] = []
    for rel in conflict_paths:
        entries = stage_entries(repo_root, rel)
        file_info: dict[str, Any] = {
            "path": rel,
            "status": git_text(["status", "--short", "--", rel], cwd=repo_root, check=False),
            "conflict_hunks": extract_conflict_hunks(repo_root / rel),
            "stages": {
                "common_base": stage_summary(repo_root, rel, 1, entries.get("1")),
                "stage_2": stage_summary(repo_root, rel, 2, entries.get("2")),
                "stage_3": stage_summary(repo_root, rel, 3, entries.get("3")),
            },
            "recent_history_all": format_log(repo_root, None, rel, log_limit),
        }
        if base and revisions.get("stage_2_revision") and revisions.get("stage_3_revision"):
            file_info["history_from_common_base"] = {
                "stage_2": format_log(repo_root, f"{base}..{revisions['stage_2_revision']}", rel, log_limit),
                "stage_3": format_log(repo_root, f"{base}..{revisions['stage_3_revision']}", rel, log_limit),
            }
        files.append(file_info)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(repo_root),
        "branch": branch,
        "head": revisions.get("head"),
        "operation": operation,
        "revisions": revisions,
        "status_porcelain_v2": status.splitlines(),
        "conflict_count": len(files),
        "files": files,
        "notes": [
            "Stage numbers are reported without assuming business meaning.",
            "Commit metadata is evidence, not proof of author intent.",
            "The script is read-only with respect to the worktree and index.",
        ],
    }


def default_output(repo: Path) -> Path:
    root = Path(git_text(["rev-parse", "--show-toplevel"], cwd=repo)).resolve()
    git_dir_raw = git_text(["rev-parse", "--git-dir"], cwd=root)
    git_dir = Path(git_dir_raw)
    if not git_dir.is_absolute():
        git_dir = (root / git_dir).resolve()
    return git_dir / "codex-merge-review" / "context.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Path inside the Git repository")
    parser.add_argument("--output", help="Output JSON path; defaults under Git metadata")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout instead of writing a file")
    parser.add_argument("--log-limit", type=int, default=12, help="Maximum commits collected per history query")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    try:
        report = collect(repo, max(1, args.log_limit))
        payload = json.dumps(report, ensure_ascii=False, indent=2)
        if args.stdout:
            print(payload)
        else:
            output = Path(args.output).resolve() if args.output else default_output(repo)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(payload + os.linesep, encoding="utf-8")
            print(output)
        return 0
    except (GitError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
