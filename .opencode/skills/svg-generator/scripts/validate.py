#!/usr/bin/env python3
"""Validate svg-generator templates, examples, and generated SVG files."""

from __future__ import annotations

import argparse
import math
import os
import re
import struct
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TEMPLATES = {
    "architecture.svg",
    "architecture-business.svg",
    "architecture-data.svg",
    "architecture-deployment.svg",
    "architecture-technical.svg",
    "comparison.svg",
    "decision-matrix.svg",
    "flow-branching.svg",
    "flow-linear.svg",
    "lifecycle.svg",
    "relationship-dependency.svg",
    "relationship-er.svg",
    "relationship-knowledge.svg",
    "roadmap.svg",
    "sequence.svg",
    "state.svg",
    "summary.svg",
    "swot.svg",
    "timeline.svg",
}
EXPECTED_EXAMPLE_PREFIXES = {
    "architecture-business-",
    "architecture-application-",
    "architecture-technical-",
    "architecture-deployment-",
    "architecture-data-",
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
    "references/catalog.md",
    "references/theme-tokens.md",
    "references/visual-style.md",
    "references/icon-policy.md",
    "scripts/palette.py",
    "scripts/style_map.py",
    "tests/test_palette.py",
    "tests/test_style_map.py",
    "tests/test_catalog_contract.py",
}

NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
URL_REF_RE = re.compile(r"url\(\s*#([^)\s]+)\s*\)")
TRANSLATE_RE = re.compile(r"translate\(\s*(-?\d+(?:\.\d+)?)\s*(?:[, ]\s*(-?\d+(?:\.\d+)?))?\s*\)")
PLACEHOLDER_RE = re.compile(r"示例|占位|TODO|待填写|\{\{[^}]+\}\}", re.IGNORECASE)
HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
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
    "domain-app",
    "domain-control",
    "domain-network",
    "domain-data",
    "status-success",
    "status-warning",
    "status-error",
}
ALLOWED_LAYOUTS = {"vertical-stack", "horizontal-flow", "mixed-axis", "matrix", "network", "timeline"}
ALLOWED_DOMINANT_AXES = {"x", "y", "mixed", "grid", "radial"}


@dataclass(frozen=True)
class Box:
    element_id: str
    role: str
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def number(value: str | None, default: float | None = None) -> float | None:
    if value is None:
        return default
    match = NUMBER_RE.search(value)
    return float(match.group()) if match else default


def style_map(element: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in (element.get("style") or "").split(";"):
        if ":" in part:
            key, value = part.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def attr(element: ET.Element, name: str) -> str | None:
    return element.get(name) or style_map(element).get(name)


def walk(element: ET.Element, offset_x: float = 0, offset_y: float = 0, inherited_size: float = 12):
    transform = element.get("transform") or ""
    match = TRANSLATE_RE.search(transform)
    if match:
        offset_x += float(match.group(1))
        offset_y += float(match.group(2) or 0)
    size = number(attr(element, "font-size"), inherited_size) or inherited_size
    yield element, offset_x, offset_y, size
    for child in element:
        yield from walk(child, offset_x, offset_y, size)


def element_box(element: ET.Element, offset_x: float, offset_y: float, inherited_size: float) -> Box | None:
    tag = local_name(element)
    element_id = element.get("id", "")
    role = element.get("data-role", "")
    if tag == "rect":
        x, y = number(element.get("x"), 0) or 0, number(element.get("y"), 0) or 0
        width, height = number(element.get("width")), number(element.get("height"))
        if width is not None and height is not None:
            return Box(element_id, role, x + offset_x, y + offset_y, width, height)
    if tag == "circle":
        cx, cy, radius = number(element.get("cx")), number(element.get("cy")), number(element.get("r"))
        if None not in (cx, cy, radius):
            return Box(element_id, role, cx - radius + offset_x, cy - radius + offset_y, radius * 2, radius * 2)
    if tag == "ellipse":
        cx, cy = number(element.get("cx")), number(element.get("cy"))
        rx, ry = number(element.get("rx")), number(element.get("ry"))
        if None not in (cx, cy, rx, ry):
            return Box(element_id, role, cx - rx + offset_x, cy - ry + offset_y, rx * 2, ry * 2)
    if tag == "text":
        x, y = number(element.get("x")), number(element.get("y"))
        size = number(attr(element, "font-size"), inherited_size) or inherited_size
        text = "".join(element.itertext()).strip()
        if x is not None and y is not None and text:
            lines = ["".join(item.itertext()).strip() for item in element if local_name(item) == "tspan"] or [text]
            width = max(max(len(line), 1) * size * 0.56 for line in lines)
            height = max(len(lines), 1) * size * 1.3
            anchor = element.get("text-anchor")
            left = x - width / 2 if anchor == "middle" else x - width if anchor == "end" else x
            return Box(element_id, "text", left + offset_x, y - size + offset_y, width, height)
    return None


def rgb(value: str) -> tuple[int, int, int] | None:
    if not HEX_RE.fullmatch(value):
        return None
    raw = value[1:]
    if len(raw) == 3:
        raw = "".join(char * 2 for char in raw)
    return tuple(int(raw[index:index + 2], 16) for index in (0, 2, 4))


def luminance(color: tuple[int, int, int]) -> float:
    channels = []
    for item in color:
        value = item / 255
        channels.append(value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(foreground: str, background: str) -> float | None:
    fg, bg = rgb(foreground), rgb(background)
    if fg is None or bg is None:
        return None
    lighter, darker = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def overlaps(left: Box, right: Box, tolerance: float = 1.0) -> bool:
    return (
        min(left.right, right.right) - max(left.x, right.x) > tolerance
        and min(left.bottom, right.bottom) - max(left.y, right.y) > tolerance
    )


def segment_hits_box(x1: float, y1: float, x2: float, y2: float, box: Box) -> bool:
    if math.isclose(x1, x2, abs_tol=0.5):
        return box.x < x1 < box.right and max(min(y1, y2), box.y) < min(max(y1, y2), box.bottom)
    if math.isclose(y1, y2, abs_tol=0.5):
        return box.y < y1 < box.bottom and max(min(x1, x2), box.x) < min(max(x1, x2), box.right)
    return False


def validate_svg(path: Path, allow_placeholders: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        source = path.read_text(encoding="utf-8")
        root = ET.fromstring(source)
    except (OSError, UnicodeDecodeError, ET.ParseError) as exc:
        return [f"无法读取或解析 UTF-8 SVG: {exc}"], warnings

    if local_name(root) != "svg":
        errors.append("根节点不是 svg")
        return errors, warnings
    theme = root.get("data-theme")
    if theme and theme not in ALLOWED_THEMES:
        errors.append(f"未知主题键: {theme}")
    if path.parent.name == "templates" and path.name in {
        "architecture.svg",
        "architecture-business.svg",
        "architecture-data.svg",
        "architecture-technical.svg",
        "architecture-deployment.svg",
    }:
        metadata = next((item for item in root if local_name(item) == "metadata"), None)
        if metadata is None or metadata.get("data-layout") != "vertical-stack":
            errors.append("架构模板必须声明 data-layout=vertical-stack")
        if metadata is None or metadata.get("data-optional-modules") != OPTIONAL_MODULES:
            errors.append("架构模板缺少完整的可选模块声明")

    width, height = number(root.get("width")), number(root.get("height"))
    viewbox = [float(item) for item in NUMBER_RE.findall(root.get("viewBox") or "")]
    if width is None or height is None or width <= 0 or height <= 0:
        errors.append("缺少有效 width/height")
    if len(viewbox) != 4:
        errors.append("缺少有效 viewBox")
    elif width is not None and height is not None and (
        not math.isclose(viewbox[0], 0, abs_tol=0.1)
        or not math.isclose(viewbox[1], 0, abs_tol=0.1)
        or not math.isclose(viewbox[2], width, abs_tol=0.1)
        or not math.isclose(viewbox[3], height, abs_tol=0.1)
    ):
        errors.append("width/height 与 viewBox 不一致，或 viewBox 原点不是 0 0")

    if root.get("role") != "img":
        warnings.append("根节点应设置 role=img")
    labelled = set((root.get("aria-labelledby") or "").split())
    titles = [item for item in root if local_name(item) == "title"]
    descriptions = [item for item in root if local_name(item) == "desc"]
    if len(titles) != 1 or not "".join(titles[0].itertext()).strip():
        errors.append("必须包含一个非空 title")
    if len(descriptions) != 1 or not "".join(descriptions[0].itertext()).strip():
        errors.append("必须包含一个非空 desc")
    for item in titles + descriptions:
        if not item.get("id") or item.get("id") not in labelled:
            warnings.append("title/desc 应通过 aria-labelledby 关联")

    all_elements = list(root.iter())
    for element in all_elements:
        module = element.get("data-module")
        if module and module not in ALLOWED_MODULES:
            errors.append(f"未知附加模块: {module}")

    if root.get("data-visual-contract") == VISUAL_CONTRACT:
        layout = root.get("data-layout")
        if layout not in ALLOWED_LAYOUTS:
            errors.append(f"视觉合同缺少有效 data-layout: {layout or '<empty>'}")
        dominant_axis = root.get("data-dominant-axis")
        if dominant_axis not in ALLOWED_DOMINANT_AXES:
            errors.append(f"视觉合同缺少有效 data-dominant-axis: {dominant_axis or '<empty>'}")

        visual_nodes = [item for item in all_elements if item.get("data-role") == "node"]
        for item in visual_nodes:
            color_role = item.get("data-color-role")
            label = item.get("id", "<node>")
            if not color_role:
                errors.append(f"{label}: enterprise-v2 节点缺少 data-color-role")
            elif color_role not in ALLOWED_COLOR_ROLES:
                errors.append(f"{label}: 未知 data-color-role {color_role}")
        if visual_nodes and not any(item.get("data-visual-role") == "focus" for item in visual_nodes):
            warnings.append("enterprise-v2 缺少明确视觉焦点")

        declared_modules = set((root.get("data-modules") or "").split())
        actual_modules = {item.get("data-module") for item in all_elements if item.get("data-module")}
        for module in sorted(declared_modules - actual_modules):
            errors.append(f"声明的附加模块 {module} 不存在实际元素")
        for module in sorted(actual_modules - declared_modules):
            errors.append(f"附加模块 {module} 未在 data-modules 中声明")

        page_titles = [item for item in all_elements if item.get("data-role") == "page-title"]
        if len(page_titles) != 1:
            errors.append("enterprise-v2 必须包含一个 data-role=page-title")
        elif (number(attr(page_titles[0], "font-size"), 0) or 0) < 32:
            warnings.append("页面标题层级不足: enterprise-v2 建议字号不小于 32px")
    ids = [item.get("id") for item in all_elements if item.get("id")]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("id 重复: " + ", ".join(duplicates))
    id_set = set(ids)
    used_references: set[str] = set()
    for element in all_elements:
        for value in element.attrib.values():
            for ref in URL_REF_RE.findall(value):
                used_references.add(ref)
                if ref not in id_set:
                    errors.append(f"引用不存在: {ref}")
        href = element.get("href") or element.get("{http://www.w3.org/1999/xlink}href")
        if href:
            if href.startswith("#"):
                used_references.add(href[1:])
                if href[1:] not in id_set:
                    errors.append(f"引用不存在: {href[1:]}")
            else:
                errors.append(f"禁止外部资源引用: {href[:60]}")

    if any(local_name(item) == "foreignObject" for item in all_elements):
        errors.append("禁止使用 foreignObject")
    if any(local_name(item) == "image" for item in all_elements):
        errors.append("禁止嵌入位图 image")
    if "@font-face" in source or "http://" in source.replace("http://www.w3.org/2000/svg", "") or "https://" in source:
        errors.append("禁止外部字体、样式或网络资源")
    for element in all_elements:
        family = attr(element, "font-family") or ""
        if any(name in family.lower() for name in ICON_FONTS):
            errors.append(f"禁止使用图标字体: {element.get('id', f'<{local_name(element)}>')}")

    defs_types = {"marker", "filter", "linearGradient", "radialGradient", "clipPath", "mask"}
    definitions = [item for item in all_elements if local_name(item) in defs_types and item.get("id")]
    for item in definitions:
        if item.get("id") not in used_references:
            warnings.append(f"未使用的 defs: {local_name(item)}#{item.get('id')}")
    filters = [item for item in definitions if local_name(item) == "filter"]
    gradients = [item for item in definitions if local_name(item) in {"linearGradient", "radialGradient"}]
    if len(filters) > 2:
        warnings.append(f"filter 数量过多: {len(filters)}")
    if len(gradients) > 1:
        errors.append(f"gradient 数量超过 1: {len(gradients)}")

    boxes: list[Box] = []
    node_boxes: list[Box] = []
    edge_segments: list[tuple[str, float, float, float, float]] = []
    edge_element_count = 0
    colors: set[str] = set()
    for element, offset_x, offset_y, inherited_size in walk(root):
        tag = local_name(element)
        if element.get("data-role") == "edge":
            edge_element_count += 1
        fill, stroke = attr(element, "fill"), attr(element, "stroke")
        for color in (fill, stroke):
            if color and HEX_RE.fullmatch(color):
                colors.add(color.upper())
        if tag == "text":
            size = number(attr(element, "font-size"), inherited_size) or inherited_size
            minimum = 11 if element.get("data-text-role") == "auxiliary" else 12
            if size < minimum:
                warnings.append(f"文字字号过小: {element.get('id', '<text>')}={size:g}px")
            family = attr(element, "font-family") or ""
            if EMOJI_RE.search("".join(element.itertext())):
                errors.append(f"禁止使用 Emoji 代替图标: {element.get('id', '<text>')}")
            if family and "sans-serif" not in family.lower():
                warnings.append(f"字体缺少通用 fallback: {element.get('id', '<text>')}")
            foreground = fill or ""
            background = element.get("data-background", "")
            ratio = contrast(foreground, background) if background else None
            if ratio is not None and ratio < (3 if size >= 18 else 4.5):
                errors.append(f"文字对比度不足: {element.get('id', '<text>')}={ratio:.2f}:1")

        box = element_box(element, offset_x, offset_y, inherited_size)
        if box is not None:
            is_canvas = width and height and box.x <= 1 and box.y <= 1 and box.width >= width * 0.95 and box.height >= height * 0.95
            if not is_canvas:
                boxes.append(box)
            if box.role == "node":
                node_boxes.append(box)
            if width is not None and height is not None and (
                box.x < -0.5 or box.y < -0.5 or box.right > width + 0.5 or box.bottom > height + 0.5
            ):
                errors.append(f"元素超出画布: {box.element_id or tag}")

        if tag == "line" and element.get("data-role") == "edge":
            x1, y1 = number(element.get("x1")), number(element.get("y1"))
            x2, y2 = number(element.get("x2")), number(element.get("y2"))
            if None not in (x1, y1, x2, y2):
                edge_segments.append((element.get("id", "<line>"), x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y))
        if tag in {"polyline", "polygon"} and element.get("data-role") == "edge":
            points = [float(item) for item in NUMBER_RE.findall(element.get("points") or "")]
            pairs = [(points[index] + offset_x, points[index + 1] + offset_y) for index in range(0, len(points) - 1, 2)]
            for start, end in zip(pairs, pairs[1:]):
                edge_segments.append((element.get("id", "<polyline>"), start[0], start[1], end[0], end[1]))

    # Vibrant uses four controlled domain hues plus optional status hues.  Count
    # derived borders and subtle surfaces separately from accent families, so its
    # legitimate ceiling is slightly higher than monochrome themes.
    color_limit = 28 if root.get("data-theme") == "vibrant" else 22
    if len(colors) > color_limit:
        warnings.append(f"颜色数量偏多: {len(colors)}")
    if not node_boxes:
        errors.append("缺少 data-role=node，无法执行节点重叠和布局检查")
    if node_boxes:
        for index, left in enumerate(node_boxes):
            for right in node_boxes[index + 1:]:
                if overlaps(left, right):
                    errors.append(f"节点重叠: {left.element_id} / {right.element_id}")
        for edge_id, x1, y1, x2, y2 in edge_segments:
            for box in node_boxes:
                if segment_hits_box(x1, y1, x2, y2, box):
                    warnings.append(f"连线可能穿越节点: {edge_id} / {box.element_id}")
                    break

    if boxes and width and height:
        left = min(item.x for item in boxes)
        top = min(item.y for item in boxes)
        right = max(item.right for item in boxes)
        bottom = max(item.bottom for item in boxes)
        usage = (right - left) * (bottom - top) / (width * height)
        if usage < 0.45:
            warnings.append(f"内容包围盒利用率过低: {usage:.1%}")
        elif usage > 0.88:
            warnings.append(f"内容包围盒利用率过高: {usage:.1%}")
        if abs(left - (width - right)) > width * 0.15:
            warnings.append(f"左右留白失衡: 左 {left:g}px / 右 {width - right:g}px")
        if abs(top - (height - bottom)) > height * 0.20:
            warnings.append(f"上下留白失衡: 上 {top:g}px / 下 {height - bottom:g}px")

    name = path.name.lower()
    if name.startswith("architecture"):
        visual_v2 = root.get("data-visual-contract") == VISUAL_CONTRACT
        tall_nodes = [
            item
            for item in node_boxes
            if item.height > (84 if visual_v2 else 40)
            and not (visual_v2 and (item.element_id or "").startswith(("footer-", "layer-title-")))
        ]
        if tall_nodes:
            warnings.append("架构图三级卡片过高: " + ", ".join(item.element_id or "<node>" for item in tall_nodes[:5]))
        if edge_element_count > 4:
            warnings.append(f"架构图连线过多: {edge_element_count}，应优先使用分层和容器表达")
    if name.startswith("flow-"):
        visible_text = " ".join("".join(item.itertext()) for item in all_elements if local_name(item) == "text")
        if "开始" not in visible_text or "结束" not in visible_text:
            errors.append("流程图必须包含明确的开始和结束")
    if name.startswith("sequence"):
        participant_count = sum(1 for item in all_elements if (item.get("id") or "").startswith("participant-") and item.get("data-role") == "node")
        lifeline_count = sum(1 for item in all_elements if item.get("data-role") == "lifeline")
        if participant_count < 2:
            errors.append("时序图至少需要两个参与者")
        if lifeline_count != participant_count:
            errors.append(f"时序图生命线不完整: 参与者 {participant_count} / 生命线 {lifeline_count}")
        visible_text = " ".join("".join(item.itertext()) for item in all_elements if local_name(item) == "text")
        if "开始" not in visible_text or "结束" not in visible_text:
            errors.append("时序图必须包含起点和终点语义")
    if name.startswith("relationship-er"):
        if edge_element_count < 1:
            errors.append("ER 图缺少带 data-role=edge 的实体关系")
        cardinalities = ["".join(item.itertext()).strip() for item in all_elements if local_name(item) == "text"]
        if not any(item in {"1", "N", "M", "0..1", "1..N"} for item in cardinalities):
            errors.append("ER 图缺少关系基数标记")

    if not allow_placeholders and PLACEHOLDER_RE.search(" ".join("".join(item.itertext()) for item in all_elements if local_name(item) == "text")):
        errors.append("示例或输出残留模板占位内容")
    return sorted(set(errors)), sorted(set(warnings))


def find_browser() -> Path | None:
    configured = os.environ.get("SVG_RENDERER")
    candidates = [
        Path(configured) if configured else None,
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    return next((item for item in candidates if item and item.is_file()), None)


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:24]
    except OSError:
        return None
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def render(svg: Path) -> tuple[bool, str]:
    browser = find_browser()
    if browser is None:
        return False, "未找到 Chrome 或 Edge；可通过 SVG_RENDERER 指定浏览器"
    root = ET.parse(svg).getroot()
    width, height = round(number(root.get("width"), 0) or 0), round(number(root.get("height"), 0) or 0)
    if width <= 0 or height <= 0:
        return False, "SVG 缺少有效 width/height"
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / "render.png"
        profile = Path(temporary) / "profile"
        command = [
            str(browser),
            "--headless=new",
            "--hide-scrollbars",
            "--disable-gpu",
            f"--window-size={width},{height}",
            f"--user-data-dir={profile}",
            f"--screenshot={target}",
            svg.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        for _ in range(20):
            if target.exists() and target.stat().st_size > 100:
                break
            time.sleep(0.1)
        size = png_size(target)
    if result.returncode != 0:
        return False, result.stderr.strip() or f"浏览器退出码 {result.returncode}"
    if size != (width, height):
        return False, f"渲染尺寸异常: {size}，期望 {(width, height)}"
    return True, f"{browser.name} {width}x{height}"


def validate_catalog(target: Path) -> list[str]:
    errors: list[str] = []
    missing_support = sorted(path for path in REQUIRED_SUPPORT_FILES if not (target / path).is_file())
    if missing_support:
        errors.append("缺少主题或图标支持文件: " + ", ".join(missing_support))
    representative = next((item for item in sorted((target / "examples").glob("architecture-application-*.svg"))), None)
    if representative is not None:
        root = ET.parse(representative).getroot()
        if not any(item.get("data-module") == "focus-node" for item in root.iter()):
            errors.append("代表架构示例缺少 focus-node 附加模块")
        if not any(item.get("data-role") == "icon" for item in root.iter()):
            errors.append("代表架构示例缺少语义图标")
    templates = target / "templates"
    examples = target / "examples"
    names = {item.name for item in templates.glob("*.svg")}
    if names != EXPECTED_TEMPLATES:
        missing, extra = sorted(EXPECTED_TEMPLATES - names), sorted(names - EXPECTED_TEMPLATES)
        if missing:
            errors.append("缺少模板: " + ", ".join(missing))
        if extra:
            errors.append("存在非目标模板: " + ", ".join(extra))
    example_names = {item.name for item in examples.glob("*.svg")}
    if len(example_names) != len(EXPECTED_EXAMPLE_PREFIXES):
        errors.append(f"示例数量必须为 {len(EXPECTED_EXAMPLE_PREFIXES)}，实际为 {len(example_names)}")
    for prefix in sorted(EXPECTED_EXAMPLE_PREFIXES):
        matches = [name for name in example_names if name.startswith(prefix)]
        if not matches:
            errors.append("缺少示例类型: " + prefix.rstrip("-"))
        elif len(matches) > 1:
            errors.append("示例类型重复: " + prefix.rstrip("-"))
    expected_types = {prefix.rstrip("-") for prefix in EXPECTED_EXAMPLE_PREFIXES}
    actual_types: set[str] = set()
    for item in sorted(templates.glob("*.svg")) + sorted(examples.glob("*.svg")):
        root = ET.parse(item).getroot()
        if root.get("data-generation") != "fresh-catalog-v1":
            errors.append(f"{item.relative_to(target)}: 缺少 fresh-catalog-v1 生成标记")
        diagram_type = root.get("data-diagram-type", "")
        if diagram_type:
            actual_types.add(diagram_type)
    if actual_types != expected_types:
        errors.append("图形类型目录不完整或包含未知类型")
    extra_files = [item for item in examples.rglob("*") if item.is_file() and item.suffix.lower() != ".svg"]
    if extra_files:
        errors.append("examples 只能包含 SVG: " + ", ".join(str(item.relative_to(target)) for item in extra_files))
    return errors


def collect_files(target: Path) -> list[tuple[Path, bool]]:
    if target.is_file():
        return [(target, "templates" in target.parts)]
    if (target / "SKILL.md").exists():
        return (
            [(item, True) for item in sorted((target / "templates").glob("*.svg"))]
            + [(item, False) for item in sorted((target / "examples").glob("*.svg"))]
        )
    return [(item, False) for item in sorted(target.rglob("*.svg"))]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true", help="将警告视为失败")
    parser.add_argument("--render", action="store_true", help="用本机 Chrome 或 Edge 进行真实渲染")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists():
        print(f"错误: 路径不存在: {target}")
        return 1

    errors = validate_catalog(target) if target.is_dir() and (target / "SKILL.md").exists() else []
    warnings: list[str] = []
    files = collect_files(target)
    if not files:
        errors.append("未找到 SVG 文件")
    for path, allow_placeholders in files:
        current_errors, current_warnings = validate_svg(path, allow_placeholders)
        label = str(path.relative_to(target)) if target.is_dir() else path.name
        errors.extend(f"{label}: {item}" for item in current_errors)
        warnings.extend(f"{label}: {item}" for item in current_warnings)
        if args.render and not current_errors:
            ok, message = render(path)
            if ok:
                print(f"渲染通过: {label}: {message}")
            else:
                errors.append(f"{label}: 渲染失败: {message}")

    for item in errors:
        print("错误: " + item)
    for item in warnings:
        print("警告: " + item)
    if errors or (args.strict and warnings):
        return 1
    print(f"校验通过: {len(files)} 个 SVG 文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
