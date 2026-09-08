# code-merge-helper 使用说明

用于合并前评估以及 merge、rebase、cherry-pick 的文本与语义冲突分析。分析期间不编辑业务代码或改变 Git 操作状态。

## 使用

```text
请使用 code-merge-helper 分析将 main 合并到当前分支的冲突，先不要执行合并。
```

- 执行规则：[SKILL.md](../../.opencode/skills/code-merge-helper/SKILL.md)
- 当前模板：[merge-resolution-report.md](../../.opencode/skills/code-merge-helper/assets/merge-resolution-report.md)
- 历史示例：[examples.md](examples.md)，结构以当前模板为准。

## 报告结构

人类决策区给出合并判断、比较范围和逐项冲突裁决，说明双方意图、保留或舍弃的行为及理由。
AI 冲突解决清单按裁决组织文件动作和对应验证，记录准确的提交与 stage blob 依据，仅在存在跨冲突依赖时补充顺序。

不同 Git 操作使用实际应用基线；stage blob 不是提交 SHA。合并前无冲突索引时不伪造 stage。
整体检查区分编辑后未暂存与经授权暂存后的索引状态，不把批准报告当作提交或推送授权。

默认输出到 `.code/merge-review/`；用户可指定路径或只在对话输出。

## 检查

在项目根目录运行下列命令，仅检查编码，不代表裁决正确或 Git 状态符合要求：

```powershell
python -B -X utf8 .opencode/skills/code-merge-helper/scripts/check_utf8.py <报告文件>
```

Python 3.10+，无第三方依赖。旧版 JSON 附录 validator 不适用于当前模板，已退出当前发布包；Git 取证与裁决验证遵循当前 skill 的参考说明。
