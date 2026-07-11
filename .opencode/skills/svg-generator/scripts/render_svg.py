#!/usr/bin/env python3
"""Render an SVG through a local Chromium browser for deterministic visual QA."""

from __future__ import annotations

import argparse
import html
import os
import struct
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path


WINDOWS_BROWSERS = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
)
PINNED_RENDERER = "Google Chrome"
PINNED_VERSION = "150.0.7871.102"


def find_browser() -> Path | None:
    configured = os.environ.get("SVG_RENDERER")
    if configured and Path(configured).is_file():
        return Path(configured)
    return next((path for path in WINDOWS_BROWSERS if path.exists()), None)


def browser_version(path: Path) -> str:
    if os.name == "nt":
        escaped = str(path).replace("'", "''")
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"(Get-Item -LiteralPath '{escaped}').VersionInfo.ProductVersion"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return result.stdout.strip()
    result = subprocess.run([str(path), "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    return result.stdout.strip() or result.stderr.strip()


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:24]
    except OSError:
        return None
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def svg_size(path: Path) -> tuple[int, int] | None:
    try:
        root = ET.parse(path).getroot()
        width = round(float(root.attrib["width"].removesuffix("px")))
        height = round(float(root.attrib["height"].removesuffix("px")))
    except (OSError, ET.ParseError, KeyError, ValueError):
        return None
    return (width, height) if width > 0 and height > 0 else None


def render(svg: Path, output: Path, scale: float = 1.0) -> tuple[bool, str]:
    browser = find_browser()
    if browser is None:
        return False, "未找到固定 Google Chrome；可通过 SVG_RENDERER 指定"
    version = browser_version(browser)
    if version != PINNED_VERSION:
        return False, f"{PINNED_RENDERER} 版本 {version or 'unknown'}，要求 {PINNED_VERSION}"
    native_size = svg_size(svg)
    if native_size is None:
        return False, "SVG 缺少可渲染的 width/height"
    width = max(1, round(native_size[0] * scale))
    height = max(1, round(native_size[1] * scale))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        profile = root / "profile"
        wrapper = root / "render.html"
        wrapper.write_text(
            "<!doctype html><meta charset='utf-8'><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#F6F8FB}img{display:block;width:100%;height:100%;object-fit:fill}</style>"
            f"<img src='{html.escape(svg.resolve().as_uri(), quote=True)}'>",
            encoding="utf-8",
        )
        command = [
            str(browser), "--headless=new", "--hide-scrollbars",
            "--default-background-color=FFFFFFFF", f"--window-size={width},{height}",
            f"--user-data-dir={profile}", f"--screenshot={output.resolve()}", wrapper.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        for _ in range(20):
            if output.exists() and output.stat().st_size > 100:
                break
            time.sleep(0.1)
    size = png_size(output)
    if result.returncode != 0:
        return False, result.stderr.strip() or f"renderer exit {result.returncode}"
    if size != (width, height):
        return False, f"PNG 尺寸异常: {size}, 期望 {(width, height)}"
    return True, f"{PINNED_RENDERER} {version} {width}x{height}"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--scale", type=float, choices=(1.0, 0.25), default=1.0)
    args = parser.parse_args()
    ok, message = render(args.svg, args.output, args.scale)
    print(("渲染通过: " if ok else "渲染失败: ") + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
