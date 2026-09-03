---
type: agent-memory-index
dashboard_version: 1
created: "{{timestamp}}"
---

# {{name}}

用于保存 AI 协作过程中的每日总结、任务交接和可复用经验。

## 目录

- `Daily/`：每日总结
- `Tasks/`：未完成任务与交接文档
- `Knowledge/`：经验、踩坑和可复用方案

## 写入原则

- 只有显式调用 `agent-offline-mermory` 才写入。
- 没有明确指定已有文档时，任务和知识记录一律新建。
- 所有内容均限制在本目录内。
