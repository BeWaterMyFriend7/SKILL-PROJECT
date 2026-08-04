# agent-offline-mermory 使用说明

## 适用场景

- 跨会话管理未完成任务、交接文档和可复用经验（如 Git 提交踩坑、部署注意事项）。
- 记忆根目录可位于 Obsidian 仓库内（默认校验 `.obsidian`），也支持纯 Markdown 文件夹（`require_obsidian=false`）。
- 经验加载支持 `auto`（默认）与 `manual` 两种模式，用于技术流程前的只读风险提醒或按需查询。

## 触发方式

这个 Skill 只有在**明确触发**时才会读写记忆，普通对话不会偷偷读取你的记忆目录。

- **明确触发**：对话中说 `$agent-offline-mermory`、说“使用 agent-offline-mermory”，或从 Skill 菜单选择本 Skill。明确触发后才会执行查询、写入、整理交接等操作。
- **自动回忆（仅 auto 模式）**：当任务确实涉及 Git、代码修改、测试、构建、部署、环境配置等可重复技术流程时，开始前只读检索 `Knowledge` 作为风险提醒，不写入任何内容。
- **不触发**：普通总结、闲聊和一般提问（如“总结一下刚才的聊天”）不会读取记忆目录，也不会加载经验。

使用示例统一以 `$agent-offline-mermory` 开头，表示这是明确调用。首次使用初始化是唯一不需要前缀的特殊情况，见下文。

## 经验加载模式

初始化时可以选定经验加载模式，之后可随时修改：

- `auto`（默认）：可重复技术流程开始前自动只读检索 `Knowledge`，最多 3 条，严格按相关度过滤；没有匹配时明确告知“未找到相关经验”，不会硬加载无关内容。适合需要风险提醒、可接受少量额外调用的场景。
- `manual`：只有明确调用 `$agent-offline-mermory` 时才加载经验，其余任务完全不检索。适合在意 token、任务多为一次性的场景。
- **临时跳过**：对话中说“这次不用加载经验”，本次任务跳过检索，不修改配置。
- **修改方式**：对 Agent 说“把经验加载模式改成 manual/auto”，Agent 会重新执行初始化并保留当前记忆根目录。

## 快速使用

所有操作都通过对话完成，不需要手敲命令。第一次使用需要先初始化（见下节），之后用 `$agent-offline-mermory` 明确触发即可：

```text
$agent-offline-mermory 查询尚未完成的任务
```

- 执行规则：[SKILL.md](../../.opencode/skills/agent-offline-mermory/SKILL.md)
- 配置模板：[settings.example.json](../../.opencode/skills/agent-offline-mermory/settings.example.json)

## 初始化（首次使用必做）

安装后必须初始化，否则查询和写入都会被拒绝。初始化只需要确认三件事，每件事都有实际意义：

1. **记忆根目录路径**：所有记录（任务、经验、临时笔记）存放的位置。它同时是安全边界——之后所有读写都只发生在这个目录内，防止写错地方。
2. **是否要求 Obsidian（`require_obsidian`）**：选 `true`（默认）要求目录位于 Obsidian 仓库内，记录可被 Obsidian 双链、图谱检索；选 `false` 则任意 Markdown 文件夹都可以，更自由，不依赖 Obsidian。
3. **经验加载模式（`experience_mode`）**：决定技术流程前是否自动加载经验提醒（`auto`）还是只用不加载（`manual`），见上文“经验加载模式”。

初始化会创建 `Inbox`、`Tasks`、`Knowledge` 三个目录、一个入口文档和 `_index.md` 索引；之后每次写入或更新记录，索引自动刷新，无需手动维护。

三种初始化方式任选其一：

### 方式一：对话初始化（推荐）

直接对 Agent 说：

```text
初始化 agent-offline-mermory
```

Agent 会通过对话逐一确认上面三件事（例如：请用户提供或帮助选择记忆根目录路径，确认是否使用 Obsidian，确认经验模式），然后代为完成初始化，并告诉你记忆根目录和后续用法。全程不需要敲任何命令。

### 方式二：命令行交互式

运行短命令，写入器会逐步提问（路径、是否 Obsidian、经验模式），不需要一次输入所有参数：

```powershell
& "<Skill目录>\scripts\write-memory.ps1" -Action Init
```

```sh
sh "<Skill目录>/scripts/write-memory.sh" --action init
```

### 方式三：编辑配置文件

如果不希望对话，也可以手动配置：

1. 将 `settings.example.json` 复制为 `settings.json`；
2. 修改其中的 `memory_root`（记忆根目录绝对路径）、`require_obsidian`、`experience_mode`；
3. 对 Agent 说“已完成初始化配置，请继续”，Agent 会读取配置完成初始化。

## 使用示例

以下示例都是明确触发（带 `$agent-offline-mermory`），可以直接照用。

### 示例 1：查询待办

```text
$agent-offline-mermory 有哪些待办需要处理？
```

Agent 查询 `Tasks` 中状态为 Active 的记录，列出标题、状态和文件路径。

### 示例 2：记录任务交接

```text
$agent-offline-mermory 把当前任务整理成交接文档
```

Agent 将当前任务的背景、进度、阻塞、下一步和关键文件整理成 Markdown，写入 `Tasks/`，并告知你文件路径。

### 示例 3：记录踩坑经验

```text
$agent-offline-mermory 记录这次 Git 提交踩坑：hooks 没生效，提交前先检查 .git/hooks
```

Agent 先只读检索 `Knowledge` 中已有的 Git 相关经验（有高相关结果时会先说明），再新建一条知识记录。

### 示例 4：查询经验

```text
$agent-offline-mermory Git 提交有哪些经验？
```

Agent 只读查询 `Knowledge`，按相关度返回最多 5 条并附摘要，没有匹配时明确告知未找到。

### 示例 5：更新已有文档

```text
$agent-offline-mermory 把“红包系统部署”这篇任务的下一步更新为：环境变量已配置，开始验证
```

Agent 定位你指出的已有文档，追加更新内容并刷新索引，同时报告更新后的路径。

### 示例 6：切换经验加载模式

```text
$agent-offline-mermory 把经验加载模式改成 manual，只在我说用的时候再加载
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
3. 明确触发后，按用户意图查询 `Tasks` / `Knowledge` / `Inbox`。
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
