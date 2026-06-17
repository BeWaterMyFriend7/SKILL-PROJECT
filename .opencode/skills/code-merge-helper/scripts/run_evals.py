#!/usr/bin/env python3
"""Self-test runner for the code-merge-helper skill package.

Validates file integrity, schema correctness, script syntax, and template
completeness. Does NOT test agent behavior (that requires live Git state).
"""
import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent


def check(description, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    line = f"  [{status}] {description}"
    if detail and not passed:
        line += f" -- {detail}"
    print(line)
    return passed


def main():
    print(f"Skill root: {SKILL_ROOT}\n")
    all_pass = True

    # === 1. File integrity ===
    print("1. File integrity")
    required_files = [
        "SKILL.md",
        "README.md",
        "agents/openai.yaml",
        "assets/merge-plan.schema.json",
        "assets/merge-plan.example.json",
        "assets/merge-resolution-report.md",
        "assets/plan-amendment.md",
        "evals/scenarios.md",
        "references/analysis-rules.md",
        "references/git-command-reference.md",
        "references/handoff-contract.md",
        "references/report-format-guide.md",
        "references/verification-matrix.md",
        "scripts/collect_merge_context.py",
        "scripts/guard_change_scope.py",
        "scripts/validate_merge_plan.py",
        "scripts/verify_merge_state.py",
    ]
    for rel in required_files:
        exists = (SKILL_ROOT / rel).is_file()
        all_pass &= check(f"exists: {rel}", exists, "file missing")
        if exists:
            size = (SKILL_ROOT / rel).stat().st_size
            nonempty = size > 0
            all_pass &= check(f"non-empty: {rel}", nonempty, f"size={size}")

    # === 2. JSON Schema validity ===
    print("\n2. JSON Schema validity")
    schema_path = SKILL_ROOT / "assets/merge-plan.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        has_props = isinstance(schema, dict) and "properties" in schema
        all_pass &= check("schema.json is valid JSON", True)
        all_pass &= check("schema.json has properties", has_props)
        required = schema.get("required", [])
        key_fields = ["plan_id", "status", "decisions", "allowed_changes", "validations"]
        for f in key_fields:
            all_pass &= check(f"required field: {f}", f in required, "missing from required[]")
    except json.JSONDecodeError as e:
        all_pass &= check("schema.json is valid JSON", False, str(e))

    # === 3. Example JSON validity ===
    print("\n3. Example plan validity")
    example_path = SKILL_ROOT / "assets/merge-plan.example.json"
    try:
        example = json.loads(example_path.read_text(encoding="utf-8"))
        all_pass &= check("example.json is valid JSON", True)
        has_status = "status" in example
        all_pass &= check("example.json has status field", has_status)
    except json.JSONDecodeError as e:
        all_pass &= check("example.json is valid JSON", False, str(e))

    # === 4. Python script syntax ===
    print("\n4. Python script syntax")
    for script_name in ["collect_merge_context.py", "guard_change_scope.py",
                         "validate_merge_plan.py", "verify_merge_state.py"]:
        sp = SKILL_ROOT / "scripts" / script_name
        try:
            code = sp.read_text(encoding="utf-8")
            compile(code, script_name, "exec")
            all_pass &= check(f"syntax: {script_name}", True)
        except SyntaxError as e:
            all_pass &= check(f"syntax: {script_name}", False, str(e))

    # === 5. Report template completeness ===
    print("\n5. Report template completeness")
    report_path = SKILL_ROOT / "assets/merge-resolution-report.md"
    report = report_path.read_text(encoding="utf-8", errors="replace")
    required_sections = [
        "合并上下文", "执行摘要", "冲突清单", "冲突详细分析",
        "行为保留矩阵", "逐文件实施清单", "影响范围评估",
        "执行顺序", "验证计划", "人工决策项",
        "停止条件", "残余风险与回滚", "人工审批", "执行指引",
    ]
    for sec in required_sections:
        found = sec.lower() in report.lower()
        all_pass &= check(f"section: {sec}", found, "not found in template")

    # === 6. Reference file content checks ===
    print("\n6. Reference completeness")
    ref_checks = {
        "report-format-guide.md": ["字段", "章节", "JSON"],
        "analysis-rules.md": ["文本冲突", "语义冲突", "接口消费者"],
        "handoff-contract.md": ["计划", "HEAD", "审批"],
        "verification-matrix.md": ["业务代码", "API", "配置"],
        "git-command-reference.md": ["git status", "git diff", "merge-base"],
    }
    for ref_file, keywords in ref_checks.items():
        content = (SKILL_ROOT / "references" / ref_file).read_text(encoding="utf-8", errors="replace")
        for kw in keywords:
            found = kw.lower() in content.lower()
            all_pass &= check(f"{ref_file}: contains '{kw}'", found)

    # === 7. No stale __pycache__ ===
    print("\n7. Cleanliness")
    pycache = SKILL_ROOT / "scripts" / "__pycache__"
    all_pass &= check("no __pycache__ residue", not pycache.exists(), str(pycache))

    # === Summary ===
    print(f"\n{'='*40}")
    if all_pass:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())