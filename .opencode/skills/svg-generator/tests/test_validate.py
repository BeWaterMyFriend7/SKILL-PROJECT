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

VISUAL_V2_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="520" viewBox="0 0 800 520" role="img" aria-labelledby="title desc" font-family="Arial, sans-serif" data-theme="tech-blue" data-layout="mixed-axis" data-dominant-axis="x" data-visual-contract="enterprise-v2" data-modules="focus-node">
<title id="title">智能服务治理架构</title><desc id="desc">验证新版视觉合同。</desc>
<rect width="800" height="520" fill="#F4F7FC"/>
<text data-role="page-title" x="40" y="58" font-size="38" font-weight="700" fill="#1F2937">智能服务治理架构</text>
<rect id="node-a" data-role="node" data-color-role="axis-main" x="40" y="100" width="220" height="120" rx="16" fill="#E9EFF8" stroke="#5B8FF9"/>
<rect id="node-b" data-role="node" data-color-role="axis-cross" data-visual-role="focus" data-module="focus-node" x="290" y="100" width="220" height="120" rx="16" fill="#FDFEFF" stroke="#3B6EDC"/>
<rect id="node-c" data-role="node" data-color-role="side-rail" x="540" y="100" width="220" height="300" rx="16" fill="#E9EFF8" stroke="#2D56B3"/>
<text x="150" y="165" text-anchor="middle" font-size="16" fill="#1F2937">主轴区域</text>
<text x="400" y="165" text-anchor="middle" font-size="16" fill="#1F2937">视觉焦点</text>
<text x="650" y="165" text-anchor="middle" font-size="16" fill="#1F2937">侧栏</text>
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

    def test_visual_contract_requires_color_roles(self):
        source = VISUAL_V2_SVG.replace(' data-color-role="axis-main"', "", 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("data-color-role" in item for item in errors))

    def test_visual_contract_rejects_unknown_dominant_axis(self):
        source = VISUAL_V2_SVG.replace('data-dominant-axis="x"', 'data-dominant-axis="diagonal"', 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("data-dominant-axis" in item for item in errors))

    def test_visual_contract_requires_declared_module_to_exist(self):
        source = VISUAL_V2_SVG.replace(' data-module="focus-node"', "", 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("focus-node" in item and "不存在" in item for item in errors))

    def test_visual_contract_warns_when_page_title_is_too_small(self):
        source = VISUAL_V2_SVG.replace('font-size="38"', 'font-size="26"', 1)
        _, warnings = self.validate(source)
        self.assertTrue(any("页面标题层级不足" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
