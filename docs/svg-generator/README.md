# svg-generator 使用说明

## 适用场景

- 生成可在浏览器、文档和网页中展示的高质量 SVG。
- 绘制业务、技术、部署、数据架构，以及流程、时序、ER、关系、对比和路线图。
- 需要 Draw.io 二次编辑时使用 `xml-diagram`；复杂自动布局优先使用 `mermaid-gen`。

## 输入输出

- 输入：系统描述、图形类型、浅色或深色主题以及需要表达的内容。
- 输出：一个或多个自包含 UTF-8 SVG 文件。
- 未指定目录时默认输出到项目根目录 `output/svg`。
- 统一使用一套视觉风格，深浅主题只切换颜色。

## 快速使用

```text
请使用 svg-generator 绘制抢红包系统的业务架构图和主要流程图，同时生成浅色与深色版本。
```

- 示例和验证记录：[examples.md](examples.md)
- SVG 示例：[svg/](svg/)
- 代表性截图：[images/](images/)

```powershell
python -X utf8 .opencode\skills\svg-generator\scripts\validate.py docs\svg-generator\svg --strict --render
```

## 核心流程

1. 确定图形类型、信息层级、主题、阅读方向和输出目录。
2. 规划区域、分组、内容、尺寸、间距和必要连线。
3. 匹配模板并计算画布。
4. 生成带校验元数据的自包含 SVG。
5. 检查颜色、布局、重叠、字号、连线和留白。
6. 使用真实浏览器渲染并修正问题。
