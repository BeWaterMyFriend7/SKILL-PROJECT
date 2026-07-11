from __future__ import annotations

import json
import hashlib
import struct
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "scripts" / name), *args],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def valid_plan() -> dict[str, object]:
    return {
        "designSystemVersion": "1.0",
        "renderer": "drawio",
        "type": "technical_architecture",
        "theme": "light",
        "template": "templates/architecture/technical-layered.drawio",
        "title": "技术架构图",
        "canvas": {"width": 1200, "height": 800, "margin": 40},
        "sections": [{"id": "core", "title": "核心系统"}],
        "nodes": [{"id": "gateway", "label": "接入网关"}, {"id": "service", "label": "核心服务"}],
        "edges": [{"id": "e1", "source": "gateway", "target": "service"}],
    }


class ValidatePlanCliTests(unittest.TestCase):
    def test_valid_plan_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(valid_plan(), ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_wrong_renderer_fails(self) -> None:
        plan = valid_plan()
        plan["renderer"] = "svg"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("renderer", result.stdout)

    def test_empty_architecture_plan_fails(self) -> None:
        plan = valid_plan()
        plan["sections"] = []
        plan["nodes"] = []
        plan["edges"] = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不得为空", result.stdout)

    def test_duplicate_node_ids_fail(self) -> None:
        plan = valid_plan()
        plan["nodes"] = [{"id": "same", "label": "A"}, {"id": "same", "label": "B"}]
        plan["edges"] = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不得重复", result.stdout)

    def test_invalid_nested_canvas_margin_fails(self) -> None:
        plan = valid_plan()
        plan["canvas"] = {"width": 1200, "height": 800, "margin": 8}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("canvas.margin", result.stdout)

    def test_empty_title_fails(self) -> None:
        plan = valid_plan()
        plan["title"] = ""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("title", result.stdout)

    def test_drawio_normal_eleven_pixel_text_fails(self) -> None:
        xml = """<mxfile><diagram><mxGraphModel pageWidth="600" pageHeight="400"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="bg" style="fillColor=#FFFFFF;strokeColor=none;" vertex="1" parent="1"><mxGeometry x="0" y="0" width="600" height="400" as="geometry"/></mxCell><mxCell id="text" value="正文" style="text;fillColor=none;strokeColor=none;fontColor=#172033;fontSize=11;" vertex="1" parent="1"><mxGeometry x="50" y="80" width="100" height="30" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "字号-light-示例.drawio"
            path.write_text(xml, encoding="utf-8")
            result = run_script("validate_drawio.py", str(path), "--fail-on-warning")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("字号", result.stdout)

    def test_text_only_cell_uses_effective_background_for_contrast(self) -> None:
        xml = """<mxfile><diagram><mxGraphModel pageWidth="600" pageHeight="400" background="#FFFFFF"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="text" value="不可见正文" style="text;fillColor=none;strokeColor=none;fontColor=#FFFFFF;fontSize=12;" vertex="1" parent="1"><mxGeometry x="50" y="80" width="120" height="30" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "contrast.drawio"
            path.write_text(xml, encoding="utf-8")
            result = run_script("check_contrast.py", str(path), "--fail-on-warning")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("对比度", result.stdout)

    def test_text_only_cell_uses_containing_sibling_background(self) -> None:
        xml = """<mxfile><diagram><mxGraphModel pageWidth="600" pageHeight="400" background="#FFFFFF"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="card" value="" style="fillColor=#172033;strokeColor=#334155;" vertex="1" parent="1"><mxGeometry x="40" y="60" width="220" height="120" as="geometry"/></mxCell><mxCell id="text" value="黑底黑字" style="text;fillColor=none;strokeColor=none;fontColor=#172033;fontSize=12;" vertex="1" parent="1"><mxGeometry x="70" y="100" width="120" height="30" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sibling-contrast.drawio"
            path.write_text(xml, encoding="utf-8")
            result = run_script("check_contrast.py", str(path), "--fail-on-warning")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("#172033", result.stdout)

    def test_catalog_has_no_cross_intent_template_duplicates(self) -> None:
        result = run_script("validate_catalog.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_folder_is_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "xml-diagram"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(copy / "scripts" / "validate_catalog.py")],
                cwd=copy,
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_five_architecture_types_have_full_and_thumbnail_snapshots(self) -> None:
        preview = ROOT / "examples" / "previews"
        manifest = json.loads((preview / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["renderer"], {"name": "draw.io Desktop", "version": "29.6.1"})
        self.assertEqual(len(manifest["snapshots"]), 10)
        for name, expected in manifest["snapshots"].items():
            data = (preview / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected["sha256"], name)
            self.assertEqual(struct.unpack(">II", data[16:24]), (expected["width"], expected["height"]), name)
            source = (preview / expected["source"]).resolve()
            self.assertTrue(source.is_relative_to(ROOT), source)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), expected["source_sha256"], source)


if __name__ == "__main__":
    unittest.main()
