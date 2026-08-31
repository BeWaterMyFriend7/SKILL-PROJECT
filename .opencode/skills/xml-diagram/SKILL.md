---
name: xml-diagram
description: 生成可在 Draw.io/diagrams.net 中继续编辑的 UTF-8 `.drawio` XML 技术图。用于业务、应用、技术、部署、数据架构，以及流程、状态、生命周期、时序、ER、依赖、知识关系、对比、决策矩阵、SWOT、时间线、路线图和总结图；不用于 Mermaid、静态 SVG、统计图表、位图插画或 UI 原型。
---

# Draw.io XML 图形生成器

生成可编辑、自包含、可离线打开的 Draw.io XML。先完成自然语言 DSL，再生成 XML。

## 资源使用

- 生成前读取 `references/diagram-dsl.md`。
- 选择图形类型与视觉骨架时读取 `references/catalog.md`。
- 选择颜色时读取 `references/theme-tokens.md`，需要图标时读取 `references/icon-policy.md`。
- 排版前读取 `references/visual-style.md`，验收时读取 `references/quality-rules.md`。
- 先读取同类型 `templates/*.drawio`，再参考同类型 `examples/*.drawio` 作为骨架参考；按实际内容、主轴和视觉合同重算画布，不得只替换标题或颜色。

## 工作流程

1. 明确受众、核心结论、图形类型、内容范围、阅读方向、显示模式和输出位置。
2. 按 `references/theme-tokens.md` 处理主题选择；识别主叙事轴、交叉轴、侧栏、焦点、功能域和真实状态。
3. 用 `references/diagram-dsl.md` 写出可执行蓝图，明确区域、节点、关系、尺寸、间距、视觉骨架、结构颜色角色、视觉配方、图标和质量预期。
4. 运行 `scripts/style_map.py` 或按同一合同应用主题色板、独立色阶和视觉配方；选择 `fresh-catalog-v1` 模板并重算画布，禁止从旧示例批量换色。
5. 生成未压缩 UTF-8 XML，保持 ID、父子关系、几何和连线合法。
6. 运行严格校验，修复全部错误和警告。
7. 使用 Draw.io/diagrams.net 渲染检查颜色、布局、重叠、文字、连线和空白，再交付。

## 模板选择

| 类型 | 模板 |
| --- | --- |
| 业务、应用、技术、部署、数据架构 | `architecture-business.drawio` / `architecture.drawio` / `architecture-technical.drawio` / `architecture-deployment.drawio` / `architecture-data.drawio` |
| 线性、分支流程 | `flow-linear.drawio` / `flow-branching.drawio` |
| 状态、生命周期、时序 | `state.drawio` / `lifecycle.drawio` / `sequence.drawio` |
| ER、依赖、知识关系 | `relationship-er.drawio` / `relationship-dependency.drawio` / `relationship-knowledge.drawio` |
| 对比、决策矩阵、SWOT | `comparison.drawio` / `decision-matrix.drawio` / `swot.drawio` |
| 时间线、路线图、总结 | `timeline.drawio` / `roadmap.drawio` / `summary.drawio` |

## XML 底线

- 设置 `mxGraphModel grid="0"`；使用 `width/height` 和 `as="geometry"`。
- 保证 ID 唯一、边引用存在、可见节点尺寸为正数。
- 架构图保持 `vertical-stack` 纵向分层，附加模块不得替代主骨架。
- 附加模块由内容决定，普通图优先使用 0～2 个；不得为统一版式机械加入顶带、侧栏和底带。
- 浅色与深色只切换令牌，不改变内容、坐标、尺寸、圆角和连线。
- 不使用外部图片、Emoji 或图标字体；内嵌 SVG 必须自包含且可解析。
- 浅色图允许统一的轻微阴影；深色图默认不用阴影。不使用标题下划线、背景网格、强渐变、重阴影或无语义箭头。

## 验证

```bash
python -X utf8 scripts/validate.py <file-or-directory> --strict
```

修改 Skill 时同时运行：

```bash
python -m unittest discover -s tests -v
```

无法完成真实渲染时，明确说明仅完成结构校验，不得声称视觉验收通过。

## 交付

默认只交付最终 `.drawio`。用户要求时再附 DSL 或 PNG 预览；不要把运行产物写入本 Skill。
