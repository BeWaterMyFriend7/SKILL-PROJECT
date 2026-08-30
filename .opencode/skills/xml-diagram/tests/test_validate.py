import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote


PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
SPEC = importlib.util.spec_from_file_location("xml_validator", PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


BASE = """<mxGraphModel grid="0" pageWidth="400" pageHeight="240"><root>
<mxCell id="0"/><mxCell id="1" parent="0"/>
<mxCell id="node" value="节点" vertex="1" parent="1" style="rounded=1;fillColor=#FFFFFF;strokeColor=#D8E1EA;fontColor=#172033;fontSize=14;">
<mxGeometry x="40" y="40" width="120" height="60" as="geometry"/></mxCell>
</root></mxGraphModel>"""

VISUAL_V2_XML = """<mxfile><diagram theme="tech-blue" layout="mixed-axis" dominantAxis="x" visualContract="enterprise-v2" modules="focus-node"><mxGraphModel grid="0" pageWidth="800" pageHeight="520"><root>
<mxCell id="0"/><mxCell id="1" parent="0"/>
<mxCell id="title" value="智能服务治理架构" role="page-title" vertex="1" parent="1" style="text=;fontSize=38;fontStyle=1;fontColor=#1F2937;"><mxGeometry x="40" y="20" width="500" height="52" as="geometry"/></mxCell>
<mxCell id="node-a" value="主轴区域" role="node" colorRole="axis-main" vertex="1" parent="1" style="rounded=1;fillColor=#E9EFF8;strokeColor=#5B8FF9;fontColor=#1F2937;fontSize=16;"><mxGeometry x="40" y="100" width="220" height="120" as="geometry"/></mxCell>
<mxCell id="node-b" value="视觉焦点" role="node" visualRole="focus" colorRole="axis-cross" module="focus-node" vertex="1" parent="1" style="rounded=1;fillColor=#FDFEFF;strokeColor=#3B6EDC;fontColor=#1F2937;fontSize=16;"><mxGeometry x="290" y="100" width="220" height="120" as="geometry"/></mxCell>
<mxCell id="node-c" value="侧栏" role="node" colorRole="side-rail" vertex="1" parent="1" style="rounded=1;fillColor=#E9EFF8;strokeColor=#2D56B3;fontColor=#1F2937;fontSize=16;"><mxGeometry x="540" y="100" width="220" height="300" as="geometry"/></mxCell>
</root></mxGraphModel></diagram></mxfile>"""


class XmlValidatorTests(unittest.TestCase):
    def validate(self, source: str):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "diagram.drawio"
            path.write_text(source, encoding="utf-8")
            return VALIDATOR.validate_file(path)

    def test_rejects_external_icon_url(self):
        source = BASE.replace("rounded=1;", "shape=image;image=https://example.com/icon.svg;")
        errors, _ = self.validate(source)
        self.assertTrue(any("内嵌 SVG" in item for item in errors))

    def test_rejects_relative_icon_path(self):
        source = BASE.replace("rounded=1;", "shape=image;image=icons/cloud.svg;")
        errors, _ = self.validate(source)
        self.assertTrue(any("相对" in item for item in errors))

    def embedded_svg(self, payload: str) -> str:
        uri = "data:image/svg+xml," + quote(payload, safe="")
        return BASE.replace("rounded=1;", f"shape=image;image={uri};")

    def test_accepts_valid_embedded_svg(self):
        source = self.embedded_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M2 12h20"/></svg>')
        errors, _ = self.validate(source)
        self.assertFalse(any("内嵌 SVG" in item for item in errors))

    def test_rejects_malformed_embedded_svg(self):
        errors, _ = self.validate(self.embedded_svg("<svg><path></svg>"))
        self.assertTrue(any("无法解析" in item for item in errors))

    def test_rejects_remote_href_inside_embedded_svg(self):
        source = self.embedded_svg('<svg xmlns="http://www.w3.org/2000/svg"><use href="https://example.com/icons.svg#cloud"/></svg>')
        errors, _ = self.validate(source)
        self.assertTrue(any("远程资源" in item or "href" in item for item in errors))

    def test_rejects_symbol_emoji(self):
        errors, _ = self.validate(BASE.replace('value="节点"', 'value="☁️ 节点"'))
        self.assertTrue(any("Emoji" in item for item in errors))

    def test_rejects_unknown_theme(self):
        source = f'<mxfile><diagram theme="custom">{BASE}</diagram></mxfile>'
        errors, _ = self.validate(source)
        self.assertTrue(any("未知主题键" in item for item in errors))

    def test_rejects_unknown_optional_module(self):
        errors, _ = self.validate(BASE.replace('id="node"', 'id="node" module="sidebar"'))
        self.assertTrue(any("未知附加模块" in item for item in errors))

    def test_rejects_icon_font(self):
        source = BASE.replace("fontSize=14;", "fontSize=14;fontFamily=Font Awesome 6 Free;")
        errors, _ = self.validate(source)
        self.assertTrue(any("图标字体" in item for item in errors))

    def test_catalog_has_theme_support_files(self):
        errors = VALIDATOR.validate_catalog(Path(__file__).resolve().parents[1])
        self.assertEqual([], errors)

    def test_visual_contract_requires_color_roles(self):
        source = VISUAL_V2_XML.replace(' colorRole="axis-main"', "", 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("colorRole" in item for item in errors))

    def test_visual_contract_rejects_unknown_dominant_axis(self):
        source = VISUAL_V2_XML.replace('dominantAxis="x"', 'dominantAxis="diagonal"', 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("dominantAxis" in item for item in errors))

    def test_visual_contract_requires_declared_module_to_exist(self):
        source = VISUAL_V2_XML.replace(' module="focus-node"', "", 1)
        errors, _ = self.validate(source)
        self.assertTrue(any("focus-node" in item and "不存在" in item for item in errors))

    def test_visual_contract_warns_when_page_title_is_too_small(self):
        source = VISUAL_V2_XML.replace('fontSize=38', 'fontSize=26', 1)
        _, warnings = self.validate(source)
        self.assertTrue(any("页面标题层级不足" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
