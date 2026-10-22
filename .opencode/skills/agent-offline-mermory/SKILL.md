---
name: agent-offline-mermory
description: 管理本地 Markdown 或 Obsidian 中的 Daily、Experience、Principle、Task。明确调用时查询或写入；auto 模式在可重复技术流程前只读检索相关原则和场景经验，manual 模式仅明确调用时检索。普通总结和闲聊不触发。
---

# Agent Offline Mermory

Memory 是供人和 AI 快速读取、检索和复用的信息单元，表达必须准确、直接、易懂、高信息密度。

## 初始化与边界

以本 SKILL.md 所在目录解析脚本、模板和 settings.json。先执行 status；未配置时只允许 status/init，不猜测用户记忆目录。初始化确认绝对路径、require_obsidian（默认 true）、experience_mode（auto 默认 / manual）。

Windows 使用 scripts/write-memory.ps1，其他平台使用 scripts/write-memory.sh，也可直接运行 Python 3.8+ 的 scripts/write-memory.py。两个包装脚本共用 Python 核心。

```sh
python scripts/write-memory.py --action status
python scripts/write-memory.py --action init --memory-root "<绝对路径>" --require-obsidian false --experience-mode auto
```

Obsidian 模式要求当前目录或父目录包含 .obsidian。初始化创建 Daily、Experience、Principle、Task 及各自 _index.md、同名 Markdown 首页。Obsidian 首页需要 Dataview 和 JavaScript 查询；普通 Markdown 首页使用标准相对链接。重新初始化升级首页。

旧 Tasks、Knowledge 全部迁移为 Experience，不兼容旧类型查询。初始化先在根目录 .migration-backup 下备份，再将旧目录归入 Experience/Tasks、Experience/Knowledge，保留正文和附件并改为 agent-experience。不会把旧任务变成新 Task，也不自动提炼 Principle。迁移后报告数量、备份路径；备份不参与检索。升级代码本身不等于授权修改用户的实际记忆库。

所有 Agent 写入经过写入器，限制在配置根目录内。Obsidian 手动建档仅在用户点击确认后通过 Vault API 写入四个分类之一，已有当天总结只打开，不覆盖。

## 触发与检索

- 明确调用 $agent-offline-mermory、菜单选择或要求使用本 Skill，才执行主动查询或写入。
- auto 模式在 Git、修改代码、测试、构建、部署等可重复技术流程前，只读检索 Principle，再补充高度相关 Experience，总计最多 3 条；manual 模式仅明确调用时检索。
- 自动回忆不写入、不初始化、不查询 Task/Daily。用户说本次跳过经验时，跳过本次，不改配置。
- 普通总结、闲聊不读取记忆库。Daily 不在任务完成后自动生成。
- 明确写入前按主题检索相似原则和经验，避免重复。查询本身是预检时不重复调用。
- 无配置、失败或无高相关匹配时说明“未找到相关经验”，继续原任务，不加载无关记录。
- 原则必须满足适用条件；旧经验不覆盖用户指示或当前事实。

```sh
python scripts/write-memory.py --action query --type principle --query "git hooks" --limit 3
python scripts/write-memory.py --action query --type experience --query "git hooks" --limit 3
python scripts/write-memory.py --action query --type task --status todo --limit 10
python scripts/write-memory.py --action query --type task --status doing --limit 10
```

查询只扫描四个分类，跳过 _index.md；需要全貌时读取索引。待办包括 todo 和 doing。Daily 是时间索引，需细节时读取关联记录，避免重复加载。

## 分类与正文模板

一条 Memory 一个主题。用户明确类型时遵从用户要求；否则按以下语义分类。模板里的方括号是说明，不得原样写入；可选字段、无内容栏目省略。

### Daily｜每日总结

记录当天重要变化，已形成独立记录的内容只保留摘要或引用，不搬运完整过程。

```markdown
# YYYY-MM-DD

## 完成
- [重要结果]

## 形成经验
- [Experience 标题/引用]

## 形成原则
- [Principle 标题/引用]

## 待处理
- [Task 标题/引用]
```

### Experience｜场景经验

一个具体场景中，一个问题如何解决。强调发生了什么、怎么解决，不主动上升为通用结论。

```markdown
# [经验标题]

- 场景：[问题发生的上下文]
- 问题：[具体问题或现象]
- 原因：[已确认原因，可选]
- 处理：[实际有效的处理方式]
- 结果：[处理结果，可选]
- 适用：[适用场景或限制，可选]
```

原因未知就省略；未验证处理不得写成有效方案；历史迁移仅归类，不编造事实补齐模板。

### Principle｜通用原则

能指导下一次类似问题的判断或行动，才值得保存。必须具备跨场景复用价值和适用条件，单次偶然经验不直接升级。

```markdown
# [原则标题]

- 原则：[核心结论]
- 适用：[什么情况下使用]
- 行动：[遇到此类问题优先做什么]
- 例外：[不适用情况，可选]
- 来源：[关联 Experience，可选]
```

### Task｜待处理任务

核心是下一步明确行动，普通任务不为了完整性增加背景。

```markdown
# [任务标题]

- 状态：[todo / doing / done]
- 行动：[下一步具体做什么]
- 目标：[预期产出，可选]
- 优先级：[high / medium / low，可选]
- 截止：[时间，可选]
- 依赖：[前置条件，可选]
```

Bug 仅在影响执行时扩展：

```markdown
- 现象：[bug 表现]
- 复现：[最小复现步骤]
- 环境：[必要环境信息]
```

状态同时由写入器保存到 frontmatter，供查询和首页统计使用。

## 语言约束与写入前检查

一句话一个事实，优先“对象 + 动作 + 结果”。保留问题、原因、动作、结果、条件、下一步。能一句话说清不写一段；没有有效信息不填字段。不捏造测量值或已确认原因。

默认删除不包含必要信息的表达：经过分析、经过排查、可以发现、可以看出、需要注意的是、值得一提的是、结合实际情况、在实际使用过程中、总体来看、综上所述、后续可以考虑、进一步进行分析、持续关注。

例如用“原因：数据库单批写入量过小。处理：批量大小从 100 调整为 1000。”代替泛泛描述；用“对 Kafka Consumer 做 5k/10k/20k TPS 压测，记录 lag、CPU 和处理耗时。”代替“持续关注消费性能”。

检查：
1. 是否一个主题、一句话一个事实？
2. 是否重复、存在空泛过程语言或可删除而不影响含义的句子？
3. Task 是否有下一步行动？
4. Experience 是否停留在具体事实？
5. Principle 是否有复用价值和适用条件？
6. 是否为填模板而生成内容？

少写背景，多写事实；少写过程，多写结论；少写描述，多写行动。

## 写入和更新

模板位于 assets/templates：daily-summary.md、experience.md、principle.md、task-handoff.md。写入正文不重复一级标题和 frontmatter，脚本负责生成这些元数据。只保留实际有内容的字段。

```sh
python scripts/write-memory.py --action capture --type experience --title "批量写入调整" --content "<正文>"
python scripts/write-memory.py --action capture --type principle --title "批量写入条件" --content "<正文>"
python scripts/write-memory.py --action capture --type task --title "消费压测" --content "<正文>"
python scripts/write-memory.py --action capture --type daily --content "<正文>"
```

可用 --content-stdin 传多行文本。PowerShell 等价参数为 -Action Capture -Type Experience -Title "标题" -Content $content。

未明确指定已有文件时，Experience、Principle、Task 新建独立记录；Daily 按日期首次创建、后续追加。只有用户明确给出路径、准确文档名或 Obsidian 链接才用 --target-file 更新；不猜测目标。拒绝根目录外路径、符号链接逃逸、非 Markdown 和不存在的目标。

写入后刷新四类索引。报告类型、新建或更新、绝对路径、索引刷新情况；失败如实报告，不改写到其他位置。
