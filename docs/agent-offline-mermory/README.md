# agent-offline-mermory 使用说明

## 适用场景

- 跨会话管理未完成任务、交接文档和可复用经验（如 Git 提交踩坑、部署注意事项）。
- 记忆根目录可位于 Obsidian 仓库内（默认校验 `.obsidian`），也支持纯 Markdown 文件夹（`require_obsidian=false`）。
- 经验加载支持 `auto`（默认）与 `manual` 两种模式，用于技术流程前的只读风险提醒或按需查询。

## 快速使用

```text
请使用 agent-offline-mermory 查询尚未完成的任务
```

- 执行规则：[SKILL.md](../../.opencode/skills/agent-offline-mermory/SKILL.md)
- 配置模板：[settings.example.json](../../.opencode/skills/agent-offline-mermory/settings.example.json)
- 写入脚本：[write-memory.py](../../.opencode/skills/agent-offline-mermory/scripts/write-memory.py)

## 初始化（首次使用必做）

安装后必须初始化，否则查询和写入会被拒绝。

Windows：

```powershell
& "...\agent-offline-mermory\scripts\write-memory.ps1" -Action Init -MemoryRoot "<记忆根目录>" -RequireObsidian True -ExperienceMode Auto
& "...\agent-offline-mermory\scripts\write-memory.ps1" -Action Status
```

Linux 或 macOS：

```sh
sh ".../agent-offline-mermory/scripts/write-memory.sh" --action init --memory-root "<记忆根目录>" --require-obsidian true --experience-mode auto
sh ".../agent-offline-mermory/scripts/write-memory.sh" --action status
```

初始化创建 `Inbox`、`Tasks`、`Knowledge` 目录、入口文档和 `_index.md` 索引；每次写入后自动刷新索引。

## 核心流程

1. 检查是否已初始化（`status`），未初始化先询问用户并执行 `init`。
2. 按 `experience_mode` 决定是否在可重复技术流程前只读检索 `Knowledge`。
3. 按用户意图查询 `Tasks` / `Knowledge` / `Inbox`。
4. 写入或更新记录；写入后自动刷新 `Tasks/`、`Knowledge/` 索引。
5. 向用户报告记录类型、新建/更新、绝对路径和索引刷新情况。

## 常用命令

查询待办（Windows）：

```powershell
& "...\write-memory.ps1" -Action Query -Type Task -Status Active -Limit 10
```

查询经验（Linux 或 macOS）：

```sh
sh ".../write-memory.sh" --action query --type knowledge --query "git 提交" --limit 5
```

记录知识（Windows）：

```powershell
$content = @'
<Markdown 内容>
'@
& "...\write-memory.ps1" -Action Capture -Type Knowledge -Title "<标题>" -Content $content
```

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
