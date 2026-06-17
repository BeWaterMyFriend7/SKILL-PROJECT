# code-merge-helper

只读分析 Git 三方冲突，产出**自包含的可执行契约**：

- `merge-resolution-report.md`：第 1-12 章供人评审，第 14 章（执行指引）供 Agent 直接执行。
- `merge-plan.json`：结构化执行契约，供脚本做确定性校验。

## 安装

```text
<repo>/.agents/skills/code-merge-helper/
```

## 调用

```text
$code-merge-helper 分析当前冲突，生成报告和执行计划，不修改代码。
```

分析阶段始终以 `WAITING_FOR_APPROVAL` 结束。批准后 Agent 直接按报告第 14 章执行，无需加载其他 Skill。
