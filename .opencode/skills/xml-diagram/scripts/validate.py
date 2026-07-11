#!/usr/bin/env python3
"""Lightweight Draw.io validator using only the Python standard library."""

from __future__ import annotations

import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TEMPLATES = {
    "architecture.drawio",
    "flow.drawio",
    "sequence.drawio",
    "relationship.drawio",
    "structured-content.drawio",
}
PLACEHOLDER_RE = re.compile(r"(标题|一级区域|分组卡片|内容标签|参与者 [ABC]|处理步骤|实体 [AB]|内容区域 [AB]|结构化内容)$")
MOJIBAKE = ("锟", "�", "鐢", "鍥", "绋", "瑙")


@dataclass(frozen=True)
class Box:
    cell_id: str
    x: float
    y: float
    width: float
    height: float
    style: str
    value: str

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


def style_map(raw: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in raw.split(";"):
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value
    return result


def number(value: str | None, default: float = 0.0) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def rgb(color: str) -> tuple[float, float, float] | None:
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        return None
    values = tuple(int(color[index : index + 2], 16) / 255 for index in (1, 3, 5))
    return values  # type: ignore[return-value]


def luminance(color: str) -> float | None:
    value = rgb(color)
    if value is None:
        return None
    converted = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in value]
    return 0.2126 * converted[0] + 0.7152 * converted[1] + 0.0722 * converted[2]


def contrast(foreground: str, background: str) -> float | None:
    first = luminance(foreground)
    second = luminance(background)
    if first is None or second is None:
        return None
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def intersects(first: Box, second: Box) -> bool:
    return first.x < second.right and first.right > second.x and first.y < second.bottom and first.bottom > second.y


def contains(first: Box, second: Box) -> bool:
    return first.x <= second.x and first.y <= second.y and first.right >= second.right and first.bottom >= second.bottom


def visible_boxes(cells: list[ET.Element]) -> list[Box]:
    boxes: list[Box] = []
    for cell in cells:
        if cell.get("vertex") != "1":
            continue
        style = cell.get("style", "")
        if "shape=line" in style:
            continue
        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue
        width = number(geometry.get("width"))
        height = number(geometry.get("height"))
        if width <= 0 or height <= 0:
            continue
        boxes.append(
            Box(
                cell.get("id", ""),
                number(geometry.get("x")),
                number(geometry.get("y")),
                width,
                height,
                style,
                cell.get("value", ""),
            )
        )
    return boxes


def point_pair(cell: ET.Element) -> tuple[ET.Element | None, ET.Element | None]:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return None, None
    return geometry.find("mxPoint[@as='sourcePoint']"), geometry.find("mxPoint[@as='targetPoint']")


def validate_file(path: Path, allow_placeholders: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append("文件包含 UTF-8 BOM")
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"无法按 UTF-8 读取: {exc}"], []

    if any(fragment in text for fragment in MOJIBAKE):
        errors.append("检测到疑似中文乱码")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"XML 无法解析: {exc}"], []

    if root.tag not in {"mxfile", "mxGraphModel"}:
        errors.append("根节点必须是 mxfile 或 mxGraphModel")
    model = root if root.tag == "mxGraphModel" else root.find(".//mxGraphModel")
    if model is None:
        return errors + ["缺少 mxGraphModel"], warnings
    if model.get("grid") != "0":
        errors.append("mxGraphModel 必须显式设置 grid=0")

    page_width = number(model.get("pageWidth"))
    page_height = number(model.get("pageHeight"))
    if page_width <= 0 or page_height <= 0:
        errors.append("pageWidth 和 pageHeight 必须为正数")

    cells = list(model.findall(".//mxCell"))
    ids = [cell.get("id", "") for cell in cells]
    duplicate_ids = sorted({cell_id for cell_id in ids if cell_id and ids.count(cell_id) > 1})
    if duplicate_ids:
        errors.append("mxCell id 重复: " + ", ".join(duplicate_ids))
    known_ids = set(ids)

    for cell in cells:
        cell_id = cell.get("id", "<unknown>")
        geometry = cell.find("mxGeometry")
        if geometry is not None and geometry.get("as") != "geometry":
            errors.append(f"{cell_id}: mxGeometry 缺少 as=geometry")
        if cell.get("edge") == "1":
            for key in ("source", "target"):
                reference = cell.get(key)
                if reference and reference not in known_ids:
                    errors.append(f"{cell_id}: {key} 引用不存在节点 {reference}")
        style = style_map(cell.get("style", ""))
        font_size = number(style.get("fontSize"), 12)
        if cell.get("value") and font_size < 11:
            errors.append(f"{cell_id}: 字号 {font_size:g} 小于 11")
        raw_style = cell.get("style", "")
        if "underline" in raw_style.lower() or "fontStyle=4" in raw_style:
            errors.append(f"{cell_id}: 禁止标题或文字下划线")
        if style.get("shadow") == "1" or model.get("shadow") == "1":
            warnings.append(f"{cell_id}: 检测到阴影，应确认仅为浅色轻微阴影")

        foreground = style.get("fontColor")
        background = style.get("fillColor")
        if background in {None, "none"}:
            background = model.get("background")
        if foreground and background:
            ratio = contrast(foreground, background)
            threshold = 3.0 if font_size >= 18 or (font_size >= 14 and "fontStyle=1" in raw_style) else 4.5
            if ratio is not None and ratio + 1e-6 < threshold:
                errors.append(f"{cell_id}: 文字对比度 {ratio:.2f}:1 低于 {threshold:.1f}:1")

    boxes = visible_boxes(cells)
    for box in boxes:
        is_title = box.cell_id == "title"
        minimum = 20 if is_title else 30
        if box.x < minimum or box.y < minimum or box.right > page_width - minimum or box.bottom > page_height - minimum:
            errors.append(f"{box.cell_id}: 超出画布安全边距")

    for index, first in enumerate(boxes):
        for second in boxes[index + 1 :]:
            if not intersects(first, second):
                continue
            if contains(first, second) or contains(second, first):
                continue
            errors.append(f"元素重叠: {first.cell_id} 与 {second.cell_id}")

    architecture_name = path.name.lower()
    diagram = root.find("diagram")
    diagram_name = diagram.get("name", "").lower() if diagram is not None else ""
    if "architecture" in architecture_name or "architecture" in diagram_name:
        for card in boxes:
            card_style = style_map(card.style)
            if card_style.get("arcSize") != "10" or card.height < 100:
                continue
            children = [child for child in boxes if child.cell_id != card.cell_id and contains(card, child)]
            if not children:
                continue
            if card.value.strip():
                errors.append(f"{card.cell_id}: 架构分组卡片容器不得承载标题文字")
            text_titles = [child for child in children if child.style.startswith("text;") and child.value.strip()]
            if not text_titles:
                errors.append(f"{card.cell_id}: 架构分组卡片缺少独立文字标题")

    if boxes and page_width > 0 and page_height > 0 and not allow_placeholders:
        min_x = min(box.x for box in boxes)
        min_y = min(box.y for box in boxes)
        max_x = max(box.right for box in boxes)
        max_y = max(box.bottom for box in boxes)
        utilization = ((max_x - min_x) * (max_y - min_y)) / (page_width * page_height)
        if utilization < 0.45:
            warnings.append(f"内容包围盒利用率 {utilization:.1%}，需检查大面积空白")
        elif utilization > 0.85:
            warnings.append(f"内容包围盒利用率 {utilization:.1%}，需检查拥挤或裁切")

    values = [re.sub(r"<[^>]+>", "", cell.get("value", "")).strip() for cell in cells]
    if not allow_placeholders:
        placeholders = [value for value in values if value and PLACEHOLDER_RE.search(value)]
        if placeholders:
            errors.append("示例或输出残留模板占位内容: " + ", ".join(sorted(set(placeholders))))

    filename = path.name.lower()
    edges = [cell for cell in cells if cell.get("edge") == "1"]
    if "state" in filename:
        unlabeled = [cell.get("id", "") for cell in edges if not cell.get("value", "").strip()]
        if unlabeled:
            errors.append("状态图转换必须有标签: " + ", ".join(unlabeled))
    if "sequence" in filename or "sequence" in diagram_name:
        lifelines = [cell for cell in cells if cell.get("id", "").startswith("life-")]
        participants = [cell for cell in cells if cell.get("id", "").startswith("actor-") or cell.get("id", "") in {"user", "gateway", "auth", "store"}]
        if len(lifelines) < max(2, len(participants)):
            errors.append("时序图每个参与者都必须具有完整竖向生命线")
        for line in lifelines:
            if line.get("vertex") == "1":
                geometry = line.find("mxGeometry")
                if geometry is not None and number(geometry.get("height")) <= number(geometry.get("width")):
                    errors.append(f"{line.get('id')}: 生命线必须竖向")
            else:
                source_point, target_point = point_pair(line)
                if source_point is None or target_point is None:
                    errors.append(f"{line.get('id')}: 生命线缺少完整起止点")
                elif not math.isclose(number(source_point.get("x")), number(target_point.get("x")), abs_tol=1.0):
                    errors.append(f"{line.get('id')}: 生命线必须竖向")
        if not any(cell.get("id") == "sequence-start" for cell in cells):
            errors.append("时序图缺少起点表示 sequence-start")
        if not any(cell.get("id") == "sequence-end" for cell in cells):
            errors.append("时序图缺少终点表示 sequence-end")
        message_edges = [cell for cell in edges if cell.get("id", "").startswith("message-") or cell.get("id", "").startswith("m")]
        if len(message_edges) < 4:
            errors.append("时序图横向请求和返回消息不完整")
        for edge in message_edges:
            source_point, target_point = point_pair(edge)
            if source_point is not None and target_point is not None:
                if not math.isclose(number(source_point.get("y")), number(target_point.get("y")), abs_tol=1.0):
                    errors.append(f"{edge.get('id')}: 时序消息必须横向")
    return errors, warnings


def collect_files(target: Path) -> list[tuple[Path, bool]]:
    if target.is_file():
        return [(target, "templates" in target.parts)]
    if target == ROOT or (target / "SKILL.md").exists():
        templates = sorted((target / "templates").glob("*.drawio"))
        examples = sorted((target / "examples").glob("*.drawio"))
        return [(path, True) for path in templates] + [(path, False) for path in examples]
    return [(path, False) for path in sorted(target.rglob("*.drawio"))]


def validate_catalog(target: Path) -> list[str]:
    errors: list[str] = []
    if not (target / "SKILL.md").exists():
        return errors
    templates_dir = target / "templates"
    examples_dir = target / "examples"
    template_names = {path.name for path in templates_dir.glob("*.drawio")}
    if template_names != EXPECTED_TEMPLATES:
        missing = sorted(EXPECTED_TEMPLATES - template_names)
        extra = sorted(template_names - EXPECTED_TEMPLATES)
        if missing:
            errors.append("缺少模板: " + ", ".join(missing))
        if extra:
            errors.append("存在非目标模板: " + ", ".join(extra))
    extra_example_files = [path for path in examples_dir.rglob("*") if path.is_file() and path.suffix.lower() != ".drawio"]
    if extra_example_files:
        errors.append("examples 只能包含 .drawio: " + ", ".join(str(path.relative_to(target)) for path in extra_example_files))
    lock_files = [path for path in target.rglob(".*") if path.is_file() and path.name.startswith(".$")]
    if lock_files:
        errors.append("存在临时锁文件: " + ", ".join(str(path.relative_to(target)) for path in lock_files))
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true", help="将警告视为失败")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists():
        print(f"错误: 路径不存在: {target}")
        return 1

    total_errors = validate_catalog(target)
    total_warnings: list[str] = []
    files = collect_files(target)
    if not files:
        total_errors.append("未找到 .drawio 文件")
    for path, allow_placeholders in files:
        errors, warnings = validate_file(path, allow_placeholders)
        label = str(path.relative_to(target)) if target.is_dir() else path.name
        for item in errors:
            total_errors.append(f"{label}: {item}")
        for item in warnings:
            total_warnings.append(f"{label}: {item}")

    for item in total_errors:
        print("错误: " + item)
    for item in total_warnings:
        print("警告: " + item)
    if total_errors or (args.strict and total_warnings):
        return 1
    print(f"校验通过: {len(files)} 个 Draw.io 文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
