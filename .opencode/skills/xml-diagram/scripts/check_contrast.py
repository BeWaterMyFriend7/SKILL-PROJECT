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


def cell_geometry(cell: ET.Element) -> tuple[float, float, float, float] | None:
    geom = cell.find("mxGeometry")
    if geom is None or geom.attrib.get("relative") == "1":
        return None
    try:
        return tuple(float(geom.attrib.get(key, "0")) for key in ("x", "y", "width", "height"))
    except ValueError:
        return None


def absolute_geometry(cell: ET.Element, cells_by_id: dict[str, ET.Element]) -> tuple[float, float, float, float] | None:
    geom = cell_geometry(cell)
    if geom is None:
        return None
    x, y, width, height = geom
    parent = cells_by_id.get(cell.attrib.get("parent", ""))
    if parent is not None:
        parent_geom = absolute_geometry(parent, cells_by_id)
        if parent_geom is not None:
            x += parent_geom[0]
            y += parent_geom[1]
    return x, y, width, height


def contains(outer: tuple[float, float, float, float], inner: tuple[float, float, float, float]) -> bool:
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner
    return ix >= ox and iy >= oy and ix + iw <= ox + ow and iy + ih <= oy + oh


def effective_background(
    cell: ET.Element,
    cells: list[ET.Element],
    cell_index: int,
    cells_by_id: dict[str, ET.Element],
    page_bg: str,
) -> str:
    current: ET.Element | None = cell
    seen: set[str] = set()
    while current is not None:
        style = parse_style(current.attrib.get("style", ""))
        fill = style.get("fillColor")
        if fill and HEX_RE.match(fill):
            return fill
        parent_id = current.attrib.get("parent")
        if not parent_id or parent_id in seen:
            break
        seen.add(parent_id)
        current = cells_by_id.get(parent_id)
    text_box = absolute_geometry(cell, cells_by_id)
    if text_box is not None:
        candidates: list[tuple[float, int, str]] = []
        for index, candidate in enumerate(cells[:cell_index]):
            if candidate.attrib.get("vertex") != "1":
                continue
            fill = parse_style(candidate.attrib.get("style", "")).get("fillColor")
            candidate_box = absolute_geometry(candidate, cells_by_id)
            if fill and HEX_RE.match(fill) and candidate_box is not None and contains(candidate_box, text_box):
                candidates.append((candidate_box[2] * candidate_box[3], -index, fill))
        if candidates:
            return min(candidates)[2]
    return page_bg


def check(path: Path, threshold: float) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors: list[str] = []

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"XML 无法解析: {exc}"], warnings

    cells = root.findall(".//mxCell")
    cells_by_id = {cell.attrib.get("id", ""): cell for cell in cells}
    model = root.find(".//mxGraphModel")
    page_bg = model.attrib.get("background", "#FFFFFF") if model is not None else "#FFFFFF"
    if not HEX_RE.match(page_bg):
        page_bg = "#FFFFFF"
    bg_cell = cells_by_id.get("bg")
    if bg_cell is not None:
        candidate = parse_style(bg_cell.attrib.get("style", "")).get("fillColor")
        if candidate and HEX_RE.match(candidate):
            page_bg = candidate

    for cell_index, cell in enumerate(cells):
        style = parse_style(cell.attrib.get("style", ""))
        font = style.get("fontColor")
        if not font:
            continue
        fill = effective_background(cell, cells, cell_index, cells_by_id, page_bg)
        if not (HEX_RE.match(fill) and HEX_RE.match(font)):
            continue
        try:
            font_size = float(style.get("fontSize", "12"))
        except ValueError:
            font_size = 12
        is_bold = style.get("fontStyle") in {"1", "3"}
        required = 3.0 if font_size >= 18 or (is_bold and font_size >= 14) else threshold
        ratio = contrast(fill, font)
        if ratio < required:
            warnings.append(
                f"{cell.attrib.get('id', '<无 id>')}: 对比度 {ratio:.2f} 低于 {required:.2f}，背景 {fill}，文字 {font}"
            )

    return errors, warnings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--threshold", type=float, default=4.5, help="普通文字阈值；大号或粗体标题自动使用 3.0。")
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
