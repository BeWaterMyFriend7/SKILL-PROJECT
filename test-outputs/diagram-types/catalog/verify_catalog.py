#!/usr/bin/env python3
"""Run the fresh 19-type generation, semantic-pair, validation, and render pipeline."""

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
GENERATOR_PATH = HERE / "generate_catalog.py"
SVG_VALIDATOR = REPO / ".opencode/skills/svg-generator/scripts/validate.py"
XML_VALIDATOR = REPO / ".opencode/skills/xml-diagram/scripts/validate.py"
SVG_SKILL = REPO / ".opencode/skills/svg-generator"
XML_SKILL = REPO / ".opencode/skills/xml-diagram"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report_arg(value: str) -> str:
    """Remove machine-specific absolute and temporary paths from the saved report."""
    text = str(value)
    if text == sys.executable:
        return "python"
    if text.startswith("--user-data-dir="):
        return "--user-data-dir=<temporary-profile>"
    repo_native = str(REPO.resolve())
    text = text.replace(repo_native, ".").replace(repo_native.replace("\\", "/"), ".")
    if Path(text).suffix.lower() == ".exe" and Path(text).is_absolute():
        return Path(text).name
    return text


def run(command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    record = {"command": [report_arg(value) for value in command], "returnCode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"command failed: {' '.join(command)}\n{detail}")
    return record


def load_svg_validator():
    spec = importlib.util.spec_from_file_location("catalog_svg_validator", SVG_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def find_drawio(configured: str | None) -> Path | None:
    local_app_data = os.environ.get("LOCALAPPDATA")
    candidates = [
        Path(configured) if configured else None,
        Path(os.environ["DRAWIO_RENDERER"]) if os.environ.get("DRAWIO_RENDERER") else None,
        Path(r"D:\Program Files\draw.io\draw.io.exe"),
        Path(r"C:\Program Files\draw.io\draw.io.exe"),
        Path(local_app_data) / "Programs/draw.io/draw.io.exe" if local_app_data else None,
    ]
    for name in ("drawio", "draw.io"):
        resolved = shutil.which(name)
        if resolved:
            candidates.append(Path(resolved))
    return next((item for item in candidates if item and item.is_file()), None)


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def render_svg(source: Path, target: Path, browser: Path) -> dict[str, object]:
    validator = load_svg_validator()
    root = ET.parse(source).getroot()
    width = round(validator.number(root.get("width"), 0) or 0)
    height = round(validator.number(root.get("height"), 0) or 0)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        profile = Path(temporary) / "profile"
        record = run([str(browser), "--headless=new", "--hide-scrollbars", "--disable-gpu", "--force-device-scale-factor=1", f"--window-size={width},{height}", f"--user-data-dir={profile}", f"--screenshot={target.resolve()}", source.resolve().as_uri()])
    for _ in range(30):
        if target.is_file() and target.stat().st_size > 100:
            break
        time.sleep(0.1)
    if png_size(target) != (width, height):
        raise RuntimeError(f"unexpected SVG render size for {source.name}: {png_size(target)}")
    record.update({"output": str(target.relative_to(REPO)).replace("\\", "/"), "dimensions": [width, height]})
    return record


def render_drawio(source: Path, target: Path, executable: Path) -> dict[str, object]:
    target.parent.mkdir(parents=True, exist_ok=True)
    record = run([str(executable), "--export", "--format", "png", "--scale", "1", "--border", "0", "--output", str(target.resolve()), str(source.resolve())])
    for _ in range(50):
        if target.is_file() and target.stat().st_size > 100:
            break
        time.sleep(0.1)
    size = png_size(target)
    if not size:
        raise RuntimeError(f"Draw.io did not create a valid PNG: {target}")
    record.update({"output": str(target.relative_to(REPO)).replace("\\", "/"), "dimensions": list(size)})
    return record


def clean_images(items: list[dict[str, object]]) -> list[str]:
    removed = []
    roots = [HERE / "images/svg", HERE / "images/xml", REPO / "test-outputs/diagram-types/svg", REPO / "test-outputs/diagram-types/xml", REPO / "docs/svg-generator/images", REPO / "docs/xml-diagram/images"]
    for root in roots:
        root.mkdir(parents=True, exist_ok=True)
        resolved = root.resolve()
        if REPO.resolve() not in resolved.parents:
            raise RuntimeError(f"refusing to clean outside repository: {resolved}")
        for path in root.glob("*.png"):
            path.unlink()
            removed.append(str(path.relative_to(REPO)).replace("\\", "/"))
    if REPORT_PATH.is_file():
        REPORT_PATH.unlink()
        removed.append(str(REPORT_PATH.relative_to(REPO)).replace("\\", "/"))
    return removed


def svg_semantics(path: Path) -> tuple[dict[str, tuple[object, ...]], dict[str, tuple[object, ...]]]:
    root = ET.parse(path).getroot()
    boxes, relations = {}, {}
    for item in root.iter():
        item_id = item.get("id")
        role = item.get("data-role")
        if not item_id or not role:
            continue
        if role in {"node", "region"}:
            boxes[item_id] = (role, item.get("data-color-role"), item.get("data-visual-role"), item.get("data-module"), float(item.get("x", 0)), float(item.get("y", 0)), float(item.get("width", 0)), float(item.get("height", 0)))
        elif role in {"edge", "lifeline", "icon"}:
            relations[item_id] = (role, item.get("data-color-role"))
    return boxes, relations


def drawio_semantics(path: Path) -> tuple[dict[str, tuple[object, ...]], dict[str, tuple[object, ...]]]:
    root = ET.parse(path).getroot()
    boxes, relations = {}, {}
    for item in root.findall(".//mxCell"):
        item_id, role = item.get("id"), item.get("role")
        if not item_id or not role:
            continue
        if role in {"node", "region"}:
            geometry = item.find("mxGeometry")
            boxes[item_id] = (role, item.get("colorRole"), item.get("visualRole"), item.get("module"), float(geometry.get("x", 0)), float(geometry.get("y", 0)), float(geometry.get("width", 0)), float(geometry.get("height", 0)))
        elif role in {"edge", "lifeline", "icon"}:
            relations[item_id] = (role, item.get("colorRole"))
    return boxes, relations


def verify_pair(svg: Path, drawio: Path) -> dict[str, object]:
    svg_boxes, svg_relations = svg_semantics(svg)
    xml_boxes, xml_relations = drawio_semantics(drawio)
    if svg_boxes != xml_boxes:
        missing_svg = sorted(set(xml_boxes) - set(svg_boxes))
        missing_xml = sorted(set(svg_boxes) - set(xml_boxes))
        mismatched = sorted(key for key in set(svg_boxes) & set(xml_boxes) if svg_boxes[key] != xml_boxes[key])
        raise RuntimeError(f"box semantic mismatch {svg.name}: missingSvg={missing_svg}, missingXml={missing_xml}, mismatched={mismatched}")
    if svg_relations != xml_relations:
        raise RuntimeError(f"edge/icon semantic mismatch {svg.name}")
    return {"boxes": len(svg_boxes), "relationsAndIcons": len(svg_relations), "status": "matched"}


def verify_sources(items: list[dict[str, object]]) -> list[dict[str, object]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("generationMode") != "fresh-catalog-v1" or manifest.get("legacyInputFiles") != []:
        raise RuntimeError("manifest does not prove fresh catalog generation")
    if manifest.get("requestSha256") != sha256(REQUEST_PATH):
        raise RuntimeError("request hash mismatch")
    artifacts = manifest.get("artifacts", [])
    if [item["id"] for item in artifacts] != [item["id"] for item in items]:
        raise RuntimeError("manifest catalog order/content mismatch")
    verified = []
    for artifact in artifacts:
        if artifact.get("legacyInputFiles") != []:
            raise RuntimeError(f"legacy input declared for {artifact['id']}")
        files = {}
        for kind in ("dsl", "svg", "drawio"):
            declared = artifact[kind]
            path = HERE / declared["path"]
            if not path.is_file() or sha256(path) != declared["sha256"]:
                raise RuntimeError(f"source hash mismatch: {declared['path']}")
            text = path.read_text(encoding="utf-8")
            if "fresh-catalog-v1" not in text or artifact["specHash"] not in text:
                raise RuntimeError(f"fresh marker/spec hash missing: {declared['path']}")
            files[kind] = {"path": declared["path"], "sha256": declared["sha256"]}
        pair = verify_pair(HERE / artifact["svg"]["path"], HERE / artifact["drawio"]["path"])
        verified.append({"id": artifact["id"], "specHash": artifact["specHash"], "pair": pair, "files": files})
    return verified


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drawio", help="Path to draw.io executable; otherwise auto-detect or use DRAWIO_RENDERER")
    args = parser.parse_args()
    request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    items = request["items"]
    validator = load_svg_validator()
    browser, drawio = validator.find_browser(), find_drawio(args.drawio)
    if browser is None:
        raise SystemExit("Chrome/Edge not found; set SVG_RENDERER")
    if drawio is None:
        raise SystemExit("draw.io not found; pass --drawio or set DRAWIO_RENDERER")
    started = datetime.now(timezone.utc).isoformat()
    removed_images = clean_images(items)
    commands = [run([sys.executable, str(GENERATOR_PATH)])]
    commands.append(run([sys.executable, str(SVG_VALIDATOR), str(SVG_SKILL), "--strict"]))
    commands.append(run([sys.executable, str(XML_VALIDATOR), str(XML_SKILL), "--strict"]))
    verified = verify_sources(items)
    image_records = []
    manifest_by_id = {item["id"]: item for item in json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["artifacts"]}
    for spec in items:
        artifact = manifest_by_id[spec["id"]]
        name = f"{spec['id']}-{spec['theme']}-light-enterprise.png"
        svg_source, xml_source = HERE / artifact["svg"]["path"], HERE / artifact["drawio"]["path"]
        svg_output, xml_output = REPO / "test-outputs/diagram-types/svg" / name, REPO / "test-outputs/diagram-types/xml" / name
        commands.append(render_svg(svg_source, svg_output, browser))
        commands.append(render_drawio(xml_source, xml_output, drawio))
        copies = [HERE / "images/svg" / name, HERE / "images/xml" / name, REPO / "docs/svg-generator/images" / name, REPO / "docs/xml-diagram/images" / name]
        for target, source in ((copies[0], svg_output), (copies[1], xml_output), (copies[2], svg_output), (copies[3], xml_output)):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        image_records.append({"id":spec["id"],"svg":{"path":str(svg_output.relative_to(REPO)).replace("\\","/"),"sha256":sha256(svg_output),"dimensions":list(png_size(svg_output))},"drawio":{"path":str(xml_output.relative_to(REPO)).replace("\\","/"),"sha256":sha256(xml_output),"dimensions":list(png_size(xml_output))}})
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    report = {"schemaVersion":"fresh-catalog-verification-v1","status":"passed","startedAtUtc":started,"completedAtUtc":datetime.now(timezone.utc).isoformat(),"generationMode":manifest["generationMode"],"legacyInputFiles":manifest["legacyInputFiles"],"removedSourceTargets":manifest["removedTargets"],"removedImageTargets":removed_images,"request":{"path":"requests.json","sha256":sha256(REQUEST_PATH)},"renderers":{"svg":browser.name,"drawio":drawio.name},"commands":commands,"semanticPairs":verified,"images":image_records}
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"full fresh-catalog verification passed: {len(items)} types, {len(items) * 2} semantic sources, {len(items) * 2} rendered images")
    print(f"report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
