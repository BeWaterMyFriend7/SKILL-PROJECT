# xml-diagram 使用说明

## 适用场景

- 生成可在 Draw.io 或 diagrams.net 中继续编辑的技术图。
- 绘制业务、应用、技术、部署、数据架构，以及流程、状态、时序和关系图。
- 只需浏览器展示的高质量矢量图时使用 `svg-generator`。

## 快速使用

```text
请使用 xml-diagram 绘制抢红包系统的业务架构图和用户抢红包时序图。
```

- 示例和验证记录：[examples.md](examples.md)
- Draw.io 示例：[drawio/](drawio/)
- 代表性截图：[images/](images/)

```powershell
python -X utf8 .opencode\skills\xml-diagram\scripts\validate.py docs\xml-diagram\drawio --strict
```

## 核心流程

1. 确认图形类型、信息层级和主题。
2. 规划元素、布局、颜色和连线。
3. 匹配模板并生成 Draw.io XML。
4. 检查颜色、布局、重叠、字体、连线和画布留白。
5. 使用校验器检查 XML，并通过 Draw.io 真实渲染。
6. 修正问题后输出最终文件。
