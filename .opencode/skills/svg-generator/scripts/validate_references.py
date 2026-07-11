#!/usr/bin/env python3
"""Check that local Markdown references stay inside the skill and exist."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_RE = re.compile(r"(?<![\w.-])((?:\.\./)?(?:assets|examples|templates|scripts|evals)/[\w./*?-]+)")


def main() -> int:
    failures: list[str] = []
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for raw in REFERENCE_RE.findall(text):
            if "*" in raw:
                continue
            target = (markdown.parent / raw).resolve() if raw.startswith("../") else (ROOT / raw).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                failures.append(f"{markdown.relative_to(ROOT)}: 跨 skill 引用 {raw}")
                continue
            if not target.exists():
                failures.append(f"{markdown.relative_to(ROOT)}: 引用不存在 {raw}")
    if failures:
        for item in failures:
            print("错误: " + item)
        return 1
    print("SVG 本地引用完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
