#!/usr/bin/env python3
"""列出并检查内置 drawio 模板。"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def inspect_template(path: Path) -> tuple[bool, str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return False, f"XML 无法解析: {exc}"

    diagrams = root.findall(".//diagram")
    cells = root.findall(".//mxCell")
    if root.tag != "mxfile":
        return False, f"根节点类型异常: {root.tag}"
    if not diagrams:
        return False, "缺少 diagram 元素"
    if not cells:
        return False, "缺少 mxCell 元素"
    return True, f"{len(diagrams)} 个页面，{len(cells)} 个单元"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("template_dir", nargs="?", default=Path(__file__).resolve().parents[1] / "templates", type=Path)
    args = parser.parse_args()

    files = sorted(args.template_dir.rglob("*.drawio"))
    if not files:
        print(f"未找到模板目录或模板文件: {args.template_dir}")
        return 1

    failed = False
    for path in files:
        ok, message = inspect_template(path)
        rel = path.relative_to(args.template_dir)
        status = "通过" if ok else "失败"
        print(f"{status} {rel}: {message}")
        failed = failed or not ok

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
