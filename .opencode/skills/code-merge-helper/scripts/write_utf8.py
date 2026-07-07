#!/usr/bin/env python3
"""
统一的 UTF-8 文件写入工具

用于确保所有 skill 输出文件都使用正确的 UTF-8 编码（无 BOM）。
适用于 Windows、Linux、macOS 等所有平台。

Usage:
    python write_utf8.py <file_path> <content>
    python write_utf8.py <file_path> --stdin

Examples:
    # 从参数写入
    python write_utf8.py output.md "# 标题\n内容"

    # 从标准输入写入
    echo "内容" | python write_utf8.py output.md --stdin

    # 在 PowerShell 中使用 here-string
    @"
    # 标题
    内容
    "@ | python write_utf8.py output.md --stdin
"""

import sys
from pathlib import Path
from typing import Optional


def write_utf8_file(file_path: str, content: str) -> None:
    """
    写入 UTF-8 编码文件（无 BOM）

    Args:
        file_path: 目标文件路径
        content: 要写入的内容

    Raises:
        IOError: 文件写入失败
        UnicodeEncodeError: 内容包含无法编码的字符
    """
    path = Path(file_path)

    # 确保父目录存在
    path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件，显式指定 UTF-8 编码，无 BOM
    path.write_text(content, encoding='utf-8', newline='\n')


def read_utf8_file(file_path: str) -> str:
    """
    读取 UTF-8 编码文件

    Args:
        file_path: 文件路径

    Returns:
        文件内容

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 文件编码错误
    """
    path = Path(file_path)
    return path.read_text(encoding='utf-8')


def validate_utf8_file(file_path: str, strict_mojibake: bool = False) -> tuple[bool, Optional[str]]:
    """
    验证文件是否为有效的 UTF-8 编码（无 BOM）

    Args:
        file_path: 文件路径
        strict_mojibake: 是否严格检查 mojibake 字符

    Returns:
        (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"文件不存在: {file_path}"

    try:
        # 检查 BOM
        with open(path, 'rb') as f:
            first_bytes = f.read(3)
            if first_bytes == b'\xef\xbb\xbf':
                return False, "文件包含 UTF-8 BOM 头（应为无 BOM）"

        # 尝试读取为 UTF-8
        content = path.read_text(encoding='utf-8')

        # 检查 Unicode 替换字符
        if '�' in content:
            return False, "文件包含 Unicode 替换字符 U+FFFD（编码损坏）"

        # 严格模式：检查常见的 mojibake 字符
        if strict_mojibake:
            mojibake_patterns = ['鍦', '鈥', '銆', '锛', '涓', '鏄']
            found_patterns = [p for p in mojibake_patterns if p in content]
            if found_patterns:
                return False, f"检测到可疑的 mojibake 字符: {', '.join(found_patterns)}"

        return True, None

    except UnicodeDecodeError as e:
        return False, f"UTF-8 解码失败: {e}"
    except Exception as e:
        return False, f"验证失败: {e}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    file_path = sys.argv[1]

    # 验证模式
    if len(sys.argv) == 3 and sys.argv[2] == '--validate':
        is_valid, error = validate_utf8_file(file_path, strict_mojibake=False)
        if is_valid:
            print(f"✓ {file_path} 是有效的 UTF-8 文件（无 BOM）")
            sys.exit(0)
        else:
            print(f"✗ {file_path} 验证失败: {error}", file=sys.stderr)
            sys.exit(1)

    # 严格验证模式
    if len(sys.argv) == 3 and sys.argv[2] == '--validate-strict':
        is_valid, error = validate_utf8_file(file_path, strict_mojibake=True)
        if is_valid:
            print(f"✓ {file_path} 是有效的 UTF-8 文件（无 BOM，无 mojibake）")
            sys.exit(0)
        else:
            print(f"✗ {file_path} 验证失败: {error}", file=sys.stderr)
            sys.exit(1)

    # 读取模式
    if len(sys.argv) == 3 and sys.argv[2] == '--read':
        try:
            content = read_utf8_file(file_path)
            print(content, end='')
            sys.exit(0)
        except Exception as e:
            print(f"读取失败: {e}", file=sys.stderr)
            sys.exit(1)

    # 写入模式
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--stdin':
            # 从标准输入读取
            content = sys.stdin.read()
        else:
            # 从参数读取
            content = sys.argv[2]

        try:
            write_utf8_file(file_path, content)
            print(f"✓ 已写入: {file_path}")

            # 自动验证
            is_valid, error = validate_utf8_file(file_path, strict_mojibake=True)
            if not is_valid:
                print(f"⚠ 警告: 写入后验证失败: {error}", file=sys.stderr)
                sys.exit(1)

            sys.exit(0)
        except Exception as e:
            print(f"写入失败: {e}", file=sys.stderr)
            sys.exit(1)

    print(__doc__)
    sys.exit(1)


if __name__ == '__main__':
    main()
