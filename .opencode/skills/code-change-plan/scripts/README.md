# 编码工具

Python 3.10+，仅标准库。两个 skill 各自携带完整工具，不依赖另一个 skill 或 shared 目录。
以下命令在当前 skill 的 scripts 目录运行，或改用脚本绝对路径。

```powershell
python -B -X utf8 write_utf8.py output.md '正文'
python -B -X utf8 write_utf8.py output.md --read
python -B -X utf8 write_utf8.py output.md --validate
python -B -X utf8 check_utf8.py output.md
```

正文参数是原样文本，字符串中的反斜杠 n 不会自动变成换行。带前导短横线的正文用 `output.md -- '-正文'`。
`--stdin` 从标准输入接收 UTF-8 字节；PowerShell 管道需先将 `$OutputEncoding` 设置为 UTF-8，Python 的 UTF-8 模式无法修复上游已丢失的字符。

写入前校验，移除一个开头 BOM，将 CRLF/CR 转为 LF，再通过同目录临时文件原子替换。确定的无效 UTF-8、U+FFFD、参数错误或替换失败均不会覆盖旧文件；临时文件会清理。拒绝替换符号链接。保留已有文件权限位，但不承诺保留 ACL、扩展属性等全部元数据，不用于依赖这些元数据的文件。

默认不会将普通汉字当作乱码判定。显式 `--validate-strict` 或 `--strict-mojibake` 启用启发式检查，可能拒绝“涓涓细流”等正常文本，不能据此自动修正文档。
`--validate` 检查 UTF-8 无 BOM 与 U+FFFD；不检查报告质量或审批正确性。报告尚未执行的验证仍应标为计划。

writer 退出码：0 成功，1 校验不通过，2 参数或 I/O/写入输入错误。
checker 退出码：0 通过，1 编码问题，2 参数或读取错误。
