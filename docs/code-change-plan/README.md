# code-change-plan 使用说明

用于代码变更分析、实施前评估和方案设计，输出供人审批、供 AI 执行的报告。明确要求直接实施的任务不会被本 skill 强制转换为规划。

## 使用

```text
请使用 code-change-plan 分析新增用户登录功能，先生成方案，不修改代码。
```

- 执行规则：[SKILL.md](../../.opencode/skills/code-change-plan/SKILL.md)
- 当前模板：[change-plan-template.md](../../.opencode/skills/code-change-plan/assets/change-plan-template.md)
- 历史示例：[examples.md](examples.md)，结构以当前模板为准。

## 报告结构

人类决策正文说明方案结论、行为变化与影响，以及确有必要的设计取舍。
AI 实施与验收清单按真实依赖组织，每个实施单元就地包含文件/符号动作、保持项、前置条件、验证和完成条件。计划新增对象须明确标注。

默认输出到 `.code/change-plans/`；用户可指定路径或只在对话输出。生成后等待审批，不实施。

## 检查

在项目根目录运行下列命令，仅检查编码，不代表方案完整性或行为正确性：

```powershell
python -B -X utf8 .opencode/skills/code-change-plan/scripts/check_utf8.py <计划文件>
```

Python 3.10+，无第三方依赖。旧版七章节 validator 不适用于当前模板，已退出当前发布包；不要将其结果作为本版验收依据。
