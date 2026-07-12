#!/usr/bin/env python3
"""Check file encoding: UTF-8 without BOM, no Unicode replacement characters.

Usage:
    python scripts/check_utf8.py [--strict-mojibake] <file>

Exit code 0 = clean, 1 = issues found, 2 = read error.
"""
import sys
from pathlib import Path


MOJIBAKE_MARKERS = (
    "鍦",
    "涓",
    "鈥",
    "銆",
    "锛",
    "绗",
    "闇",
    "浠",
    "Ã",
    "Â",
)


def _format_marker(marker: str) -> str:
    return marker.encode("unicode_escape").decode("ascii")


def suspicious_mojibake_markers(text: str) -> list[str]:
    return [marker for marker in MOJIBAKE_MARKERS if marker in text]


def check(filepath: str, strict_mojibake: bool = False) -> int:
    path = Path(filepath)
    if not path.is_file():
        print(f"ERROR: File not found: {filepath}")
        return 2

    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"ERROR: Cannot read {filepath}: {exc}")
        return 2

    errors = []

    # BOM check
    if raw[:3] == b'\xef\xbb\xbf':
        errors.append("BOM detected (file starts with UTF-8 BOM)")

    # Valid UTF-8 decode
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as ude:
        errors.append(f"Invalid UTF-8 encoding: {ude}")
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    # Replacement character check
    if '\ufffd' in text:
        errors.append("Unicode replacement characters found (mojibake / encoding corruption)")

    if strict_mojibake:
        markers = suspicious_mojibake_markers(text)
        if markers:
            rendered = ", ".join(_format_marker(marker) for marker in markers)
            errors.append(f"Suspicious mojibake markers found: {rendered}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print(f"UTF-8 OK: {filepath}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    strict_mojibake = False
    if "--strict-mojibake" in args:
        strict_mojibake = True
        args.remove("--strict-mojibake")

    if len(args) != 1:
        print(f"Usage: {sys.argv[0]} [--strict-mojibake] <file>")
        raise SystemExit(2)
    raise SystemExit(check(args[0], strict_mojibake=strict_mojibake))
