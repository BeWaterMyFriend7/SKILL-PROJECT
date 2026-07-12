# code-merge-helper 使用说明

## 适用场景

- 合并前预演或分析已经出现的 Git 冲突。
- 对比 common-base、当前分支和合入分支，追溯双方改动目的。
- 生成可审批的解决方案，不在分析阶段修改业务代码。

## 快速使用

```text
请使用 code-merge-helper 分析将远端 main 合并到当前分支的冲突，先不要执行。
```

- 完整输出示例：[examples.md](examples.md)
- 执行规则：[SKILL.md](../../.opencode/skills/code-merge-helper/SKILL.md)
- 报告模板：[merge-resolution-report.md](../../.opencode/skills/code-merge-helper/assets/merge-resolution-report.md)

```powershell
python .opencode\skills\code-merge-helper\scripts\validate_merge_plan.py --plan <报告文件> --repo . --pre-merge
```

## 核心流程

1. 识别文本冲突和潜在语义冲突。
2. 对比 common-base、stage-2 和 stage-3。
3. 查看提交历史，理解双方改动目的。
4. 推荐保留一侧、语义融合或人工决策方案。
5. 评估风险并制定验证和回滚步骤。
6. 生成报告并等待审批。
