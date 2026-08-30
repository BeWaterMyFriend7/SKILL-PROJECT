import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "scripts" / "style_map.py"
SPEC = importlib.util.spec_from_file_location("svg_style_map", PATH)
STYLE_MAP = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(STYLE_MAP)


class StyleMapTests(unittest.TestCase):
    def test_axis_mapping_changes_with_layout_without_changing_theme(self):
        vertical = STYLE_MAP.build_style_map("tech-blue", layout="vertical-stack")
        horizontal = STYLE_MAP.build_style_map("tech-blue", layout="horizontal-flow")

        self.assertEqual(vertical["palette"], horizontal["palette"])
        self.assertEqual("#5B8FF9", vertical["roles"]["axis-cross"]["base"])
        self.assertEqual("#2AA7C8", horizontal["roles"]["axis-cross"]["base"])
        self.assertNotEqual(vertical["role-colors"], horizontal["role-colors"])

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


if __name__ == "__main__":
    unittest.main()
