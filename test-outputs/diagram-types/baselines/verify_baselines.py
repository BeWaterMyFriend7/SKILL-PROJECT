#!/usr/bin/env python3
"""Regenerate, validate, render, and fingerprint the four visual baselines."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
REQUEST_PATH = HERE / "requests.json"
MANIFEST_PATH = HERE / "generation-manifest.json"
REPORT_PATH = HERE / "verification-report.json"
GENERATOR_PATH = HERE / "generate_baselines.py"
SVG_VALIDATOR = REPO / ".opencode" / "skills" / "svg-generator" / "scripts" / "validate.py"
XML_VALIDATOR = REPO / ".opencode" / "skills" / "xml-diagram" / "scripts" / "validate.py"
STYLE_MAP_PATH = REPO / ".opencode" / "skills" / "svg-generator" / "scripts" / "style_map.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> dict[str, object]:
    result = subprocess.run(
        command,
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    record = {
        "command": command,
        "returnCode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"command failed: {' '.join(command)}\n{detail}")
    return record


def import_svg_validator():
    spec = importlib.util.spec_from_file_location("baseline_svg_validator", SVG_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def import_style_map():
    spec = importlib.util.spec_from_file_location("baseline_style_map", STYLE_MAP_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def find_drawio(configured: str | None) -> Path | None:
    local_app_data = os.environ.get("LOCALAPPDATA")
    candidates = [
        Path(configured) if configured else None,
        Path(os.environ["DRAWIO_RENDERER"]) if os.environ.get("DRAWIO_RENDERER") else None,
        Path(r"D:\Program Files\draw.io\draw.io.exe"),
        Path(r"C:\Program Files\draw.io\draw.io.exe"),
        Path(local_app_data) / "Programs" / "draw.io" / "draw.io.exe" if local_app_data else None,
    ]
    for name in ("drawio", "draw.io"):
        resolved = shutil.which(name)
        if resolved:
            candidates.append(Path(resolved))
    return next((candidate for candidate in candidates if candidate and candidate.is_file()), None)


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def render_svg(source: Path, target: Path, browser: Path) -> dict[str, object]:
    validator = import_svg_validator()
    root = validator.ET.parse(source).getroot()
    width = round(validator.number(root.get("width"), 0) or 0)
    height = round(validator.number(root.get("height"), 0) or 0)
    if width <= 0 or height <= 0:
        raise RuntimeError(f"SVG has no valid dimensions: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        profile = Path(temporary) / "profile"
        record = run([
            str(browser),
            "--headless=new",
            "--hide-scrollbars",
            "--disable-gpu",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--user-data-dir={profile}",
            f"--screenshot={target.resolve()}",
            source.resolve().as_uri(),
        ])
    for _ in range(30):
        if target.is_file() and target.stat().st_size > 100:
            break
        time.sleep(0.1)
    if png_size(target) != (width, height):
        raise RuntimeError(f"unexpected SVG render size: {png_size(target)}, expected {(width, height)}")
    record["output"] = str(target.relative_to(HERE)).replace("\\", "/")
    record["dimensions"] = [width, height]
    return record


def render_drawio(source: Path, target: Path, executable: Path) -> dict[str, object]:
    target.parent.mkdir(parents=True, exist_ok=True)
    record = run([
        str(executable),
        "--export",
        "--format",
        "png",
        "--scale",
        "1",
        "--border",
        "0",
        "--output",
        str(target.resolve()),
        str(source.resolve()),
    ])
    for _ in range(50):
        if target.is_file() and target.stat().st_size > 100:
            break
        time.sleep(0.1)
    size = png_size(target)
    if not size:
        raise RuntimeError(f"Draw.io did not create a valid PNG: {target}")
    record["output"] = str(target.relative_to(HERE)).replace("\\", "/")
    record["dimensions"] = list(size)
    return record


def clean_expected_outputs(themes: list[str]) -> list[str]:
    removed: list[str] = []
    for theme in themes:
        for relative in (
            Path("dsl") / f"{theme}.md",
            Path("svg") / f"{theme}.svg",
            Path("xml") / f"{theme}.drawio",
            Path("images") / "svg" / f"{theme}.png",
            Path("images") / "xml" / f"{theme}.png",
        ):
            target = (HERE / relative).resolve()
            if HERE.resolve() not in target.parents:
                raise RuntimeError(f"refusing to clean outside baseline directory: {target}")
            if target.is_file():
                target.unlink()
                removed.append(relative.as_posix())
    if MANIFEST_PATH.is_file():
        MANIFEST_PATH.unlink()
        removed.append(MANIFEST_PATH.name)
    if REPORT_PATH.is_file():
        REPORT_PATH.unlink()
        removed.append(REPORT_PATH.name)
    return removed


def verify_theme_recipe(theme: str, path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    style = import_style_map().build_style_map(theme, layout="mixed-axis", dominant_axis="x")
    tokens = {**style["roles"], **style["semantic-roles"]}
    neutral = style["neutral"]
    roles = {
        item.get("data-color-role")
        for item in root.iter()
        if item.get("data-color-role")
    }
    required_roles = {
        "tech-blue": {"axis-main", "axis-cross", "focus", "data-flow"},
        "vibrant": {"domain-app", "domain-control", "domain-network", "domain-data"},
        "mint-green": {"axis-main", "axis-cross", "focus", "data-flow"},
        "steady-red-blue": {"focus", "side-rail", "axis-cross"},
    }[theme]
    missing = sorted(required_roles - roles)
    if missing:
        raise RuntimeError(f"theme recipe roles missing for {theme}: {missing}")
    source = path.read_text(encoding="utf-8").upper()
    required_colors = {
        "tech-blue": {"#3B6EDC", "#2AA7C8"},
        # Green is verified through the domain-data role; this baseline uses its
        # subtle/border/strong tones rather than painting a large solid green area.
        "vibrant": {"#3B82F6", "#8B5CF6", "#06B6D4"},
        "mint-green": {"#2E8B57", "#14B8A6"},
        "steady-red-blue": {"#C62828", "#243B63", "#4A90E2"},
    }[theme]
    missing_colors = sorted(color for color in required_colors if color not in source)
    if missing_colors:
        raise RuntimeError(f"theme recipe colors missing for {theme}: {missing_colors}")
    boxes = [
        item
        for item in root.iter()
        if item.get("data-role") in {"node", "region"} and item.get("data-color-role")
    ]
    total_area = strong_area = focus_area = status_area = 0.0
    ordinary_card_area = surface_card_area = 0.0
    for item in boxes:
        role = item.get("data-color-role")
        token = tokens[role]
        fill = item.get("fill")
        allowed_fills = {neutral["surface"], neutral["surface-muted"], token["base"], token["soft"], token["subtle"]}
        if fill not in allowed_fills:
            raise RuntimeError(f"unexpected baseline fill for {theme}/{item.get('id')}: {fill}")
        area = float(item.get("width", 0)) * float(item.get("height", 0))
        total_area += area
        strong_area += area if fill == token["base"] else 0
        focus_area += area if item.get("data-visual-role") == "focus" else 0
        status_area += area if role.startswith("status-") else 0
        if item.get("data-role") == "node" and item.get("data-visual-role") != "focus" and not role.startswith("status-"):
            ordinary_card_area += area
            surface_card_area += area if fill in {neutral["surface"], neutral["surface-muted"]} else 0
    metrics = {
        "strongAreaRatio": round(strong_area / total_area, 4),
        "focusAreaRatio": round(focus_area / total_area, 4),
        "statusAreaRatio": round(status_area / total_area, 4),
        "surfaceCardRatio": round(surface_card_area / ordinary_card_area, 4) if ordinary_card_area else 1.0,
    }
    budgets = style["recipe"]["area-budget"]
    for metric, budget_key in (("strongAreaRatio", "strong"), ("focusAreaRatio", "focus"), ("statusAreaRatio", "status")):
        if metrics[metric] > budgets[budget_key]:
            raise RuntimeError(f"{metric} budget exceeded for {theme}: {metrics[metric]} > {budgets[budget_key]}")
    if metrics["surfaceCardRatio"] < 0.70:
        raise RuntimeError(f"white/surface card ratio too low for {theme}: {metrics['surfaceCardRatio']}")
    return {
        "status": "matched",
        "roles": sorted(roles),
        "requiredColors": sorted(required_colors),
        "metrics": metrics,
        "budgets": budgets,
    }


def verify_manifest(themes: list[str]) -> tuple[dict[str, object], list[dict[str, object]]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("generationMode") != "fresh-dsl-v1" or manifest.get("legacyInputFiles") != []:
        raise RuntimeError("manifest does not prove fresh generation")
    if manifest.get("requestSha256") != sha256(REQUEST_PATH):
        raise RuntimeError("request hash does not match manifest")
    artifacts = manifest.get("artifacts", [])
    if [item.get("theme") for item in artifacts] != themes:
        raise RuntimeError("manifest theme order/content does not match request")
    verified: list[dict[str, object]] = []
    for item in artifacts:
        if item.get("generationMode") != "fresh-dsl-v1" or item.get("legacyInputFiles") != []:
            raise RuntimeError(f"theme is not fresh-generated: {item.get('theme')}")
        theme_files: dict[str, object] = {}
        for kind in ("dsl", "svg", "drawio"):
            declared = item[kind]
            path = HERE / declared["path"]
            if not path.is_file() or sha256(path) != declared["sha256"]:
                raise RuntimeError(f"hash mismatch: {declared['path']}")
            content = path.read_text(encoding="utf-8")
            if "fresh-dsl-v1" not in content or item["specHash"] not in content:
                raise RuntimeError(f"fresh-generation marker missing: {declared['path']}")
            if kind == "svg" and content.count('data-role="icon"') < 3:
                raise RuntimeError(f"semantic SVG icons missing: {declared['path']}")
            if kind == "drawio" and (
                content.count('role="icon"') < 3 or content.count("data:image/svg+xml,") < 3
            ):
                raise RuntimeError(f"self-contained Draw.io icons missing: {declared['path']}")
            theme_files[kind] = {"path": declared["path"], "sha256": declared["sha256"]}
        for kind in ("svg", "xml"):
            image = HERE / "images" / kind / f"{item['theme']}.png"
            size = png_size(image)
            if not size:
                raise RuntimeError(f"missing rendered image: {image}")
            theme_files[f"{kind}Png"] = {
                "path": str(image.relative_to(HERE)).replace("\\", "/"),
                "sha256": sha256(image),
                "dimensions": list(size),
            }
        recipe = verify_theme_recipe(item["theme"], HERE / item["svg"]["path"])
        verified.append({"theme": item["theme"], "specHash": item["specHash"], "recipe": recipe, "files": theme_files})
    return manifest, verified


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drawio", help="Path to draw.io executable; otherwise auto-detect or use DRAWIO_RENDERER")
    args = parser.parse_args()
    request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    themes = request["themes"]
    drawio = find_drawio(args.drawio)
    svg_validator = import_svg_validator()
    browser = svg_validator.find_browser()
    if browser is None:
        raise SystemExit("Chrome/Edge not found; set SVG_RENDERER")
    if drawio is None:
        raise SystemExit("draw.io not found; pass --drawio or set DRAWIO_RENDERER")

    started = datetime.now(timezone.utc).isoformat()
    removed = clean_expected_outputs(themes)
    commands = [run([sys.executable, str(GENERATOR_PATH)])]
    for theme in themes:
        svg = HERE / "svg" / f"{theme}.svg"
        drawio_source = HERE / "xml" / f"{theme}.drawio"
        commands.append(run([sys.executable, str(SVG_VALIDATOR), str(svg), "--strict", "--render"]))
        commands.append(run([sys.executable, str(XML_VALIDATOR), str(drawio_source), "--strict"]))
        commands.append(render_svg(svg, HERE / "images" / "svg" / f"{theme}.png", browser))
        commands.append(render_drawio(drawio_source, HERE / "images" / "xml" / f"{theme}.png", drawio))

    manifest, artifacts = verify_manifest(themes)
    report = {
        "schemaVersion": "fresh-generation-verification-v1",
        "status": "passed",
        "startedAtUtc": started,
        "completedAtUtc": datetime.now(timezone.utc).isoformat(),
        "generationMode": manifest["generationMode"],
        "legacyInputFiles": manifest["legacyInputFiles"],
        "cleanedFiles": removed,
        "request": {"path": REQUEST_PATH.name, "sha256": sha256(REQUEST_PATH)},
        "renderers": {"svg": str(browser), "drawio": str(drawio)},
        "commands": commands,
        "artifacts": artifacts,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"full fresh-generation verification passed: {len(themes)} themes, {len(artifacts) * 5} artifacts")
    print(f"report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
