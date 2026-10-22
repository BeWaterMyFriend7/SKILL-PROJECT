# agent-offline-mermory 使用手册

记录保存在本地 Markdown 文件中，支持普通文件夹和 Obsidian。

| 分类 | 用途 |
| --- | --- |
| Daily | 当天重要结果、形成经验、形成原则、待处理的摘要或引用 |
| Experience | 一个具体场景的问题与实际有效处理方式 |
| Principle | 带适用条件、可跨场景复用的原则和行动 |
| Task | 下一步明确行动，状态为 todo / doing / done |

完整正文模板、分类标准和表达约束见 [Skill 规则](../../.opencode/skills/agent-offline-mermory/SKILL.md)。

## 初始化

对 Agent 说“初始化 agent-offline-mermory”，确认记忆根目录、是否使用 Obsidian、经验模式。也可运行：

```sh
python <Skill目录>/scripts/write-memory.py --action init --memory-root "<绝对路径>" --require-obsidian false --experience-mode auto
```

Windows 可使用 scripts/write-memory.ps1 -Action Init，Linux/macOS 可使用 scripts/write-memory.sh --action init。

目录为 Daily、Experience、Principle、Task，每类有 _index.md。普通 Markdown 首页提供四类索引入口；Obsidian 首页提供统计、搜索、列表和四类手动建档，需要启用 Dataview 及 JavaScript 查询。dashboard_limit 控制每区条数（1–100）；搜索过滤当前展示列表。

## 升级旧记录

重新初始化会备份旧 Tasks、Knowledge 到记忆根目录 .migration-backup，再全部归入 Experience/Tasks、Experience/Knowledge，保留原正文和附件，类型设为 agent-experience。不保留旧类型查询，不把旧任务作为新 Task。备份不参与索引和检索。

迁移改变分类而不补写事实或提炼原则。实际记忆库需在明确执行初始化升级时迁移；仓库代码更新不会自动修改外部笔记。

## 对话示例

```text
$agent-offline-mermory 记录这次问题的有效处理方式
$agent-offline-mermory 提炼这几次经验中有适用条件的通用原则
$agent-offline-mermory 查询待处理任务
$agent-offline-mermory 记录今天的每日总结
```

auto 模式在可重复技术流程前只读加载适用 Principle 和相关 Experience；manual 仅明确调用时加载。没有高相关结果时说明未找到，继续工作。普通对话不写入，Daily 不自动生成。

## 内容原则

一条记录一个主题，一句话一个事实。可选字段和空栏目省略。Task 明确下一步行动，Experience 保留具体事实，Principle 必须带适用条件。独立记录通过 Daily 引用，避免重复搬运。

首页手动建档提供必需字段供填写；保存笔记前删除无内容栏目。当天 Daily 已存在则打开，不覆盖。
