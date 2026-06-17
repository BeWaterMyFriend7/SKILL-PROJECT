#!/usr/bin/env python3
"""校验 drawio XML 的基础结构和强制图形规则。"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MOJIBAKE_MARKERS = (
    "\ufffd",
    "ï¿½",
    "䴢",
    "鏁版",
    "瀹㈡",
    "鐢ㄦ",
    "绋嬪",
    "鍥剧",
    "銆",
    "锛",
    "鈥",
    "鈹",
    "骞",
    "璁㈠",
    "寰",
    "鍏ㄩ",
)

EXAMPLE_NAME_RE = re.compile(r"^[^-]+(?:-[^-]+)?-(?:dark|light)-.+\.drawio$")


def read_xml_text(path: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    try:
        return path.read_text(encoding="utf-8"), errors
    except UnicodeDecodeError as exc:
        errors.append(f"文件不是严格 UTF-8 编码: {exc}")
    except OSError as exc:
        errors.append(f"文件无法读取: {exc}")
    return None, errors


def detect_text_damage(text: str) -> list[str]:
    hits = [marker for marker in MOJIBAKE_MARKERS if marker in text]
    if not hits:
        return []
    display = "、".join(repr(item) for item in hits[:6])
    return [f"疑似中文编码损坏或 mojibake: {display}"]


def parse_style(style: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in (style or "").split(";"):
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value
        elif part:
            result[part] = "1"
    return result


def cell_geometry(cell: ET.Element) -> tuple[float, float, float, float] | None:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return None
    try:
        x = float(geometry.attrib.get("x", "0"))
        y = float(geometry.attrib.get("y", "0"))
        w = float(geometry.attrib.get("width", "0"))
        h = float(geometry.attrib.get("height", "0"))
    except ValueError:
        return None
    if w <= 0 or h <= 0:
        return None
    return x, y, w, h


def absolute_geometry(
    cell: ET.Element,
    cells_by_id: dict[str, ET.Element],
    seen: set[str] | None = None,
) -> tuple[float, float, float, float] | None:
    geom = cell_geometry(cell)
    if geom is None:
        return None
    x, y, w, h = geom
    parent_id = cell.attrib.get("parent")
    if not parent_id or parent_id == "1":
        return x, y, w, h
    if seen is None:
        seen = set()
    if parent_id in seen:
        return x, y, w, h
    parent = cells_by_id.get(parent_id)
    if parent is None:
        return x, y, w, h
    seen.add(parent_id)
    parent_geom = absolute_geometry(parent, cells_by_id, seen)
    if parent_geom is None:
        return x, y, w, h
    px, py, _, _ = parent_geom
    return px + x, py + y, w, h


def visible_vertex(cell: ET.Element) -> bool:
    if cell.attrib.get("vertex") != "1":
        return False
    style_text = cell.attrib.get("style", "")
    style = parse_style(style_text)
    if "edgeLabel" in style_text:
        return False
    if style.get("shape") == "line":
        return False
    try:
        if float(style.get("opacity", "100")) < 80:
            return False
    except ValueError:
        pass
    return True


def overlap_candidate(cell: ET.Element) -> bool:
    if not visible_vertex(cell):
        return False
    cell_id = cell.attrib.get("id", "")
    if cell_id == "bg" or cell_id.endswith("-bg"):
        return False
    if cell_id in {"tl-bar", "timeline-bar"} or cell_id.endswith("-bar"):
        return False
    style_text = cell.attrib.get("style", "")
    style = parse_style(style_text)
    if style_text.startswith("text;") and style.get("fillColor", "none") == "none":
        return False
    return True


def contains(outer: tuple[float, float, float, float], inner: tuple[float, float, float, float]) -> bool:
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner
    return ix >= ox - 1 and iy >= oy - 1 and ix + iw <= ox + ow + 1 and iy + ih <= oy + oh + 1


def overlap_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    width = min(ax + aw, bx + bw) - max(ax, bx)
    height = min(ay + ah, by + bh) - max(ay, by)
    if width <= 1 or height <= 1:
        return 0
    return width * height


def content_bounds(
    cells: list[ET.Element],
    cells_by_id: dict[str, ET.Element],
    page_w: float,
    page_h: float,
) -> tuple[float, float, float, float] | None:
    boxes: list[tuple[float, float, float, float]] = []
    for cell in cells:
        if not visible_vertex(cell):
            continue
        geom = absolute_geometry(cell, cells_by_id)
        if geom is None:
            continue
        x, y, w, h = geom
        is_full_page_bg = x <= 1 and y <= 1 and w >= page_w * 0.95 and h >= page_h * 0.95
        if is_full_page_bg:
            continue
        boxes.append(geom)
    if not boxes:
        return None
    left = min(x for x, _, _, _ in boxes)
    top = min(y for _, y, _, _ in boxes)
    right = max(x + w for x, y, w, h in boxes)
    bottom = max(y + h for x, y, w, h in boxes)
    return left, top, right - left, bottom - top


def cell_text(cell: ET.Element) -> str:
    return (cell.attrib.get("value") or "").strip()


def is_text_only(cell: ET.Element) -> bool:
    style_text = cell.attrib.get("style", "")
    style = parse_style(style_text)
    return style_text.startswith("text;") or (
        style.get("fillColor", "none") == "none" and style.get("strokeColor", "none") == "none"
    )


def is_architecture_diagram(path: Path, cells: list[ET.Element]) -> bool:
    name = path.name.lower()
    if any(marker in name for marker in ("architecture", "架构", "case-ba", "case-aa", "case-ta", "case-da")):
        return True
    text = " ".join(cell_text(cell) for cell in cells)
    return "架构图" in text


def is_sequence_diagram(path: Path, cells: list[ET.Element]) -> bool:
    name = path.name.lower()
    if any(marker in name for marker in ("sequence", "时序", "case-sq")):
        return True
    text = " ".join(cell_text(cell) for cell in cells)
    life_count = sum(1 for cell in lifeline_cells(cells))
    msg_count = sum(1 for cell in cells if cell.attrib.get("id", "").lower().startswith("msg") and cell.attrib.get("edge") == "1")
    return "时序图" in text or (life_count >= 2 and msg_count >= 2)


def lifeline_cells(cells: list[ET.Element]) -> list[ET.Element]:
    result: list[ET.Element] = []
    for cell in cells:
        if cell.attrib.get("vertex") != "1":
            continue
        style = parse_style(cell.attrib.get("style", ""))
        geom = cell_geometry(cell)
        if geom is None:
            continue
        _, _, w, h = geom
        if style.get("shape") == "line" and w <= 4 and h >= 120:
            result.append(cell)
    return result


def participant_cells(cells: list[ET.Element]) -> list[ET.Element]:
    result: list[ET.Element] = []
    for cell in cells:
        if cell.attrib.get("vertex") != "1" or not cell_text(cell):
            continue
        style = parse_style(cell.attrib.get("style", ""))
        if style.get("shape") == "line" or is_text_only(cell):
            continue
        geom = cell_geometry(cell)
        if geom is None:
            continue
        _, y, w, h = geom
        if y <= 190 and 70 <= w <= 220 and 32 <= h <= 72:
            result.append(cell)
    return result


def activation_cells(cells: list[ET.Element]) -> list[ET.Element]:
    result: list[ET.Element] = []
    for cell in cells:
        if cell.attrib.get("vertex") != "1":
            continue
        if is_text_only(cell):
            continue
        style = parse_style(cell.attrib.get("style", ""))
        if style.get("shape") == "line":
            continue
        geom = cell_geometry(cell)
        if geom is None:
            continue
        _, _, w, h = geom
        cell_id = cell.attrib.get("id", "").lower()
        if 8 <= w <= 24 and h >= 36 and ("act" in cell_id or not cell_text(cell)):
            result.append(cell)
    return result


def architecture_semantic_warnings(cells: list[ET.Element]) -> list[str]:
    warnings: list[str] = []
    tag_count = 0
    card_count = 0
    inline_detail_count = 0
    for cell in cells:
        if cell.attrib.get("vertex") != "1":
            continue
        value = cell_text(cell)
        if not value:
            continue
        style_text = cell.attrib.get("style", "")
        style = parse_style(style_text)
        geom = cell_geometry(cell)
        if geom is None:
            continue
        _, _, w, h = geom
        cell_id = cell.attrib.get("id", "")
        lower_id = cell_id.lower()

        if "title" in lower_id and not is_text_only(cell):
            warnings.append(f"{cell_id}: 架构图一级或区域标题应为纯文本，不要使用标题矩形框")

        if is_text_only(cell):
            continue

        if w <= 120 and h <= 32 and style.get("shape") != "line":
            tag_count += 1
            continue

        is_card = 90 <= w <= 280 and 40 <= h <= 130 and not (
            lower_id == "bg" or lower_id.endswith("-bg") or "legend" in lower_id
        )
        if is_card:
            card_count += 1
            plain_value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
            plain_value = re.sub(r"<[^>]+>", "", plain_value)
            detail_lines = [line.strip() for line in plain_value.splitlines() if line.strip()]
            if len(detail_lines) > 1 or " | " in plain_value or " / " in plain_value or "、" in plain_value:
                inline_detail_count += 1
                warnings.append(f"{cell_id}: 架构图三级内容应拆成小矩形标签，不要内联在卡片文字中")

    if card_count >= 4 and tag_count < max(4, card_count // 2):
        warnings.append("架构图小矩形标签数量偏少，三级内容可能仍是纯文字或语义密度不足")
    if inline_detail_count >= 3:
        warnings.append("架构图存在多处卡片内联明细，建议统一改为可编辑小矩形标签")
    return warnings


def sequence_structure_warnings(cells: list[ET.Element]) -> list[str]:
    warnings: list[str] = []
    participants = participant_cells(cells)
    lifelines = lifeline_cells(cells)
    activations = activation_cells(cells)
    message_edges = [cell for cell in cells if cell.attrib.get("edge") == "1"]

    if len(participants) < 2:
        warnings.append("时序图参与者数量不足，不能画成流程图节点链")
    if len(lifelines) < max(2, len(participants) - 1):
        warnings.append("时序图缺少足够的垂直生命线")
    if len(message_edges) > 3 and not activations:
        warnings.append("时序图多消息链路缺少激活条，竖向处理区间不明确")

    if participants:
        ys = [cell_geometry(cell)[1] for cell in participants if cell_geometry(cell) is not None]
        if ys and max(ys) - min(ys) > 4:
            warnings.append("时序图参与者未在同一水平线对齐")

    return warnings


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if path.parent.name == "examples" and not EXAMPLE_NAME_RE.match(path.name):
        errors.append("examples 文件名不符合：一级类别[-二级类别]-背景风格-业务说明[-其他].drawio")

    text, read_errors = read_xml_text(path)
    if read_errors:
        return read_errors, warnings
    assert text is not None
    errors.extend(detect_text_damage(text))

    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"XML 无法解析: {exc}"], warnings

    if root.tag not in {"mxfile", "mxGraphModel"}:
        errors.append(f"根节点类型异常: {root.tag}")

    models = root.findall(".//mxGraphModel")
    if root.tag == "mxGraphModel":
        models.append(root)
    if not models:
        errors.append("缺少 mxGraphModel")

    cells = root.findall(".//mxCell")
    if not cells:
        errors.append("缺少 mxCell 元素")

    seen: set[str] = set()
    for cell in cells:
        cell_id = cell.attrib.get("id")
        if not cell_id:
            errors.append("存在没有 id 的 mxCell")
            continue
        if cell_id in seen:
            errors.append(f"mxCell id 重复: {cell_id}")
        seen.add(cell_id)

    for geometry in root.findall(".//mxGeometry"):
        if geometry.attrib.get("as") != "geometry":
            parent = next((cell.attrib.get("id", "<无 id>") for cell in cells if geometry in list(cell)), "<未知>")
            errors.append(f"{parent}: mxGeometry 缺少 as=\"geometry\"")

    id_set = {cell.attrib.get("id") for cell in cells}
    cells_by_id = {cell.attrib.get("id", ""): cell for cell in cells}

    if is_architecture_diagram(path, cells):
        warnings.extend(architecture_semantic_warnings(cells))
    if is_sequence_diagram(path, cells):
        warnings.extend(sequence_structure_warnings(cells))

    for cell in cells:
        style = parse_style(cell.attrib.get("style", ""))
        label = (cell.attrib.get("value") or "").lower()

        if cell.attrib.get("edge") == "1":
            source = cell.attrib.get("source")
            target = cell.attrib.get("target")
            if source and source not in id_set:
                errors.append(f"{cell.attrib.get('id')}: source 引用不存在 {source}")
            if target and target not in id_set:
                errors.append(f"{cell.attrib.get('id')}: target 引用不存在 {target}")
            if style.get("curved") == "1":
                errors.append(f"{cell.attrib.get('id')}: 禁止使用曲线连线")
            if style.get("edgeStyle") and style.get("edgeStyle") != "orthogonalEdgeStyle":
                warnings.append(f"{cell.attrib.get('id')}: 不是正交连线 {style.get('edgeStyle')}")
            if ("error" in label or "失败" in label or "异常" in label or "否" in label) and style.get("dashed") == "1":
                errors.append(f"{cell.attrib.get('id')}: 错误或失败路径必须使用实线")

    for model in models:
        try:
            page_w = float(model.attrib.get("pageWidth", "0"))
            page_h = float(model.attrib.get("pageHeight", "0"))
        except ValueError:
            page_w = page_h = 0
        if page_w <= 0 or page_h <= 0:
            warnings.append("pageWidth/pageHeight 缺失或无效")
            continue
        for cell in cells:
            if cell.attrib.get("vertex") != "1":
                continue
            geom = absolute_geometry(cell, cells_by_id)
            if geom is None:
                continue
            x, y, w, h = geom
            if x < 0 or y < 0 or x + w > page_w or y + h > page_h:
                warnings.append(f"{cell.attrib.get('id')}: 图形元素超出页面边界")
        bounds = content_bounds(cells, cells_by_id, page_w, page_h)
        if bounds is not None:
            x, y, w, h = bounds
            usage = (w * h) / (page_w * page_h)
            if usage < 0.50:
                warnings.append(f"画布利用率过低: {usage:.0%}")
            if usage > 0.85:
                warnings.append(f"内容过满: {usage:.0%}")

        boxes: list[tuple[str, tuple[float, float, float, float]]] = []
        for cell in cells:
            if not overlap_candidate(cell):
                continue
            geom = absolute_geometry(cell, cells_by_id)
            if geom is not None:
                boxes.append((cell.attrib.get("id", "<无 id>"), geom))
        for left_index, (left_id, left_box) in enumerate(boxes):
            for right_id, right_box in boxes[left_index + 1 :]:
                if contains(left_box, right_box) or contains(right_box, left_box):
                    continue
                area = overlap_area(left_box, right_box)
                if area >= 100:
                    warnings.append(f"{left_id} 与 {right_id}: 图形元素重叠")
                    if len(warnings) > 80:
                        break
            if len(warnings) > 80:
                break

    return errors, warnings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true", help="存在布局或连线警告时也返回失败。")
    args = parser.parse_args()

    failed = False
    for path in args.files:
        errors, warnings = validate(path)
        print(f"{path}: {len(errors)} 个错误，{len(warnings)} 个警告")
        for item in errors:
            print(f"  错误: {item}")
        for item in warnings[:20]:
            print(f"  警告: {item}")
        if len(warnings) > 20:
            print(f"  警告: 还有 {len(warnings) - 20} 项")
        failed = failed or bool(errors) or (args.fail_on_warning and bool(warnings))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
