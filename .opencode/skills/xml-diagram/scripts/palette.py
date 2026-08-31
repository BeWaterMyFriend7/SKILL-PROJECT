#!/usr/bin/env python3
"""Generate deterministic color tokens for diagram themes."""

from __future__ import annotations

import argparse
import json
import re


THEMES = {
    "tech-blue": {
        "name": "Tech Blue｜科技蓝（默认）",
        "primary": "#3B6EDC",
        "secondary": "#2D56B3",
        "tertiary": "#5B8FF9",
        "accent": "#2AA7C8",
        "palette": {
            "background": "#F4F7FC",
            "container": "#E9EFF8",
            "card": "#FDFEFF",
            "main-blue": "#3B6EDC",
            "deep-blue": "#2D56B3",
            "medium-blue": "#5B8FF9",
            "data-cyan": "#2AA7C8",
            "border": "#C9D7EA",
        },
    },
    "vibrant": {
        "name": "Vibrant ｜活力",
        "primary": "#3B82F6",
        "secondary": "#8B5CF6",
        "tertiary": "#06B6D4",
        "accent": "#22C55E",
        "palette": {
            "blue": "#3B82F6",
            "purple": "#8B5CF6",
            "cyan": "#06B6D4",
            "green": "#22C55E",
            "orange": "#F59E0B",
            "red": "#EF4444",
            "background": "#FAFBFC",
            "border": "#D1D5DB",
        },
    },
    "mint-green": {
        "name": "Mint green｜清爽绿",
        "primary": "#2E8B57",
        "secondary": "#14B8A6",
        "tertiary": "#2E8B57",
        "accent": "#14B8A6",
        "palette": {
            "background": "#F8FAFC",
            "container": "#EEF6F4",
            "card": "#FFFFFF",
            "mint-green": "#2E8B57",
            "light-green": "#DDF5E8",
            "teal-green": "#14B8A6",
            "light-cyan": "#CCFBF1",
            "border": "#C7D2D9",
        },
    },
    "steady-red-blue": {
        "name": "Steady Red & Blue｜稳重红蓝",
        "primary": "#C62828",
        "secondary": "#243B63",
        "tertiary": "#4A90E2",
        "accent": "#C62828",
        "palette": {
            "background": "#F6F7FB",
            "container": "#E9EEF5",
            "card": "#FFFFFF",
            "red": "#C62828",
            "navy": "#243B63",
            "light-red": "#FBE4E4",
            "accent-blue": "#4A90E2",
            "border": "#CAD3DF",
        },
    },
}

# Theme anchors stay exactly as specified by the user.  These ramps describe how
# each anchor behaves on enterprise diagrams; they intentionally are not derived
# by one universal "mix with white" formula.
LIGHT_TONES = {
    "tech-blue": {
        "main-blue": {"soft": "#EAF1FF", "subtle": "#F3F7FF", "border": "#AFC5EE"},
        "deep-blue": {"soft": "#E8EEF8", "subtle": "#F2F5FA", "border": "#9FB2D2"},
        "medium-blue": {"soft": "#EEF4FF", "subtle": "#F6F9FF", "border": "#B9CCF2"},
        "data-cyan": {"soft": "#E8F7FA", "subtle": "#F2FBFC", "border": "#A7D8E2"},
    },
    "vibrant": {
        "blue": {"soft": "#EAF3FF", "subtle": "#F4F8FF", "border": "#B8D3FA"},
        "purple": {"soft": "#F2ECFF", "subtle": "#F8F5FF", "border": "#D2BFFA"},
        "cyan": {"soft": "#E7F9FC", "subtle": "#F2FCFD", "border": "#A9DFE9"},
        "green": {"soft": "#EAF9EF", "subtle": "#F3FCF6", "border": "#AFE2BF"},
        "orange": {"soft": "#FFF4E2", "subtle": "#FFF9F0", "border": "#F5D19B"},
        "red": {"soft": "#FDECEC", "subtle": "#FFF5F5", "border": "#F3B6B6"},
    },
    "mint-green": {
        "mint-green": {"soft": "#DDF5E8", "subtle": "#F2FAF6", "border": "#A8D5BE"},
        "teal-green": {"soft": "#CCFBF1", "subtle": "#F0FDFA", "border": "#9ADDD2"},
    },
    "steady-red-blue": {
        "red": {"soft": "#FBE4E4", "subtle": "#FFF4F4", "border": "#E2A4A4"},
        "navy": {"soft": "#E9EEF5", "subtle": "#F4F6FA", "border": "#AEBBD0"},
        "accent-blue": {"soft": "#EAF3FD", "subtle": "#F4F8FD", "border": "#B4CFEC"},
    },
}

THEME_RECIPES = {
    "tech-blue": {
        "title-role": "focus",
        "accent-role": "axis-main",
        "layer-roles": ["data-flow", "axis-main", "axis-cross", "group"],
        "structure-roles": ["axis-main", "axis-cross", "data-flow"],
        "baseline-roles": {"entry": "axis-main", "governance": "group", "provider": "axis-cross", "data": "data-flow", "side": "side-rail"},
        "layer-title-solid": "all",
        "surface-policy": {"shell": "surface", "region": "role-subtle", "card": "surface", "top-band": "role-subtle", "footer-band": "surface", "side-rail": "role-soft", "insight": "role-subtle"},
        "badge-roles": ["axis-main", "axis-cross", "data-flow"],
        "shadow-opacity": 0.07,
        "area-budget": {"strong": 0.20, "focus": 0.08, "status": 0.00},
    },
    "vibrant": {
        "title-role": "axis-main",
        "accent-role": "axis-main",
        "layer-roles": ["domain-app", "domain-control", "domain-network", "domain-data"],
        "structure-roles": ["axis-main", "axis-cross", "data-flow"],
        "baseline-roles": {"entry": "domain-app", "governance": "domain-control", "provider": "domain-network", "data": "domain-data", "side": "domain-network"},
        "layer-title-solid": "none",
        "surface-policy": {"shell": "surface", "region": "role-subtle", "card": "surface", "top-band": "surface", "footer-band": "surface", "side-rail": "surface", "insight": "surface"},
        "badge-roles": ["axis-main", "axis-cross", "data-flow"],
        "shadow-opacity": 0.06,
        "area-budget": {"strong": 0.18, "focus": 0.08, "status": 0.06},
    },
    "mint-green": {
        "title-role": "axis-main",
        "accent-role": "axis-main",
        "layer-roles": ["axis-main", "axis-cross", "axis-main", "data-flow"],
        "structure-roles": ["axis-main", "axis-cross", "data-flow"],
        "baseline-roles": {"entry": "axis-main", "governance": "axis-cross", "provider": "axis-main", "data": "data-flow", "side": "side-rail"},
        "layer-title-solid": "none",
        "surface-policy": {"shell": "surface", "region": "role-subtle", "card": "surface", "top-band": "surface", "footer-band": "role-subtle", "side-rail": "role-subtle", "insight": "role-subtle"},
        "badge-roles": ["axis-main", "axis-cross", "data-flow"],
        "shadow-opacity": 0.045,
        "area-budget": {"strong": 0.12, "focus": 0.07, "status": 0.00},
    },
    "steady-red-blue": {
        "title-role": "focus",
        "accent-role": "focus",
        "layer-roles": ["focus", "side-rail", "side-rail", "axis-cross"],
        "structure-roles": ["side-rail", "axis-cross"],
        "baseline-roles": {"entry": "focus", "governance": "side-rail", "provider": "axis-cross", "data": "side-rail", "side": "side-rail"},
        "layer-title-solid": "all",
        "surface-policy": {"shell": "surface", "region": "surface-muted", "card": "surface", "top-band": "surface", "footer-band": "surface", "side-rail": "role-base", "insight": "surface"},
        "badge-roles": ["focus", "side-rail", "axis-cross"],
        "shadow-opacity": 0.055,
        "area-budget": {"strong": 0.18, "focus": 0.08, "status": 0.00},
    },
}
SLOTS = ("primary", "secondary", "tertiary", "accent")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def normalize_hex(value: str) -> str:
    if not HEX_RE.fullmatch(value):
        raise ValueError(f"颜色必须是 #RRGGBB: {value}")
    return value.upper()


def rgb(value: str) -> tuple[int, int, int]:
    value = normalize_hex(value)
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))


def mix(color: str, target: str, target_weight: float) -> str:
    source_rgb, target_rgb = rgb(color), rgb(target)
    mixed = tuple(round(a * (1 - target_weight) + b * target_weight) for a, b in zip(source_rgb, target_rgb))
    return "#" + "".join(f"{channel:02X}" for channel in mixed)


def luminance(color: str) -> float:
    channels = []
    for channel in rgb(color):
        value = channel / 255
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first: str, second: str) -> float:
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def foreground(background: str) -> str:
    candidates = ("#172033", "#FFFFFF", "#000000")
    return max(candidates, key=lambda candidate: contrast(background, candidate))


def ensure_contrast(color: str, background: str, minimum: float, target: str) -> str:
    """Move a derived structural color toward target until it remains visible."""
    if contrast(color, background) >= minimum:
        return normalize_hex(color)
    for step in range(1, 21):
        adjusted = mix(color, target, step / 20)
        if contrast(adjusted, background) >= minimum:
            return adjusted
    return normalize_hex(target)


def build_tone(base: str, soft: str, subtle: str, border: str) -> dict[str, str]:
    return {"base": normalize_hex(base), "strong": ensure_contrast(mix(base, "#000000", 0.18), "#FFFFFF", 4.5, "#000000"), "soft": normalize_hex(soft), "subtle": normalize_hex(subtle), "border": normalize_hex(border), "foreground": foreground(base)}


def build_palette(theme: str = "tech-blue", mode: str = "light", **overrides: str | None) -> dict[str, object]:
    if theme not in THEMES:
        raise ValueError(f"未知主题: {theme}")
    if mode not in {"light", "dark"}:
        raise ValueError(f"未知显示模式: {mode}")

    base = {slot: normalize_hex(overrides.get(slot) or THEMES[theme][slot]) for slot in SLOTS}
    if mode == "light":
        palette = THEMES[theme]["palette"]
        theme_text = {"tech-blue": "#162A50", "vibrant": "#172033", "mint-green": "#154E49", "steady-red-blue": "#142744"}
        neutral = {
            "canvas": palette["background"],
            "surface": palette.get("card", "#FFFFFF"),
            "surface-muted": palette.get("container", "#F5F7FA"),
            "border": palette["border"],
            "text-strong": theme_text[theme],
            "text": "#475569",
            "text-muted": "#64748B",
        }
        derived = {
            slot: {
                "base": color,
                "strong": mix(color, "#000000", 0.18),
                "soft": ensure_contrast(mix(color, "#FFFFFF", 0.88), neutral["canvas"], 1.12, "#000000"),
                "subtle": ensure_contrast(mix(color, "#FFFFFF", 0.94), neutral["canvas"], 1.06, "#000000"),
                "border": ensure_contrast(mix(color, "#FFFFFF", 0.58), neutral["surface"], 1.5, "#000000"),
                "foreground": foreground(color),
            }
            for slot, color in base.items()
        }
    else:
        neutral = {
            "canvas": "#0F172A",
            "surface": "#172033",
            "surface-muted": "#1E293B",
            "border": "#334155",
            "text-strong": "#F8FAFC",
            "text": "#CBD5E1",
            "text-muted": "#94A3B8",
        }
        derived = {
            slot: {
                "base": color,
                "strong": mix(color, "#FFFFFF", 0.22),
                "soft": ensure_contrast(mix(color, neutral["surface"], 0.72), neutral["canvas"], 1.12, "#FFFFFF"),
                "subtle": ensure_contrast(mix(color, neutral["surface"], 0.84), neutral["canvas"], 1.06, "#FFFFFF"),
                "border": ensure_contrast(mix(color, neutral["surface"], 0.38), neutral["surface"], 1.5, "#FFFFFF"),
                "foreground": foreground(color),
            }
            for slot, color in base.items()
        }

    palette_tones = {}
    for key, color in THEMES[theme]["palette"].items():
        if key in {"background", "container", "card", "border", "light-green", "light-cyan", "light-red"}:
            continue
        if mode == "light" and key in LIGHT_TONES[theme]:
            values = LIGHT_TONES[theme][key]
            palette_tones[key] = build_tone(color, values["soft"], values["subtle"], values["border"])
        else:
            palette_tones[key] = {"base": color, "strong": mix(color, "#FFFFFF", 0.22) if mode == "dark" else ensure_contrast(mix(color, "#000000", 0.18), "#FFFFFF", 4.5, "#000000"), "soft": ensure_contrast(mix(color, neutral["surface"], 0.72 if mode == "dark" else 0.88), neutral["canvas"], 1.12, "#FFFFFF" if mode == "dark" else "#000000"), "subtle": ensure_contrast(mix(color, neutral["surface"], 0.84 if mode == "dark" else 0.94), neutral["canvas"], 1.06, "#FFFFFF" if mode == "dark" else "#000000"), "border": ensure_contrast(mix(color, neutral["surface"], 0.38 if mode == "dark" else 0.58), neutral["surface"], 1.5, "#FFFFFF" if mode == "dark" else "#000000"), "foreground": foreground(color)}

    return {
        "theme": theme,
        "theme-name": THEMES[theme]["name"],
        "mode": mode,
        "neutral": neutral,
        "colors": derived,
        "palette": THEMES[theme]["palette"],
        "tones": palette_tones,
        "recipe": THEME_RECIPES[theme],
        "semantic": {
            "success": "#22C55E" if mode == "light" else "#4ADE80",
            "warning": "#F59E0B" if mode == "light" else "#FBBF24",
            "error": "#EF4444" if mode == "light" else "#F87171",
            "async": "#8B5CF6" if mode == "light" else "#A78BFA",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", choices=sorted(THEMES), default="tech-blue")
    parser.add_argument("--mode", choices=("light", "dark"), default="light")
    for slot in SLOTS:
        parser.add_argument(f"--{slot}")
    args = parser.parse_args()
    overrides = {slot: getattr(args, slot) for slot in SLOTS}
    try:
        palette = build_palette(args.theme, args.mode, **overrides)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(palette, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
