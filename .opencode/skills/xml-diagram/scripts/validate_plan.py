#!/usr/bin/env python3
"""Validate the public Draw.io DiagramPlan contract without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "assets" / "diagram-plan.schema.json"


def validate_value(value: object, rule: dict[str, object], path: str) -> list[str]:
    errors: list[str] = []
    if "const" in rule and value != rule["const"]:
        errors.append(f"{path} 必须为 {rule['const']!r}")
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{path} 不在允许范围")

    expected = rule.get("type")
    valid_type = {
        "string": isinstance(value, str),
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
        "integer": isinstance(value, int) and not isinstance(value, bool),
    }.get(expected, True)
    if not valid_type:
        errors.append(f"{path} 类型必须为 {expected}")
        return errors

    if isinstance(value, str) and isinstance(rule.get("minLength"), int) and len(value) < rule["minLength"]:
        errors.append(f"{path} 长度不得小于 {rule['minLength']}")
    if isinstance(value, list):
        if isinstance(rule.get("minItems"), int) and len(value) < rule["minItems"]:
            errors.append(f"{path} 元素数量不得小于 {rule['minItems']}")
        item_rule = rule.get("items")
        if isinstance(item_rule, dict):
            for index, item in enumerate(value):
                errors.extend(validate_value(item, item_rule, f"{path}[{index}]"))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(rule.get("minimum"), (int, float)) and value < rule["minimum"]:
            errors.append(f"{path} 不得小于 {rule['minimum']}")
        if isinstance(rule.get("maximum"), (int, float)) and value > rule["maximum"]:
            errors.append(f"{path} 不得大于 {rule['maximum']}")

    if isinstance(value, dict):
        properties = rule.get("properties", {})
        required = rule.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    errors.append(f"缺少必填字段: {path}.{key}")
        if isinstance(properties, dict):
            for key, child_rule in properties.items():
                if key in value and isinstance(child_rule, dict):
                    errors.extend(validate_value(value[key], child_rule, f"{path}.{key}"))
            if rule.get("additionalProperties") is False:
                extra = sorted(set(value) - set(properties))
                if extra:
                    errors.append(f"{path} 存在未声明字段: " + ", ".join(extra))
    return errors


def validate(plan: object, schema: dict[str, object]) -> list[str]:
    if not isinstance(plan, dict):
        return ["plan 必须是 JSON object"]
    errors = validate_value(plan, schema, "plan")
    diagram_type = plan.get("type")
    if isinstance(diagram_type, str) and (diagram_type.endswith("_architecture") or diagram_type == "system_context"):
        if not plan.get("sections"):
            errors.append("架构图 sections 不得为空")
        if not plan.get("nodes"):
            errors.append("架构图 nodes 不得为空")
    nodes = plan.get("nodes")
    edges = plan.get("edges")
    if isinstance(nodes, list) and isinstance(edges, list):
        raw_node_ids = [item.get("id") for item in nodes if isinstance(item, dict)]
        node_ids = set(raw_node_ids)
        if len(raw_node_ids) != len(node_ids):
            errors.append("nodes id 不得重复")
        raw_edge_ids = [item.get("id") for item in edges if isinstance(item, dict)]
        if len(raw_edge_ids) != len(set(raw_edge_ids)):
            errors.append("edges id 不得重复")
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                continue
            for key in ("source", "target"):
                if edge.get(key) not in node_ids:
                    errors.append(f"plan.edges[{index}].{key} 引用不存在")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"错误: 无法读取 JSON: {exc}")
        return 1
    errors = validate(plan, schema)
    for item in errors:
        print("错误: " + item)
    if errors:
        return 1
    print("DiagramPlan 有效")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
