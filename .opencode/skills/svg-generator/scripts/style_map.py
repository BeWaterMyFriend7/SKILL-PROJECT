#!/usr/bin/env python3
"""Map a diagram theme to axis-aware structural color roles."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


_PALETTE_PATH = Path(__file__).with_name("palette.py")
_SPEC = importlib.util.spec_from_file_location("_diagram_palette", _PALETTE_PATH)
PALETTE = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(PALETTE)


ROLES = (
    "axis-main",
    "axis-cross",
    "side-rail",
    "focus",
    "data-flow",
    "group",
    "connector",
)
LAYOUT_AXES = {
    "vertical-stack": "y",
    "horizontal-flow": "x",
    "mixed-axis": "mixed",
    "matrix": "grid",
    "network": "radial",
    "timeline": "x",
}
ALLOWED_DOMINANT_AXES = frozenset(LAYOUT_AXES.values())
ROLE_KEYS = {
    "tech-blue": {
        "vertical-stack": {
            "axis-main": "main-blue",
            "axis-cross": "medium-blue",
            "side-rail": "deep-blue",
            "focus": "main-blue",
            "data-flow": "data-cyan",
            "group": "medium-blue",
            "connector": "main-blue",
        },
        "horizontal-flow": {
            "axis-main": "main-blue",
            "axis-cross": "data-cyan",
            "side-rail": "deep-blue",
            "focus": "medium-blue",
            "data-flow": "data-cyan",
            "group": "medium-blue",
            "connector": "main-blue",
        },
        "mixed-axis": {
            "axis-main": "medium-blue",
            "axis-cross": "main-blue",
            "side-rail": "deep-blue",
            "focus": "main-blue",
            "data-flow": "data-cyan",
            "group": "medium-blue",
            "connector": "main-blue",
        },
    },
    "vibrant": {
        "vertical-stack": {
            "axis-main": "blue",
            "axis-cross": "purple",
            "side-rail": "cyan",
            "focus": "purple",
            "data-flow": "cyan",
            "group": "blue",
            "connector": "blue",
        },
        "horizontal-flow": {
            "axis-main": "cyan",
            "axis-cross": "blue",
            "side-rail": "purple",
            "focus": "purple",
            "data-flow": "cyan",
            "group": "blue",
            "connector": "cyan",
        },
        "mixed-axis": {
            "axis-main": "blue",
            "axis-cross": "purple",
            "side-rail": "cyan",
            "focus": "purple",
            "data-flow": "cyan",
            "group": "blue",
            "connector": "blue",
        },
    },
    "mint-green": {
        "vertical-stack": {
            "axis-main": "mint-green",
            "axis-cross": "teal-green",
            "side-rail": "mint-green",
            "focus": "teal-green",
            "data-flow": "teal-green",
            "group": "mint-green",
            "connector": "mint-green",
        },
        "horizontal-flow": {
            "axis-main": "teal-green",
            "axis-cross": "mint-green",
            "side-rail": "mint-green",
            "focus": "teal-green",
            "data-flow": "teal-green",
            "group": "mint-green",
            "connector": "teal-green",
        },
        "mixed-axis": {
            "axis-main": "mint-green",
            "axis-cross": "teal-green",
            "side-rail": "mint-green",
            "focus": "teal-green",
            "data-flow": "teal-green",
            "group": "mint-green",
            "connector": "teal-green",
        },
    },
    "steady-red-blue": {
        "vertical-stack": {
            "axis-main": "navy",
            "axis-cross": "accent-blue",
            "side-rail": "navy",
            "focus": "red",
            "data-flow": "accent-blue",
            "group": "navy",
            "connector": "navy",
        },
        "horizontal-flow": {
            "axis-main": "accent-blue",
            "axis-cross": "navy",
            "side-rail": "navy",
            "focus": "red",
            "data-flow": "accent-blue",
            "group": "navy",
            "connector": "accent-blue",
        },
        "mixed-axis": {
            "axis-main": "navy",
            "axis-cross": "accent-blue",
            "side-rail": "navy",
            "focus": "red",
            "data-flow": "accent-blue",
            "group": "navy",
            "connector": "navy",
        },
    },
}


def _profile(theme: str, layout: str) -> dict[str, str]:
    if layout not in LAYOUT_AXES:
        raise ValueError(f"未知布局: {layout}")
    theme_profiles = ROLE_KEYS.get(theme)
    if theme_profiles is None:
        raise ValueError(f"未知主题: {theme}")
    if layout in theme_profiles:
        return theme_profiles[layout]
    if layout in {"matrix", "network"}:
        return theme_profiles["mixed-axis"]
    if layout == "timeline":
        return theme_profiles["horizontal-flow"]
    raise ValueError(f"主题 {theme} 缺少布局映射: {layout}")


def _derive(base: str, mode: str, neutral: dict[str, str]) -> dict[str, str]:
    base = PALETTE.normalize_hex(base)
    if mode == "light":
        return {
            "base": base,
            "strong": PALETTE.mix(base, "#000000", 0.18),
            "soft": PALETTE.ensure_contrast(
                PALETTE.mix(base, "#FFFFFF", 0.88),
                neutral["canvas"],
                1.12,
                "#000000",
            ),
            "border": PALETTE.ensure_contrast(
                PALETTE.mix(base, "#FFFFFF", 0.58),
                neutral["surface"],
                1.5,
                "#000000",
            ),
            "foreground": PALETTE.foreground(base),
        }
    return {
        "base": base,
        "strong": PALETTE.mix(base, "#FFFFFF", 0.22),
        "soft": PALETTE.ensure_contrast(
            PALETTE.mix(base, neutral["surface"], 0.72),
            neutral["canvas"],
            1.12,
            "#FFFFFF",
        ),
        "border": PALETTE.ensure_contrast(
            PALETTE.mix(base, neutral["surface"], 0.38),
            neutral["surface"],
            1.5,
            "#FFFFFF",
        ),
        "foreground": PALETTE.foreground(base),
    }


def build_style_map(
    theme: str = "tech-blue",
    mode: str = "light",
    layout: str = "vertical-stack",
    dominant_axis: str | None = None,
    **role_overrides: str | None,
) -> dict[str, object]:
    palette = PALETTE.build_palette(theme, mode)
    profile = _profile(theme, layout)
    resolved_axis = dominant_axis or LAYOUT_AXES[layout]
    if resolved_axis not in ALLOWED_DOMINANT_AXES:
        raise ValueError(f"未知主轴: {resolved_axis}")
    normalized_overrides = {key.replace("_", "-"): value for key, value in role_overrides.items() if value}
    unknown = sorted(set(normalized_overrides) - set(ROLES))
    if unknown:
        raise ValueError("未知结构颜色角色: " + ", ".join(unknown))

    roles: dict[str, dict[str, str]] = {}
    sources: dict[str, str] = {}
    for role in ROLES:
        override = normalized_overrides.get(role)
        if override:
            base = PALETTE.normalize_hex(override)
            sources[role] = "user"
        else:
            palette_key = profile[role]
            base = palette["palette"][palette_key]
            sources[role] = palette_key
        roles[role] = _derive(base, mode, palette["neutral"])

    return {
        "theme": theme,
        "theme-name": palette["theme-name"],
        "mode": mode,
        "layout": layout,
        "dominant-axis": resolved_axis,
        "palette": palette["palette"],
        "neutral": palette["neutral"],
        "semantic": palette["semantic"],
        "role-colors": {role: values["base"] for role, values in roles.items()},
        "role-sources": sources,
        "roles": roles,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", choices=sorted(PALETTE.THEMES), default="tech-blue")
    parser.add_argument("--mode", choices=("light", "dark"), default="light")
    parser.add_argument("--layout", choices=sorted(LAYOUT_AXES), default="vertical-stack")
    parser.add_argument("--dominant-axis")
    for role in ROLES:
        parser.add_argument(f"--{role}")
    args = parser.parse_args()
    overrides = {role.replace("-", "_"): getattr(args, role.replace("-", "_")) for role in ROLES}
    result = build_style_map(
        args.theme,
        args.mode,
        args.layout,
        args.dominant_axis,
        **overrides,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
