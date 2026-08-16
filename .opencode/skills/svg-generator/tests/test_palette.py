import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "scripts" / "palette.py"
SPEC = importlib.util.spec_from_file_location("svg_palette", PATH)
PALETTE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(PALETTE)


class PaletteTests(unittest.TestCase):
    def test_default_theme(self):
        result = PALETTE.build_palette()
        self.assertEqual("tech-blue", result["theme"])
        self.assertEqual("科技蓝", result["theme-name"])
        self.assertEqual("#2E69E1", result["colors"]["primary"]["base"])

    def test_all_theme_anchors(self):
        self.assertEqual(
            {
                "tech-blue": {"name": "科技蓝", "primary": "#2E69E1", "secondary": "#1A388D", "tertiary": "#819FDE", "accent": "#1A388D"},
                "vibrant": {"name": "活力多彩", "primary": "#1B9CDE", "secondary": "#A039B9", "tertiary": "#39A95B", "accent": "#FE9022"},
                "focused": {"name": "稳健聚焦", "primary": "#1F5CD7", "secondary": "#12939D", "tertiary": "#4B9654", "accent": "#FF6B1A"},
            },
            PALETTE.THEMES,
        )

    def test_partial_override_is_preserved(self):
        result = PALETTE.build_palette("tech-blue", primary="#123456")
        self.assertEqual("#123456", result["colors"]["primary"]["base"])
        self.assertEqual("#1A388D", result["colors"]["secondary"]["base"])

    def test_dark_mode_keeps_geometry_independent_tokens(self):
        light = PALETTE.build_palette("focused", "light")
        dark = PALETTE.build_palette("focused", "dark")
        self.assertEqual(light["colors"]["accent"]["base"], dark["colors"]["accent"]["base"])
        self.assertNotEqual(light["neutral"]["canvas"], dark["neutral"]["canvas"])

    def test_invalid_color_is_rejected(self):
        with self.assertRaises(ValueError):
            PALETTE.build_palette(primary="blue")

    def test_custom_color_foreground_meets_normal_text_contrast(self):
        result = PALETTE.build_palette(primary="#777777")
        color = result["colors"]["primary"]
        self.assertGreaterEqual(PALETTE.contrast(color["base"], color["foreground"]), 4.5)

    def test_light_white_override_keeps_structural_tokens_visible(self):
        result = PALETTE.build_palette(primary="#FFFFFF")
        color = result["colors"]["primary"]
        self.assertEqual("#FFFFFF", color["base"])
        self.assertGreaterEqual(PALETTE.contrast(color["soft"], result["neutral"]["canvas"]), 1.12)
        self.assertGreaterEqual(PALETTE.contrast(color["border"], result["neutral"]["surface"]), 1.5)

    def test_dark_black_override_keeps_structural_tokens_visible(self):
        result = PALETTE.build_palette("tech-blue", "dark", primary="#000000")
        color = result["colors"]["primary"]
        self.assertEqual("#000000", color["base"])
        self.assertGreaterEqual(PALETTE.contrast(color["soft"], result["neutral"]["canvas"]), 1.12)
        self.assertGreaterEqual(PALETTE.contrast(color["border"], result["neutral"]["surface"]), 1.5)

    def test_theme_selection_contract_is_documented(self):
        source = (PATH.parents[1] / "references" / "theme-tokens.md").read_text(encoding="utf-8")
        for phrase in ("只询问一次", "不再追问", "tech-blue/light"):
            self.assertIn(phrase, source)


if __name__ == "__main__":
    unittest.main()
