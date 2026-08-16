#!/usr/bin/env python3
"""Generate deterministic color tokens for diagram themes."""

from __future__ import annotations

import argparse
import json
import re


THEMES = {
    "tech-blue": {
        "name": "科技蓝",
        "primary": "#2E69E1",
        "secondary": "#1A388D",
        "tertiary": "#819FDE",
        "accent": "#1A388D",
    },
    "vibrant": {
        "name": "活力多彩",
        "primary": "#1B9CDE",
        "secondary": "#A039B9",
        "tertiary": "#39A95B",
        "accent": "#FE9022",
    },
    "focused": {
        "name": "稳健聚焦",
        "primary": "#1F5CD7",
        "secondary": "#12939D",
        "tertiary": "#4B9654",
        "accent": "#FF6B1A",
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


def build_palette(theme: str = "tech-blue", mode: str = "light", **overrides: str | None) -> dict[str, object]:
    if theme not in THEMES:
        raise ValueError(f"未知主题: {theme}")
    if mode not in {"light", "dark"}:
        raise ValueError(f"未知显示模式: {mode}")

    base = {slot: normalize_hex(overrides.get(slot) or THEMES[theme][slot]) for slot in SLOTS}
    if mode == "light":
        neutral = {
            "canvas": "#F6F8FB",
            "surface": "#FFFFFF",
            "surface-muted": "#EEF3F8",
            "border": "#D8E1EA",
            "text-strong": "#172033",
            "text": "#475569",
            "text-muted": "#64748B",
        }
        derived = {
            slot: {
                "base": color,
                "strong": mix(color, "#000000", 0.18),
                "soft": ensure_contrast(mix(color, "#FFFFFF", 0.88), neutral["canvas"], 1.12, "#000000"),
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
                "border": ensure_contrast(mix(color, neutral["surface"], 0.38), neutral["surface"], 1.5, "#FFFFFF"),
                "foreground": foreground(color),
            }
            for slot, color in base.items()
        }

    return {
        "theme": theme,
        "theme-name": THEMES[theme]["name"],
        "mode": mode,
        "neutral": neutral,
        "colors": derived,
        "semantic": {
            "success": "#16A34A" if mode == "light" else "#4ADE80",
            "warning": "#D97706" if mode == "light" else "#FBBF24",
            "error": "#DC2626" if mode == "light" else "#F87171",
            "async": "#7C3AED" if mode == "light" else "#A78BFA",
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
