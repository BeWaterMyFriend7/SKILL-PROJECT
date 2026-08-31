import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "scripts" / "style_map.py"
SPEC = importlib.util.spec_from_file_location("svg_style_map", PATH)
STYLE_MAP = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(STYLE_MAP)
XML_PATH = PATH.parents[2] / "xml-diagram" / "scripts" / "style_map.py"


class StyleMapTests(unittest.TestCase):
    def test_axis_mapping_changes_with_layout_without_changing_theme(self):
        vertical = STYLE_MAP.build_style_map("tech-blue", layout="vertical-stack")
        horizontal = STYLE_MAP.build_style_map("tech-blue", layout="horizontal-flow")

        self.assertEqual(vertical["palette"], horizontal["palette"])
        self.assertEqual("#2AA7C8", vertical["roles"]["axis-cross"]["base"])
        self.assertEqual("#2AA7C8", horizontal["roles"]["axis-main"]["base"])
        self.assertEqual("#3B6EDC", horizontal["roles"]["axis-cross"]["base"])
        self.assertNotEqual(vertical["role-colors"], horizontal["role-colors"])

    def test_tech_blue_recipe_allows_cyan_as_structural_container_color(self):
        result = STYLE_MAP.build_style_map("tech-blue", layout="mixed-axis")
        self.assertEqual("#2AA7C8", result["roles"]["axis-main"]["base"])
        self.assertEqual("role-subtle", result["recipe"]["surface-policy"]["top-band"])
        self.assertIn("data-flow", result["recipe"]["layer-roles"])

    def test_vibrant_exposes_controlled_domain_and_status_colors(self):
        result = STYLE_MAP.build_style_map("vibrant", layout="vertical-stack")
        self.assertEqual("#3B82F6", result["semantic-roles"]["domain-app"]["base"])
        self.assertEqual("#8B5CF6", result["semantic-roles"]["domain-control"]["base"])
        self.assertEqual("#06B6D4", result["semantic-roles"]["domain-network"]["base"])
        self.assertEqual("#22C55E", result["semantic-roles"]["domain-data"]["base"])
        self.assertEqual("#F59E0B", result["semantic-roles"]["status-warning"]["base"])
        self.assertEqual("#EF4444", result["semantic-roles"]["status-error"]["base"])
        self.assertEqual(
            ["axis-main", "axis-cross", "data-flow"],
            result["recipe"]["structure-roles"],
        )

    def test_steady_horizontal_backbone_stays_navy(self):
        result = STYLE_MAP.build_style_map("steady-red-blue", layout="horizontal-flow")
        self.assertEqual("#243B63", result["roles"]["axis-main"]["base"])
        self.assertEqual("#243B63", result["roles"]["connector"]["base"])
        self.assertEqual("#4A90E2", result["roles"]["axis-cross"]["base"])

    def test_fixed_semantics_do_not_change_with_axis_mapping(self):
        vertical = STYLE_MAP.build_style_map("vibrant", layout="vertical-stack")
        horizontal = STYLE_MAP.build_style_map("vibrant", layout="horizontal-flow")

        self.assertEqual(vertical["neutral"], horizontal["neutral"])
        self.assertEqual(vertical["semantic"], horizontal["semantic"])
        self.assertEqual("#EF4444", vertical["semantic"]["error"])

    def test_role_override_is_preserved(self):
        result = STYLE_MAP.build_style_map(
            "mint-green",
            layout="mixed-axis",
            axis_main="#123456",
        )
        self.assertEqual("#123456", result["roles"]["axis-main"]["base"])
        self.assertEqual("user", result["role-sources"]["axis-main"])

    def test_rejects_unknown_layout(self):
        with self.assertRaises(ValueError):
            STYLE_MAP.build_style_map("tech-blue", layout="diagonal-random")

    def test_rejects_unknown_dominant_axis(self):
        with self.assertRaises(ValueError):
            STYLE_MAP.build_style_map("tech-blue", dominant_axis="diagonal")

    def test_all_roles_are_present(self):
        result = STYLE_MAP.build_style_map("steady-red-blue", layout="mixed-axis")
        self.assertEqual(
            {
                "axis-main",
                "axis-cross",
                "side-rail",
                "focus",
                "data-flow",
                "group",
                "connector",
            },
            set(result["roles"]),
        )

    def test_svg_and_drawio_style_contracts_are_equal(self):
        if not XML_PATH.is_file():
            self.skipTest("xml-diagram 未安装在同级目录")
        xml_spec = importlib.util.spec_from_file_location("xml_style_map_parity", XML_PATH)
        xml_style_map = importlib.util.module_from_spec(xml_spec)
        assert xml_spec.loader
        xml_spec.loader.exec_module(xml_style_map)
        for theme in ("tech-blue", "vibrant", "mint-green", "steady-red-blue"):
            for layout in ("vertical-stack", "horizontal-flow", "mixed-axis", "matrix", "network", "timeline"):
                self.assertEqual(
                    STYLE_MAP.build_style_map(theme, layout=layout),
                    xml_style_map.build_style_map(theme, layout=layout),
                    f"{theme}/{layout}",
                )


if __name__ == "__main__":
    unittest.main()
