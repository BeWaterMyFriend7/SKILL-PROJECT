#!/usr/bin/env python3
"""Generate fresh XML/SVG theme baselines from a natural-language request manifest."""

from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
REQUEST_PATH = HERE / "requests.json"
STYLE_PATH = REPO / ".opencode" / "skills" / "svg-generator" / "scripts" / "style_map.py"
GENERATOR_VERSION = "fresh-dsl-v1"


def load_style_module():
    spec = importlib.util.spec_from_file_location("baseline_style_map", STYLE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


STYLE = load_style_module()


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_text(text: str) -> str:
    return digest_bytes(text.encode("utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_text(x: int, y: int, value: str, size: int, color: str, *, weight: int = 400, anchor: str = "start", role: str | None = None) -> str:
    attrs = f' x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}"'
    if role:
        attrs += f' data-role="{role}"'
    if size <= 11:
        attrs += ' data-text-role="auxiliary"'
    return f"<text{attrs}>{esc(value)}</text>"


def svg_rect(x: int, y: int, width: int, height: int, fill: str, stroke: str, *, radius: int = 14, role: str | None = None, color_role: str | None = None, visual_role: str | None = None, module: str | None = None, shadow: bool = False, element_id: str | None = None) -> str:
    attrs = f' x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"'
    if element_id:
        attrs += f' id="{element_id}"'
    if role:
        attrs += f' data-role="{role}"'
    if color_role:
        attrs += f' data-color-role="{color_role}"'
    if visual_role:
        attrs += f' data-visual-role="{visual_role}"'
    if module:
        attrs += f' data-module="{module}"'
    if shadow:
        attrs += ' filter="url(#softShadow)"'
    return f"<rect{attrs}/>"


def svg_icon(x: int, y: int, color: str, kind: str) -> str:
    if kind == "users":
        body = f'<circle cx="{x + 12}" cy="{y + 8}" r="5"/><path d="M{x + 3} {y + 25}c1-7 5-10 9-10s8 3 9 10" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
    elif kind == "shield":
        body = f'<path d="M{x + 12} {y + 2}l9 4v7c0 7-4 11-9 14-5-3-9-7-9-14V{y + 6}z" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M{x + 8} {y + 13}l3 3 6-7" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    elif kind == "cluster":
        body = f'<rect x="{x + 2}" y="{y + 4}" width="7" height="18" rx="2"/><rect x="{x + 11}" y="{y + 1}" width="7" height="21" rx="2"/><rect x="{x + 20}" y="{y + 8}" width="7" height="14" rx="2"/>'
    else:
        body = f'<circle cx="{x + 14}" cy="{y + 14}" r="11" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M{x + 14} {y + 7}v7l5 3" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
    return f'<g data-role="icon" fill="{color}">{body}</g>'


def drawio_icon_data(color: str, kind: str) -> str:
    if kind == "users":
        body = f'<circle cx="14" cy="8" r="5" fill="{color}"/><path d="M5 25c1-7 5-10 9-10s8 3 9 10" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
    elif kind == "shield":
        body = f'<path d="M14 2l9 4v7c0 7-4 11-9 14-5-3-9-7-9-14V6z" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M10 13l3 3 6-7" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    elif kind == "cluster":
        body = f'<rect x="2" y="4" width="7" height="18" rx="2" fill="{color}"/><rect x="11" y="1" width="7" height="21" rx="2" fill="{color}"/><rect x="20" y="8" width="7" height="14" rx="2" fill="{color}"/>'
    else:
        raise ValueError(f"unknown icon kind: {kind}")
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">{body}</svg>'
    return "data:image/svg+xml," + quote(svg, safe="")


def add_svg_node(lines: list[str], x: int, y: int, width: int, height: int, label: str, role_name: str, style: dict[str, object], *, visual_role: str | None = None, module: str | None = None, solid: bool = False, sublabel: str | None = None, element_id: str | None = None) -> None:
    token = style["roles"][role_name]
    fill = token["base"] if solid else token["soft"]
    stroke = token["strong"] if solid else token["border"]
    foreground = token["foreground"] if solid else style["neutral"]["text-strong"]
    lines.append(svg_rect(x, y, width, height, fill, stroke, radius=12, role="node", color_role=role_name, visual_role=visual_role, module=module, element_id=element_id))
    lines.append(svg_text(x + width // 2, y + (height // 2 if not sublabel else height // 2 - 5), label, 15 if height >= 48 else 13, foreground, weight=700, anchor="middle"))
    if sublabel:
        lines.append(svg_text(x + width // 2, y + height // 2 + 18, sublabel, 11, foreground if solid else style["neutral"]["text-muted"], anchor="middle"))


def build_svg(spec: dict[str, object], theme: str, style: dict[str, object], spec_hash: str) -> str:
    n = style["neutral"]
    r = style["roles"]
    c = spec["content"]
    modules = " ".join(spec["modules"])
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="1000" viewBox="0 0 1560 1000" role="img" aria-labelledby="title desc" font-family="Inter, Noto Sans SC, Microsoft YaHei, Arial, sans-serif" data-theme="{theme}" data-mode="light" data-layout="mixed-axis" data-dominant-axis="x" data-visual-contract="enterprise-v2" data-modules="{modules}" data-generation="{GENERATOR_VERSION}" data-spec-hash="{spec_hash}">',
        f'<title id="title">{esc(c["governance"]["title"])}主题基准图</title>',
        f'<desc id="desc">{esc(spec["coreConclusion"])}</desc>',
        '<defs><filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.08"/></filter><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0l10 5-10 5z" fill="context-stroke"/></marker></defs>',
        f'<rect width="1560" height="1000" fill="{n["canvas"]}"/>',
        f'<rect x="52" y="36" width="8" height="76" rx="4" fill="{r["focus"]["base"]}"/>',
        svg_text(82, 76, "智能服务治理平台", 42, n["text-strong"], weight=800, role="page-title"),
        svg_text(82, 106, spec["coreConclusion"], 15, n["text"], weight=400),
    ]
    badge_labels = ["混合轴布局", "策略驱动", style["theme-name"].split("｜")[0].strip()]
    badge_roles = ["axis-main", "focus", "data-flow"]
    bx = 1010
    for label, role_name in zip(badge_labels, badge_roles):
        token = r[role_name]
        width = 130 if label != badge_labels[-1] else 190
        lines.append(svg_rect(bx, 52, width, 42, n["surface"], token["border"], radius=21))
        lines.append(svg_text(bx + width // 2, 79, label, 13, n["text-strong"], weight=700, anchor="middle"))
        bx += width + 14

    lines.append(svg_rect(40, 136, 1420, 650, n["surface"], n["border"], radius=22, role="region", shadow=True))
    lines.append(f'<g data-module="top-band" data-color-role="axis-main">')
    lines.append(svg_rect(70, 162, 1360, 56, r["axis-main"]["soft"], r["axis-main"]["border"], radius=14))
    top_items = c["topBand"]
    for index, item in enumerate(top_items):
        add_svg_node(lines, 105 + index * 440, 173, 380, 34, item, "axis-main", style)
    lines.append("</g>")

    lines.append(f'<line id="edge-entry-governance" data-role="edge" data-color-role="connector" x1="400" y1="490" x2="472" y2="490" stroke="{r["connector"]["base"]}" stroke-width="3" marker-end="url(#arrow)"/>')
    lines.append(f'<line id="edge-governance-provider" data-role="edge" data-color-role="connector" x1="938" y1="490" x2="1008" y2="490" stroke="{r["connector"]["base"]}" stroke-width="3" marker-end="url(#arrow)"/>')

    lines.append(svg_rect(70, 246, 330, 500, r["axis-main"]["soft"], r["axis-main"]["border"], radius=20, role="region", color_role="axis-main", shadow=True))
    lines.append(svg_icon(100, 278, r["axis-main"]["strong"], "users"))
    lines.append(svg_text(142, 303, c["entry"]["title"], 22, r["axis-main"]["strong"], weight=800))
    for index, item in enumerate(c["entry"]["items"]):
        add_svg_node(lines, 105, 350 + index * 116, 260, 82, item, "axis-main", style, sublabel=("稳定访问入口" if index == 0 else "统一配置与观测"))
    lines.append(svg_text(235, 660, "入口保持稳定，实例选择由治理策略完成", 12, n["text-muted"], anchor="middle"))

    lines.append(svg_rect(472, 246, 466, 500, r["group"]["soft"], r["group"]["border"], radius=20, role="region", color_role="group", shadow=True))
    lines.append(svg_icon(506, 278, r["focus"]["strong"], "shield"))
    lines.append(svg_text(548, 303, c["governance"]["title"], 22, r["focus"]["strong"], weight=800))
    for index, item in enumerate(c["governance"]["controls"]):
        add_svg_node(lines, 506 + index * 200, 340, 180, 68, item, "group", style)
    add_svg_node(lines, 556, 442, 300, 82, c["governance"]["focus"], "focus", style, visual_role="focus", module="focus-node", solid=True, sublabel="策略决策 · 服务发现 · 负载调节", element_id="focus-engine")
    lines.append(svg_rect(512, 566, 386, 136, n["surface"], r["data-flow"]["border"], radius=16, role="region", color_role="data-flow"))
    lines.append(svg_text(538, 596, c["governance"]["planeTitle"], 17, r["data-flow"]["strong"], weight=800))
    for index, item in enumerate(c["governance"]["planeItems"]):
        add_svg_node(lines, 536 + index * 120, 622, 105, 48, item, "data-flow", style)

    lines.append(svg_rect(1008, 246, 300, 500, r["axis-cross"]["soft"], r["axis-cross"]["border"], radius=20, role="region", color_role="axis-cross", shadow=True))
    lines.append(svg_icon(1038, 278, r["axis-cross"]["strong"], "cluster"))
    lines.append(svg_text(1080, 303, c["providers"]["title"], 22, r["axis-cross"]["strong"], weight=800))
    for index, item in enumerate(c["providers"]["items"]):
        add_svg_node(lines, 1042, 344 + index * 100, 232, 70, item, "axis-cross", style, sublabel="服务实例 · eBPF 程序")
    lines.append(svg_text(1158, 678, "按策略动态选择实际实例", 12, n["text-muted"], weight=600, anchor="middle"))

    lines.append(f'<g data-module="aux-column" data-color-role="side-rail">')
    lines.append(svg_rect(1332, 246, 98, 500, r["side-rail"]["soft"], r["side-rail"]["border"], radius=20, role="region", color_role="side-rail", shadow=True))
    lines.append(svg_text(1381, 286, c["sideRail"]["title"], 16, r["side-rail"]["strong"], weight=800, anchor="middle"))
    for index, item in enumerate(c["sideRail"]["items"]):
        add_svg_node(lines, 1345, 330 + index * 88, 72, 58, item, "side-rail", style)
    lines.append("</g>")

    lines.append(f'<g data-module="footer-band" data-color-role="data-flow">')
    lines.append(svg_rect(40, 812, 1420, 104, r["data-flow"]["soft"], r["data-flow"]["border"], radius=20, role="region", color_role="data-flow"))
    lines.append(svg_text(74, 850, "核心价值", 20, r["data-flow"]["strong"], weight=800))
    for index, item in enumerate(c["footer"]):
        add_svg_node(lines, 230 + index * 290, 833, 245, 58, item, "data-flow", style)
    lines.append("</g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def style_string(fill: str, stroke: str, font: str, size: int = 14, *, bold: bool = False, rounded: bool = True, shadow: bool = False, align: str = "center") -> str:
    parts = [
        "rounded=1" if rounded else "rounded=0",
        "arcSize=8" if rounded else "arcSize=0",
        "whiteSpace=wrap",
        "html=1",
        f"fillColor={fill}",
        f"strokeColor={stroke}",
        f"fontColor={font}",
        f"fontSize={size}",
        "fontFamily=Microsoft YaHei",
        f"align={align}",
        "verticalAlign=middle",
    ]
    if bold:
        parts.append("fontStyle=1")
    if shadow:
        parts.append("shadow=1")
    return ";".join(parts) + ";"


def build_drawio(spec: dict[str, object], theme: str, style: dict[str, object], spec_hash: str) -> str:
    n = style["neutral"]
    r = style["roles"]
    c = spec["content"]
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "xml-diagram"})
    diagram = ET.SubElement(mxfile, "diagram", {
        "name": f"{style['theme-name']} Baseline",
        "id": f"baseline-{theme}",
        "theme": theme,
        "mode": "light",
        "layout": "mixed-axis",
        "dominantAxis": "x",
        "visualContract": "enterprise-v2",
        "modules": " ".join(spec["modules"]),
        "generation": GENERATOR_VERSION,
        "specHash": spec_hash,
    })
    model = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "1500", "dy": "950", "grid": "0", "gridSize": "10", "guides": "1",
        "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1",
        "pageScale": "1", "pageWidth": "1560", "pageHeight": "1000", "math": "0",
        "shadow": "0", "background": n["canvas"],
    })
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    def vertex(cell_id: str, value: str, x: int, y: int, width: int, height: int, fill: str, stroke: str, font: str, *, size: int = 14, bold: bool = False, role: str | None = None, color_role: str | None = None, visual_role: str | None = None, module: str | None = None, shadow: bool = False, rounded: bool = True, align: str = "center") -> ET.Element:
        attrs = {
            "id": cell_id,
            "value": value,
            "vertex": "1",
            "parent": "1",
            "style": style_string(fill, stroke, font, size, bold=bold, rounded=rounded, shadow=shadow, align=align),
        }
        if role:
            attrs["role"] = role
        if color_role:
            attrs["colorRole"] = color_role
        if visual_role:
            attrs["visualRole"] = visual_role
        if module:
            attrs["module"] = module
        cell = ET.SubElement(root, "mxCell", attrs)
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"})
        return cell

    def text(cell_id: str, value: str, x: int, y: int, width: int, height: int, size: int, color: str, *, bold: bool = False, role: str | None = None, align: str = "left") -> ET.Element:
        attrs = {
            "id": cell_id,
            "value": value,
            "vertex": "1",
            "parent": "1",
            "style": f"text=;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;whiteSpace=wrap;fontFamily=Microsoft YaHei;fontSize={size};fontStyle={1 if bold else 0};fontColor={color};",
        }
        if role:
            attrs["role"] = role
        cell = ET.SubElement(root, "mxCell", attrs)
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"})
        return cell

    def icon(cell_id: str, kind: str, x: int, y: int, color: str, color_role: str) -> ET.Element:
        cell = ET.SubElement(root, "mxCell", {
            "id": cell_id,
            "value": "",
            "vertex": "1",
            "parent": "1",
            "role": "icon",
            "colorRole": color_role,
            "style": f"shape=image;html=1;imageAspect=0;aspect=fixed;strokeColor=none;fillColor=none;image={drawio_icon_data(color, kind)};",
        })
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": "28", "height": "28", "as": "geometry"})
        return cell

    def node(cell_id: str, label: str, x: int, y: int, width: int, height: int, role_name: str, *, sublabel: str | None = None, visual_role: str | None = None, module: str | None = None, solid: bool = False) -> ET.Element:
        token = r[role_name]
        fill = token["base"] if solid else token["soft"]
        stroke = token["strong"] if solid else token["border"]
        foreground = token["foreground"] if solid else n["text-strong"]
        value = f"<b>{html.escape(label)}</b>"
        if sublabel:
            value += f"<br><font style='font-size:11px;color:{foreground if solid else n['text-muted']}'>{html.escape(sublabel)}</font>"
        return vertex(cell_id, value, x, y, width, height, fill, stroke, foreground, size=15, bold=False, role="node", color_role=role_name, visual_role=visual_role, module=module)

    vertex("accent-bar", "", 52, 36, 8, 76, r["focus"]["base"], r["focus"]["base"], r["focus"]["foreground"], rounded=True)
    text("page-title", "智能服务治理平台", 82, 36, 700, 52, 42, n["text-strong"], bold=True, role="page-title")
    text("subtitle", spec["coreConclusion"], 82, 88, 900, 28, 15, n["text"])

    badge_x = 1010
    for index, (label, role_name, width) in enumerate(zip(["混合轴布局", "策略驱动", style["theme-name"].split("｜")[0].strip()], ["axis-main", "focus", "data-flow"], [130, 130, 190])):
        token = r[role_name]
        vertex(f"badge-{index}", label, badge_x, 52, width, 42, n["surface"], token["border"], n["text-strong"], size=13, bold=True)
        badge_x += width + 14

    vertex("main-shell", "", 40, 136, 1420, 650, n["surface"], n["border"], n["text"], shadow=True)
    vertex("top-band", "", 70, 162, 1360, 56, r["axis-main"]["soft"], r["axis-main"]["border"], n["text"], module="top-band")
    for index, item in enumerate(c["topBand"]):
        node(f"top-{index}", item, 105 + index * 440, 173, 380, 34, "axis-main")

    left_region = vertex("entry-region", "", 70, 246, 330, 500, r["axis-main"]["soft"], r["axis-main"]["border"], n["text"], role="region", color_role="axis-main", shadow=True)
    icon("entry-icon", "users", 100, 278, r["axis-main"]["base"], "axis-main")
    text("entry-title", c["entry"]["title"], 142, 272, 210, 44, 22, r["axis-main"]["strong"], bold=True)
    for index, item in enumerate(c["entry"]["items"]):
        node(f"entry-{index}", item, 105, 350 + index * 116, 260, 82, "axis-main", sublabel=("稳定访问入口" if index == 0 else "统一配置与观测"))
    text("entry-note", "入口保持稳定，实例选择由治理策略完成", 95, 640, 280, 42, 12, n["text"], align="center")

    center_region = vertex("governance-region", "", 472, 246, 466, 500, r["group"]["soft"], r["group"]["border"], n["text"], role="region", color_role="group", shadow=True)
    icon("governance-icon", "shield", 506, 278, r["focus"]["base"], "focus")
    text("governance-title", c["governance"]["title"], 548, 272, 230, 44, 22, r["focus"]["strong"], bold=True)
    for index, item in enumerate(c["governance"]["controls"]):
        node(f"control-{index}", item, 506 + index * 200, 340, 180, 68, "group")
    node("focus-engine", c["governance"]["focus"], 556, 442, 300, 82, "focus", sublabel="策略决策 · 服务发现 · 负载调节", visual_role="focus", module="focus-node", solid=True)
    vertex("data-plane", "", 512, 566, 386, 136, n["surface"], r["data-flow"]["border"], n["text"], role="region", color_role="data-flow")
    text("data-plane-title", c["governance"]["planeTitle"], 538, 576, 220, 34, 17, r["data-flow"]["strong"], bold=True)
    for index, item in enumerate(c["governance"]["planeItems"]):
        node(f"plane-{index}", item, 536 + index * 120, 622, 105, 48, "data-flow")

    right_region = vertex("provider-region", "", 1008, 246, 300, 500, r["axis-cross"]["soft"], r["axis-cross"]["border"], n["text"], role="region", color_role="axis-cross", shadow=True)
    icon("provider-icon", "cluster", 1038, 278, r["axis-cross"]["base"], "axis-cross")
    text("provider-title", c["providers"]["title"], 1080, 272, 190, 44, 22, r["axis-cross"]["strong"], bold=True)
    for index, item in enumerate(c["providers"]["items"]):
        node(f"provider-{index}", item, 1042, 344 + index * 100, 232, 70, "axis-cross", sublabel="服务实例 · eBPF 程序")
    text("provider-note", "按策略动态选择实际实例", 1038, 660, 240, 34, 12, n["text"], bold=True, align="center")

    vertex("side-rail", "", 1332, 246, 98, 500, r["side-rail"]["soft"], r["side-rail"]["border"], n["text"], role="region", color_role="side-rail", module="aux-column", shadow=True)
    text("side-title", c["sideRail"]["title"], 1342, 262, 78, 50, 16, r["side-rail"]["strong"], bold=True, align="center")
    for index, item in enumerate(c["sideRail"]["items"]):
        node(f"side-{index}", item, 1345, 330 + index * 88, 72, 58, "side-rail")

    vertex("footer-band", "", 40, 812, 1420, 104, r["data-flow"]["soft"], r["data-flow"]["border"], n["text"], role="region", color_role="data-flow", module="footer-band")
    text("footer-title", "核心价值", 74, 828, 130, 42, 20, r["data-flow"]["strong"], bold=True)
    for index, item in enumerate(c["footer"]):
        node(f"footer-{index}", item, 230 + index * 290, 833, 245, 58, "data-flow")

    def arrow_line(line_id: str, x: int, y: int, width: int) -> None:
        cell = ET.SubElement(root, "mxCell", {
            "id": line_id,
            "value": "",
            "vertex": "1",
            "parent": "1",
            "colorRole": "connector",
            "style": f"shape=line;html=1;strokeColor={r['connector']['base']};strokeWidth=3;endArrow=block;endFill=1;",
        })
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(width), "height": "20", "as": "geometry"})

    arrow_line("edge-entry-governance", 400, 480, 72)
    arrow_line("edge-governance-provider", 938, 480, 70)

    ET.indent(mxfile, space="  ")
    return "<?xml version='1.0' encoding='utf-8'?>\n" + ET.tostring(mxfile, encoding="unicode") + "\n"


def build_dsl(spec: dict[str, object], theme: str, style: dict[str, object], spec_hash: str) -> str:
    role_lines = "\n".join(f"- {role}: {color}（来源：{style['role-sources'][role]}）" for role, color in style["role-colors"].items())
    return f"""# 四主题基准图 DSL：{style['theme-name']}

生成方式：{GENERATOR_VERSION}
规格哈希：{spec_hash}

## 原始自然语言需求

{spec['request']}

## 可执行蓝图

- 图形目标：面向{spec['audience']}，说明“{spec['coreConclusion']}”
- 图形类型：混合轴分层架构
- 视觉主题：{style['theme-name']}
- 显示模式：light
- 视觉合同：enterprise-v2
- 视觉骨架：分层架构
- 主叙事轴：x，用户入口 → 治理中心 → 服务集群
- 交叉轴与侧栏：治理中心内部纵向处理；右侧为运维保障栏
- 附加模块：top-band、aux-column、focus-node、footer-band
- 图标策略：用户入口、治理中心、服务集群使用三个语义图标

## 结构颜色映射

{role_lines}

## 质量预期

标题层级清楚；大面积使用浅色；策略治理引擎为唯一焦点；同类卡片颜色一致；连线不穿越节点；XML/SVG 结构语义一致。
"""


def main() -> int:
    spec = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    raw_spec_hash = digest_bytes(REQUEST_PATH.read_bytes())
    for folder in ("dsl", "svg", "xml"):
        (HERE / folder).mkdir(parents=True, exist_ok=True)

    artifacts = []
    for theme in spec["themes"]:
        theme_spec_hash = digest_text(json.dumps({"requestHash": raw_spec_hash, "theme": theme}, sort_keys=True))
        style = STYLE.build_style_map(theme, layout=spec["layout"], dominant_axis=spec["dominantAxis"])
        dsl_path = HERE / "dsl" / f"{theme}.md"
        svg_path = HERE / "svg" / f"{theme}.svg"
        xml_path = HERE / "xml" / f"{theme}.drawio"
        dsl_path.write_text(build_dsl(spec, theme, style, theme_spec_hash), encoding="utf-8", newline="\n")
        svg_path.write_text(build_svg(spec, theme, style, theme_spec_hash), encoding="utf-8", newline="\n")
        xml_path.write_text(build_drawio(spec, theme, style, theme_spec_hash), encoding="utf-8", newline="\n")
        artifacts.append({
            "theme": theme,
            "themeName": style["theme-name"],
            "requestHash": raw_spec_hash,
            "specHash": theme_spec_hash,
            "generationMode": GENERATOR_VERSION,
            "legacyInputFiles": [],
            "dsl": {"path": str(dsl_path.relative_to(HERE)).replace("\\", "/"), "sha256": digest_bytes(dsl_path.read_bytes())},
            "svg": {"path": str(svg_path.relative_to(HERE)).replace("\\", "/"), "sha256": digest_bytes(svg_path.read_bytes())},
            "drawio": {"path": str(xml_path.relative_to(HERE)).replace("\\", "/"), "sha256": digest_bytes(xml_path.read_bytes())},
            "layout": style["layout"],
            "dominantAxis": style["dominant-axis"],
            "roleColors": style["role-colors"],
        })

    manifest = {
        "schemaVersion": "fresh-generation-manifest-v1",
        "requestFile": "requests.json",
        "requestSha256": raw_spec_hash,
        "generationMode": GENERATOR_VERSION,
        "legacyInputFiles": [],
        "artifacts": artifacts,
    }
    (HERE / "generation-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"fresh generation complete: {len(artifacts)} themes, {len(artifacts) * 3} source artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
