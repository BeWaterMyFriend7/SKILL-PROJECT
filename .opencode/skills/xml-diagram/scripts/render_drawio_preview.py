#!/usr/bin/env python3
"""Export Draw.io PNG previews with the pinned official Desktop CLI."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


PINNED_VERSION = "29.6.1"
WINDOWS_CANDIDATES = (
    Path(r"D:\Program Files\draw.io\draw.io.exe"),
    Path(r"C:\Program Files\draw.io\draw.io.exe"),
    Path(r"C:\Program Files (x86)\draw.io\draw.io.exe"),
)


def find_cli() -> Path | None:
    configured = os.environ.get("DRAWIO_CLI")
    if configured and Path(configured).is_file():
        return Path(configured)
    discovered = shutil.which("draw.io") or shutil.which("drawio")
    if discovered:
        return Path(discovered)
    return next((path for path in WINDOWS_CANDIDATES if path.is_file()), None)


def cli_version(path: Path) -> str:
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


def export(drawio: Path, output: Path, scale: float) -> tuple[bool, str]:
    cli = find_cli()
    if cli is None:
        return False, "未找到官方 Draw.io Desktop CLI；可通过 DRAWIO_CLI 指定"
    version = cli_version(cli)
    if not version.startswith(PINNED_VERSION):
        return False, f"Draw.io 版本 {version or 'unknown'}，要求 {PINNED_VERSION}"
    output.parent.mkdir(parents=True, exist_ok=True)
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    result = subprocess.run(
        [str(cli), "--export", "--format", "png", "--scale", str(scale), "--border", "0", "--output", str(output.resolve()), str(drawio.resolve())],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=flags,
        check=False,
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or f"export exit {result.returncode}"
    if not output.exists() or output.stat().st_size < 1000:
        return False, "官方导出未生成有效 PNG"
    return True, f"draw.io {version} scale={scale:g}"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("drawio", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--scale", type=float, choices=(1.0, 0.25), default=1.0)
    args = parser.parse_args()
    ok, message = export(args.drawio, args.output, args.scale)
    print(("官方导出通过: " if ok else "官方导出失败: ") + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
