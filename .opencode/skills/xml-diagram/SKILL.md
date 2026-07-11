---
name: xml-diagram
description: 生成可在 Draw.io/diagrams.net 中继续编辑的 UTF-8 `.drawio` XML 图形。适用于用户明确要求 Draw.io、diagrams.net、mxGraph、XML 图或可编辑图，支持业务/应用/技术/部署/系统架构、简约步骤流程、结构化复杂流程、时序、状态、ER、对比、时间线、生命周期和总结图。不用于静态 SVG 或 Mermaid/Markdown 图表。
---

# Draw.io XML 图形生成器

本 skill 是完全自包含的 Draw.io 渲染模块。所有规范、模板、示例和脚本都位于本文件夹内，禁止读取其他 skill 的文件。

## 接口

输入：用户的图形主题、内容、可选主题和可编辑性要求。
输出：可由 Draw.io/diagrams.net 打开和编辑的 `.drawio` 文件，默认保存到 `output/drawio/`。

先读取 `assets/routing.md`。用户明确要求 SVG 或 Mermaid 时停止使用本 skill。

## 强制流程

```text
用户输入
-> 本地路由判断
-> DiagramPlan
-> 模板选择
-> 内容充实
-> 布局/样式/连线计划
-> mxGraph XML
-> 结构与对比度校验
-> 渲染检查
-> 交付
```

禁止从自然语言一步生成 XML。

### 1. 整理 DiagramPlan

按 `assets/diagram-plan.schema.json` 整理本地中间结构。架构图必须在 `enrichment` 中区分 confirmed、inferred 和 needs_confirmation。

### 2. 选择模板

| 意图 | 模板 |
| --- | --- |
| 业务架构 | `templates/architecture/business-layered.drawio` |
| 应用架构 | `templates/architecture/application-pipeline.drawio` |
| 技术架构 | `templates/architecture/technical-layered.drawio` |
| 部署架构 | `templates/architecture/deployment-region.drawio` |
| 系统上下文 | `templates/architecture/system-context.drawio` |
| 简约步骤流程 | `templates/flow/simple-step-flow.drawio` |
| 结构化复杂流程 | `templates/flow/structured-flow.drawio` |
| 时序图 | `templates/sequence/sequence-login.drawio` |
| 时间线/生命周期 | `templates/project/` |
| 对比、矩阵、SWOT | `templates/analysis/` |
| 总结与知识结构 | `templates/summary/` |

模板是中性骨架，examples 是业务完成品。禁止用完全相同内容冒充不同模板意图。

### 3. 加载本地规则

必须读取：

- `assets/visual-tokens.md`：基础视觉值唯一来源；
- `assets/quality-contract.md`：交付阈值；
- `assets/dsl-schema.md`：mxGraph 中间结构说明。

按任务读取：

- `assets/architecture-system.md`
- `assets/typography-rules.md`
- `assets/component-rules.md`
- `assets/layout-rules.md`
- `assets/edge-rules.md`
- `assets/legend-rules.md`
- `assets/validation-rules.md`

`assets/design-system.md` 和 `assets/theme-tokens.md` 只解释媒介实现，不得重新定义与 `visual-tokens.md` 冲突的基础值。

### 4. 生成规则

- 架构图先充实内容，再计算画布；三级信息必须是独立可编辑小标签。
- 页面标题、区域标题、卡片标题、小标签形成四级层次。
- 简约流程使用 4-8 个主步骤，禁止复杂回环。
- 复杂分支、循环和错误/异步路径必须使用 `structured-flow` 模板。
- 默认正交连线；错误路径红色实线；异步路径紫色虚线。
- 深色模式禁止阴影；浅色只允许轻微阴影。
- 每个 `mxGeometry` 必须包含 `as="geometry"`。
- 禁止内嵌图片，保持所有内容可编辑。

### 5. UTF-8 和 XML

- 所有 `.drawio`、`.md`、`.json`、`.py` 使用 UTF-8 无 BOM。
- Python 必须显式指定 `encoding="utf-8"`。
- 禁止把 UTF-8 字节按 GBK 解码后写回。
- XML 注释不得包含 `--`。
- `mxCell` id 唯一，source/target 必须引用存在节点。

### 6. 校验

交付前运行：

```bash
python -X utf8 scripts/validate_plan.py <diagram-plan.json>
python -X utf8 scripts/validate_drawio.py output/drawio/文件名.drawio --fail-on-warning
python -X utf8 scripts/check_contrast.py output/drawio/文件名.drawio --fail-on-warning
python -X utf8 scripts/render_drawio_preview.py output/drawio/文件名.drawio output/drawio/文件名-preview.png --scale 1
```

模板或示例变更还必须运行：

```bash
python -X utf8 scripts/validate_catalog.py
```

渲染结果必须满足：无裁切、无重叠、无穿线、文字清晰、画布利用率 50%-85%（目标 60%-80%）。

## 输出说明

交付时说明文件路径、使用的模板、主题模式和全部校验结果。
