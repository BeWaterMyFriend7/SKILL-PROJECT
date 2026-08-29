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
        self.assertEqual("Tech Blue｜科技蓝（默认）", result["theme-name"])
        self.assertEqual("#3B6EDC", result["colors"]["primary"]["base"])
        self.assertEqual("#F4F7FC", result["neutral"]["canvas"])

    def test_all_theme_anchors(self):
        self.assertEqual(
            {
                "tech-blue": {"name": "Tech Blue｜科技蓝（默认）", "primary": "#3B6EDC", "secondary": "#2D56B3", "tertiary": "#5B8FF9", "accent": "#2AA7C8", "palette": {"background": "#F4F7FC", "container": "#E9EFF8", "card": "#FDFEFF", "main-blue": "#3B6EDC", "deep-blue": "#2D56B3", "medium-blue": "#5B8FF9", "data-cyan": "#2AA7C8", "border": "#C9D7EA"}},
                "vibrant": {"name": "Vibrant ｜活力", "primary": "#3B82F6", "secondary": "#8B5CF6", "tertiary": "#06B6D4", "accent": "#22C55E", "palette": {"blue": "#3B82F6", "purple": "#8B5CF6", "cyan": "#06B6D4", "green": "#22C55E", "orange": "#F59E0B", "red": "#EF4444", "background": "#FAFBFC", "border": "#D1D5DB"}},
                "mint-green": {"name": "Mint green｜清爽绿", "primary": "#2E8B57", "secondary": "#14B8A6", "tertiary": "#2E8B57", "accent": "#14B8A6", "palette": {"background": "#F8FAFC", "container": "#EEF6F4", "card": "#FFFFFF", "mint-green": "#2E8B57", "light-green": "#DDF5E8", "teal-green": "#14B8A6", "light-cyan": "#CCFBF1", "border": "#C7D2D9"}},
                "steady-red-blue": {"name": "Steady Red & Blue｜稳重红蓝", "primary": "#C62828", "secondary": "#243B63", "tertiary": "#4A90E2", "accent": "#C62828", "palette": {"background": "#F6F7FB", "container": "#E9EEF5", "card": "#FFFFFF", "red": "#C62828", "navy": "#243B63", "light-red": "#FBE4E4", "accent-blue": "#4A90E2", "border": "#CAD3DF"}},
            },
            PALETTE.THEMES,
        )

    def test_partial_override_is_preserved(self):
        result = PALETTE.build_palette("tech-blue", primary="#123456")
        self.assertEqual("#123456", result["colors"]["primary"]["base"])
        self.assertEqual("#2D56B3", result["colors"]["secondary"]["base"])

    def test_dark_mode_keeps_geometry_independent_tokens(self):
        light = PALETTE.build_palette("mint-green", "light")
        dark = PALETTE.build_palette("mint-green", "dark")
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
