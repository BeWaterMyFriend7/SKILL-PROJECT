# Changelog

本文件按项目关键日期记录当时状态和重要变化，不逐条复制 Git 提交记录。

## 2026-08-04

### 当前状态

- 新增 `agent-offline-mermory`：管理本地 Obsidian 或纯 Markdown 文件夹中的 AI 协作记忆（待办、交接、可复用经验），经验加载支持 `auto`（默认）与 `manual` 两种模式。
- 记忆根目录支持纯文件夹模式（`require_obsidian=false`），不再强制要求 Obsidian。

### 主要变化

- 安装后必须初始化；未初始化时查询和写入会被拒绝，只允许 `status` / `init`。
- 初始化时确认记忆根目录、是否要求 Obsidian、经验加载模式；`set-root` 默认沿用已有配置。
- 每次写入或更新记录后自动刷新 `Tasks/_index.md` 和 `Knowledge/_index.md`。
- `settings.json` 不再入库，改为 `settings.example.json` 模板并加入 .gitignore，避免本地路径泄露。
- 根 README 的 Skill 索引与如何选择新增“记忆协作相关”分类，并新增 `docs/agent-offline-mermory/README.md`。


## 2026-07-12

### 当前状态

- 项目形成绘图、原型和代码变更三类共 7 个 Skill。
- 绘图类包含 `xml-diagram`、`svg-generator`、`mermaid-gen`。
- 原型类包含 `prototype-design-html`、`prototype-design-xml`。
- 代码变更类包含 `code-change-plan`、`code-merge-helper`。
- 根 README 作为统一索引；绘图和原型说明内嵌示例输出，两个报告型 Skill 保留独立示例文档。

### 主要变化

- 新增 `code-change-plan` 和 `code-merge-helper`。
- `svg-generator` 统一视觉风格并扩展架构、流程、时序和关系图能力。
- `xml-diagram` 统一架构图布局并强化数据架构图支持。
- 重构绘图和原型绘图skill生成逻辑、生图更稳，主要逻辑增加dsl自然语言描述层，校验更强，模板更规范，设计规范也更强。
- 建立 `docs/<skill>/` 使用说明、示例产物和验证记录体系。
- 删除已被新 Skill 替代的 `drawio-diagram`、`prototype-design`、`requirements-analysis`、`requirements-review` 和 `technical-design`。
- 删除过期的根目录图片、旧输出目录


## 2026-07-07

### 当前状态与变化

- 新增 `code-change-plan`，用于在编码前分析需求、方案、影响范围、验证和回滚步骤。
- 新增 `code-merge-helper`，用于三方冲突分析、改动意图追溯和合并方案评估。
- 为两个代码变更类 Skill 提供完整报告示例。
- 增加高质量开发流程增强 Skills 和通用 Agent Skills 推荐列表。
- README 开始承担代码变更类 Skill 的发现和导航入口。

## 2026-03-17

### 项目初始状态

- 仓库已具备 OpenCode Skill 目录和基础安装、使用说明。
- 当时包含 `xml-diagram`、`svg-generator`、`drawio-diagram`、`prototype-design`、`requirements-analysis`、`requirements-review`、`technical-design` 共 7 个 Skill。
- 绘图能力以 Draw.io XML、SVG、流程图和架构图为主，`xml-diagram` 与 `svg-generator` 是主要推荐入口。
- 需求分析、需求评审、交互原型和技术设计 Skill 仍处于持续优化阶段。
- 仓库使用 `image/`、`img-output/` 和 `output/` 保存图形预览与 Skill 输出示例。
- README 已包含项目结构、OpenCode 安装使用方式和外部 Skill 推荐列表。
