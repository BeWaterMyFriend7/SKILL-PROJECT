#!/usr/bin/env python3
"""
UTF-8 File Writer and Validator

Ensures all output files use correct UTF-8 encoding (without BOM).
Works across Windows, Linux, and macOS.

Usage:
    python write_utf8.py <file_path> <content>
    python write_utf8.py <file_path> --stdin
    python write_utf8.py <file_path> --validate
    python write_utf8.py <file_path> --validate-strict
    python write_utf8.py <file_path> --read

Examples:
    # Write from argument
    python write_utf8.py output.md "# Title\\nContent"

    # Write from stdin
    echo "Content" | python write_utf8.py output.md --stdin

    # Validate encoding
    python write_utf8.py output.md --validate-strict

    # Read file safely (Windows PowerShell)
    python write_utf8.py output.md --read
"""

import sys
from pathlib import Path
from typing import Optional


def write_utf8_file(file_path: str, content: str) -> None:
    """Write UTF-8 file without BOM"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8', newline='\n')


def read_utf8_file(file_path: str) -> str:
    """Read UTF-8 file"""
    return Path(file_path).read_text(encoding='utf-8')


def validate_utf8_file(file_path: str, strict_mojibake: bool = False) -> tuple[bool, Optional[str]]:
    """
    Validate file is valid UTF-8 without BOM

    Returns: (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"File not found: {file_path}"

    try:
        # Check for BOM
        with open(path, 'rb') as f:
            first_bytes = f.read(3)
            if first_bytes == b'\xef\xbb\xbf':
                return False, "File contains UTF-8 BOM (should be without BOM)"

        # Try reading as UTF-8
        content = path.read_text(encoding='utf-8')

        # Check for Unicode replacement character
        if '�' in content:
            return False, "File contains Unicode replacement character U+FFFD (corrupted encoding)"

        # Strict mode: check common mojibake patterns
        if strict_mojibake:
            mojibake_patterns = ['鑬', '钉', '銆', '閑', '涓', '霄']
            found_patterns = [p for p in mojibake_patterns if p in content]
            if found_patterns:
                return False, f"Detected suspicious mojibake characters: {', '.join(found_patterns)}"

        return True, None

    except UnicodeDecodeError as e:
        return False, f"UTF-8 decode failed: {e}"
    except Exception as e:
        return False, f"Validation failed: {e}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    file_path = sys.argv[1]

    # Validate mode
    if len(sys.argv) == 3 and sys.argv[2] == '--validate':
        is_valid, error = validate_utf8_file(file_path, strict_mojibake=False)
        if is_valid:
            print(f"OK: {file_path} is valid UTF-8 without BOM")
            sys.exit(0)
        else:
            print(f"ERROR: {file_path} validation failed: {error}", file=sys.stderr)
            sys.exit(1)

    # Strict validate mode
    if len(sys.argv) == 3 and sys.argv[2] == '--validate-strict':
        is_valid, error = validate_utf8_file(file_path, strict_mojibake=True)
        if is_valid:
            print(f"OK: {file_path} is valid UTF-8 without BOM and mojibake")
            sys.exit(0)
        else:
            print(f"ERROR: {file_path} validation failed: {error}", file=sys.stderr)
            sys.exit(1)

    # Read mode
    if len(sys.argv) == 3 and sys.argv[2] == '--read':
        try:
            content = read_utf8_file(file_path)
            print(content, end='')
            sys.exit(0)
        except Exception as e:
            print(f"Read failed: {e}", file=sys.stderr)
            sys.exit(1)

    # Write mode
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--stdin':
            content = sys.stdin.read()
        else:
            content = sys.argv[2]

        try:
            write_utf8_file(file_path, content)
            print(f"OK: Written to {file_path}")

            # Auto-validate
            is_valid, error = validate_utf8_file(file_path, strict_mojibake=True)
            if not is_valid:
                print(f"WARNING: Post-write validation failed: {error}", file=sys.stderr)
                sys.exit(1)

            sys.exit(0)
        except Exception as e:
            print(f"Write failed: {e}", file=sys.stderr)
            sys.exit(1)

    print(__doc__)
    sys.exit(1)


if __name__ == '__main__':
    main()
