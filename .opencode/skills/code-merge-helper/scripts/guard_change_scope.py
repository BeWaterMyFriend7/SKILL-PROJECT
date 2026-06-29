#!/usr/bin/env python3
"""Check that current repository changes stay within a merge plan whitelist.

Accepts a Markdown plan file (single output of code-merge-helper).
Extracts the JSON execution contract from the appendix A fenced code block.

The script is read-only. It reports changed paths outside allowed_changes and
separately lists pre-existing protected changes declared by the plan.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def extract_json_from_markdown(md_path: Path) -> dict:
    """Extract JSON execution contract from appendix A fenced code block.

    Reads raw bytes for UTF-8 safety, then locates the appendix A JSON block.
    Prefers the JSON block immediately following the appendix A header when present.
    """
    raw_bytes = md_path.read_bytes()
    try:
        content_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as ude:
        raise ValueError(f"Invalid UTF-8 in {md_path}: {ude}") from ude
    if '\ufffd' in content_text:
        raise ValueError(f"Unicode replacement characters found in {md_path}; file encoding is corrupted")

    # Try to anchor to appendix A header first
    appendix_idx = content_text.rfind("附录 A")
    if appendix_idx >= 0:
        search_from = content_text[appendix_idx:]
    else:
        search_from = content_text

    pattern = re.compile(r'```json\s*\n(.*?)\n```', re.DOTALL)
    matches = pattern.findall(search_from)
    if not matches:
        # Fallback: search whole document
        matches = pattern.findall(content_text)
    if not matches:
        raise ValueError(f"No fenced JSON block found in {md_path}")
    # Take the first json block after appendix A (or last in document as fallback)
    raw_json = matches[0] if appendix_idx >= 0 else matches[-1]
    return json.loads(raw_json)


def run_git(repo: Path, args: list[str], binary: bool = False):
    return subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, encoding=None if binary else "utf-8",
        errors=None if binary else "replace", check=False,
    )


def nul_paths(repo: Path, args: list[str]) -> set[str]:
    p = run_git(repo, args, binary=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace").strip())
    return {x.decode("utf-8", "surrogateescape") for x in p.stdout.split(b"\0") if x}


def changed_paths(repo: Path) -> set[str]:
    result: set[str] = set()
    result |= nul_paths(repo, ["diff", "--name-only", "-z"])
    result |= nul_paths(repo, ["diff", "--cached", "--name-only", "-z"])
    result |= nul_paths(repo, ["ls-files", "--others", "--exclude-standard", "-z"])
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", required=True, help="Path to plan Markdown file (JSON extracted from appendix A)")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json-output")
    args = ap.parse_args()
    try:
        plan_path = Path(args.plan).resolve()
        plan = extract_json_from_markdown(plan_path)
        repo = Path(args.repo).resolve()
        root_proc = run_git(repo, ["rev-parse", "--show-toplevel"])
        if root_proc.returncode != 0:
            raise RuntimeError(root_proc.stderr.strip())
        root = Path(root_proc.stdout.strip()).resolve()

        allowed: set[str] = set()
        for action in plan.get("allowed_changes", []):
            path = action.get("path")
            if path:
                allowed.add(path)
            if action.get("action") == "rename" and action.get("from_path"):
                allowed.add(action["from_path"])

        protected = set(plan.get("repository", {}).get("existing_worktree_changes", []))
        changed = changed_paths(root)
        unexpected = changed - allowed - protected
        planned_changed = changed & allowed
        protected_present = changed & protected
        planned_missing = allowed - changed

        report = {
            "repository_root": str(root),
            "allowed_paths": sorted(allowed),
            "changed_paths": sorted(changed),
            "planned_changed_paths": sorted(planned_changed),
            "protected_preexisting_paths": sorted(protected_present),
            "unexpected_paths": sorted(unexpected),
            "planned_paths_not_currently_changed": sorted(planned_missing),
            "passed": not unexpected,
        }
        if args.json_output:
            out = Path(args.json_output).resolve()
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print(f"Repository: {root}")
        print(f"Allowed paths: {len(allowed)}")
        print(f"Changed paths: {len(changed)}")
        print(f"Unexpected paths: {len(unexpected)}")
        for p in sorted(unexpected):
            print(f"  - {p}")
        if protected_present:
            print("Protected pre-existing changes (not owned by agent):")
            for p in sorted(protected_present):
                print(f"  - {p}")
        print(f"Overall: {'PASS' if not unexpected else 'FAIL'}")
        return 0 if not unexpected else 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
