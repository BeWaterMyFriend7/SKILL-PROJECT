# 路由与功能边界

`mermaid-gen` 只负责生成 Mermaid 代码或包含 Mermaid fence 的 Markdown 文档。

## 应触发

- 用户明确要求 Mermaid、Markdown 图表、文档即代码或可 diff 图表。
- 用户需要由 Mermaid renderer 自动布局的技术图。

## 不应触发

- 明确要求 SVG、静态高级矢量视觉：交给 `svg-generator`。
- 明确要求 Draw.io、可编辑 XML：交给 `xml-diagram`。
- 只说“画一张高级架构图”且未指定 Mermaid：不要抢占。

## 能力边界

Mermaid 优先保证语法、结构和文档可维护性，不承诺像素级排版。用户强调品牌化、精确坐标或高级展示时应选择 SVG。
