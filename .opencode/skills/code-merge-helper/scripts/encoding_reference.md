# UTF-8 编码参考指南

本文档为各 skill 提供统一的 UTF-8 编码处理规则。

## 快速参考

**写入文件：**
```bash
python write_utf8.py output.md --stdin < content.txt
```

**验证文件：**
```bash
python write_utf8.py output.md --validate-strict
```

**读取文件（PowerShell）：**
```bash
python write_utf8.py output.md --read
```

## 在 Skill 中引用

各 skill 的 SKILL.md 应简化编码说明，引用本文档：

```markdown
### 文件编码规则

**必须使用 UTF-8 编码（无 BOM）**。推荐使用统一工具：

```bash
python ../.opencode/skills/shared/write_utf8.py output.md --stdin
python ../.opencode/skills/shared/write_utf8.py output.md --validate-strict
```

详细说明见 `../shared/encoding_reference.md`
```

## 常见编码问题

### 问题 1: PowerShell 乱码

**症状：** 使用 `Set-Content` 或 `Out-File` 后，中文显示为乱码

**原因：** PowerShell 默认使用系统编码（Windows 简体中文为 GBK）

**解决：** 使用 `write_utf8.py` 工具，或显式指定编码：
```powershell
[System.IO.File]::WriteAllText("output.md", $content, [System.Text.UTF8Encoding]::new($false))
```

### 问题 2: 文件包含 BOM

**症状：** Git diff 显示文件开头有 `<U+FEFF>`

**原因：** 某些编辑器或工具默认添加 UTF-8 BOM

**解决：** 使用 `write_utf8.py` 重新写入（自动去除 BOM）

### 问题 3: 乱码字符

如果看到以下字符，说明存在 GBK→UTF-8 误解析：

| 乱码 | 原字符 |
|-----|-------|
| 鍦 | 在 |
| 鈥 | " |
| 銆 | 、 |
| 锛 | ， |
| � | 任意（损坏） |

**解决：** 从源头重新生成，确保使用正确的 UTF-8 编码。

## 技术细节

- **编码：** UTF-8 without BOM
- **换行符：** LF (`\n`)，即使在 Windows
- **验证：** 自动检查 BOM、替换字符、mojibake 模式
