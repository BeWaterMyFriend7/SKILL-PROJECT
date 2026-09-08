#!/usr/bin/env python3
"""Read-only UTF-8 check. Exit 0 clean, 1 invalid, 2 usage/read error."""
import argparse
from pathlib import Path
import sys
from write_utf8 import validate_text, suspicious_mojibake_markers


def check(filepath, strict_mojibake=False):
    try:
        raw = Path(filepath).read_bytes()
    except OSError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    try:
        if raw.startswith(b"\xef\xbb\xbf"):
            raise ValueError("UTF-8 BOM detected")
        validate_text(raw.decode("utf-8"), strict_mojibake)
    except ValueError as exc:
        print("INVALID: " + str(exc), file=sys.stderr)
        return 1
    print("UTF-8 OK: " + str(filepath))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--strict-mojibake", action="store_true", help="Heuristic; may reject valid text")
    args = parser.parse_args()
    raise SystemExit(check(args.file, args.strict_mojibake))
