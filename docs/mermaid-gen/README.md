# mermaid-gen 使用说明

## 适用场景

- 在 Markdown 中维护流程、时序、ER、状态、甘特、框图等图形。
- 需要自动布局、可版本管理且可由 Mermaid CLI 真实渲染的图形。
- 精确坐标和高级视觉使用 `svg-generator`；需要 Draw.io 编辑时使用 `xml-diagram`。

## 快速使用

```text
请使用 mermaid-gen 绘制用户登录时序图，并输出为 Markdown。
```

- 示例和验证记录：[examples.md](examples.md)
- Mermaid 示例源码：[markdown/](markdown/)
- 渲染截图：[images/](images/)

```powershell
python -X utf8 .opencode\skills\mermaid-gen\scripts\validate_mermaid.py docs\mermaid-gen\markdown --require-render
```

## 核心流程

1. 分析需求并选择 Mermaid 图型。
2. 规划节点、关系、分区、方向和复杂度。
3. 生成一个完整 Mermaid block。
4. 检查围栏、主题和图型语义。
5. 使用固定版本 Mermaid CLI 渲染，并在拥挤或交叉时调整方向、简化关系或拆图。
