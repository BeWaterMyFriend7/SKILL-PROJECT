from __future__ import annotations

import os
import json
import hashlib
import struct
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


class ValidateSvgCliTests(unittest.TestCase):
    def test_valid_svg_passes(self) -> None:
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
<title>示例</title><desc>有效 SVG</desc>
<rect id="bg" x="0" y="0" width="600" height="400" fill="#F6F8FB"/>
<rect id="panel" x="50" y="70" width="500" height="260" rx="10" fill="#FFFFFF" stroke="#D8E1EA"/>
<text id="title" x="300" y="120" text-anchor="middle" font-size="26" fill="#172033">稳定示例</text>
<text id="body" x="300" y="180" text-anchor="middle" font-size="12" fill="#475569">正文清晰可读</text>
</svg>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "valid.svg"
            path.write_text(svg, encoding="utf-8")
            result = run_script("validate_svg.py", str(path), "--fail-on-warning")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_small_text_fails_with_warning_gate(self) -> None:
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
<rect x="0" y="0" width="600" height="400" fill="#F6F8FB"/>
<text x="100" y="100" font-size="8" fill="#172033">过小文字</text>
</svg>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "small.svg"
            path.write_text(svg, encoding="utf-8")
            result = run_script("validate_svg.py", str(path), "--fail-on-warning")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("字号", result.stdout)

    def test_normal_eleven_pixel_text_fails(self) -> None:
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400"><title>示例</title><desc>字号门禁</desc><rect width="600" height="400" fill="#F6F8FB"/><text x="100" y="100" font-size="11">普通正文</text></svg>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "normal-11.svg"
            path.write_text(svg, encoding="utf-8")
            result = run_script("validate_svg.py", str(path), "--fail-on-warning")
        self.assertNotEqual(result.returncode, 0)

    def test_auxiliary_eleven_pixel_text_passes_font_gate(self) -> None:
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400"><title>示例</title><desc>辅助字号</desc><rect width="600" height="400" fill="#F6F8FB"/><rect x="50" y="60" width="500" height="260" fill="#FFFFFF"/><text x="100" y="100" font-size="11" data-text-role="auxiliary">辅助标签</text></svg>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aux-11.svg"
            path.write_text(svg, encoding="utf-8")
            result = run_script("validate_svg.py", str(path), "--fail-on-warning")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_local_references_are_complete(self) -> None:
        result = run_script("validate_references.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_evals_define_executable_contracts(self) -> None:
        payload = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(payload["evals"]), 5)
        for item in payload["evals"]:
            self.assertTrue(item.get("template"), item)
            self.assertTrue(item.get("output_file", "").endswith(".svg"), item)
            self.assertGreaterEqual(len(item.get("assertions", [])), 4, item)
            self.assertIn("validate_svg.py", item.get("validator", ""), item)

    def test_skill_folder_is_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "svg-generator"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(copy / "scripts" / "validate_references.py")],
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
        self.assertEqual(manifest["renderer"], {"name": "Google Chrome", "version": "150.0.7871.102"})
        self.assertEqual(len(manifest["snapshots"]), 10)
        for name, expected in manifest["snapshots"].items():
            data = (preview / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected["sha256"], name)
            self.assertEqual(struct.unpack(">II", data[16:24]), (expected["width"], expected["height"]), name)
            source = (preview / expected["source"]).resolve()
            self.assertTrue(source.is_relative_to(ROOT), source)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), expected["source_sha256"], source)

    def test_svg_diagram_plan_rejects_duplicate_ids_and_bad_references(self) -> None:
        plan = {"designSystemVersion": "1.0", "renderer": "svg", "type": "technical_architecture", "theme": "light", "title": "架构", "canvas": {"width": 1200, "height": 760, "margin": 40}, "sections": [{"id": "s", "title": "层"}], "nodes": [{"id": "a", "label": "A"}, {"id": "a", "label": "B"}], "edges": [{"id": "e", "source": "a", "target": "missing"}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_plan.py", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不得重复", result.stdout)
        self.assertIn("引用不存在", result.stdout)


if __name__ == "__main__":
    unittest.main()
