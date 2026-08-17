---
name: svg-generator
description: 生成浏览器可直接展示、缩放和嵌入网页或文档的自包含 UTF-8 SVG 矢量图。用于 SVG、矢量图、网页配图，以及业务、应用、技术、部署、数据架构、流程、生命周期、状态、时序、ER、依赖、知识关系、对比、决策矩阵、SWOT、时间线、路线图和总结图；不用于 Draw.io 可编辑 XML、Mermaid、统计图表或照片插画。
---

# SVG 图形生成器

生成可访问、自包含、可真实渲染的 SVG。需要拖拽编辑时改用 `xml-diagram`。

## 资源使用

- 生成前读取 `references/svg-dsl.md`。
- 选择颜色时读取 `references/theme-tokens.md`，需要图标时读取 `references/icon-policy.md`。
- 排版和验收时读取 `references/quality-rules.md`。
- 读取同类型 `templates/*.svg` 和 `examples/*.svg`，继承设计语言并按实际内容重算画布。

## 工作流程

1. 明确受众、核心结论、图形类型、内容范围、阅读方向、显示模式和输出位置。
2. 按 `references/theme-tokens.md` 处理主题选择；区分用户事实、合理补充和不可擅自推断的信息。
3. 用 `references/svg-dsl.md` 写出区域、节点、关系、尺寸、间距、颜色角色、图标和质量预期。
4. 选择模板并计算画布；禁止只替换标题或机械保留空层。
5. 按背景、区域、连线、节点、文字、图例顺序生成 SVG。
6. 运行严格校验和浏览器渲染，修复颜色、布局、重叠、文字、连线和空白问题。
7. 只交付最终 SVG，除非用户明确要求 PNG 预览或中间 DSL。

## 模板选择

| 类型 | 模板 |
| --- | --- |
| 业务、应用、技术、部署、数据架构 | `architecture-business.svg` / `architecture.svg` / `architecture-technical.svg` / `architecture-deployment.svg` / `architecture-data.svg` |
| 线性、分支流程 | `flow-linear.svg` / `flow-branching.svg` |
| 状态、生命周期、时序 | `state.svg` / `lifecycle.svg` / `sequence.svg` |
| ER、依赖、知识关系 | `relationship-er.svg` / `relationship-dependency.svg` / `relationship-knowledge.svg` |
| 对比、决策矩阵、SWOT | `comparison.svg` / `decision-matrix.svg` / `swot.svg` |
| 时间线、路线图、总结 | `timeline.svg` / `roadmap.svg` / `summary.svg` |

## SVG 底线

- `width`、`height` 与 `viewBox` 一致；根节点包含 `role="img"` 和 `aria-labelledby`。
- 提供 `<title>`、`<desc>`；主要节点、连线和辅助文字带相应 `data-role`。
- 使用唯一 ID；引用的 marker、filter、gradient 和 clipPath 必须存在。
- 架构图保持 `vertical-stack` 纵向分层，附加模块不得替代主骨架。
- 浅色与深色只切换令牌，不改变内容、坐标、尺寸、圆角和连线。
- 不使用 `foreignObject`、外部字体、外部 CSS、远程图片、位图 data URI、Emoji 或图标字体。
- 默认不使用渐变和阴影；禁止背景网格、霓虹描边、装饰噪声和无语义箭头。

## 验证

```bash
python -X utf8 scripts/validate.py <file-or-directory> --strict --render
```

修改 Skill 时同时运行：

```bash
python -X utf8 scripts/validate.py . --strict
python -m unittest discover -s tests -v
```

## 交付

用户未指定目录时保存到当前任务的 `output/svg/`。交付时说明图形类型、主题、显示模式和校验结果。
