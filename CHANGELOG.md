# Changelog

本文件记录项目中面向使用者的重要变化，不逐条复制 Git 提交记录。

## Unreleased

### Changed

- 重构根 README，将当前 8 个 Skill、使用说明和示例统一收录到一个索引。
- 统一 `docs/<skill>/README.md` 的章节结构。
- 将代码变更规划和合并分析的说明及示例迁入 `docs/`。
- 将各模块的 `test-example.md` 统一命名为 `examples.md`。

### Fixed

- 删除根 README 中已经失效的旧 Skill、图片和输出目录引用。
- 修正 README 中与当前 SVG、Mermaid 和原型 Skill 行为不一致的说明。

## 2026-07-12

### Added

- 新增 `mermaid-gen`、`prototype-design-html` 和 `prototype-design-xml`。
- 补充 SVG、Draw.io、Mermaid 和原型的使用说明、示例产物及验证记录。

### Changed

- `svg-generator` 统一为一套视觉风格并扩展架构、流程、时序和关系图能力。
- `xml-diagram` 统一架构图布局并强化数据架构图支持。

### Removed

- 删除已经被新 Skill 替代的 `drawio-diagram`、`prototype-design`、`requirements-analysis`、`requirements-review` 和 `technical-design`。
- 删除过期的根目录图片、`svg-output` 和旧设计输出。

## 2026-07-07

### Added

- 新增 `code-change-plan` 和 `code-merge-helper`，并提供输出示例。
- 增加开发流程增强类 Skill 推荐列表。
