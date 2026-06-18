#!/usr/bin/env python3

"""Validate a semantic merge plan and optionally compare it with live Git state.

Accepts a Markdown plan file (single output of code-merge-helper).
Extracts the JSON execution contract from the appendix A fenced code block.

Uses only the Python standard library. It never modifies the worktree or index.

Modes:

  --pre-merge    Skip operation/conflict/stage-blob checks (use during review phase).

  --repo <path>  Full repo consistency check (use during execution phase).

"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ALLOWED_STATUS = {"WAITING_FOR_APPROVAL", "APPROVED", "IMPLEMENTING", "IMPLEMENTED", "VERIFIED", "BLOCKED", "SUPERSEDED"}
ALLOWED_APPROVAL = {"WAITING_FOR_APPROVAL", "APPROVED", "REJECTED"}
ALLOWED_ACTIONS = {"modify", "add", "delete", "rename", "regenerate"}
REQUIRED_TOP = ["schema_version", "plan_id", "status", "report_path", "generated_at", "repository", "git_snapshot", "approval", "decisions", "allowed_changes", "execution_steps", "validations", "stop_conditions", "prohibited_actions"]

def extract_json_from_markdown(md_path: Path) -> dict[str, Any]:
    """Extract JSON execution contract from appendix A fenced code block.
    
    Reads raw bytes for UTF-8 safety, then locates the appendix A JSON block.
    Prefers the JSON block immediately following the appendix A header when present.
    """
    raw_bytes = md_path.read_bytes()
    try:
        content_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as ude:
        raise ValueError(f"Invalid UTF-8 in {md_path}: {ude}") from ude
    if '�' in content_text:
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

def git(repo: Path, *args: str, check: bool = True) -> str:

    p = subprocess.run(["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")

    if check and p.returncode != 0:

        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")

    return p.stdout.strip()

def detect_operation(repo: Path) -> tuple[str, str | None]:

    checks = [

        ("merge", "MERGE_HEAD"),

        ("cherry-pick", "CHERRY_PICK_HEAD"),

        ("revert", "REVERT_HEAD"),

    ]

    for name, marker in checks:

        path = Path(git(repo, "rev-parse", "--git-path", marker))

        if not path.is_absolute():

            path = repo / path

        if path.is_file():

            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

            return name, lines[0].strip() if lines else None

    git_dir = Path(git(repo, "rev-parse", "--git-dir"))

    if not git_dir.is_absolute():

        git_dir = repo / git_dir

    if (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists():

        return "rebase", None

    return "none", None

def unresolved(repo: Path) -> list[str]:

    raw = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U", "-z"], cwd=repo, stdout=subprocess.PIPE).stdout

    return sorted(p.decode("utf-8", "surrogateescape") for p in raw.split(b"\0") if p)

def stage_blobs(repo: Path) -> dict[str, dict[str, str]]:

    raw = subprocess.run(["git", "ls-files", "-u", "-z"], cwd=repo, stdout=subprocess.PIPE).stdout

    out: dict[str, dict[str, str]] = {}

    for record in raw.split(b"\0"):

        if not record:

            continue

        meta, _, path = record.partition(b"\t")

        parts = meta.decode("ascii", "replace").split()

        if len(parts) != 3:

            continue

        _, blob, stage = parts

        rel = path.decode("utf-8", "surrogateescape")

        out.setdefault(rel, {})[stage] = blob

    return out

def require(obj: dict[str, Any], keys: list[str], where: str, errors: list[str]) -> None:

    for key in keys:

        if key not in obj:

            errors.append(f"{where}: missing required field '{key}'")

def validate_structure(plan: dict[str, Any]) -> list[str]:

    errors: list[str] = []

    require(plan, REQUIRED_TOP, "plan", errors)

    if plan.get("schema_version") != "1.0": errors.append("plan.schema_version must be '1.0'")

    if plan.get("status") not in ALLOWED_STATUS: errors.append("plan.status is invalid")

    approval = plan.get("approval", {})

    if not isinstance(approval, dict):

        errors.append("plan.approval must be an object")

        approval = {}

    require(approval, ["status", "scope"], "plan.approval", errors)

    if approval.get("status") not in ALLOWED_APPROVAL: errors.append("plan.approval.status is invalid")

    if approval.get("status") == "APPROVED" and plan.get("status") not in {"APPROVED", "IMPLEMENTING", "IMPLEMENTED", "VERIFIED", "BLOCKED"}:

        errors.append("approved approval status is inconsistent with plan.status")

    if plan.get("status") == "APPROVED" and approval.get("status") != "APPROVED":

        errors.append("plan.status APPROVED requires approval.status APPROVED")

    decisions = plan.get("decisions", [])

    actions = plan.get("allowed_changes", [])

    steps = plan.get("execution_steps", [])

    validations = plan.get("validations", [])

    if not isinstance(decisions, list) or not decisions: errors.append("plan.decisions must be a non-empty array")

    if not isinstance(actions, list) or not actions: errors.append("plan.allowed_changes must be a non-empty array")

    if not isinstance(steps, list) or not steps: errors.append("plan.execution_steps must be a non-empty array")

    if not isinstance(validations, list) or not validations: errors.append("plan.validations must be a non-empty array")

    decision_ids: set[str] = set()

    behavior_ids: set[str] = set()

    validation_ids: set[str] = set()

    action_ids: set[str] = set()

    paths: set[str] = set()

    for i, d in enumerate(decisions if isinstance(decisions, list) else []):

        if not isinstance(d, dict): continue

        did = d.get("id")

        if not did:

            errors.append(f"decision[{i}]: missing id")

            continue

        if did in decision_ids: errors.append(f"duplicate decision id: {did}")

        decision_ids.add(did)

        for p in d.get("preserve", []):

            if not isinstance(p, dict): continue

            bid = p.get("behavior_id")

            if not bid: errors.append(f"decision {did}: preserve entry missing behavior_id")

            else:

                if bid in behavior_ids: errors.append(f"duplicate behavior_id: {bid}")

                behavior_ids.add(bid)

    for i, a in enumerate(actions if isinstance(actions, list) else []):

        if not isinstance(a, dict): continue

        aid = a.get("id")

        if not aid:

            errors.append(f"allowed_change[{i}]: missing id")

            continue

        if aid in action_ids: errors.append(f"duplicate action id: {aid}")

        action_ids.add(aid)

        if a.get("action") not in ALLOWED_ACTIONS: errors.append(f"action {aid}: invalid action type '{a.get('action')}'")

        path = a.get("path")

        if not path: errors.append(f"action {aid}: missing path")

        else: paths.add(path)

    for i, v in enumerate(validations if isinstance(validations, list) else []):

        if not isinstance(v, dict): continue

        vid = v.get("id")

        if not vid:

            errors.append(f"validation[{i}]: missing id")

            continue

        if vid in validation_ids: errors.append(f"duplicate validation id: {vid}")

        validation_ids.add(vid)

    for i, s in enumerate(steps if isinstance(steps, list) else []):

        if not isinstance(s, dict): continue

        if not s.get("order"): errors.append(f"execution_step[{i}]: missing order")

    step_orders: set[int] = set()

    covered_action_ids: set[str] = set()

    for s in (steps if isinstance(steps, list) else []):

        if not isinstance(s, dict): continue

        order = s.get("order")

        if isinstance(order, int):

            step_orders.add(order)

        for aid in s.get("action_ids", []):

            covered_action_ids.add(aid)

            if aid not in action_ids: errors.append(f"execution step {s.get('order')}: unknown action id {aid}")

    for d in decisions if isinstance(decisions, list) else []:

        if not isinstance(d, dict): continue

        for p in d.get("preserve", []):

            if not isinstance(p, dict): continue

            for vid in p.get("validation_ids", []):

                if vid not in validation_ids: errors.append(f"behavior {p.get('behavior_id')}: unknown validation id {vid}")

    missing_actions = action_ids - covered_action_ids

    if missing_actions:

        errors.append(f"allowed actions missing from execution_steps: {sorted(missing_actions)}")

    if step_orders and step_orders != set(range(1, len(step_orders) + 1)):

        errors.append(f"execution step orders must be contiguous from 1: {sorted(step_orders)}")

    scope = approval.get("scope", [])

    known_scope_ids = decision_ids | action_ids | validation_ids | {"ALL"}

    if isinstance(scope, list):

        unknown_scope = [item for item in scope if item not in known_scope_ids]

        if unknown_scope:

            errors.append(f"approval.scope contains unknown ids: {unknown_scope}")

    else:

        errors.append("plan.approval.scope must be an array")

    required_validation_count = sum(1 for v in validations if isinstance(v, dict) and v.get("required") is True)

    if required_validation_count == 0: errors.append("at least one validation must be required")

    return errors

def check_repo(plan: dict[str, Any], repo: Path, *, pre_merge: bool = False) -> list[str]:

    """Check repo consistency against plan.

    In pre_merge mode, skips operation/conflict/stage-blob checks since

    the merge has not been executed yet. Only HEAD is verified.

    """

    errors: list[str] = []

    root = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()

    expected_root = Path(plan.get("repository", {}).get("root", "")).expanduser()

    if str(expected_root) and expected_root.resolve() != root:

        errors.append(f"repository root drift: expected {expected_root}, actual {root}")

    head = git(root, "rev-parse", "HEAD")

    expected_head = plan.get("repository", {}).get("head")

    if expected_head and head != expected_head:

        errors.append(f"HEAD drift: expected {expected_head}, actual {head}")

    # In pre-merge mode, skip operation/conflict/stage-blob checks

    # because the merge has not been executed yet and no conflict

    # files or stage blobs exist.

    if pre_merge:

        return errors

    operation, operation_head = detect_operation(root)

    snap = plan.get("git_snapshot", {})

    if snap.get("operation") != operation:

        errors.append(f"operation drift: expected {snap.get('operation')}, actual {operation}")

    if snap.get("operation_head") is not None and snap.get("operation_head") != operation_head:

        errors.append(f"operation head drift: expected {snap.get('operation_head')}, actual {operation_head}")

    actual_conflicts = unresolved(root)

    expected_conflicts = sorted(snap.get("conflict_files", []))

    if actual_conflicts != expected_conflicts:

        errors.append(f"conflict set drift: expected {expected_conflicts}, actual {actual_conflicts}")

    actual_stages = stage_blobs(root)

    for item in snap.get("stages", []):

        path = item.get("path")

        actual = actual_stages.get(path, {})

        mapping = [("base_blob", "1"), ("stage_2_blob", "2"), ("stage_3_blob", "3")]

        for field, stage in mapping:

            expected = item.get(field)

            if expected is not None and actual.get(stage) != expected:

                errors.append(f"stage blob drift for {path} {field}: expected {expected}, actual {actual.get(stage)}")

    return errors

def main() -> int:

    ap = argparse.ArgumentParser(description=__doc__)

    ap.add_argument("--plan", required=True, help="Path to plan Markdown file (JSON extracted from appendix A)")

    ap.add_argument("--repo")

    ap.add_argument("--require-approved", action="store_true")

    ap.add_argument("--pre-merge", action="store_true",

                    help="Skip operation/conflict/stage-blob checks (for review phase validation)")

    ap.add_argument("--no-repo-check", action="store_true",

                    help="Skip all repo checks entirely")

    args = ap.parse_args()

    try:

        path = Path(args.plan).resolve()

        # --- UTF-8 integrity check ---

        raw_bytes = path.read_bytes()

        if raw_bytes[:3] == b'\xef\xbb\xbf':

            raise ValueError(f"UTF-8 BOM detected in {path}; plans must be UTF-8 without BOM")

        try:

            test_decode = raw_bytes.decode("utf-8")

        except UnicodeDecodeError as ude:

            raise ValueError(f"Invalid UTF-8 in {path}: {ude}") from ude

        if '\ufffd' in test_decode:

            raise ValueError(f"Unicode replacement characters found in {path}; file encoding is corrupted")

        # --- end UTF-8 check ---

        plan = extract_json_from_markdown(path)

        errors = validate_structure(plan)

        if args.require_approved:

            if plan.get("status") != "APPROVED" or plan.get("approval", {}).get("status") != "APPROVED":

                errors.append("plan is not APPROVED")

            if not plan.get("approval", {}).get("scope"):

                errors.append("approved plan must define non-empty approval.scope")

        if args.repo and not args.no_repo_check:

            errors.extend(check_repo(plan, Path(args.repo).resolve(), pre_merge=args.pre_merge))

        if errors:

            print("INVALID")

            for e in errors:

                print(f"- {e}")

            return 1

        print("VALID")

        print(f"plan_id: {plan.get('plan_id')}")

        print(f"status: {plan.get('status')}")

        print(f"approval: {plan.get('approval', {}).get('status')}")

        print(f"allowed_changes: {len(plan.get('allowed_changes', []))}")

        print(f"validations: {len(plan.get('validations', []))}")

        if args.pre_merge:

            print("mode: pre-merge (operation/conflict/blob checks skipped)")

        return 0

    except (OSError, ValueError, RuntimeError) as exc:

        print(f"ERROR: {exc}", file=sys.stderr)

        return 2

if __name__ == "__main__":

    raise SystemExit(main())
