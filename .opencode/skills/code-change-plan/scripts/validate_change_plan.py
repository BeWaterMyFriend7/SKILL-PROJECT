#!/usr/bin/env python3
"""Validate a code change plan Markdown file.

Checks: mandatory sections, approval status, traceability chains.
Supports --mode SIMPLE (12 chapters) and FULL (23 chapters, default).
Read-only, standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

FULL_SECTIONS = [
    ("1", "基本信息"),
    ("2", "需求分析"),
    ("3", "假设"),
    ("4", "验收标准"),
    ("5", "当前实现"),
    ("6", "当前功能流程"),
    ("7", "差距分析"),
    ("8", "目标方案"),
    ("9", "目标功能流程"),
    ("10", "修改前后对比"),
    ("11", "修改单元"),
    ("12", "全项目影响"),
    ("13", "旧逻辑退役"),
    ("14", "文件变更清单"),
    ("15", "实施顺序"),
    ("16", "测试与验证"),
    ("17", "追踪矩阵"),
    ("18", "发布与回滚"),
    ("19", "风险"),
    ("20", "执行契约"),
    ("21", "完成条件"),
    ("22", "审批记录"),
    ("23", "直接执行"),
]

SIMPLE_SECTIONS = [
    ("1", "基本信息"),
    ("2", "需求分析"),
    ("3", "假设"),
    ("4", "验收标准"),
    ("5", "当前实现与差距"),
    ("6", "目标方案与对比"),
    ("7", "修改单元"),
    ("8", "影响与清理"),
    ("9", "实施与验证"),
    ("10", "发布与风险"),
    ("11", "执行契约"),
    ("12", "审批与执行"),
]

APPROVAL_RE = re.compile(
    r"WAITING_FOR_APPROVAL|APPROVED_WITH_CHANGES|APPROVED(?!_)|REJECTED|SUPERSEDED",
    re.IGNORECASE,
)


def find_sections(content):
    sections = []
    for i, line in enumerate(content.splitlines(), start=1):
        m = re.match(r"^##\s+\d+\.\s*(.+)$", line)
        if m:
            sections.append((m.group(1).strip(), i))
    return sections


def extract_ids(content, prefix):
    pattern = re.compile(r"\b(" + prefix + r"-\d+)\b", re.IGNORECASE)
    return {m.group(1).upper() for m in pattern.finditer(content)}


def check_traceability(content):
    errors = []
    req_ids = extract_ids(content, "REQ")
    ac_ids = extract_ids(content, "AC")
    cu_ids = extract_ids(content, "CU")
    v_ids = extract_ids(content, "V")
    lr_ids = extract_ids(content, "LR")

    if req_ids and not ac_ids:
        errors.append("REQ IDs found but no AC (acceptance criteria) IDs")
    if ac_ids and not cu_ids:
        errors.append("AC IDs found but no CU (modification unit) IDs")
    if cu_ids and not v_ids:
        errors.append("CU IDs found but no V (verification) IDs")
    if lr_ids and not cu_ids:
        errors.append("LR IDs found but no CU references")

    return errors


def validate(plan_path, mode="FULL"):
    result = {
        "plan_path": str(plan_path),
        "valid": True,
        "errors": [],
        "warnings": [],
        "sections_found": [],
        "sections_missing": [],
        "approval_status": None,
        "mode": mode,
    }

    if not plan_path.is_file():
        result["valid"] = False
        result["errors"].append("Plan file not found: " + str(plan_path))
        return result

    content = plan_path.read_text(encoding="utf-8", errors="replace")
    check_sections = SIMPLE_SECTIONS if mode == "SIMPLE" else FULL_SECTIONS

    sections = find_sections(content)
    result["sections_found"] = [s[0] for s in sections]

    section_titles_lower = [s[0].lower() for s in sections]
    for sid, keyword in check_sections:
        found = any(keyword.lower() in t for t in section_titles_lower)
        if not found:
            result["sections_missing"].append(sid + ". " + keyword)
            result["errors"].append("Missing section: " + sid + ". " + keyword)

    # Check approval status
    for line in content.splitlines():
        if any(kw in line for kw in ["审批状态", "审批记录", "status"]):
            m = APPROVAL_RE.search(line)
            if m:
                result["approval_status"] = m.group(0).upper()
                break

    if result["approval_status"]:
        if result["approval_status"] != "WAITING_FOR_APPROVAL":
            result["errors"].append(
                "Approval status is " + result["approval_status"] + ", must be WAITING_FOR_APPROVAL"
            )
    else:
        result["approval_status"] = "WAITING_FOR_APPROVAL"

    trace_errors = check_traceability(content)
    result["errors"].extend(trace_errors)

    if result["errors"]:
        result["valid"] = False

    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", required=True, help="Path to the change plan Markdown file")
    ap.add_argument("--mode", choices=["SIMPLE", "FULL"], default="FULL", help="Plan complexity mode")
    args = ap.parse_args()

    plan_path = Path(args.plan).resolve()
    result = validate(plan_path, args.mode)

    total = 12 if args.mode == "SIMPLE" else 23
    print("Plan: " + result["plan_path"])
    print("Mode: " + result["mode"])
    print("Sections found: " + str(len(result["sections_found"])) + "/" + str(total))
    if result["sections_missing"]:
        print("Missing sections:")
        for s in result["sections_missing"]:
            print("  - " + s)
    print("Approval status: " + (result["approval_status"] or "NOT DETECTED"))
    if result["errors"]:
        print("\nErrors (" + str(len(result["errors"])) + "):")
        for e in result["errors"]:
            print("  - " + e)
    if result["warnings"]:
        print("\nWarnings (" + str(len(result["warnings"])) + "):")
        for w in result["warnings"]:
            print("  - " + w)

    if result["valid"]:
        print("\nVALID")
        return 0
    else:
        print("\nINVALID (" + str(len(result["errors"])) + " errors)")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())