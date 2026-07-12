# Shared Utilities

本目录包含跨 skill 共享的工具脚本。

## write_utf8.py

统一的 UTF-8 文件写入和验证工具，解决 Windows/PowerShell 环境下的编码问题。

### 为什么需要这个工具？

在 Windows PowerShell 环境中，使用 `Set-Content` / `Out-File` 写入中文内容时，默认使用系统编码（如 GBK），导致：
- UTF-8 文件被错误编码
- 可能添加不需要的 BOM 头
- 跨平台兼容性问题

本工具确保：
- 始终使用 UTF-8 编码（无 BOM）
- 统一的换行符（LF）
- 自动验证写入结果
- 跨平台兼容（Windows/Linux/macOS）

### 使用方法

#### 1. 写入文件

**从参数写入：**
```bash
python write_utf8.py output.md "# 标题\n内容"
```

**从标准输入写入（推荐）：**
```bash
# Linux/macOS
echo "内容" | python write_utf8.py output.md --stdin

# Windows PowerShell
@"
# 标题
内容
"@ | python write_utf8.py output.md --stdin
```

#### 2. 读取文件

在 PowerShell 中安全读取 UTF-8 文件：
```bash
python write_utf8.py output.md --read
```

等价于（但更安全）：
```bash
python -c "from pathlib import Path; print(Path('output.md').read_text(encoding='utf-8'))"
```

#### 3. 验证文件

**基本验证（检查 UTF-8 和 BOM）：**
```bash
python write_utf8.py output.md --validate
```

**严格验证（额外检查 mojibake）：**
```bash
python write_utf8.py output.md --validate-strict
```

### 常见的编码错误特征

如果在输出中看到以下字符，说明存在编码问题：

| 乱码字符 | 原始字符 | 原因 |
|---------|---------|------|
| 鍦 | 在 | GBK → UTF-8 误解析 |
| 鈥 | " | 同上 |
| 銆 | 、 | 同上 |
| 锛 | ， | 同上 |
| � (U+FFFD) | （任意） | Unicode 替换字符，编码损坏 |

**解决方法：** 使用本工具重新生成文件。

### 在 Skill 中的使用

各个 skill 的 SKILL.md 中应引用本工具，而非重复编码规则：

```markdown
### 文件编码规则

使用统一的 UTF-8 工具写入文件：
\`\`\`bash
python ../.opencode/skills/shared/write_utf8.py output.md --stdin
\`\`\`

详细说明见 `../shared/README.md`
```

### 技术细节

- **编码：** UTF-8 without BOM
- **换行符：** LF (`\n`)，即使在 Windows 上
- **自动创建目录：** 父目录不存在时自动创建
- **验证：** 写入后自动验证编码正确性

### 依赖

Python 3.7+ 标准库，无第三方依赖。
