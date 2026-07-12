# Changelog

本文件按项目关键日期记录当时状态和重要变化，不逐条复制 Git 提交记录。

## 2026-07-12

### 当前状态

- 项目形成绘图、原型和代码变更三类共 7 个 Skill。
- 绘图类包含 `xml-diagram`、`svg-generator`、`mermaid-gen`。
- 原型类包含 `prototype-design-html`、`prototype-design-xml`。
- 代码变更类包含 `code-change-plan`、`code-merge-helper`。
- 根 README 作为统一索引；绘图和原型说明内嵌示例输出，两个报告型 Skill 保留独立示例文档。

### 主要变化

- 新增 `mermaid-gen`、`prototype-design-html`、`prototype-design-xml`、`code-change-plan` 和 `code-merge-helper`。
- `svg-generator` 统一视觉风格并扩展架构、流程、时序和关系图能力。
- `xml-diagram` 统一架构图布局并强化数据架构图支持。
- 建立 `docs/<skill>/` 使用说明、示例产物和验证记录体系。
- 删除已被新 Skill 替代的 `drawio-diagram`、`prototype-design`、`requirements-analysis`、`requirements-review` 和 `technical-design`。
- 删除过期的根目录图片、旧输出目录和 `graphify` gitlink。

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
