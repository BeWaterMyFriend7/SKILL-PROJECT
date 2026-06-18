#!/usr/bin/env python3
"""Check file encoding: UTF-8 without BOM, no Unicode replacement characters.

Usage:
    python scripts/check_utf8.py <file>

Exit code 0 = clean, 1 = issues found, 2 = read error.
"""
import sys
from pathlib import Path


def check(filepath: str) -> int:
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
    if '�' in text:
        errors.append("Unicode replacement characters found (mojibake / encoding corruption)")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print(f"UTF-8 OK: {filepath}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        raise SystemExit(2)
    raise SystemExit(check(sys.argv[1]))
