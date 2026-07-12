#!/usr/bin/env python3
"""Validate Mermaid Markdown structure, semantics, coverage, and rendering."""

from __future__ import annotations

import argparse
import csv
import io
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FENCE_LINE_RE = re.compile(r"^\s*```([A-Za-z0-9_-]*)\s*$")
INIT_RE = re.compile(r"^\s*%%\{init:\s*\{.*\}\s*\}%%\s*$", re.MULTILINE)
TYPE_RE = re.compile(
    r"^(flowchart|graph|sequenceDiagram|classDiagram|erDiagram|stateDiagram-v2|gantt|gitGraph|journey|pie|mindmap|timeline|quadrantChart|xychart-beta|sankey-beta|block-beta)\b",
    re.MULTILINE,
)
REQUIRED_EXAMPLES = {
    "flowchart.md", "sequence-diagram.md", "class-diagram.md", "ER-diagram.md",
    "state-diagram.md", "gantt-chart.md", "git-diagram.md", "user-journey.md",
    "pie-chart.md", "mindmap.md", "timeline.md", "quadrant-chart.md",
    "xy-chart.md", "sankey.md", "block-diagram.md",
}
PLACEHOLDER_RE = re.compile(r"TODO|待填写|占位|示例内容|\{\{[^}]+\}\}", re.IGNORECASE)


def markdown_files(path: Path) -> list[Path]:
    return sorted(path.rglob("*.md")) if path.is_dir() else [path]


def extract_mermaid_blocks(text: str) -> tuple[list[str], list[str]]:
    blocks: list[str] = []
    errors: list[str] = []
    opened: tuple[str, int, list[str]] | None = None
    for line_number, line in enumerate(text.splitlines(), 1):
        match = FENCE_LINE_RE.match(line)
        if opened is None:
            if match:
                opened = (match.group(1).lower(), line_number, [])
            continue
        language, start_line, content = opened
        if match:
            if language == "mermaid":
                blocks.append("\n".join(content).strip())
            opened = None
        else:
            content.append(line)
    if opened is not None:
        language, start_line, _ = opened
        errors.append(f"第 {start_line} 行代码围栏未闭合" + ("（Mermaid）" if language == "mermaid" else ""))
    return blocks, errors


def source_without_init(block: str) -> str:
    return INIT_RE.sub("", block, count=1).strip()


def diagram_type(source: str) -> str | None:
    match = TYPE_RE.search(source)
    return match.group(1) if match else None


def semantic_errors(kind: str, source: str) -> list[str]:
    errors: list[str] = []
    if kind in {"flowchart", "graph"}:
        if "开始" not in source or "结束" not in source:
            errors.append("flowchart 必须包含明确的开始和结束")
        decision_count = len(re.findall(r"\w+\s*\{[^{}]+\}", source))
        labelled_edges = len(re.findall(r"--?>\|[^|]+\|", source))
        if decision_count and labelled_edges < decision_count * 2:
            errors.append("flowchart 判断节点必须提供完整出口标签")
        node_ids = set(re.findall(r"^\s*([A-Za-z][\w-]*)\s*(?:\[|\(|\{)", source, re.MULTILINE))
        if len(node_ids) > 20:
            errors.append(f"flowchart 节点过多: {len(node_ids)} > 20")
        if len(re.findall(r"^\s*subgraph\b", source, re.MULTILINE)) > 8:
            errors.append("flowchart subgraph 超过 8 个")
    elif kind == "sequenceDiagram":
        participants = re.findall(r"^\s*(?:participant|actor)\s+", source, re.MULTILINE)
        messages = re.findall(r"^\s*\S+\s*(?:->>|-->>|->|-->|-x|--)\s*\S+\s*:", source, re.MULTILINE)
        if len(participants) < 2:
            errors.append("sequenceDiagram 至少需要两个参与者")
        if len(participants) > 8:
            errors.append(f"sequenceDiagram 参与者过多: {len(participants)} > 8")
        if not messages:
            errors.append("sequenceDiagram 缺少消息")
        if len(messages) > 24:
            errors.append(f"sequenceDiagram 消息过多: {len(messages)} > 24")
    elif kind == "classDiagram":
        if len(re.findall(r"^\s*class\s+", source, re.MULTILINE)) < 2:
            errors.append("classDiagram 至少需要两个类")
        if not re.search(r"(?:<\|--|\*--|o--|-->|<\.\.|--)", source):
            errors.append("classDiagram 缺少类关系")
    elif kind == "erDiagram":
        if len(re.findall(r"^\s*\S+\s*\{\s*$", source, re.MULTILINE)) < 2:
            errors.append("erDiagram 至少需要两个实体")
        if not re.search(r"(?:\|\||\|o|o\||\}o|o\{|\}\||\|\{)--", source):
            errors.append("erDiagram 缺少关系基数")
    elif kind == "stateDiagram-v2":
        if source.count("[*]") < 2:
            errors.append("stateDiagram-v2 必须包含初始和终止状态")
    elif kind == "gantt":
        if not re.search(r"^\s*title\s+\S+", source, re.MULTILINE):
            errors.append("gantt 缺少 title")
        if not re.search(r"^\s*dateFormat\s+\S+", source, re.MULTILINE):
            errors.append("gantt 缺少 dateFormat")
    elif kind == "gitGraph" and not re.search(r"^\s*commit\b", source, re.MULTILINE):
        errors.append("gitGraph 缺少 commit")
    elif kind == "journey":
        if not re.search(r"^\s*section\s+", source, re.MULTILINE) or not re.search(r":\s*[1-5]\s*:", source):
            errors.append("journey 必须包含 section 和 1-5 评分")
    elif kind == "pie" and len(re.findall(r'^\s*"[^"]+"\s*:\s*\d', source, re.MULTILINE)) < 2:
        errors.append("pie 至少需要两个数据类别")
    elif kind == "mindmap" and not re.search(r"^\s*root\b", source, re.MULTILINE):
        errors.append("mindmap 缺少 root")
    elif kind == "timeline" and len(re.findall(r"^\s*[^:]+\s*:\s*.+", source, re.MULTILINE)) < 2:
        errors.append("timeline 至少需要两个时间节点")
    elif kind == "quadrantChart":
        if "x-axis" not in source or "y-axis" not in source:
            errors.append("quadrantChart 必须定义 x-axis 和 y-axis")
        if not re.search(r":\s*\[\s*0?\.\d+\s*,\s*0?\.\d+\s*\]", source):
            errors.append("quadrantChart 缺少数据点")
    elif kind == "xychart-beta":
        if "x-axis" not in source or "y-axis" not in source or not re.search(r"^\s*(?:bar|line)\s*\[", source, re.MULTILINE):
            errors.append("xychart-beta 必须包含坐标轴和数据序列")
    elif kind == "sankey-beta":
        rows = [line for line in source.splitlines()[1:] if line.strip()]
        if len(rows) < 2:
            errors.append("sankey-beta 至少需要两条流量关系")
        for line in rows:
            try:
                row = next(csv.reader(io.StringIO(line)))
                if len(row) != 3 or float(row[2]) < 0:
                    raise ValueError
            except (ValueError, StopIteration):
                errors.append(f"sankey-beta 非法流量行: {line.strip()}")
                break
    elif kind == "block-beta":
        match = re.search(r"^\s*columns\s+(\d+)", source, re.MULTILINE)
        if not match:
            errors.append("block-beta 缺少 columns")
        elif not 2 <= int(match.group(1)) <= 4:
            errors.append("block-beta columns 应在 2-4 之间")
    return errors


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"无法按 UTF-8 读取: {exc}"], []
    blocks, errors = extract_mermaid_blocks(text)
    if not blocks:
        errors.append("缺少完整 Mermaid fence")
        return errors, blocks
    if len(blocks) != 1:
        errors.append(f"每个示例文件只允许一个主 Mermaid block，当前 {len(blocks)} 个")
    for index, block in enumerate(blocks, 1):
        if not INIT_RE.search(block):
            errors.append(f"block {index}: 缺少有效 init 主题配置")
        source = source_without_init(block)
        kind = diagram_type(source)
        if kind is None:
            errors.append(f"block {index}: 无法识别 Mermaid 图类型")
            continue
        if PLACEHOLDER_RE.search(source):
            errors.append(f"block {index}: 残留占位内容")
        labels = re.findall(r"\[([^\]]+)\]", source)
        if any(len(label.strip()) > 48 for label in labels):
            errors.append(f"block {index}: 节点标签过长")
        errors.extend(f"block {index}: {item}" for item in semantic_errors(kind, source))
    return sorted(set(errors)), blocks


def renderer_command() -> list[str] | None:
    mmdc = shutil.which("mmdc") or shutil.which("mmdc.cmd")
    if mmdc:
        return [mmdc]
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if npx:
        return [npx, "--yes", "@mermaid-js/mermaid-cli@11.16.0"]
    return None


def render_blocks(blocks: list[str]) -> list[str]:
    command = renderer_command()
    if not command:
        return ["未找到 mmdc 或 npx，渲染未验证"]
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for index, block in enumerate(blocks, 1):
            source = root / f"block-{index}.mmd"
            output = root / f"block-{index}.svg"
            source.write_text(block, encoding="utf-8")
            try:
                result = subprocess.run(
                    [*command, "-i", str(source), "-o", str(output)],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=120, check=False,
                )
            except subprocess.TimeoutExpired:
                errors.append(f"block {index}: mmdc 渲染超时")
                continue
            if result.returncode != 0:
                errors.append(f"block {index}: mmdc 渲染失败: {result.stderr.strip()}")
            elif not output.exists() or output.stat().st_size == 0:
                errors.append(f"block {index}: mmdc 未生成有效输出")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--check-coverage", action="store_true")
    parser.add_argument("--require-render", action="store_true")
    args = parser.parse_args()
    if not args.path.exists():
        print(f"错误: 路径不存在: {args.path}")
        return 1
    errors: list[str] = []
    all_blocks: list[str] = []
    files = markdown_files(args.path)
    if args.check_coverage and args.path.is_dir():
        missing = sorted(REQUIRED_EXAMPLES - {path.name for path in files})
        if missing:
            errors.append("缺少示例类型: " + ", ".join(missing))
    for path in files:
        file_errors, blocks = validate_file(path)
        errors.extend(f"{path.name}: {item}" for item in file_errors)
        all_blocks.extend(blocks)
    if args.require_render and all_blocks and not errors:
        errors.extend(render_blocks(all_blocks))
    for item in errors:
        print("错误: " + item)
    if errors:
        return 1
    print(f"Mermaid 校验通过: {len(files)} files, {len(all_blocks)} blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
