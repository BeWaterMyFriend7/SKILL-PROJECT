#!/usr/bin/env python3
"""Validate local Draw.io template/example catalog integrity."""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_RE = re.compile(r"^[^-]+(?:-[^-]+)?-(?:dark|light)-.+\.drawio$")


def main() -> int:
    errors: list[str] = []
    templates = sorted((ROOT / "templates").rglob("*.drawio"))
    examples = sorted((ROOT / "examples").glob("*.drawio"))
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in templates:
        groups[hashlib.sha256(path.read_bytes()).hexdigest()].append(path)
    for paths in groups.values():
        if len(paths) > 1:
            errors.append("不同模板内容完全相同: " + ", ".join(str(path.relative_to(ROOT)) for path in paths))
    for path in examples:
        if not EXAMPLE_RE.match(path.name):
            errors.append(f"示例命名不合规: {path.name}")
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for raw in re.findall(r"(?<![\w.-])((?:assets|examples|templates|scripts)/[\w./?-]+)", text):
            if "*" in raw:
                continue
            target = (ROOT / raw).resolve()
            if not target.exists():
                errors.append(f"{markdown.relative_to(ROOT)}: 引用不存在 {raw}")
    for item in errors:
        print("错误: " + item)
    if errors:
        return 1
    print(f"Draw.io catalog 有效: {len(templates)} templates, {len(examples)} examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
