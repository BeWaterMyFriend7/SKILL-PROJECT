#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
WRITER="$SCRIPT_DIR/write-memory.py"

if command -v python3 >/dev/null 2>&1 &&
    python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1 &&
    python -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
    PYTHON=python
else
    printf '%s\n' \
        '需要 Python 3.8 或更高版本，并确保 python3 或 python 已加入 PATH。' >&2
    exit 1
fi

exec "$PYTHON" "$WRITER" "$@"
