#!/usr/bin/env python3
"""Validate SVG structure, readability, references, and coarse layout bounds."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
import tempfile
from pathlib import Path

from render_svg import render


NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
URL_REF_RE = re.compile(r"url\(#([^)]+)\)")
TRANSLATE_RE = re.compile(r"translate\(\s*(-?\d+(?:\.\d+)?)\s*(?:[, ]\s*(-?\d+(?:\.\d+)?))?\s*\)")


def number(value: str | None) -> float | None:
    if not value:
        return None
    match = NUMBER_RE.search(value)
    return float(match.group()) if match else None


def style_map(element: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in (element.get("style") or "").split(";"):
        if ":" in part:
            key, value = part.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def attr(element: ET.Element, name: str) -> str | None:
    return element.get(name) or style_map(element).get(name)


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def element_box(
    element: ET.Element,
    offset_x: float = 0,
    offset_y: float = 0,
    inherited_font_size: float = 12,
) -> tuple[float, float, float, float] | None:
    tag = local_name(element)
    if tag == "rect":
        x, y = number(element.get("x")) or 0, number(element.get("y")) or 0
        w, h = number(element.get("width")), number(element.get("height"))
        return (x + offset_x, y + offset_y, w, h) if w is not None and h is not None else None
    if tag == "circle":
        cx, cy, r = number(element.get("cx")), number(element.get("cy")), number(element.get("r"))
        return (cx - r + offset_x, cy - r + offset_y, 2 * r, 2 * r) if None not in (cx, cy, r) else None
    if tag == "ellipse":
        cx, cy = number(element.get("cx")), number(element.get("cy"))
        rx, ry = number(element.get("rx")), number(element.get("ry"))
        return (cx - rx + offset_x, cy - ry + offset_y, 2 * rx, 2 * ry) if None not in (cx, cy, rx, ry) else None
    if tag == "line":
        x1, y1 = number(element.get("x1")), number(element.get("y1"))
        x2, y2 = number(element.get("x2")), number(element.get("y2"))
        if None not in (x1, y1, x2, y2):
            return min(x1, x2) + offset_x, min(y1, y2) + offset_y, abs(x2 - x1), abs(y2 - y1)
    if tag == "text":
        x, y = number(element.get("x")), number(element.get("y"))
        size = number(attr(element, "font-size")) or inherited_font_size
        text = "".join(element.itertext()).strip()
        if x is not None and y is not None and text:
            width = max(size * 0.55 * len(text), size)
            anchor = element.get("text-anchor")
            left = x - width / 2 if anchor == "middle" else x - width if anchor == "end" else x
            return left + offset_x, y - size + offset_y, width, size * 1.25
    return None


def walk(
    element: ET.Element,
    offset_x: float = 0,
    offset_y: float = 0,
    inherited_font_size: float = 12,
):
    transform = element.get("transform") or ""
    match = TRANSLATE_RE.search(transform)
    if match:
        offset_x += float(match.group(1))
        offset_y += float(match.group(2) or 0)
    font_size = number(attr(element, "font-size")) or inherited_font_size
    yield element, offset_x, offset_y, font_size
    for child in element:
        yield from walk(child, offset_x, offset_y, font_size)


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"文件无法按 UTF-8 读取: {exc}"], warnings
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"SVG XML 无法解析: {exc}"], warnings
    if local_name(root) != "svg":
        errors.append("根节点不是 svg")

    width, height = number(root.get("width")), number(root.get("height"))
    viewbox = [float(item) for item in NUMBER_RE.findall(root.get("viewBox") or "")]
    if width is None or height is None:
        errors.append("缺少有效 width/height")
    if len(viewbox) != 4:
        errors.append("缺少有效 viewBox")
    elif width is not None and height is not None and (abs(viewbox[2] - width) > 0.1 or abs(viewbox[3] - height) > 0.1):
        errors.append("width/height 与 viewBox 不一致")

    ids: list[str] = [item.get("id") for item in root.iter() if item.get("id")]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("id 重复: " + ", ".join(duplicates))
    id_set = set(ids)
    for element in root.iter():
        values = list(element.attrib.values())
        for value in values:
            for ref in URL_REF_RE.findall(value):
                if ref not in id_set:
                    errors.append(f"引用不存在: {ref}")
        href = element.get("href") or element.get("{http://www.w3.org/1999/xlink}href")
        if href and href.startswith("#") and href[1:] not in id_set:
            errors.append(f"引用不存在: {href[1:]}")

    if not any(local_name(item) == "title" for item in root):
        warnings.append("缺少 title 元素")
    if not any(local_name(item) == "desc" for item in root):
        warnings.append("缺少 desc 元素")

    boxes: list[tuple[float, float, float, float]] = []
    for element, offset_x, offset_y, inherited_font_size in walk(root):
        if local_name(element) == "text":
            size = number(attr(element, "font-size")) or inherited_font_size
            auxiliary = element.get("data-text-role") == "auxiliary"
            minimum = 11 if auxiliary else 12
            if size is not None and size < minimum:
                warnings.append(f"文字字号过小: {size:g}px")
        box = element_box(element, offset_x, offset_y, inherited_font_size)
        if box is None:
            continue
        x, y, w, h = box
        is_background = width is not None and height is not None and x <= 1 and y <= 1 and w >= width * 0.95 and h >= height * 0.95
        if not is_background:
            boxes.append(box)
        if width is not None and height is not None and (x < -0.5 or y < -0.5 or x + w > width + 0.5 or y + h > height + 0.5):
            warnings.append(f"元素超出画布: {local_name(element)}#{element.get('id', '')}")

    if boxes and width and height:
        left = min(box[0] for box in boxes)
        top = min(box[1] for box in boxes)
        right = max(box[0] + box[2] for box in boxes)
        bottom = max(box[1] + box[3] for box in boxes)
        usage = (right - left) * (bottom - top) / (width * height)
        if usage < 0.50:
            warnings.append(f"画布利用率过低: {usage:.0%}")
        elif usage > 0.85:
            warnings.append(f"画布利用率过高: {usage:.0%}")

    return errors, warnings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--require-render", action="store_true")
    args = parser.parse_args()
    failed = False
    for path in args.files:
        errors, warnings = validate(path)
        render_message: str | None = None
        if args.require_render and not errors:
            with tempfile.TemporaryDirectory() as tmp:
                ok, message = render(path, Path(tmp) / "render.png")
            render_message = ("渲染: " if ok else "渲染错误: ") + message
            if not ok:
                errors.append(message)
        print(f"{path}: {len(errors)} 个错误，{len(warnings)} 个警告")
        for item in errors:
            print("  错误: " + item)
        for item in warnings:
            print("  警告: " + item)
        if render_message:
            print("  " + render_message)
        failed = failed or bool(errors) or (args.fail_on_warning and bool(warnings))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
