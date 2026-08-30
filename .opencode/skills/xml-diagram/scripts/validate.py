#!/usr/bin/env python3
"""Lightweight Draw.io validator using only the Python standard library."""

from __future__ import annotations

import argparse
import base64
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote_to_bytes


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TEMPLATES = {
    "architecture.drawio",
    "architecture-data.drawio",
    "comparison.drawio",
    "decision-matrix.drawio",
    "flow-branching.drawio",
    "flow-linear.drawio",
    "lifecycle.drawio",
    "relationship-dependency.drawio",
    "relationship-er.drawio",
    "relationship-knowledge.drawio",
    "roadmap.drawio",
    "sequence.drawio",
    "state.drawio",
    "summary.drawio",
    "swot.drawio",
    "timeline.drawio",
}
EXPECTED_EXAMPLE_MARKERS = {
    "architecture-data-",
    "architecture-application-",
    "architecture-business-",
    "architecture-deployment-",
    "architecture-technical-",
    "comparison-",
    "decision-matrix-",
    "flow-branching-",
    "flow-linear-",
    "lifecycle-",
    "relationship-dependency-",
    "relationship-er-",
    "relationship-knowledge-",
    "roadmap-",
    "sequence-",
    "state-",
    "summary-",
    "swot-",
    "timeline-",
}
REQUIRED_SUPPORT_FILES = {
    "references/theme-tokens.md",
    "references/visual-style.md",
    "references/icon-policy.md",
    "scripts/palette.py",
    "scripts/style_map.py",
    "tests/test_palette.py",
    "tests/test_style_map.py",
    "tests/test_validate.py",
}
PLACEHOLDER_RE = re.compile(
    r"(图形标题|区域标题|卡片标题|内容标签|参与者 [ABCD]|处理步骤|实体 [AB]|阶段 [AB]|主题节点|"
    r"能力[一二三]|目标[一二三]|要点[一二三]|关键因素[一二三])$"
)
MOJIBAKE = ("锟", "�", "鐢", "鍥", "绋", "瑙")
TITLE_RE = re.compile(r"(^|[-_])(title|diagram-title)([-_]|$)", re.IGNORECASE)
EMOJI_RE = re.compile("[\u2600-\u27BF\U0001F300-\U0001FAFF]")
ICON_FONTS = ("font awesome", "material icons", "segoe mdl2 assets", "bootstrap icons")
ALLOWED_THEMES = {"tech-blue", "vibrant", "mint-green", "steady-red-blue"}
ALLOWED_MODULES = {"top-band", "aux-column", "callout", "numbered-flow", "focus-node", "footer-band"}
OPTIONAL_MODULES = "top-band aux-column callout numbered-flow focus-node footer-band"
VISUAL_CONTRACT = "enterprise-v2"
ALLOWED_COLOR_ROLES = {
    "axis-main",
    "axis-cross",
    "side-rail",
    "focus",
    "data-flow",
    "group",
    "connector",
}
ALLOWED_LAYOUTS = {"vertical-stack", "horizontal-flow", "mixed-axis", "matrix", "network", "timeline"}
ALLOWED_DOMINANT_AXES = {"x", "y", "mixed", "grid", "radial"}


@dataclass(frozen=True)
class Box:
    cell_id: str
    parent_id: str
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


def validate_embedded_svg(image: str, cell_id: str, errors: list[str]) -> None:
    """Validate that a Draw.io image is a self-contained, parseable SVG data URI."""
    if not image.lower().startswith("data:image/svg+xml"):
        errors.append(f"{cell_id}: 图片必须使用内嵌 SVG data URI，禁止外部、相对或本地路径")
        return
    if "," not in image:
        errors.append(f"{cell_id}: 内嵌 SVG data URI 缺少内容")
        return
    metadata, payload = image.split(",", 1)
    try:
        raw = base64.b64decode(payload, validate=True) if ";base64" in metadata.lower() else unquote_to_bytes(payload)
        source = raw.decode("utf-8")
        root = ET.fromstring(source)
    except (ValueError, UnicodeDecodeError, ET.ParseError) as exc:
        errors.append(f"{cell_id}: 内嵌 SVG 无法解析: {exc}")
        return
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        errors.append(f"{cell_id}: 内嵌图片根节点必须是 SVG")
        return
    namespace_free = re.sub(r"xmlns(?::\w+)?=[\"']https?://[^\"']+[\"']", "", source, flags=re.IGNORECASE)
    lowered = namespace_free.lower()
    if "http://" in lowered or "https://" in lowered or "@import" in lowered or "@font-face" in lowered:
        errors.append(f"{cell_id}: 内嵌 SVG 禁止远程资源、外部 CSS 或字体")
    for element in root.iter():
        element_name = element.tag.rsplit("}", 1)[-1].lower()
        if element_name == "image":
            errors.append(f"{cell_id}: 内嵌 SVG 禁止嵌套 image")
        if element_name in {"script", "foreignobject"}:
            errors.append(f"{cell_id}: 内嵌 SVG 禁止 script 或 foreignObject")
        for attribute, value in element.attrib.items():
            name = attribute.rsplit("}", 1)[-1].lower()
            stripped = value.strip()
            if name == "href" and stripped and not stripped.startswith("#"):
                errors.append(f"{cell_id}: 内嵌 SVG href 只允许本地 #id 引用")
            for reference in re.findall(r"url\(([^)]+)\)", stripped, re.IGNORECASE):
                if not reference.strip(" '\"").startswith("#"):
                    errors.append(f"{cell_id}: 内嵌 SVG url() 只允许本地 #id 引用")


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


def contains(first: Box, second: Box, tolerance: float = 0.01) -> bool:
    return (
        first.x - tolerance <= second.x
        and first.y - tolerance <= second.y
        and first.right + tolerance >= second.right
        and first.bottom + tolerance >= second.bottom
    )


def is_background(box: Box, page_width: float, page_height: float) -> bool:
    cell_id = box.cell_id.lower()
    return cell_id in {"bg", "background", "canvas"} or (
        math.isclose(box.x, 0.0)
        and math.isclose(box.y, 0.0)
        and math.isclose(box.width, page_width)
        and math.isclose(box.height, page_height)
    )


def is_title(box: Box) -> bool:
    font_size = number(style_map(box.style).get("fontSize"), 12)
    return bool(TITLE_RE.search(box.cell_id)) or font_size >= 20


def point_pair(cell: ET.Element) -> tuple[ET.Element | None, ET.Element | None]:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return None, None
    return geometry.find("mxPoint[@as='sourcePoint']"), geometry.find("mxPoint[@as='targetPoint']")


def build_boxes(cells: list[ET.Element], errors: list[str]) -> tuple[list[Box], dict[str, Box]]:
    cell_by_id = {cell.get("id", ""): cell for cell in cells if cell.get("id")}
    raw: dict[str, tuple[float, float, float, float]] = {}

    for cell in cells:
        if cell.get("vertex") != "1":
            continue
        cell_id = cell.get("id", "<unknown>")
        geometry = cell.find("mxGeometry")
        style = cell.get("style", "")
        if geometry is None:
            errors.append(f"{cell_id}: 可见节点缺少 mxGeometry")
            continue
        parent = cell_by_id.get(cell.get("parent", ""))
        if parent is not None and parent.get("edge") == "1" and geometry.get("relative") == "1":
            # Draw.io edge labels are relative vertices and do not have box dimensions.
            continue
        if geometry.get("w") is not None or geometry.get("h") is not None:
            errors.append(f"{cell_id}: mxGeometry 禁止使用 w/h，必须使用 width/height")
            continue
        if "shape=line" in style:
            width = number(geometry.get("width"), 1.0)
            height = number(geometry.get("height"))
        else:
            if geometry.get("width") is None or geometry.get("height") is None:
                errors.append(f"{cell_id}: 可见节点必须包含 width 和 height")
                continue
            width = number(geometry.get("width"))
            height = number(geometry.get("height"))
        if width <= 0 or height <= 0:
            errors.append(f"{cell_id}: 可见节点宽高必须为正数")
            continue
        raw[cell_id] = (number(geometry.get("x")), number(geometry.get("y")), width, height)

    absolute: dict[str, tuple[float, float, float, float]] = {}
    resolving: set[str] = set()

    def resolve(cell_id: str) -> tuple[float, float, float, float]:
        if cell_id in absolute:
            return absolute[cell_id]
        if cell_id in resolving:
            errors.append(f"{cell_id}: parent 引用形成循环")
            return raw[cell_id]
        resolving.add(cell_id)
        x, y, width, height = raw[cell_id]
        parent_id = cell_by_id[cell_id].get("parent", "")
        if parent_id in raw:
            parent_x, parent_y, _, _ = resolve(parent_id)
            x += parent_x
            y += parent_y
        resolving.remove(cell_id)
        absolute[cell_id] = (x, y, width, height)
        return absolute[cell_id]

    boxes: list[Box] = []
    for cell_id in raw:
        cell = cell_by_id[cell_id]
        x, y, width, height = resolve(cell_id)
        boxes.append(
            Box(
                cell_id,
                cell.get("parent", ""),
                x,
                y,
                width,
                height,
                cell.get("style", ""),
                cell.get("value", ""),
            )
        )
    return boxes, {box.cell_id: box for box in boxes}


def edge_points(cell: ET.Element, box_by_id: dict[str, Box]) -> list[tuple[float, float]]:
    geometry = cell.find("mxGeometry")
    points: list[tuple[float, float]] = []
    if geometry is not None:
        for point in geometry.findall(".//mxPoint"):
            if point.get("x") is not None and point.get("y") is not None:
                points.append((number(point.get("x")), number(point.get("y"))))
    for key in ("source", "target"):
        reference = cell.get(key)
        if reference in box_by_id:
            box = box_by_id[reference]
            points.append((box.x + box.width / 2, box.y + box.height / 2))
    return points


def diagram_kind(path: Path, diagram_name: str) -> str:
    name = f"{path.name.lower()} {diagram_name.lower()}"
    for kind in (
        "architecture-data",
        "flow-linear",
        "flow-branching",
        "sequence",
        "state",
        "lifecycle",
        "relationship-er",
        "relationship-dependency",
        "relationship-knowledge",
        "roadmap",
        "timeline",
        "decision-matrix",
        "comparison",
        "swot",
        "summary",
        "architecture",
    ):
        if kind in name:
            return kind
    return ""


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
    diagram = root.find("diagram") if root.tag == "mxfile" else None
    if diagram is not None:
        theme = diagram.get("theme")
        if theme and theme not in ALLOWED_THEMES:
            errors.append(f"未知主题键: {theme}")
        if path.parent.name == "templates" and path.name in {"architecture.drawio", "architecture-data.drawio"}:
            if diagram.get("layout") != "vertical-stack":
                errors.append("架构模板必须声明 layout=vertical-stack")
            if diagram.get("optionalModules") != OPTIONAL_MODULES:
                errors.append("架构模板缺少完整的可选模块声明")
    models = [root] if root.tag == "mxGraphModel" else list(root.findall(".//mxGraphModel"))
    if not models:
        return errors + ["缺少 mxGraphModel"], warnings
    if len(models) > 1:
        errors.append("每个示例或模板只允许一个 mxGraphModel，避免多页匹配歧义")
    model = models[0]
    if model.get("grid") != "0":
        errors.append("mxGraphModel 必须显式设置 grid=0")

    page_width = number(model.get("pageWidth"))
    page_height = number(model.get("pageHeight"))
    if page_width <= 0 or page_height <= 0:
        errors.append("pageWidth 和 pageHeight 必须为正数")

    cells = list(model.findall(".//mxCell"))
    cell_by_id = {cell.get("id", ""): cell for cell in cells if cell.get("id")}
    ids = [cell.get("id", "") for cell in cells]
    duplicate_ids = sorted({cell_id for cell_id in ids if cell_id and ids.count(cell_id) > 1})
    if duplicate_ids:
        errors.append("mxCell id 重复: " + ", ".join(duplicate_ids))
    known_ids = set(ids)

    if diagram is not None and diagram.get("visualContract") == VISUAL_CONTRACT:
        layout = diagram.get("layout")
        if layout not in ALLOWED_LAYOUTS:
            errors.append(f"视觉合同缺少有效 layout: {layout or '<empty>'}")
        dominant_axis = diagram.get("dominantAxis")
        if dominant_axis not in ALLOWED_DOMINANT_AXES:
            errors.append(f"视觉合同缺少有效 dominantAxis: {dominant_axis or '<empty>'}")

        visual_nodes = [cell for cell in cells if cell.get("role") == "node"]
        for cell in visual_nodes:
            color_role = cell.get("colorRole")
            label = cell.get("id", "<node>")
            if not color_role:
                errors.append(f"{label}: enterprise-v2 节点缺少 colorRole")
            elif color_role not in ALLOWED_COLOR_ROLES:
                errors.append(f"{label}: 未知 colorRole {color_role}")
        if visual_nodes and not any(cell.get("visualRole") == "focus" for cell in visual_nodes):
            warnings.append("enterprise-v2 缺少明确视觉焦点")

        declared_modules = set((diagram.get("modules") or "").split())
        actual_modules = {cell.get("module") for cell in cells if cell.get("module")}
        for module in sorted(declared_modules - actual_modules):
            errors.append(f"声明的附加模块 {module} 不存在实际元素")
        for module in sorted(actual_modules - declared_modules):
            errors.append(f"附加模块 {module} 未在 modules 中声明")

        page_titles = [cell for cell in cells if cell.get("role") == "page-title"]
        if len(page_titles) != 1:
            errors.append("enterprise-v2 必须包含一个 role=page-title")
        elif number(style_map(page_titles[0].get("style", "")).get("fontSize"), 0) < 32:
            warnings.append("页面标题层级不足: enterprise-v2 建议字号不小于 32px")

    def effective_background(cell: ET.Element) -> str | None:
        current: ET.Element | None = cell
        visited: set[str] = set()
        while current is not None:
            fill = style_map(current.get("style", "")).get("fillColor")
            if fill not in {None, "none"}:
                return fill
            parent_id = current.get("parent", "")
            if not parent_id or parent_id in visited:
                break
            visited.add(parent_id)
            current = cell_by_id.get(parent_id)
        return model.get("background")

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
        module = cell.get("module")
        if module and module not in ALLOWED_MODULES:
            errors.append(f"{cell_id}: 未知附加模块 {module}")
        font_size = number(style.get("fontSize"), 12)
        if cell.get("value") and font_size < 11:
            errors.append(f"{cell_id}: 字号 {font_size:g} 小于 11")
        raw_style = cell.get("style", "")
        image = style.get("image", "").strip()
        if image:
            validate_embedded_svg(image, cell_id, errors)
        font_family = style.get("fontFamily", "").lower()
        if any(name in font_family for name in ICON_FONTS):
            errors.append(f"{cell_id}: 禁止使用图标字体")
        if EMOJI_RE.search(cell.get("value", "")):
            errors.append(f"{cell_id}: 禁止使用 Emoji 代替图标")
        if "underline" in raw_style.lower() or "fontStyle=4" in raw_style:
            errors.append(f"{cell_id}: 禁止标题或文字下划线")
        if (style.get("shadow") == "1" or model.get("shadow") == "1") and not (
            diagram is not None and diagram.get("visualContract") == VISUAL_CONTRACT
        ):
            warnings.append(f"{cell_id}: 检测到阴影，应确认仅为浅色轻微阴影")
        foreground = style.get("fontColor")
        background = effective_background(cell)
        if cell.get("value", "").strip() and foreground and background:
            ratio = contrast(foreground, background)
            threshold = 3.0 if font_size >= 18 or (font_size >= 14 and "fontStyle=1" in raw_style) else 4.5
            if ratio is not None and ratio + 1e-6 < threshold:
                errors.append(f"{cell_id}: 文字对比度 {ratio:.2f}:1 低于 {threshold:.1f}:1")

    boxes, box_by_id = build_boxes(cells, errors)
    content_boxes = [box for box in boxes if not is_background(box, page_width, page_height) and "shape=line" not in box.style]

    for box in content_boxes:
        minimum = 20 if is_title(box) else 30
        if box.x < minimum or box.y < minimum or box.right > page_width - minimum or box.bottom > page_height - minimum:
            errors.append(f"{box.cell_id}: 超出画布安全边距")
        parent = box_by_id.get(box.parent_id)
        if parent is not None and not contains(parent, box):
            errors.append(f"{box.cell_id}: 超出父容器 {parent.cell_id}")

    for index, first in enumerate(content_boxes):
        for second in content_boxes[index + 1 :]:
            if first.parent_id != second.parent_id or not intersects(first, second):
                continue
            if contains(first, second) or contains(second, first):
                continue
            errors.append(f"同级元素重叠: {first.cell_id} 与 {second.cell_id}")

    horizontal_groups: dict[tuple[str, int, int], list[Box]] = {}
    for box in content_boxes:
        if is_title(box):
            continue
        horizontal_groups.setdefault((box.parent_id, round(box.y / 4), round(box.width / 4)), []).append(box)
    for group in horizontal_groups.values():
        if len(group) < 3:
            continue
        ordered = sorted(group, key=lambda item: item.x)
        gaps = []
        for index in range(len(ordered) - 1):
            first, second = ordered[index], ordered[index + 1]
            intervening = any(
                candidate.parent_id == first.parent_id
                and candidate.cell_id not in {first.cell_id, second.cell_id}
                and candidate.y < first.bottom
                and candidate.bottom > first.y
                and candidate.x >= first.right
                and candidate.right <= second.x
                for candidate in content_boxes
            )
            if not intervening:
                gaps.append(second.x - first.right)
        if len(gaps) < 2:
            continue
        if min(gaps) >= 0 and max(gaps) - min(gaps) > 4:
            warnings.append("同级元素间距不均匀: " + ", ".join(box.cell_id for box in ordered))

    diagram = root.find("diagram")
    diagram_name = diagram.get("name", "") if diagram is not None else ""
    kind = diagram_kind(path, diagram_name)
    edges = [cell for cell in cells if cell.get("edge") == "1"]

    for edge in edges:
        for x, y in edge_points(edge, box_by_id):
            if x < 0 or y < 0 or x > page_width or y > page_height:
                errors.append(f"{edge.get('id', '<unknown>')}: 连线路径超出画布")
                break

        source = box_by_id.get(edge.get("source", ""))
        target = box_by_id.get(edge.get("target", ""))
        if source is not None and target is not None:
            source_center = (source.x + source.width / 2, source.y + source.height / 2)
            target_center = (target.x + target.width / 2, target.y + target.height / 2)
            horizontal = math.isclose(source_center[1], target_center[1], abs_tol=1.0)
            vertical = math.isclose(source_center[0], target_center[0], abs_tol=1.0)
            if horizontal or vertical:
                for box in content_boxes:
                    if box.cell_id in {source.cell_id, target.cell_id}:
                        continue
                    if horizontal:
                        low, high = sorted((source_center[0], target_center[0]))
                        crosses = low < box.right and high > box.x and box.y < source_center[1] < box.bottom
                    else:
                        low, high = sorted((source_center[1], target_center[1]))
                        crosses = low < box.bottom and high > box.y and box.x < source_center[0] < box.right
                    if crosses:
                        errors.append(f"{edge.get('id', '<unknown>')}: 连线穿越无关节点 {box.cell_id}")
                        break

        source_point, target_point = point_pair(edge)
        if source_point is not None and target_point is not None and kind not in {
            "relationship-er",
            "relationship-dependency",
            "relationship-knowledge",
        }:
            dx = abs(number(source_point.get("x")) - number(target_point.get("x")))
            dy = abs(number(source_point.get("y")) - number(target_point.get("y")))
            if dx > 80 and dy > 80:
                errors.append(f"{edge.get('id', '<unknown>')}: 存在长斜线风险，应改用正交折线")

    if kind in {"architecture", "architecture-data"}:
        regions = [box for box in boxes if re.fullmatch(r"region-(?:\d+|crosscut)", box.cell_id)]
        for region in regions:
            title = box_by_id.get(f"{region.cell_id}-title")
            if title is None or not title.value.strip():
                errors.append(f"{region.cell_id}: 架构一级区域缺少独立标题")
                continue
            if title.parent_id == region.cell_id:
                errors.append(f"{title.cell_id}: 架构一级标题必须位于容器外部")
            if title.bottom > region.y:
                errors.append(f"{title.cell_id}: 架构一级标题必须位于对应容器上方")
            title_gap = region.y - title.bottom
            if title_gap < 8 or title_gap > 12:
                warnings.append(f"{title.cell_id}: 一级标题与容器间距应为 8～12px，当前 {title_gap:g}px")
            if abs(title.x - region.x) > 20:
                warnings.append(f"{title.cell_id}: 一级标题应与容器内容左边缘对齐")

            region_cards = [box for box in boxes if box.parent_id == region.cell_id and box.cell_id.startswith("card-")]
            if region_cards:
                top_gap = min(card.y for card in region_cards) - region.y
                if top_gap > 24:
                    warnings.append(f"{region.cell_id}: 首行卡片距容器顶部 {top_gap:g}px，存在过多留白")

        cards = [box for box in boxes if box.cell_id.startswith("card-") and box.value.strip() == ""]
        for card in cards:
            children = [box for box in boxes if box.parent_id == card.cell_id]
            titles = [child for child in children if "title" in child.cell_id and child.value.strip()]
            if not titles:
                errors.append(f"{card.cell_id}: 架构分组卡片缺少独立文字标题")
                continue
            title = titles[0]
            title_style = style_map(title.style)
            if title_style.get("align") != "center":
                errors.append(f"{title.cell_id}: 架构二级标题必须水平居中")
            if not math.isclose(title.x + title.width / 2, card.x + card.width / 2, abs_tol=2.0):
                errors.append(f"{title.cell_id}: 架构二级标题条必须与卡片共用中心轴")
            content = [child for child in children if child.cell_id != title.cell_id and child.value.strip()]
            if content:
                content_gap = min(child.y for child in content) - title.bottom
                if content_gap < 12 or content_gap > 16:
                    warnings.append(f"{card.cell_id}: 二级标题到内容间距应为 12～16px，当前 {content_gap:g}px")

    if kind == "architecture-data":
        layers = sorted(
            (box for box in boxes if re.fullmatch(r"region-\d+", box.cell_id)),
            key=lambda box: box.y,
        )
        if len(layers) < 3:
            errors.append("数据架构图至少需要 3 个有效主层")
        for index, layer in enumerate(layers):
            cards = [box for box in boxes if box.parent_id == layer.cell_id and box.cell_id.startswith("card-")]
            if not cards:
                errors.append(f"{layer.cell_id}: 禁止保留空层")
            if index:
                previous = layers[index - 1]
                if layer.y <= previous.y:
                    errors.append(f"{layer.cell_id}: 主层必须自上而下排列")
                if layer.y - previous.bottom < 20:
                    errors.append(f"{layer.cell_id}: 主层间距不足 20px")
                if not math.isclose(layer.x, previous.x, abs_tol=2.0) or not math.isclose(layer.width, previous.width, abs_tol=2.0):
                    errors.append(f"{layer.cell_id}: 主层必须等宽并纵向对齐")

        data_flows = [edge for edge in edges if edge.get("id", "").startswith("data-flow-")]
        if layers and not data_flows:
            errors.append("数据架构图缺少聚合主数据流")
        if len(data_flows) > 3:
            warnings.append("数据架构图连线过多，应合并为聚合数据流或拆分血缘关系图")
        for flow in data_flows:
            source_point, target_point = point_pair(flow)
            if source_point is None or target_point is None:
                errors.append(f"{flow.get('id')}: 主数据流必须具有明确起止点")
                continue
            source_x, source_y = number(source_point.get("x")), number(source_point.get("y"))
            target_x, target_y = number(target_point.get("x")), number(target_point.get("y"))
            if target_y <= source_y:
                errors.append(f"{flow.get('id')}: 主数据流必须总体向下")
            if not math.isclose(source_x, target_x, abs_tol=1.0) and style_map(flow.get("style", "")).get("edgeStyle") != "orthogonalEdgeStyle":
                errors.append(f"{flow.get('id')}: 主数据流必须使用正交路径")

    if kind in {"flow-linear", "flow-branching"}:
        if "flow-start" not in known_ids or "flow-end" not in known_ids:
            errors.append("流程图必须包含 flow-start 和 flow-end")
        if len(edges) < 2:
            errors.append("流程图缺少完整流程连线")
        adjacency: dict[str, list[str]] = {}
        for edge in edges:
            source_id, target_id = edge.get("source", ""), edge.get("target", "")
            if source_id and target_id:
                adjacency.setdefault(source_id, []).append(target_id)
        pending, reached = ["flow-start"], set()
        while pending:
            current = pending.pop()
            if current in reached:
                continue
            reached.add(current)
            pending.extend(adjacency.get(current, []))
        if "flow-start" in known_ids and "flow-end" in known_ids and "flow-end" not in reached:
            errors.append("流程图从 flow-start 无法到达 flow-end")

        start_box, end_box = box_by_id.get("flow-start"), box_by_id.get("flow-end")
        if start_box is not None and end_box is not None:
            start_center = (start_box.x + start_box.width / 2, start_box.y + start_box.height / 2)
            end_center = (end_box.x + end_box.width / 2, end_box.y + end_box.height / 2)
            horizontal_main = abs(end_center[0] - start_center[0]) >= abs(end_center[1] - start_center[1])
            for edge in edges:
                if edge.get("target", "").startswith("error-"):
                    continue
                source_box = box_by_id.get(edge.get("source", ""))
                target_box = box_by_id.get(edge.get("target", ""))
                if source_box is None or target_box is None:
                    continue
                source_axis = source_box.x + source_box.width / 2 if horizontal_main else source_box.y + source_box.height / 2
                target_axis = target_box.x + target_box.width / 2 if horizontal_main else target_box.y + target_box.height / 2
                if target_axis + 1 < source_axis:
                    errors.append(f"{edge.get('id', '<unknown>')}: 主流程沿主轴反向，存在蛇形折返")
            for box in boxes:
                if not box.cell_id.startswith("error-"):
                    continue
                offset = abs((box.y + box.height / 2) - start_center[1]) if horizontal_main else abs((box.x + box.width / 2) - start_center[0])
                if offset < 32:
                    errors.append(f"{box.cell_id}: 异常分支应明显偏离主流程轴线")

        for decision in (box for box in boxes if box.cell_id.startswith("decision-")):
            outgoing = [edge for edge in edges if edge.get("source") == decision.cell_id]
            if len(outgoing) < 2:
                errors.append(f"{decision.cell_id}: 判断节点至少需要两个出口")
            unlabeled = [edge.get("id", "") for edge in outgoing if not edge.get("value", "").strip()]
            if unlabeled:
                errors.append(f"{decision.cell_id}: 判断出口必须有标签: " + ", ".join(unlabeled))

    if kind == "state":
        unlabeled = [cell.get("id", "") for cell in edges if not cell.get("value", "").strip()]
        if unlabeled:
            errors.append("状态图转换必须有标签: " + ", ".join(unlabeled))

    if kind == "sequence":
        participants = [cell for cell in cells if cell.get("id", "").startswith("participant-")]
        lifelines = [cell for cell in cells if cell.get("id", "").startswith("lifeline-")]
        if len(participants) < 2:
            errors.append("时序图至少需要两个参与者")
        if len(lifelines) != len(participants):
            errors.append("时序图每个参与者都必须具有完整竖向生命线")
        for line in lifelines:
            geometry = line.find("mxGeometry")
            if line.get("vertex") == "1":
                if geometry is None or number(geometry.get("height")) <= number(geometry.get("width"), 1.0):
                    errors.append(f"{line.get('id')}: 生命线必须竖向")
            else:
                source_point, target_point = point_pair(line)
                if source_point is None or target_point is None:
                    errors.append(f"{line.get('id')}: 生命线缺少完整起止点")
                elif not math.isclose(number(source_point.get("x")), number(target_point.get("x")), abs_tol=1.0):
                    errors.append(f"{line.get('id')}: 生命线必须竖向")
        if "sequence-start" not in known_ids:
            errors.append("时序图缺少起点 sequence-start")
        if "sequence-end" not in known_ids:
            errors.append("时序图缺少终点 sequence-end")
        message_edges = [cell for cell in edges if cell.get("id", "").startswith(("message-", "return-"))]
        if len(message_edges) < 4:
            errors.append("时序图横向请求和返回消息不完整")
        for edge in message_edges:
            source_point, target_point = point_pair(edge)
            if source_point is None or target_point is None:
                errors.append(f"{edge.get('id')}: 时序消息缺少明确起止点")
            elif not math.isclose(number(source_point.get("y")), number(target_point.get("y")), abs_tol=1.0):
                errors.append(f"{edge.get('id')}: 时序消息必须横向")
        if not any(cell.get("id", "").startswith("return-") for cell in message_edges):
            errors.append("时序图必须包含至少一条返回消息")

        participant_boxes = {
            box.cell_id.removeprefix("participant-"): box
            for box in boxes
            if box.cell_id.startswith("participant-")
        }
        lifeline_cells = {
            cell.get("id", "").removeprefix("lifeline-"): cell
            for cell in lifelines
        }
        endpoint_x: set[float] = set()
        last_message_y = 0.0
        for edge in message_edges:
            source_point, target_point = point_pair(edge)
            if source_point is None or target_point is None:
                continue
            endpoint_x.update((round(number(source_point.get("x")), 1), round(number(target_point.get("x")), 1)))
            last_message_y = max(last_message_y, number(source_point.get("y")), number(target_point.get("y")))
        for suffix, participant in participant_boxes.items():
            line = lifeline_cells.get(suffix)
            if line is None:
                errors.append(f"participant-{suffix}: 缺少对应 lifeline-{suffix}")
                continue
            source_point, target_point = point_pair(line)
            if source_point is None or target_point is None:
                continue
            center_x = participant.x + participant.width / 2
            if not math.isclose(number(source_point.get("x")), center_x, abs_tol=1.0):
                errors.append(f"lifeline-{suffix}: 生命线必须位于参与者中心")
            if not math.isclose(number(source_point.get("y")), participant.bottom, abs_tol=1.0):
                errors.append(f"lifeline-{suffix}: 生命线必须从参与者底部开始")
            if number(target_point.get("y")) + 1 < last_message_y:
                errors.append(f"lifeline-{suffix}: 生命线必须覆盖最后一条消息")
            if round(center_x, 1) not in endpoint_x:
                errors.append(f"participant-{suffix}: 未参与任何请求或返回消息")

    if content_boxes and page_width > 0 and page_height > 0 and not allow_placeholders:
        min_x = min(box.x for box in content_boxes)
        min_y = min(box.y for box in content_boxes)
        max_x = max(box.right for box in content_boxes)
        max_y = max(box.bottom for box in content_boxes)
        utilization = ((max_x - min_x) * (max_y - min_y)) / (page_width * page_height)
        if utilization < 0.45:
            warnings.append(f"内容包围盒利用率 {utilization:.1%}，需检查大面积空白")
        elif utilization > 0.85:
            warnings.append(f"内容包围盒利用率 {utilization:.1%}，需检查拥挤或裁切")
        left, right = min_x, page_width - max_x
        top, bottom = min_y, page_height - max_y
        if abs(left - right) > 120:
            warnings.append(f"左右留白失衡: 左 {left:g}px / 右 {right:g}px")
        if abs(top - bottom) > 120:
            warnings.append(f"上下留白失衡: 上 {top:g}px / 下 {bottom:g}px")

    values = [re.sub(r"<[^>]+>", "", cell.get("value", "")).strip() for cell in cells]
    if not allow_placeholders:
        placeholders = [value for value in values if value and PLACEHOLDER_RE.search(value)]
        if placeholders:
            errors.append("示例或输出残留模板占位内容: " + ", ".join(sorted(set(placeholders))))
    return errors, warnings


def geometry_signature(path: Path) -> tuple[tuple[str, ...], ...]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    model = root if root.tag == "mxGraphModel" else root.find(".//mxGraphModel")
    if model is None:
        return ()
    result: list[tuple[str, ...]] = []
    for cell in model.findall(".//mxCell"):
        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue
        points = tuple(
            f"{point.get('as', '')}:{point.get('x', '')}:{point.get('y', '')}"
            for point in geometry.findall(".//mxPoint")
        )
        style = style_map(cell.get("style", ""))
        structural_style = tuple(
            f"{key}={style.get(key, '')}"
            for key in (
                "rounded",
                "arcSize",
                "dashed",
                "endArrow",
                "startArrow",
                "edgeStyle",
                "strokeWidth",
                "shape",
                "align",
            )
        )
        result.append(
            (
                cell.get("id", ""),
                cell.get("parent", ""),
                cell.get("source", ""),
                cell.get("target", ""),
                geometry.get("x", ""),
                geometry.get("y", ""),
                geometry.get("width", ""),
                geometry.get("height", ""),
                geometry.get("relative", ""),
                *structural_style,
                *points,
            )
        )
    return tuple(result)


def collect_files(target: Path) -> list[tuple[Path, bool]]:
    if target.is_file():
        return [(target, "templates" in target.parts)]
    if target == ROOT or (target / "SKILL.md").exists():
        templates = sorted((target / "templates").glob("*.drawio"))
        examples = sorted((target / "examples").glob("*.drawio"))
        return [(path, True) for path in templates] + [(path, False) for path in examples]
    return [(path, False) for path in sorted(target.rglob("*.drawio"))]


def validate_theme_pairs(target: Path) -> list[str]:
    errors: list[str] = []
    for light in target.rglob("*-light-*.drawio"):
        dark = light.with_name(light.name.replace("-light-", "-dark-"))
        if dark.exists() and geometry_signature(light) != geometry_signature(dark):
            errors.append(f"浅深版本几何不一致: {light.relative_to(target)} / {dark.relative_to(target)}")
    return errors


def validate_catalog(target: Path) -> list[str]:
    errors: list[str] = []
    if not (target / "SKILL.md").exists():
        return errors
    missing_support = sorted(path for path in REQUIRED_SUPPORT_FILES if not (target / path).is_file())
    if missing_support:
        errors.append("缺少主题或图标支持文件: " + ", ".join(missing_support))
    representative = target / "examples" / "architecture-application-light-ecommerce.drawio"
    if representative.is_file():
        tree = ET.parse(representative)
        if not tree.findall(".//mxCell[@module='focus-node']"):
            errors.append("代表架构示例缺少 focus-node 附加模块")
        if not tree.findall(".//mxCell[@role='icon']"):
            errors.append("代表架构示例缺少语义图标")
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
    example_names = {path.name for path in examples_dir.glob("*.drawio")}
    for marker in sorted(EXPECTED_EXAMPLE_MARKERS):
        if not any(name.startswith(marker) for name in example_names):
            errors.append(f"缺少示例类型: {marker.rstrip('-')}")
    extra_example_files = [path for path in examples_dir.rglob("*") if path.is_file() and path.suffix.lower() != ".drawio"]
    if extra_example_files:
        errors.append("examples 只能包含 .drawio: " + ", ".join(str(path.relative_to(target)) for path in extra_example_files))
    lock_files = [path for path in target.rglob(".*") if path.is_file() and path.name.startswith(".$")]
    if lock_files:
        errors.append("存在临时锁文件: " + ", ".join(str(path.relative_to(target)) for path in lock_files))
    errors.extend(validate_theme_pairs(examples_dir))
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
    if target.is_dir() and not (target / "SKILL.md").exists():
        total_errors.extend(validate_theme_pairs(target))
    total_warnings: list[str] = []
    files = collect_files(target)
    if not files:
        total_errors.append("未找到 .drawio 文件")
    for path, allow_placeholders in files:
        errors, warnings = validate_file(path, allow_placeholders)
        label = str(path.relative_to(target)) if target.is_dir() else path.name
        total_errors.extend(f"{label}: {item}" for item in errors)
        total_warnings.extend(f"{label}: {item}" for item in warnings)

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
