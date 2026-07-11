#!/usr/bin/env python3
"""Validate Mermaid Markdown fences, local coverage, and optional renderer availability."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FENCE_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
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


def markdown_files(path: Path) -> list[Path]:
    return sorted(path.rglob("*.md")) if path.is_dir() else [path]


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    blocks: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"无法按 UTF-8 读取: {exc}"], blocks
    blocks = FENCE_RE.findall(text)
    if not blocks:
        return ["缺少 Mermaid fence"], blocks
    for index, block in enumerate(blocks, 1):
        if "%%{init:" not in block:
            errors.append(f"block {index}: 缺少 init 主题配置")
        source = re.sub(r"^\s*%%\{init:.*?\}%%\s*", "", block, count=1, flags=re.DOTALL)
        if not TYPE_RE.search(source):
            errors.append(f"block {index}: 无法识别 Mermaid 图类型")
        labels = re.findall(r"\[([^\]]+)\]", source)
        if any(len(label.strip()) > 48 for label in labels):
            errors.append(f"block {index}: 节点标签过长")
    return errors, blocks


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
        return ["未找到 mmdc，渲染未验证"]
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for index, block in enumerate(blocks, 1):
            source = root / f"block-{index}.mmd"
            output = root / f"block-{index}.svg"
            source.write_text(block, encoding="utf-8")
            result = subprocess.run([*command, "-i", str(source), "-o", str(output)], capture_output=True, text=True, encoding="utf-8")
            if result.returncode != 0:
                errors.append(f"block {index}: mmdc 渲染失败: {result.stderr.strip()}")
            elif not output.exists() or output.stat().st_size == 0:
                errors.append(f"block {index}: mmdc 未生成有效输出")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--check-coverage", action="store_true")
    parser.add_argument("--require-render", action="store_true")
    args = parser.parse_args()
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
    if args.require_render and all_blocks:
        errors.extend(render_blocks(all_blocks))
    for item in errors:
        print("错误: " + item)
    if errors:
        return 1
    print(f"Mermaid 校验通过: {len(files)} files, {len(all_blocks)} blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
