# 路由与功能边界

`xml-diagram` 只负责生成可在 Draw.io/diagrams.net 中继续编辑的 `.drawio` XML 文件。

## 应触发

- 用户明确要求 Draw.io、diagrams.net、mxGraph、XML 图形或可编辑图。
- 用户要求后续能拖拽节点、修改连线、编辑文字。

## 不应触发

- 明确要求 SVG 或浏览器静态矢量图：交给 `svg-generator`。
- 明确要求 Mermaid 或 Markdown 图表：交给 `mermaid-gen`。
- 未要求可编辑媒介的泛化“做一张高级架构图”：默认不抢占。

## 默认决策

- 未指定主题时使用浅色。
- 架构图优先选择对应架构模板。
- 简约流程与结构化复杂流程必须使用不同模板，不从简约模板临时扩展复杂回环。
