#!/usr/bin/env python3
"""Generate the complete 19-type XML/SVG catalog from natural-language request specs."""

from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
REQUEST_PATH = HERE / "requests.json"
STYLE_PATH = REPO / ".opencode" / "skills" / "svg-generator" / "scripts" / "style_map.py"
GENERATION = "fresh-catalog-v1"
OPTIONAL_MODULES = "top-band aux-column callout numbered-flow focus-node footer-band"

SVG_TEMPLATES = {
    "architecture-application": "architecture.svg",
    "architecture-business": "architecture-business.svg",
    "architecture-data": "architecture-data.svg",
    "architecture-deployment": "architecture-deployment.svg",
    "architecture-technical": "architecture-technical.svg",
    "comparison": "comparison.svg",
    "decision-matrix": "decision-matrix.svg",
    "flow-branching": "flow-branching.svg",
    "flow-linear": "flow-linear.svg",
    "lifecycle": "lifecycle.svg",
    "relationship-dependency": "relationship-dependency.svg",
    "relationship-er": "relationship-er.svg",
    "relationship-knowledge": "relationship-knowledge.svg",
    "roadmap": "roadmap.svg",
    "sequence": "sequence.svg",
    "state": "state.svg",
    "summary": "summary.svg",
    "swot": "swot.svg",
    "timeline": "timeline.svg",
}
XML_TEMPLATES = {key: value.replace(".svg", ".drawio") for key, value in SVG_TEMPLATES.items()}


def load_style_module():
    spec = importlib.util.spec_from_file_location("catalog_style_map", STYLE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


STYLE = load_style_module()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass
class Box:
    id: str
    x: int
    y: int
    width: int
    height: int
    label: str = ""
    sublabel: str = ""
    color_role: str = "group"
    kind: str = "node"
    solid: bool = False
    visual_role: str | None = None
    module: str | None = None
    shadow: bool = False
    font_size: int = 15


@dataclass
class Label:
    id: str
    x: int
    y: int
    width: int
    height: int
    value: str
    size: int
    color_role: str | None = None
    bold: bool = False
    align: str = "left"
    role: str | None = None


@dataclass
class Icon:
    id: str
    x: int
    y: int
    kind: str
    color_role: str


@dataclass
class Line:
    id: str
    x1: int
    y1: int
    x2: int
    y2: int
    color_role: str = "connector"
    dashed: bool = False
    arrow: bool = True
    label: str = ""
    role: str = "edge"
    source: str | None = None
    target: str | None = None


@dataclass
class Scene:
    spec: dict[str, object]
    style: dict[str, object]
    boxes: list[Box] = field(default_factory=list)
    labels: list[Label] = field(default_factory=list)
    icons: list[Icon] = field(default_factory=list)
    lines: list[Line] = field(default_factory=list)
    modules: set[str] = field(default_factory=lambda: {"top-band", "focus-node", "footer-band"})

    def box(self, *args, **kwargs) -> Box:
        item = Box(*args, **kwargs)
        self.boxes.append(item)
        if item.module:
            self.modules.add(item.module)
        return item

    def label(self, *args, **kwargs) -> Label:
        item = Label(*args, **kwargs)
        self.labels.append(item)
        return item

    def icon(self, *args, **kwargs) -> Icon:
        item = Icon(*args, **kwargs)
        self.icons.append(item)
        return item

    def line(self, *args, **kwargs) -> Line:
        item = Line(*args, **kwargs)
        self.lines.append(item)
        return item


def add_common(scene: Scene) -> None:
    spec = scene.spec
    scene.box("main-shell", 40, 140, 1420, 720, color_role="group", kind="region", shadow=True, visual_role="canvas")
    scene.box("top-band", 70, 165, 1360, 58, color_role="axis-main", kind="region", module="top-band")
    chips = TOP_BAND_LABELS[spec["skeleton"]]
    for index, value in enumerate(chips):
        scene.box(f"top-chip-{index}", 105 + index * 440, 176, 380, 36, value, color_role=("axis-main", "axis-cross", "data-flow")[index], font_size=13)
    scene.box("footer-band", 40, 890, 1420, 78, color_role="data-flow", kind="region", module="footer-band")
    scene.label("footer-title", 74, 906, 130, 42, "核心价值", 20, "data-flow", True)
    for index, value in enumerate(spec["footer"]):
        scene.box(f"footer-{index}", 230 + index * 290, 902, 245, 52, value, color_role="data-flow", font_size=14)


def add_layered(scene: Scene) -> None:
    groups = scene.spec["groups"]
    for index, group in enumerate(groups):
        y = 245 + index * 108
        scene.box(f"layer-{index}", 70, y, 1230, 88, color_role=("axis-main" if index == 0 else "group"), kind="region")
        scene.box(f"layer-title-{index}", 88, y + 14, 205, 60, group["title"], color_role=("axis-main" if index == 0 else "axis-cross"), solid=index == 0, font_size=17)
        if index < 3:
            scene.icon(f"layer-icon-{index}", 104, y + 30, ("users", "shield", "cluster")[index], ("axis-main", "axis-cross", "data-flow")[index])
        for item_index, value in enumerate(group["items"]):
            scene.box(f"layer-{index}-item-{item_index}", 320 + item_index * 245, y + 14, 220, 60, value, color_role=("axis-main" if index == 0 else "group"))
        if index == 1:
            scene.box("focus", 1055, y + 14, 220, 60, scene.spec["focus"], "", "focus", solid=True, visual_role="focus", module="focus-node", font_size=15)
    scene.modules.add("aux-column")
    scene.box("side-rail", 1325, 245, 105, 565, color_role="side-rail", kind="region", module="aux-column", shadow=True)
    scene.label("side-title", 1336, 260, 82, 42, "治理保障", 16, "side-rail", True, "center")
    for index, value in enumerate(scene.spec["sideRail"]):
        scene.box(f"side-{index}", 1339, 320 + index * 80, 77, 54, value, color_role="side-rail", font_size=13)
    scene.box("layer-insight", 70, 690, 1230, 120, scene.spec["conclusion"], "架构能力形成统一承载、弹性扩展与闭环治理", "data-flow", kind="region", font_size=18)


def add_matrix(scene: Scene) -> None:
    columns = scene.spec["columns"]
    count = len(columns)
    gap = 20
    width = (1320 - gap * (count - 1)) // count
    start = 70
    for index, column in enumerate(columns):
        x = start + index * (width + gap)
        role = ("axis-main", "axis-cross", "data-flow", "side-rail")[index]
        scene.box(f"matrix-column-{index}", x, 250, width, 480, color_role=role, kind="region", shadow=True)
        scene.box(f"matrix-title-{index}", x + 20, 270, width - 40, 62, column["title"], color_role=role, solid=index == 0, font_size=17)
        if index < 3:
            scene.icon(f"matrix-icon-{index}", x + 34, 287, ("users", "shield", "cluster")[index], role)
        for row, value in enumerate(column["items"]):
            scene.box(f"matrix-{index}-{row}", x + 24, 355 + row * 78, width - 48, 58, value, color_role=role, font_size=14)
    scene.box("focus", 560, 770, 440, 62, f"推荐关注：{scene.spec['focus']}", "", "focus", solid=True, visual_role="focus", module="focus-node", font_size=17)


def add_flow_linear(scene: Scene) -> None:
    steps = scene.spec["steps"]
    count = len(steps)
    width = 185 if count == 6 else 205
    gap = (1360 - count * width) // max(1, count - 1)
    start = 70
    y = 390
    for index, value in enumerate(steps):
        x = start + index * (width + gap)
        focus = value == scene.spec["focus"]
        node_id = "flow-start" if index == 0 else ("flow-end" if index == count - 1 else f"step-{index}")
        stage_label = "开始" if index == 0 else ("结束" if index == count - 1 else f"步骤 {index + 1}")
        scene.box(node_id, x, y, width, 112, value, stage_label, ("focus" if focus else "axis-main"), solid=focus, visual_role=("focus" if focus else None), module=("focus-node" if focus else None), font_size=16)
        if index in {0, count // 2, count - 1}:
            scene.icon(f"step-icon-{index}", x + 16, y + 18, ("users", "shield", "cluster")[len(scene.icons) % 3], ("focus" if focus else "axis-main"))
        if index < count - 1:
            target_id = "flow-end" if index + 1 == count - 1 else f"step-{index + 1}"
            scene.line(f"edge-{index}", x + width, y + 56, x + width + gap, y + 56, source=node_id, target=target_id)
    scene.label("flow-note", 260, 570, 1040, 70, scene.spec["conclusion"], 18, "data-flow", True, "center")
    scene.box("flow-control-band", 170, 690, 1160, 100, "关键控制点", "入口校验 · 核心处理 · 异常兜底 · 结果闭环", "axis-cross", kind="region", font_size=18)


def add_flow_branching(scene: Scene) -> None:
    positions = [(80, 410), (330, 410), (580, 410), (1060, 410), (1300, 410)]
    widths = [190, 190, 200, 190, 130]
    for index, (value, (x, y), width) in enumerate(zip(scene.spec["steps"], positions, widths)):
        focus = value == scene.spec["focus"]
        node_id = "flow-start" if index == 0 else ("decision-risk" if focus else ("flow-end" if index == len(scene.spec["steps"]) - 1 else f"step-{index}"))
        stage_label = "开始" if index == 0 else ("结束" if node_id == "flow-end" else f"阶段 {index + 1}")
        scene.box(node_id, x, y, width, 100, value, stage_label, ("focus" if focus else "axis-main"), solid=focus, visual_role=("focus" if focus else None), module=("focus-node" if focus else None), font_size=16)
        if index in {0, 2, 4}:
            scene.icon(f"branch-icon-{index}", x + 14, y + 16, ("users", "shield", "cluster")[len(scene.icons) % 3], ("focus" if focus else "axis-main"))
    scene.line("edge-0", 270, 460, 330, 460, source="flow-start", target="step-1")
    scene.line("edge-1", 520, 460, 580, 460, source="step-1", target="decision-risk")
    scene.line("edge-main-2", 780, 460, 1060, 460, label="通过", source="decision-risk", target="step-3")
    scene.line("edge-main-3", 1250, 460, 1300, 460, source="step-3", target="flow-end")
    for index, (value, y) in enumerate(zip(scene.spec["branches"], (270, 575))):
        branch_id = f"error-{index}"
        scene.box(branch_id, 830, y, 190, 88, value, ("风险路径" if index == 0 else "补偿路径"), "axis-cross", font_size=15)
        scene.line(f"edge-branch-{index}", 780, 460, 830, y + 44, "axis-cross", dashed=True, label=("复核" if index == 0 else "补偿"), source="decision-risk", target=branch_id)
    scene.label("branch-note", 470, 700, 620, 54, "判断结果决定主流程、人工路径与补偿路径", 17, "data-flow", True, "center")


def add_cycle(scene: Scene) -> None:
    positions = [(100, 300), (360, 300), (620, 300), (880, 300), (1140, 300), (1140, 580)]
    for index, (value, (x, y)) in enumerate(zip(scene.spec["steps"], positions)):
        focus = value == scene.spec["focus"]
        scene.box(f"cycle-{index}", x, y, 220, 96, value, f"阶段 {index + 1}", ("focus" if focus else ("axis-main" if index < 3 else "axis-cross")), solid=focus, visual_role=("focus" if focus else None), module=("focus-node" if focus else None), font_size=16)
        if index in {0, 3, 5}:
            scene.icon(f"cycle-icon-{index}", x + 16, y + 16, ("users", "shield", "cluster")[len(scene.icons) % 3], ("focus" if focus else "axis-main"))
        if index:
            px, py = positions[index - 1]
            transition = ("提交", "确认", "处理", "完成", "退出")[index - 1] if scene.spec["id"] == "state" else "进入下一阶段"
            if px == x:
                x1, y1, x2, y2 = px + 110, py + 96, x + 110, y
            else:
                x1, y1, x2, y2 = px + 220, py + 48, x, y + 48
            scene.line(f"cycle-edge-{index}", x1, y1, x2, y2, "connector", dashed=index > 3, label=transition, source=f"cycle-{index - 1}", target=f"cycle-{index}")
    scene.box("cycle-center", 610, 420, 340, 110, "持续反馈闭环", scene.spec["conclusion"], "data-flow", kind="region", font_size=18)


def add_relationship(scene: Scene) -> None:
    positions = [(120, 270), (620, 250), (1120, 270), (120, 610), (620, 630), (1120, 610)]
    center = Box("focus", 620, 420, 320, 120, scene.spec["focus"], "核心主题", "focus", solid=True, visual_role="focus", module="focus-node", font_size=20)
    scene.boxes.append(center)
    for index, (value, (x, y)) in enumerate(zip(scene.spec["nodes"], positions)):
        role = ("axis-main", "axis-cross", "data-flow")[index % 3]
        scene.box(f"relation-{index}", x, y, 260, 88, value, f"关联域 {index + 1}", role, font_size=16)
        if index < 3:
            scene.icon(f"relation-icon-{index}", x + 16, y + 16, ("users", "shield", "cluster")[index], role)
        if index < 3:
            scene.line(f"relation-edge-{index}", x + 130, y + 88, 780, 420, role, dashed=True, arrow=False)
        else:
            scene.line(f"relation-edge-{index}", 780, 540, x + 130, y, role, dashed=True, arrow=False)
    if scene.spec["id"] == "relationship-er":
        scene.label("cardinality-one", 535, 375, 40, 24, "1", 13, None, True, "center")
        scene.label("cardinality-many", 985, 555, 40, 24, "N", 13, None, True, "center")


def add_sequence(scene: Scene) -> None:
    participants = scene.spec["participants"]
    xs = [105 + index * 285 for index in range(len(participants))]
    for index, (value, x) in enumerate(zip(participants, xs)):
        focus = value == scene.spec["focus"]
        scene.box(f"participant-{index}", x, 260, 190, 72, value, "参与方", ("focus" if focus else "axis-main"), solid=focus, visual_role=("focus" if focus else None), module=("focus-node" if focus else None), font_size=16)
        if index in {0, 2, 4}:
            scene.icon(f"sequence-icon-{index}", x + 14, 280, ("users", "shield", "cluster")[len(scene.icons) % 3], ("focus" if focus else "axis-main"))
        scene.line(f"lifeline-{index}", x + 95, 332, x + 95, 775, "axis-cross", dashed=True, arrow=False, role="lifeline")
    scene.label("sequence-start", 70, 228, 130, 28, "开始", 13, "axis-main", True)
    scene.label("sequence-end", 1320, 790, 130, 28, "结束", 13, None, True, "center")
    pairs = [(0, 1), (1, 2), (2, 1), (2, 3), (3, 2), (2, 4)]
    for index, (message, pair) in enumerate(zip(scene.spec["messages"], pairs)):
        y = 380 + index * 62
        a, b = pair
        x1, x2 = xs[a] + 95, xs[b] + 95
        edge_id = f"return-{index}" if index in {2, 5} else f"message-{index}"
        scene.line(edge_id, x1, y, x2, y, ("data-flow" if index in {2, 5} else "connector"), dashed=index in {2, 5}, source=f"lifeline-{a}", target=f"lifeline-{b}")
        scene.label(f"message-label-{index}", min(x1, x2) + 10, y - 28, abs(x2 - x1) - 20, 24, f"{index + 1}. {message}", 12, None, True, "center")


def add_timeline(scene: Scene) -> None:
    stages = scene.spec["stages"]
    count = len(stages)
    start, end, y_line = 160, 1340, 500
    scene.line("timeline-axis", start, y_line, end, y_line, "axis-main", arrow=False)
    for index, stage in enumerate(stages):
        center = start + int(index * (end - start) / max(1, count - 1))
        y = 285 if index % 2 == 0 else 570
        focus = stage["title"] == scene.spec["focus"]
        role = "focus" if focus else ("axis-main" if index % 2 == 0 else "axis-cross")
        scene.box(f"stage-{index}", center - 120, y, 240, 126, stage["title"], " · ".join(stage["items"]), role, solid=focus, visual_role=("focus" if focus else None), module=("focus-node" if focus else None), font_size=17)
        scene.line(f"stage-link-{index}", center, y + (126 if y < y_line else 0), center, y_line, role, dashed=True, arrow=False)
        if index in {0, count // 2, count - 1}:
            scene.icon(f"timeline-icon-{index}", center - 104, y + 18, ("users", "shield", "cluster")[len(scene.icons) % 3], role)


def add_summary(scene: Scene) -> None:
    add_relationship(scene)
    scene.boxes[-7].sublabel = "核心能力"


SKELETON_NAMES = {
    "layered": "分层架构",
    "matrix": "矩阵对比",
    "flow-linear": "线性流程",
    "flow-branching": "分支流程",
    "flow-cycle": "闭环状态",
    "relationship": "关系数据",
    "sequence": "交互时序",
    "timeline": "时间规划",
    "summary": "能力总结",
}
TOP_BAND_LABELS = {
    "layered": ("业务入口", "核心能力", "治理保障"),
    "matrix": ("评估维度", "方案差异", "决策建议"),
    "flow-linear": ("流程入口", "关键控制", "结果闭环"),
    "flow-branching": ("流程入口", "分支决策", "异常闭环"),
    "flow-cycle": ("状态演进", "持续反馈", "闭环优化"),
    "relationship": ("关系主体", "核心聚合", "治理边界"),
    "sequence": ("调用角色", "交互消息", "返回结果"),
    "timeline": ("目标阶段", "关键里程碑", "验收结果"),
    "summary": ("能力域", "价值聚合", "落地重点"),
}
BUILDERS = {
    "layered": add_layered,
    "matrix": add_matrix,
    "flow-linear": add_flow_linear,
    "flow-branching": add_flow_branching,
    "flow-cycle": add_cycle,
    "relationship": add_relationship,
    "sequence": add_sequence,
    "timeline": add_timeline,
    "summary": add_summary,
}


def build_scene(spec: dict[str, object]) -> Scene:
    style = STYLE.build_style_map(spec["theme"], layout=spec["layout"], dominant_axis=spec["dominantAxis"])
    scene = Scene(spec, style)
    add_common(scene)
    BUILDERS[spec["skeleton"]](scene)
    if not any(box.visual_role == "focus" for box in scene.boxes):
        raise ValueError(f"scene has no focus: {spec['id']}")
    return scene


def svg_icon(icon: Icon, color: str) -> str:
    x, y = icon.x, icon.y
    if icon.kind == "users":
        body = f'<circle cx="{x + 14}" cy="{y + 8}" r="5"/><path d="M{x + 5} {y + 27}c1-8 5-11 9-11s8 3 9 11" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
    elif icon.kind == "shield":
        body = f'<path d="M{x + 14} {y + 2}l9 4v7c0 7-4 11-9 14-5-3-9-7-9-14V{y + 6}z" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M{x + 10} {y + 13}l3 3 6-7" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        body = f'<rect x="{x + 2}" y="{y + 5}" width="7" height="18" rx="2"/><rect x="{x + 11}" y="{y + 1}" width="7" height="22" rx="2"/><rect x="{x + 20}" y="{y + 9}" width="7" height="14" rx="2"/>'
    return f'<g id="{icon.id}" data-role="icon" data-color-role="{icon.color_role}" fill="{color}">{body}</g>'


def icon_data(icon: Icon, color: str) -> str:
    local = Icon(icon.id, 0, 0, icon.kind, icon.color_role)
    body = svg_icon(local, color)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30">{body}</svg>'
    return "data:image/svg+xml," + quote(svg, safe="")


def svg_text(item: Label, color: str) -> str:
    anchor = "middle" if item.align == "center" else "start"
    x = item.x + item.width // 2 if anchor == "middle" else item.x
    y = item.y + item.height // 2 + item.size // 3
    extra = ' data-text-role="auxiliary"' if item.size <= 11 else ""
    role = f' data-role="{item.role}"' if item.role else ""
    return f'<text id="{item.id}" x="{x}" y="{y}" font-size="{item.size}" font-weight="{700 if item.bold else 400}" text-anchor="{anchor}" fill="{color}"{role}{extra}>{html.escape(item.value)}</text>'


def build_svg(scene: Scene, spec_hash: str) -> str:
    spec, style = scene.spec, scene.style
    n, roles = style["neutral"], style["roles"]
    modules = " ".join(sorted(scene.modules))
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="1000" viewBox="0 0 1560 1000" role="img" aria-labelledby="title desc" font-family="Inter, Noto Sans SC, Microsoft YaHei, Arial, sans-serif" data-theme="{spec["theme"]}" data-mode="light" data-layout="{spec["layout"]}" data-dominant-axis="{spec["dominantAxis"]}" data-visual-contract="enterprise-v2" data-modules="{modules}" data-generation="{GENERATION}" data-diagram-type="{spec["id"]}" data-spec-hash="{spec_hash}">',
        f'<title id="title">{html.escape(spec["title"])}</title>',
        f'<desc id="desc">{html.escape(spec["conclusion"])}</desc>',
        f'<metadata data-layout="{spec["layout"]}" data-optional-modules="{OPTIONAL_MODULES}"/>',
        '<defs><filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.08"/></filter>' + ('<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0l10 5-10 5z" fill="context-stroke"/></marker>' if any(item.arrow for item in scene.lines) else '') + '</defs>',
        f'<rect width="1560" height="1000" fill="{n["canvas"]}"/>',
        f'<rect x="52" y="36" width="8" height="76" rx="4" fill="{roles["focus"]["base"]}"/>',
        svg_text(Label("page-title", 82, 32, 760, 58, spec["title"], 40, bold=True, role="page-title"), n["text-strong"]),
        svg_text(Label("subtitle", 82, 86, 900, 30, spec["conclusion"], 15), n["text"]),
    ]
    badges = [(spec["label"], "axis-main", 150), (SKELETON_NAMES[spec["skeleton"]], "focus", 150), (style["theme-name"].split("｜")[0].strip(), "data-flow", 190)]
    bx = 985
    for index, (value, role, width) in enumerate(badges):
        token = roles[role]
        lines.append(f'<rect x="{bx}" y="52" width="{width}" height="42" rx="21" fill="{n["surface"]}" stroke="{token["border"]}" stroke-width="1.2"/>')
        lines.append(svg_text(Label(f"badge-{index}", bx, 52, width, 42, value, 13, bold=True, align="center"), n["text-strong"]))
        bx += width + 14
    for box in scene.boxes:
        token = roles[box.color_role]
        fill = token["base"] if box.solid else (n["surface"] if box.visual_role == "canvas" or (box.kind == "node" and box.color_role == "group") else token["soft"])
        stroke = token["strong"] if box.solid else token["border"]
        foreground = token["foreground"] if box.solid else n["text-strong"]
        attrs = [f'id="{box.id}"', f'x="{box.x}"', f'y="{box.y}"', f'width="{box.width}"', f'height="{box.height}"', 'rx="14"', f'fill="{fill}"', f'stroke="{stroke}"', 'stroke-width="1.2"', f'data-role="{box.kind}"', f'data-color-role="{box.color_role}"']
        if box.visual_role:
            attrs.append(f'data-visual-role="{box.visual_role}"')
        if box.module:
            attrs.append(f'data-module="{box.module}"')
        if box.shadow:
            attrs.append('filter="url(#softShadow)"')
        lines.append("<rect " + " ".join(attrs) + "/>")
        if box.label:
            center_x = box.x + box.width // 2
            label_y = box.y + box.height // 2 + (0 if not box.sublabel else -8)
            lines.append(f'<text x="{center_x}" y="{label_y}" font-size="{box.font_size}" font-weight="700" text-anchor="middle" fill="{foreground}">{html.escape(box.label)}</text>')
            if box.sublabel:
                lines.append(f'<text x="{center_x}" y="{label_y + 24}" font-size="11" data-text-role="auxiliary" text-anchor="middle" fill="{foreground if box.solid else n["text-muted"]}">{html.escape(box.sublabel)}</text>')
    for item in scene.labels:
        color = roles[item.color_role]["strong"] if item.color_role else n["text"]
        lines.append(svg_text(item, color))
    for icon in scene.icons:
        lines.append(svg_icon(icon, roles[icon.color_role]["base"]))
    for edge in scene.lines:
        token = roles[edge.color_role]
        dash = ' stroke-dasharray="7 6"' if edge.dashed else ""
        arrow = ' marker-end="url(#arrow)"' if edge.arrow else ""
        lines.append(f'<line id="{edge.id}" data-role="{edge.role}" data-color-role="{edge.color_role}" x1="{edge.x1}" y1="{edge.y1}" x2="{edge.x2}" y2="{edge.y2}" stroke="{token["base"]}" stroke-width="2.4"{dash}{arrow}/>' )
        if edge.label:
            lines.append(svg_text(Label(f"{edge.id}-label", min(edge.x1, edge.x2), min(edge.y1, edge.y2) - 26, max(abs(edge.x2 - edge.x1), 70), 24, edge.label, 12, bold=True, align="center"), n["text"]))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def xml_style(fill: str, stroke: str, font: str, size: int, *, bold: bool = False, shadow: bool = False, align: str = "center", image: str | None = None, line: bool = False, dashed: bool = False, arrow: bool = False) -> str:
    if image:
        return f"shape=image;html=1;imageAspect=0;aspect=fixed;strokeColor=none;fillColor=none;image={image};"
    if line:
        return f"edgeStyle=none;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={stroke};strokeWidth=2.4;dashed={1 if dashed else 0};endArrow={'block' if arrow else 'none'};endFill={1 if arrow else 0};"
    parts = ["rounded=1", "absoluteArcSize=1", "arcSize=14", "whiteSpace=wrap", "html=1", f"fillColor={fill}", f"strokeColor={stroke}", "strokeWidth=1.2", f"fontColor={font}", f"fontSize={size}", "fontFamily=Microsoft YaHei", f"align={align}", "verticalAlign=middle"]
    if bold:
        parts.append("fontStyle=1")
    if shadow:
        parts.append("shadow=1")
    return ";".join(parts) + ";"


def build_drawio(scene: Scene, spec_hash: str) -> str:
    spec, style = scene.spec, scene.style
    n, roles = style["neutral"], style["roles"]
    modules = " ".join(sorted(scene.modules))
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "xml-diagram"})
    diagram = ET.SubElement(mxfile, "diagram", {"name": spec["title"], "id": f"catalog-{spec['id']}", "theme": spec["theme"], "mode": "light", "layout": spec["layout"], "dominantAxis": spec["dominantAxis"], "visualContract": "enterprise-v2", "modules": modules, "optionalModules": OPTIONAL_MODULES, "generation": GENERATION, "diagramType": spec["id"], "specHash": spec_hash})
    model = ET.SubElement(diagram, "mxGraphModel", {"dx":"1500","dy":"950","grid":"0","gridSize":"10","guides":"1","tooltips":"1","connect":"1","arrows":"1","fold":"1","page":"1","pageScale":"1","pageWidth":"1560","pageHeight":"1000","math":"0","shadow":"0","background":n["canvas"]})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id":"0"})
    ET.SubElement(root, "mxCell", {"id":"1","parent":"0"})

    def cell(cell_id: str, value: str, x: int, y: int, width: int, height: int, style_value: str, **metadata: str) -> ET.Element:
        attrs = {"id":cell_id,"value":value,"vertex":"1","parent":"1","style":style_value, **{key:value for key,value in metadata.items() if value}}
        item = ET.SubElement(root, "mxCell", attrs)
        ET.SubElement(item, "mxGeometry", {"x":str(x),"y":str(y),"width":str(width),"height":str(height),"as":"geometry"})
        return item

    cell("accent-bar", "", 52, 36, 8, 76, xml_style(roles["focus"]["base"], roles["focus"]["base"], roles["focus"]["foreground"], 12))
    cell("page-title", spec["title"], 82, 32, 760, 48, xml_style("none", "none", n["text-strong"], 40, bold=True, align="left"), role="page-title")
    cell("subtitle", spec["conclusion"], 82, 84, 900, 28, xml_style("none", "none", n["text"], 15, align="left"))
    badges = [(spec["label"], "axis-main", 150), (SKELETON_NAMES[spec["skeleton"]], "focus", 150), (style["theme-name"].split("｜")[0].strip(), "data-flow", 190)]
    bx = 985
    for index, (value, role, width) in enumerate(badges):
        cell(f"badge-{index}", value, bx, 52, width, 42, xml_style(n["surface"], roles[role]["border"], n["text-strong"], 13, bold=True))
        bx += width + 14
    for box in scene.boxes:
        token = roles[box.color_role]
        fill = token["base"] if box.solid else (n["surface"] if box.visual_role == "canvas" or (box.kind == "node" and box.color_role == "group") else token["soft"])
        stroke = token["strong"] if box.solid else token["border"]
        foreground = token["foreground"] if box.solid else n["text-strong"]
        value = f"<b>{html.escape(box.label)}</b>" if box.label else ""
        if box.sublabel:
            value += f"<br><font style='font-size:11px;color:{foreground if box.solid else n['text-muted']}'>{html.escape(box.sublabel)}</font>"
        cell(box.id, value, box.x, box.y, box.width, box.height, xml_style(fill, stroke, foreground, box.font_size, shadow=box.shadow), role=box.kind, colorRole=box.color_role, visualRole=box.visual_role or "", module=box.module or "")
    for item in scene.labels:
        color = roles[item.color_role]["strong"] if item.color_role else n["text"]
        cell(item.id, item.value, item.x, item.y, item.width, item.height, xml_style("none", "none", color, item.size, bold=item.bold, align=item.align), role=item.role or "")
    for icon in scene.icons:
        color = roles[icon.color_role]["base"]
        cell(icon.id, "", icon.x, icon.y, 30, 30, xml_style("none", "none", color, 12, image=icon_data(icon, color)), role="icon", colorRole=icon.color_role)
    for edge in scene.lines:
        attrs = {"id":edge.id,"value":edge.label,"edge":"1","parent":"1","style":xml_style("none", roles[edge.color_role]["base"], n["text"], 11, line=True, dashed=edge.dashed, arrow=edge.arrow),"role":edge.role,"colorRole":edge.color_role}
        explicit_sequence_geometry = scene.spec["skeleton"] == "sequence" and edge.id.startswith(("message-", "return-"))
        if edge.source:
            attrs["semanticSource"] = edge.source
            if not explicit_sequence_geometry:
                attrs["source"] = edge.source
        if edge.target:
            attrs["semanticTarget"] = edge.target
            if not explicit_sequence_geometry:
                attrs["target"] = edge.target
        item = ET.SubElement(root, "mxCell", attrs)
        geometry = ET.SubElement(item, "mxGeometry", {"relative":"1","as":"geometry"})
        ET.SubElement(geometry, "mxPoint", {"x":str(edge.x1),"y":str(edge.y1),"as":"sourcePoint"})
        ET.SubElement(geometry, "mxPoint", {"x":str(edge.x2),"y":str(edge.y2),"as":"targetPoint"})
    ET.indent(mxfile, space="  ")
    return "<?xml version='1.0' encoding='utf-8'?>\n" + ET.tostring(mxfile, encoding="unicode") + "\n"


def build_dsl(scene: Scene, spec_hash: str) -> str:
    spec, style = scene.spec, scene.style
    roles = "\n".join(f"- {role}: {color}（来源：{style['role-sources'][role]}）" for role, color in style["role-colors"].items())
    modules = "、".join(sorted(scene.modules))
    return f"""# {spec['label']} DSL：{spec['title']}

生成方式：{GENERATION}
规格哈希：{spec_hash}

## 原始自然语言需求

{spec['request']}

## 可执行蓝图

- 图形类型：{spec['id']}（{spec['label']}）
- 核心结论：{spec['conclusion']}
- 视觉骨架：{SKELETON_NAMES[spec['skeleton']]}
- 视觉主题：{style['theme-name']}
- 布局：{spec['layout']}
- 主叙事轴：{spec['dominantAxis']}
- 视觉合同：enterprise-v2
- 附加模块：{modules}
- 图标策略：仅在入口、焦点或关键区域按内容少量使用自包含线性图标，不设置硬上限

## 结构颜色映射

{roles}

## 质量预期

页面标题、区域、卡片和辅助信息层级清楚；唯一焦点承载核心结论；同类组件颜色一致；连线不穿越节点；XML/SVG 节点、角色和几何语义一致。
"""


def guarded_clean(directory: Path, suffixes: set[str]) -> list[str]:
    directory = directory.resolve()
    if REPO.resolve() not in directory.parents:
        raise RuntimeError(f"refusing to clean outside repository: {directory}")
    removed = []
    if not directory.exists():
        return removed
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in suffixes:
            path.unlink()
            removed.append(str(path.relative_to(REPO)).replace("\\", "/"))
    return removed


def write_docs(kind: str, artifacts: list[dict[str, object]]) -> None:
    source_dir = "svg" if kind == "svg" else "drawio"
    extension = ".svg" if kind == "svg" else ".drawio"
    title = "svg-generator" if kind == "svg" else "xml-diagram"
    lines = [f"# {title} 使用说明", "", "两套绘图 Skill 共享 `enterprise-v2` 视觉合同和 19 类自然语言新生目录。主题名称与配色固定，结构颜色会按主轴、交叉轴、侧栏、焦点和数据流受控映射。", "", "## 生成与主题规则", "", "- 用户未指定主题时询问一次；仍不指定则使用 Tech Blue｜科技蓝（默认）。", "- 架构图保持纵向分层主骨架；流程、关系、矩阵和时间类选择相应视觉骨架。", "- 图标由内容决定，不设硬上限，但只在具有导航、识别或焦点价值时使用。", "- 所有文件都从自然语言请求重新生成，不从旧示例批量换色。", "", "## 19 类新生示例", "", f"| 图形类型 | 主题 | {('SVG' if kind == 'svg' else 'Draw.io')} 源文件 | PNG 预览 |", "| --- | --- | --- | --- |"]
    for item in artifacts:
        name = f"{item['id']}-{item['theme']}-light-enterprise"
        lines.append(f"| {item['label']} | {item['themeName']} | [文件]({source_dir}/{name}{extension}) | [预览](images/{name}.png) |")
    lines.extend(["", "## 验证", "", "本目录源文件与测试截图来自同一请求清单。完整流程会清理旧目标、生成 DSL 和两种源文件、严格校验、真实渲染，并记录 SHA-256；详情见 `test-outputs/diagram-types/catalog/verification-report.json`。", ""])
    (REPO / "docs" / title / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_test_index(artifacts: list[dict[str, object]]) -> None:
    lines = ["# 19 类图形全流程新生测试", "", "本目录图片不是旧示例重导出。每一类都由固定自然语言需求生成 DSL，再从共享场景分别生成 XML/Draw.io 与 SVG，经过严格校验和真实渲染。", "", "| 图形类型 | 主题 | XML/Draw.io PNG | SVG PNG |", "| --- | --- | --- | --- |"]
    for item in artifacts:
        name = f"{item['id']}-{item['theme']}-light-enterprise.png"
        lines.append(f"| {item['label']} | {item['themeName']} | [预览](xml/{name}) | [预览](svg/{name}) |")
    lines.extend(["", "生成清单、DSL、源文件和哈希报告见 [catalog](catalog/README.md)。四主题审批基线保留在 [baselines](baselines/README.md)。", ""])
    (REPO / "test-outputs" / "diagram-types" / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_catalog_index(artifacts: list[dict[str, object]]) -> None:
    lines = ["# 19 类绘图全流程目录", "", "本目录是两套绘图 Skill 的端到端验证源。固定自然语言需求先生成 DSL，再经共享场景模型分别生成 SVG 与 Draw.io；不读取旧模板或旧示例。", "", "## 重新生成与验证", "", "```powershell", "python test-outputs/diagram-types/catalog/verify_catalog.py", "```", "", "验证流程会清理声明目标、重新生成 19 类 × 2 格式源文件、检查 XML/SVG 语义与几何一致性、严格校验、真实渲染 38 张 PNG，并写入 `verification-report.json`。", "", "| 图形类型 | 主题 | DSL | SVG | Draw.io | SVG PNG | Draw.io PNG |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for item in artifacts:
        name = f"{item['id']}-{item['theme']}-light-enterprise"
        lines.append(f"| {item['label']} | {item['themeName']} | [DSL](dsl/{item['id']}.md) | [SVG](svg/{name}.svg) | [Draw.io](xml/{name}.drawio) | [预览](images/svg/{name}.png) | [预览](images/xml/{name}.png) |")
    lines.extend(["", "`generation-manifest.json` 记录请求、主题、骨架、主轴、结构角色和源文件哈希；`verification-report.json` 记录渲染器、清理目标、语义配对结果及全部图片哈希。", ""])
    (HERE / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    items = request["items"]
    expected = set(SVG_TEMPLATES)
    actual = {item["id"] for item in items}
    if actual != expected or len(items) != 19:
        raise SystemExit(f"request catalog mismatch: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    clean_targets = [
        (HERE / "dsl", {".md"}), (HERE / "svg", {".svg"}), (HERE / "xml", {".drawio"}),
        (REPO / ".opencode/skills/svg-generator/templates", {".svg"}),
        (REPO / ".opencode/skills/svg-generator/examples", {".svg"}),
        (REPO / ".opencode/skills/xml-diagram/templates", {".drawio"}),
        (REPO / ".opencode/skills/xml-diagram/examples", {".drawio"}),
        (REPO / "docs/svg-generator/svg", {".svg"}), (REPO / "docs/svg-generator/images", {".png"}),
        (REPO / "docs/xml-diagram/drawio", {".drawio"}), (REPO / "docs/xml-diagram/images", {".png"}),
        (REPO / "test-outputs/diagram-types/svg", {".png"}), (REPO / "test-outputs/diagram-types/xml", {".png"}),
    ]
    removed = []
    for directory, suffixes in clean_targets:
        directory.mkdir(parents=True, exist_ok=True)
        removed.extend(guarded_clean(directory, suffixes))
    for folder in (HERE / "dsl", HERE / "svg", HERE / "xml"):
        folder.mkdir(parents=True, exist_ok=True)

    request_hash = digest(REQUEST_PATH)
    artifacts = []
    for spec in items:
        scene = build_scene(spec)
        spec_hash = digest_text(json.dumps({"requestHash": request_hash, "spec": spec}, ensure_ascii=False, sort_keys=True))
        name = f"{spec['id']}-{spec['theme']}-light-enterprise"
        dsl_path, svg_path, xml_path = HERE / "dsl" / f"{spec['id']}.md", HERE / "svg" / f"{name}.svg", HERE / "xml" / f"{name}.drawio"
        dsl_path.write_text(build_dsl(scene, spec_hash), encoding="utf-8", newline="\n")
        svg_path.write_text(build_svg(scene, spec_hash), encoding="utf-8", newline="\n")
        xml_path.write_text(build_drawio(scene, spec_hash), encoding="utf-8", newline="\n")

        svg_template = REPO / ".opencode/skills/svg-generator/templates" / SVG_TEMPLATES[spec["id"]]
        xml_template = REPO / ".opencode/skills/xml-diagram/templates" / XML_TEMPLATES[spec["id"]]
        svg_example = REPO / ".opencode/skills/svg-generator/examples" / f"{name}.svg"
        xml_example = REPO / ".opencode/skills/xml-diagram/examples" / f"{name}.drawio"
        docs_svg = REPO / "docs/svg-generator/svg" / f"{name}.svg"
        docs_xml = REPO / "docs/xml-diagram/drawio" / f"{name}.drawio"
        for target in (svg_template, svg_example, docs_svg):
            shutil.copyfile(svg_path, target)
        for target in (xml_template, xml_example, docs_xml):
            shutil.copyfile(xml_path, target)
        artifacts.append({
            "id":spec["id"], "label":spec["label"], "theme":spec["theme"], "themeName":scene.style["theme-name"], "skeleton":spec["skeleton"], "layout":spec["layout"], "dominantAxis":spec["dominantAxis"], "modules":sorted(scene.modules), "specHash":spec_hash,
            "dsl":{"path":str(dsl_path.relative_to(HERE)).replace("\\","/"),"sha256":digest(dsl_path)},
            "svg":{"path":str(svg_path.relative_to(HERE)).replace("\\","/"),"sha256":digest(svg_path)},
            "drawio":{"path":str(xml_path.relative_to(HERE)).replace("\\","/"),"sha256":digest(xml_path)},
            "roleColors":scene.style["role-colors"], "legacyInputFiles":[],
        })
    manifest = {"schemaVersion":"fresh-catalog-manifest-v1","generationMode":GENERATION,"requestFile":"requests.json","requestSha256":request_hash,"legacyInputFiles":[],"removedTargets":removed,"artifacts":artifacts}
    (HERE / "generation-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_docs("svg", artifacts)
    write_docs("xml", artifacts)
    write_test_index(artifacts)
    write_catalog_index(artifacts)
    print(f"fresh catalog generation complete: {len(artifacts)} types, {len(artifacts) * 3} catalog sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
