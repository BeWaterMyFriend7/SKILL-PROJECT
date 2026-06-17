#!/usr/bin/env python3
"""检查 drawio 单元格中文字与背景的对比度。"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def parse_style(style: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in (style or "").split(";"):
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value
    return result


def luminance(hex_color: str) -> float:
    rgb = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]

    def channel(value: float) -> float:
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    r, g, b = [channel(v) for v in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(bg: str, fg: str) -> float:
    left = luminance(bg)
    right = luminance(fg)
    lighter = max(left, right)
    darker = min(left, right)
    return (lighter + 0.05) / (darker + 0.05)


def check(path: Path, threshold: float) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors: list[str] = []

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"XML 无法解析: {exc}"], warnings

    for cell in root.findall(".//mxCell"):
        style = parse_style(cell.attrib.get("style", ""))
        fill = style.get("fillColor")
        font = style.get("fontColor")
        if not fill or fill in {"none", "transparent"} or not font:
            continue
        if not (HEX_RE.match(fill) and HEX_RE.match(font)):
            continue
        ratio = contrast(fill, font)
        if ratio < threshold:
            warnings.append(
                f"{cell.attrib.get('id', '<无 id>')}: 对比度 {ratio:.2f} 低于 {threshold:.2f}，背景 {fill}，文字 {font}"
            )

    return errors, warnings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--threshold", type=float, default=3.0, help="默认值适合标题条；正文严格检查可使用 4.5。")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    failed = False
    for path in args.files:
        errors, warnings = check(path, args.threshold)
        print(f"{path}: {len(errors)} 个错误，{len(warnings)} 个对比度警告")
        for item in errors:
            print(f"  错误: {item}")
        for item in warnings[:30]:
            print(f"  警告: {item}")
        if len(warnings) > 30:
            print(f"  警告: 还有 {len(warnings) - 30} 项")
        failed = failed or bool(errors) or (args.fail_on_warning and bool(warnings))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
