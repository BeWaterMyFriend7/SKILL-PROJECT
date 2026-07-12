# mermaid-gen 使用说明

`mermaid-gen` 根据自然语言需求生成 Mermaid 源码或包含 Mermaid fence 的 Markdown 文件，适合技术文档、版本管理和文档即代码场景。

## 输入与输出

- 输入：图表目的、内容、可选图型、方向和浅色或深色主题。
- 输出：Mermaid 代码块或自包含 Markdown 文件。
- 用户未指定目录时默认输出到项目根目录 `output/mermaid`。
- 流程不使用 DiagramPlan、JSON 或 JSON Schema。

## 主要流程

1. 分析需求并判断 Mermaid 是否适合。
2. 选择 flowchart、sequence、ER、state、gantt、block 等图型。
3. 生成自然语言 Mermaid DSL，列出节点、关系、分区、方向和复杂度。
4. 生成一个完整 Mermaid block。
5. 检查围栏、主题、图型语义、节点数量和标签长度。
6. 使用固定版本 Mermaid CLI 真实渲染，发现拥挤或交叉时简化关系、调整方向或拆图。

## 适用边界

- 精确坐标、高级视觉和复杂部署边界使用 `svg-generator`。
- Draw.io 可编辑文件使用 `xml-diagram`。
- Mermaid 优先保证自动布局、语法可靠和文档可维护性。

## 校验

```powershell
python -X utf8 .opencode\skills\mermaid-gen\scripts\validate_mermaid.py docs\mermaid-gen\markdown --require-render
```

代表性测试案例和渲染截图见 [test-example.md](test-example.md)。
