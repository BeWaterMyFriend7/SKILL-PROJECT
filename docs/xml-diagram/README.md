# xml-diagram 使用说明

`xml-diagram` 用于根据自然语言需求生成可继续编辑的 Draw.io XML 图形文件。

## 输入与输出

- 输入：用自然语言描述系统、图形类型、主题和需要表达的内容。
- 输出：一个或多个 `.drawio` 文件，可使用 diagrams.net 或 Draw.io 桌面版打开。
- 可选要求：浅色或深色主题、指定图形类型、文件名和输出目录。

示例输入：

```text
请使用 xml-diagram 绘制抢红包系统的业务架构图、主要流程图和用户抢红包时序图，同时生成浅色和深色版本。
```

## 主要流程

1. 分析用户需求，确认图形类型、信息层级和主题。
2. 生成详细的自然语言图形 DSL，明确元素、布局、颜色和连线。
3. 匹配对应模板，生成 Draw.io XML。
4. 检查颜色搭配、布局均匀、元素重叠、字体、连线和画布留白。
5. 使用校验器检查 XML，再通过 Draw.io 真实渲染确认视觉效果。
6. 输出最终 `.drawio` 文件。

## 打开文件

进入 [drawio](drawio/) 目录，使用以下任一方式打开文件：

- 浏览器访问 [diagrams.net](https://app.diagrams.net/)，选择“设备”并打开 `.drawio` 文件。
- 使用 Draw.io 桌面版直接打开 `.drawio` 文件。

## 校验命令

在项目根目录执行：

```powershell
python -X utf8 .opencode\skills\xml-diagram\scripts\validate.py docs\xml-diagram\drawio --strict
```

测试示例、文件索引和截图见 [test-example.md](test-example.md)。
