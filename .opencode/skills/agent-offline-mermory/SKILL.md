---
name: agent-offline-mermory
description: 管理用户配置的本地 AI 协作记忆（Obsidian 仓库或纯 Markdown 文件夹）：在用户明确调用 `$agent-offline-mermory`、从 Skill 菜单选择本 Skill，或明确要求使用 agent-offline-mermory 时，先只读检索当前请求相关的 Knowledge，再按要求写入记录或查询待办与经验；经验加载模式默认为 auto，在执行 Git、代码修改、测试、构建、部署、环境配置或其他可重复技术流程时，仅自动只读检索相关 Knowledge 作为风险提醒；可选 manual 模式，仅在明确调用本 Skill 时加载经验。安装后必须先初始化记忆根目录，未初始化时只允许 status/init。没有匹配经验时必须明确告知用户，不能硬加载不存在或无关的经验。普通总结、闲聊和一般提问不得触发。
---

# Agent Offline Mermory

管理本地的 AI 协作记忆，支持两种记忆根目录：Obsidian 仓库（默认校验 `.obsidian`）和纯 Markdown 文件夹。这个 Skill 有两种触发模式：明确触发模式负责写入和主动查询；自动回忆模式只负责在相似技术流程前只读检索经验。

## 首次使用必读：初始化

安装后必须初始化记忆根目录，否则查询和写入都会被拒绝。未初始化时不得自动猜测路径，必须停下，优先用对话引导用户完成初始化。初始化只需确认三件事：

- 记忆根目录绝对路径；
- 是否要求位于 Obsidian 仓库内（`require_obsidian`，默认 `true`，可选 `false` 使用纯文件夹）；
- 经验加载模式（`experience_mode`，默认 `auto`，可选 `manual`）。

推荐按以下顺序选择初始化方式：

### 方式一：对话初始化（首选）

用户只需要说“初始化 agent-offline-mermory”或首次使用时要求查询/写入，Agent 通过对话确认上面三件事（例如：请用户提供或帮助选择记忆根目录路径，确认是否使用 Obsidian，确认经验模式），然后代为调用写入器完成初始化。全程用户不需要敲任何命令。完成后用中文向用户报告记忆根目录、模式选择和后续用法。

### 方式二：命令行交互式

用户运行短命令，写入器会逐步提问（路径、是否 Obsidian、经验模式），不需要一次输入所有参数：

```powershell
& "<Skill目录>\scripts\write-memory.ps1" -Action Init
```

```sh
sh "<Skill目录>/scripts/write-memory.sh" --action init
```

### 方式三：编辑配置文件

1. 将 `settings.example.json` 复制为 `settings.json`；
2. 修改其中的 `memory_root`（记忆根目录绝对路径）、`require_obsidian`、`experience_mode`；
3. 在终端运行 `-Action Init`（短命令）交互确认，或让 Agent 读取配置后代为完成初始化。

初始化会创建 `Daily`、`Tasks`、`Knowledge` 三个目录、一个与记忆根目录同名的入口文档，以及三个目录各自的 `_index.md` 索引。之后每次写入或更新记录，写入器会自动刷新全部索引。

## 经验加载模式

- `auto`（默认）：当前任务确实涉及 Git、代码修改、测试、构建、部署、环境配置、迁移或其他可重复技术流程时，执行一次只读检索 `Knowledge`，严格相关性过滤、最多 3 条，作为风险提醒；不写入任何内容。
- `manual`：只有用户明确调用 `$agent-offline-mermory` 时才加载经验，其余任务完全不检索，减少不必要的调用和 token 消耗。
- 对话内可临时覆盖：用户说“这次不用加载经验”时，单次跳过检索，不需要改配置。
- 修改方式：通过对话让 Agent 重新执行 `init`，或运行 `set-root` / `SetRoot` 短命令，写入器会沿用已有配置并逐步提问。

## 判断触发模式

- 明确触发包括：用户输入 `$agent-offline-mermory`、从 Skill 菜单选择本 Skill，或明确说“使用 agent-offline-mermory”。明确触发后，除纯状态查询和初始化外，先执行一次相关经验预检，再按用户要求执行写入或主动查询。
- 自动回忆（仅 `auto` 模式）只在当前任务确实涉及 Git、代码修改、测试、构建、部署、环境配置、迁移或其他可重复技术流程时执行，并且只能查询 `Knowledge`；`manual` 模式下不得执行自动回忆。
- 自动回忆模式不得写入、更新、初始化或修改任何文件，也不得查询 `Tasks` 或 `Daily`。
- 每日总结只能在用户明确调用本 Skill 时写入，不得在任务结束后自动生成或追加总结。
- 普通的“总结一下”“记住这个”“有哪些待办”或“某类操作有哪些经验”等请求，如果没有明确触发，只在当前上下文中回答，不读取记忆目录。
- 不得写入已配置记忆根目录之外的位置。
- 不得自行推断应该更新某个已有任务或知识文档。
- 仅当用户明确提供文件路径、准确文档名或 Obsidian 链接时，才更新已有文档。

自动回忆的查询失败、配置不存在或没有高相关结果时，继续当前任务，不创建记录，也不把失败升级为写入请求。只有检索结果与当前操作明确相关时，才将其压缩成风险提醒并应用；不得让历史经验覆盖当前仓库、当前命令或用户的明确要求。

## 明确触发后的经验预检

用户明确调用本 Skill 后，先从当前请求和当前任务中提取 2–6 个具体关键词，只读查询 `Knowledge`，最多加载 3 条高相关经验，然后继续执行用户要求的操作。

- 用户明确查询某类经验时，该查询本身就是经验检索，不要重复执行同一次预检。
- 用户要求写入记录、整理交接文档或记录踩坑时，先按当前主题检索相关 `Knowledge`。
- 只有关键词有明确匹配且内容与当前任务直接相关时，才算“已加载经验”；不得把模糊、无关或不存在的文档当作匹配结果。
- 找到高相关经验时，先用中文简要说明已加载哪些经验及其适用范围，再继续当前操作。
- 没有匹配、记忆目录未初始化、查询失败或相关度不足时，必须明确告知用户“未找到相关经验”，并说明不会硬加载无关内容；随后仍继续当前任务。
- 经验只作为提醒和参考，不能覆盖用户的明确要求、当前仓库事实、当前命令输出或最新验证结果。

示例：

```text
$agent-offline-mermory 记录这次 Git 提交踩坑

执行顺序：
1. 只读查询 Knowledge，关键词为“Git 提交 踩坑”
2. 有高相关结果：说明已加载的经验，再新建 Knowledge 记录
3. 没有匹配：明确告知“未找到相关 Git 提交经验”，再新建 Knowledge 记录
```

触发示例：

- `初始化 agent-offline-mermory`：未初始化时触发，通过对话确认三件事并完成初始化。
- `$agent-offline-mermory 把当前任务整理成交接文档`：明确触发，创建 `Task`。
- `$agent-offline-mermory 有哪些待办需要处理`：明确触发，只读查询 `Tasks`。
- `$agent-offline-mermory 查询 Git 提交经验`：明确触发，只读查询 `Knowledge`。
- `$agent-offline-mermory 记录这次部署踩坑`：明确触发，先预检 `Knowledge`，再新建知识记录。
- `$agent-offline-mermory 记录今天的每日总结`：明确触发，写入或追加当天的 `Daily` 总结。
- `$agent-offline-mermory 把经验加载模式改成 manual`：明确触发，重新初始化或 `set-root` 时切换模式。
- `这次不用加载经验`：对话内临时跳过本次经验检索，不修改配置。
- `请修改这个函数并补测试`：`auto` 模式下如果确实开始执行代码修改，可自动回忆相关 `Knowledge`，但不能写入记忆；`manual` 模式下不检索。
- `总结一下刚才的聊天`、`有哪些待办`：没有明确触发，不读取记忆目录。

## 使用 Skill 自带的写入器

以本 `SKILL.md` 所在目录为 Skill 根目录解析所有路径。Agent 发起的配置和记忆写入操作都必须使用自带写入器，不得绕过其路径检查直接写入文件。唯一例外是 Obsidian 首页中的“手动记录”：它只在用户点击、选择类型并确认后，使用 Obsidian Vault API 在当前记忆根目录的 `Daily`、`Tasks` 或 `Knowledge` 中按内置模板创建文件并刷新该目录的 `_index.md`；不得后台触发、不得写到其他目录、不得覆盖已有的当天总结。

根据当前平台选择入口：

- Windows PowerShell：`scripts/write-memory.ps1`
- Linux 或 macOS Shell：`scripts/write-memory.sh`
- 任意安装了 Python 3 的平台：`scripts/write-memory.py`

PowerShell 和 Shell 文件只是同一 Python 核心的启动入口。三种入口共用 `settings.json`、`assets/templates` 中的模板和相同的路径安全规则。需要 Python 3.8 或更高版本。

## 只读查询

查询只扫描已配置记忆根目录中的 `Daily`、`Tasks` 和 `Knowledge` Markdown 文件，不修改任何内容，并且跳过 `_index.md` 索引文件本身。想了解全貌时，可以直接阅读 `Tasks/_index.md`、`Knowledge/_index.md` 或 `Daily/_index.md`。

按用户意图选择范围：

- “有哪些待办需要处理”：查询 `Task`，状态选择 `Active`。
- “Git 提交有哪些经验”：查询 `Knowledge`，关键词使用 `git 提交`。
- 用户未指定分类：查询 `All`。

Windows：

```powershell
& "<Skill目录>\scripts\write-memory.ps1" `
  -Action Query `
  -Type Task `
  -Status Active `
  -Limit 10

& "<Skill目录>\scripts\write-memory.ps1" `
  -Action Query `
  -Type Knowledge `
  -Query "git 提交" `
  -Limit 5

& "<Skill目录>\scripts\write-memory.ps1" `
  -Action Query `
  -Type Daily `
  -Query "今日总结" `
  -Limit 5
```

Linux 或 macOS：

```sh
sh "<Skill目录>/scripts/write-memory.sh" \
  --action query \
  --type task \
  --status active \
  --limit 10

sh "<Skill目录>/scripts/write-memory.sh" \
  --action query \
  --type knowledge \
  --query "git 提交" \
  --limit 5

sh "<Skill目录>/scripts/write-memory.sh" \
  --action query \
  --type daily \
  --query "今日总结" \
  --limit 5
```

返回结果包含类型、标题、状态、绝对路径、匹配摘要和相关度。用中文概括结果，并提供可点击的绝对文件路径。没有匹配时明确说明未找到，不得改为扫描记忆根目录之外的位置。

自动回忆模式的调用方式：

```text
查询类型：Knowledge
关键词：从当前技术任务提取 2–6 个具体词，例如 git 提交 hooks
数量：最多 3 条
```

自动回忆只采用有明确关键词匹配的结果，重点关注前置检查、已知坑、验证方法和回滚方式。没有高相关结果时，不向用户展示无关的历史记录。

## 初始化或修改记忆目录

首次使用时，如果不存在 `settings.json`，优先通过对话询问用户希望使用的记忆根目录，并确认 `require_obsidian` 与 `experience_mode`，然后代为执行。用户也可以自行运行短命令进入交互式提问：

Windows：

```powershell
& "<Skill目录>\scripts\write-memory.ps1" -Action Init
& "<Skill目录>\scripts\write-memory.ps1" -Action Status
& "<Skill目录>\scripts\write-memory.ps1" -Action SetRoot
```

Linux 或 macOS：

```sh
sh "<Skill目录>/scripts/write-memory.sh" --action init
sh "<Skill目录>/scripts/write-memory.sh" --action status
sh "<Skill目录>/scripts/write-memory.sh" --action set-root
```

- `require_obsidian` 为 `true` 时，目标目录本身或其某一级父目录必须包含 `.obsidian`；为 `false` 时，任意 Markdown 文件夹即可，纯文件夹模式下 `[[Tasks/example]]` 链接按相对路径解析，同样可用。
- 初始化会创建 `Daily`、`Tasks`、`Knowledge` 三个目录、一个与记忆根目录同名的入口文档，以及 `Tasks/_index.md`、`Knowledge/_index.md`、`Daily/_index.md` 索引。
- Obsidian 模式下入口文档是带 Dataview 统计的仪表盘（需启用社区插件 Dataview）；重新执行 `init` 或 `set-root` 时，检测到旧版入口会自动升级，不影响已有记录。
- `set-root` / `SetRoot` 默认沿用已有配置（`require_obsidian`、`experience_mode`）；Agent 代为调用时可以直接传参数避免交互式阻塞。

## 判断记录类型

按以下优先级选择：

1. 用户明确指定记录位置或类型时，遵从用户要求。
2. 未完成事项、当前进度、阻塞问题、后续步骤和可恢复的交接内容记录到 `Task`。
3. 可复用的问题原因、解决方案、验证方法、工作流程、提示词或经验教训记录到 `Knowledge`。
4. 内容零散、暂时无法分类、一般摘要或当天进展统一记录到当天的 `Daily` 每日总结。

只有当会话中同时存在“未完成任务”和“可以独立复用的经验”时，才分别创建任务文档和知识文档。不得在两个文档中重复堆放相同内容。

## 组织记录内容

使用简短且能说明内容的标题。

任务交接文档优先使用：

```markdown
## 目标
## 进度与下一步
## 阻塞与风险
## 关键文件与命令
```

省略空章节。保留恢复任务所需的准确路径、命令、已经确认的决定和尚未解决的问题。

示例：

```markdown
## 目标
- 完成 write-memory.py 的 Inbox 到 Daily 迁移并提交

## 进度与下一步
- 已完成：脚本与模板改造、本地验证
- 下一步：提交并推送远程

## 阻塞与风险
- 无

## 关键文件与命令
- .opencode/skills/agent-offline-mermory/scripts/write-memory.py
- git push origin dev
```

知识文档优先使用：

```markdown
## 场景
## 问题与原因
## 解决方案与验证
## 注意事项
```

省略空章节。记录可复用结论，不要照搬完整聊天记录。

示例：

```markdown
## 场景
- 在 Windows 上运行跨平台 Python 脚本时

## 问题与原因
- 脚本报路径错误；原因是硬编码了反斜杠分隔符

## 解决方案与验证
- 改用 pathlib.Path 拼接路径，测试通过

## 注意事项
- 纯文本模式不校验 Obsidian，链接按相对路径解析
```

可在知识或任务文档的 frontmatter 中添加 `tags: [git, 部署]`，仪表盘会按标签统计。

每日总结文档按日期一个文件，优先使用：

```markdown
## 完成
## 问题
## 明日计划
```

省略空章节。只记录当天实际发生或计划的内容，不重复搬运 Task 和 Knowledge 中的细节。

示例：

```markdown
## 完成
- 完成 write-memory.py 的 Inbox 到 Daily 重命名，临时目录验证通过

## 问题
- Windows 控制台中文乱码；原因：编码未切换；处理：脚本已用 UTF-8 输出，已解决

## 明日计划
- 提交并推送本次改动，同步安装副本
```

## 新建记录

如果用户没有明确指定已有目标文档，不传目标文件参数。`Task` 和 `Knowledge` 每次新建独立文档，`Daily` 追加到当天的每日总结中（首次创建、之后追加“补充”小节）。写入完成后，写入器自动刷新 `Tasks/_index.md`、`Knowledge/_index.md` 和 `Daily/_index.md`。Obsidian 首页的“手动记录”是显式人工入口：选择任务或知识时要求填写标题并新建独立文件；选择总结时创建或打开当天文件；三类文件都直接预置对应章节，不复制 Agent 提示词。

Windows：

```powershell
$content = @'
<Markdown 内容>
'@
& "<Skill目录>\scripts\write-memory.ps1" `
  -Action Capture `
  -Type Task `
  -Title "<标题>" `
  -Content $content

& "<Skill目录>\scripts\write-memory.ps1" `
  -Action Capture `
  -Type Daily `
  -Title "每日总结" `
  -Content $content
```

Linux 或 macOS：

```sh
sh "<Skill目录>/scripts/write-memory.sh" \
  --action capture \
  --type task \
  --title "<标题>" \
  --content-stdin <<'EOF'
<Markdown 内容>
EOF

sh "<Skill目录>/scripts/write-memory.sh" \
  --action capture \
  --type daily \
  --title "每日总结" \
  --content-stdin <<'EOF'
<Markdown 内容>
EOF
```

## 更新用户明确指定的文档

只有当用户明确指出已有文档时，才传入目标文件参数。

Windows：

```powershell
& "<Skill目录>\scripts\write-memory.ps1" `
  -Action Capture `
  -Type Task `
  -Title "<本次更新标题>" `
  -Content $content `
  -TargetFile "Tasks\<已有文档>.md"
```

Linux 或 macOS：

```sh
sh "<Skill目录>/scripts/write-memory.sh" \
  --action capture \
  --type task \
  --title "<本次更新标题>" \
  --target-file "Tasks/<已有文档>.md" \
  --content-stdin <<'EOF'
<Markdown 更新内容>
EOF
```

目标可以是绝对路径、相对于记忆根目录的路径，或 `[[Tasks/example]]` 形式的 Obsidian 链接。写入器必须拒绝不存在的目标、非 Markdown 文件、通过符号链接逃逸的路径，以及记忆根目录之外的路径。

## 向用户报告结果

操作成功后，使用中文说明：

- 记录类型；
- 是新建还是更新；
- 输出文件的绝对路径；
- 是否额外创建了其他记录（例如索引文件刷新）。

如果写入器返回错误，直接报告错误，不得静默改写到其他位置。
