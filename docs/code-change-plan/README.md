# code-change-plan 使用说明

## 适用场景

- 在改代码前分析需求、验收标准、技术方案和影响范围。
- 生成可审核、可执行、带验证与回滚步骤的变更计划。
- 只负责规划，不直接修改业务代码。

## 快速使用

```text
请使用 code-change-plan 分析新增用户登录功能，先生成方案，不修改代码。
```

- 完整输出示例：[examples.md](examples.md)
- 执行规则：[SKILL.md](../../.opencode/skills/code-change-plan/SKILL.md)
- 报告模板：[change-plan-template.md](../../.opencode/skills/code-change-plan/assets/change-plan-template.md)

```powershell
python .opencode\skills\code-change-plan\scripts\validate_change_plan.py --plan <计划文件>
```

## 核心流程

1. 明确业务目标、功能和验收条件。
2. 分析当前实现与目标差距。
3. 设计技术方案并说明关键决策。
4. 列出允许修改的文件和影响范围。
5. 设计验证与回滚步骤。
6. 生成计划并等待审批。
