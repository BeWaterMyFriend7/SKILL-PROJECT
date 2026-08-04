# agent-offline-mermory 使用说明

## 适用场景

- 跨会话管理未完成任务、交接文档和可复用经验（如 Git 提交踩坑、部署注意事项）。
- 记忆根目录可位于 Obsidian 仓库内（默认校验 `.obsidian`），也支持纯 Markdown 文件夹（`require_obsidian=false`）。
- 经验加载支持 `auto`（默认）与 `manual` 两种模式，用于技术流程前的只读风险提醒或按需查询。

## 快速使用

所有操作都通过对话完成，不需要手敲命令。直接对 Agent 说：

```text
请使用 agent-offline-mermory 查询尚未完成的任务
```

首次使用时 Agent 会引导完成初始化（见下节），之后的查询和写入都可以用日常语言表达。

- 执行规则：[SKILL.md](../../.opencode/skills/agent-offline-mermory/SKILL.md)
- 配置模板：[settings.example.json](../../.opencode/skills/agent-offline-mermory/settings.example.json)

## 初始化（首次使用必做）

安装后必须初始化，否则查询和写入会被拒绝。初始化只需要确认三件事：记忆根目录路径、是否使用 Obsidian、经验加载模式。

### 方式一：对话初始化（推荐）

直接对 Agent 说：

```text
初始化 agent-offline-mermory
```

Agent 会通过对话逐一确认上面三件事，然后代为完成初始化，并告诉你记忆根目录和后续用法。全程不需要敲任何命令。

### 方式二：编辑配置文件

如果不希望对话，也可以手动配置：

1. 将 `settings.example.json` 复制为 `settings.json`；
2. 修改其中的 `memory_root`（记忆根目录绝对路径）、`require_obsidian`、`experience_mode`；
3. 对 Agent 说“已完成初始化配置，请继续”，Agent 会读取配置完成初始化。

初始化会创建 `Inbox`、`Tasks`、`Knowledge` 目录、入口文档和 `_index.md` 索引；之后每次写入或更新记录，索引自动刷新，无需手动维护。

## 使用示例

以下是常见场景的对话示例，可以直接照用。

### 示例 1：查询待办

```text
有哪些待办需要处理？
```

Agent 查询 `Tasks` 中状态为 Active 的记录，列出标题、状态和文件路径。也可以用更明确的说法：

```text
使用 agent-offline-mermory 查看所有未完成的任务
```

### 示例 2：记录任务交接

```text
请把当前任务整理成交接文档
```

Agent 将当前任务的背景、进度、阻塞、下一步和关键文件整理成 Markdown，写入 `Tasks/`，并告知你文件路径。

### 示例 3：记录踩坑经验

```text
记录这次 Git 提交踩坑：hooks 没生效，提交前先检查 .git/hooks
```

Agent 先只读检索 `Knowledge` 中已有的 Git 相关经验（有高相关结果时会先说明），再新建一条知识记录。

### 示例 4：查询经验

```text
Git 提交有哪些经验？
```

Agent 只读查询 `Knowledge`，按相关度返回最多 5 条并附摘要，没有匹配时明确告知未找到。

### 示例 5：更新已有文档

```text
把“红包系统部署”这篇任务的下一步更新为：环境变量已配置，开始验证
```

Agent 定位你指出的已有文档，追加更新内容并刷新索引，同时报告更新后的路径。

### 示例 6：切换经验加载模式

```text
把经验加载模式改成 manual，只在我说用的时候再加载
```

Agent 重新执行初始化并保留当前记忆根目录，将 `experience_mode` 切换为 `manual`。

### 示例 7：单次跳过经验加载

```text
这次不用加载经验，直接开始
```

Agent 本次任务跳过经验检索，不修改任何配置；后续任务按原有模式继续。

## 核心流程

1. 检查是否已初始化，未初始化先引导用户完成初始化。
2. 按 `experience_mode` 决定是否在可重复技术流程前只读检索 `Knowledge`。
3. 按用户意图查询 `Tasks` / `Knowledge` / `Inbox`。
4. 写入或更新记录；写入后自动刷新 `Tasks/`、`Knowledge/` 索引。
5. 向用户报告记录类型、新建/更新、绝对路径和索引刷新情况。

## 记忆目录结构

```text
<记忆根目录>/
├── <记忆根目录名>.md        # 入口文档
├── Inbox/                    # 临时记录（按天）
├── Tasks/                    # 任务交接与待办
│   └── _index.md             # 自动维护的任务索引
└── Knowledge/                # 可复用经验
    └── _index.md             # 自动维护的知识索引
```
