from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
SPEC = importlib.util.spec_from_file_location("svg_validator", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


VALID_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="240" viewBox="0 0 400 240" role="img" aria-labelledby="title desc" font-family="Arial, sans-serif">
<title id="title">测试图</title><desc id="desc">验证基础结构。</desc>
<rect width="400" height="240" fill="#F6F8FB"/>
<rect x="24" y="32" width="352" height="176" rx="12" fill="#FFFFFF" stroke="#D8E1EA"/>
<rect id="node-a" data-role="node" x="40" y="70" width="120" height="70" rx="10" fill="#FFFFFF" stroke="#D8E1EA"/>
<rect id="node-b" data-role="node" x="240" y="70" width="120" height="70" rx="10" fill="#FFFFFF" stroke="#D8E1EA"/>
<text x="100" y="112" text-anchor="middle" font-size="14" fill="#172033">节点 A</text>
<text x="300" y="112" text-anchor="middle" font-size="14" fill="#172033">节点 B</text>
</svg>"""


class SvgValidatorTests(unittest.TestCase):
    def validate(self, source: str):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "diagram.svg"
            path.write_text(source, encoding="utf-8")
            return VALIDATOR.validate_svg(path)

    def test_valid_svg_passes(self):
        errors, warnings = self.validate(VALID_SVG)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_requires_title_and_description(self):
        source = VALID_SVG.replace('<title id="title">测试图</title>', "").replace('<desc id="desc">验证基础结构。</desc>', "")
        errors, _ = self.validate(source)
        self.assertTrue(any("title" in item for item in errors))
        self.assertTrue(any("desc" in item for item in errors))

    def test_rejects_missing_reference(self):
        source = VALID_SVG.replace('stroke="#D8E1EA"', 'stroke="url(#missing)"', 1)
        errors, _ = self.validate(source)
        self.assertIn("引用不存在: missing", errors)

    def test_rejects_external_resources(self):
        source = VALID_SVG.replace("</svg>", '<image href="https://example.com/a.png"/></svg>')
        errors, _ = self.validate(source)
        self.assertTrue(any("外部资源" in item or "网络资源" in item for item in errors))

    def test_rejects_icon_font(self):
        source = VALID_SVG.replace("Arial, sans-serif", "Font Awesome 6 Free, sans-serif")
        errors, _ = self.validate(source)
        matches = [item for item in errors if "图标字体" in item]
        self.assertEqual(1, len(matches))

    def test_rejects_symbol_emoji(self):
        source = VALID_SVG.replace("节点 A", "☁️ 节点 A")
        errors, _ = self.validate(source)
        self.assertTrue(any("Emoji" in item for item in errors))

    def test_rejects_unknown_theme(self):
        source = VALID_SVG.replace('role="img"', 'role="img" data-theme="custom"')
        errors, _ = self.validate(source)
        self.assertTrue(any("未知主题键" in item for item in errors))

    def test_rejects_unknown_optional_module(self):
        source = VALID_SVG.replace('data-role="node"', 'data-role="node" data-module="sidebar"', 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("未知附加模块" in item for item in errors))

    def test_warns_for_small_text(self):
        source = VALID_SVG.replace('font-size="14"', 'font-size="9"', 1)
        _, warnings = self.validate(source)
        self.assertTrue(any("字号过小" in item for item in warnings))

    def test_detects_node_overlap(self):
        source = VALID_SVG.replace('x="240" y="70"', 'x="120" y="70"', 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("节点重叠" in item for item in errors))

    def test_requires_node_metadata(self):
        source = VALID_SVG.replace(' data-role="node"', "")
        errors, _ = self.validate(source)
        self.assertTrue(any("data-role=node" in item for item in errors))

    def test_architecture_warns_for_tall_third_level_cards(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "architecture-test.svg"
            path.write_text(VALID_SVG.replace('height="70"', 'height="54"'), encoding="utf-8")
            _, warnings = VALIDATOR.validate_svg(path)
        self.assertTrue(any("三级卡片过高" in item for item in warnings))

    def test_flow_requires_start_and_end(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "flow-linear-test.svg"
            path.write_text(VALID_SVG, encoding="utf-8")
            errors, _ = VALIDATOR.validate_svg(path)
        self.assertTrue(any("开始和结束" in item for item in errors))

    def test_rejects_multiple_gradients(self):
        definitions = '<defs><linearGradient id="a"/><linearGradient id="b"/></defs>'
        source = VALID_SVG.replace('<rect width="400"', definitions + '<rect width="400"')
        errors, _ = self.validate(source)
        self.assertTrue(any("gradient 数量超过" in item for item in errors))

    def test_catalog_matches_target_structure(self):
        errors = VALIDATOR.validate_catalog(Path(__file__).resolve().parents[1])
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
