#!/usr/bin/env python3
"""UTF-8 writer/reader/validator. Python 3.10+, standard library only."""
import argparse
import os
from pathlib import Path
import stat
import sys
import tempfile

# Heuristics only: these characters can occur in perfectly valid text.
MOJIBAKE_MARKERS = ("鍦", "涓", "鈥", "銆", "锛", "绗", "闇", "浠", "Ã", "Â")


def suspicious_mojibake_markers(text):
    return [marker for marker in MOJIBAKE_MARKERS if marker in text]


def validate_text(text, strict_mojibake=False):
    text.encode("utf-8", errors="strict")
    if "\ufffd" in text:
        raise ValueError("U+FFFD found; check the original input")
    if strict_mojibake and suspicious_mojibake_markers(text):
        raise ValueError("Suspected mojibake (heuristic; valid text may match)")


def read_utf8_file(file_path):
    return Path(file_path).read_bytes().decode("utf-8", errors="strict")


def validate_utf8_file(file_path, strict_mojibake=False):
    try:
        raw = Path(file_path).read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            return False, "UTF-8 BOM detected"
        text = raw.decode("utf-8", errors="strict")
        validate_text(text, strict_mojibake)
        return True, None
    except (OSError, ValueError) as exc:
        return False, str(exc)


def write_utf8_file(file_path, content, strict_mojibake=False):
    # Prepare and validate before creating directories or touching the target.
    text = content.removeprefix("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    validate_text(text, strict_mojibake)
    raw = text.encode("utf-8")
    path = Path(file_path)
    if path.is_symlink():
        raise ValueError("Refusing to replace a symbolic link")
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        # Same directory is required for atomic replacement on one filesystem.
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix="." + path.name + ".", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file_path")
    parser.add_argument("content", nargs="?", help="Literal text; use -- before text beginning with -")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--stdin", action="store_true")
    mode.add_argument("--read", action="store_true")
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--validate-strict", action="store_true")
    parser.add_argument("--strict-mojibake", action="store_true", help="Opt-in heuristic; may reject valid text")
    args = parser.parse_args(argv)
    selected = args.stdin or args.read or args.validate or args.validate_strict
    if selected and args.content is not None:
        parser.error("content cannot be combined with a mode")
    if not selected and args.content is None:
        parser.error("provide content or a mode")
    if args.read and args.strict_mojibake:
        parser.error("--strict-mojibake is not a read option")
    try:
        strict = args.strict_mojibake or args.validate_strict
        if args.read:
            sys.stdout.buffer.write(read_utf8_file(args.file_path).encode("utf-8"))
        elif args.validate or args.validate_strict:
            valid, error = validate_utf8_file(args.file_path, strict)
            if not valid:
                print("INVALID: " + error, file=sys.stderr)
                return 1
            print("UTF-8 OK: " + args.file_path)
        else:
            content = sys.stdin.buffer.read().decode("utf-8") if args.stdin else args.content
            if not strict and suspicious_mojibake_markers(content):
                print("NOTE: suspicious characters are only a heuristic; input is accepted if valid", file=sys.stderr)
            write_utf8_file(args.file_path, content, strict)
            print("Written: " + args.file_path)
        return 0
    except (OSError, ValueError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
