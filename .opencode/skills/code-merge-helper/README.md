# code-merge-helper

只读分析 Git 三方冲突，产出**自包含的可执行契约**——单一 Markdown 文件：

- 第 1-12 章供人评审
- 第 14 章（执行指引）供 Agent 直接执行
- 附录 A：JSON 执行契约（fenced code block），供脚本做确定性校验

## 安装

```text
<repo>/.agents/skills/code-merge-helper/
```

## 调用

```text
$code-merge-helper 分析当前冲突，生成报告，不修改代码。
```

分析阶段始终以 `WAITING_FOR_APPROVAL` 结束。批准后 Agent 直接按报告第 14 章执行，无需加载其他 Skill。

## 与其他 Skill 的协作

- **code-change-plan**：当合并涉及大规模重构或新功能引入时，建议先用 `code-change-plan` 生成变更方案，再在合并分析报告中引用该方案的 plan-id。
- 如果在执行 code-change-plan 过程中发现需要先解决合并冲突，应暂停并建议使用本 Skill 完成三方合并分析。

## 自检

```bash
python scripts/run_evals.py
```

检查：文件完整性、Schema 合法性、脚本语法、模板完整性、参考文档覆盖。
