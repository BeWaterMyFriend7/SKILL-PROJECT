---
name: mermaid-gen
description: 生成 Mermaid 源码或包含 Mermaid fence 的 Markdown 图表，适用于用户明确要求 Mermaid、Markdown 图表、文档即代码或可 diff 图形。支持 flowchart、sequence、class、ER、state、gantt、gitGraph、journey、pie、mindmap、timeline、quadrant、xy、sankey 和 block。优先保证类型选择、语法、自动布局和文档可维护性，不用于 Draw.io 可编辑 XML、精确坐标 SVG 或照片插画。
---

# Mermaid 图表生成器

生成 Mermaid 代码块或 Markdown 文件。用户未指定目录时保存到项目根目录 `output/mermaid/`。明确要求 SVG 时使用 `svg-generator`，明确要求 Draw.io 时使用 `xml-diagram`。

## 必读资源

- 分析需求和规划图形前读取 `references/mermaid-dsl.md`。
- 遇到具体语法、特殊字符或 beta 图型时读取 `references/mermaid-syntax.md`。
- 读取对应的 `examples/*.md`；示例用于理解图型结构，禁止只替换标题后交付。

## 强制流程

```text
分析需求 → 选择图型 → 自然语言 Mermaid DSL → 控制方向和复杂度
        → 生成 Mermaid → 结构/语义校验 → CLI 真实渲染 → 简化并交付
```

### 1. 分析需求

确定图表目的、受众、输出形式、浅色或深色主题、阅读方向、核心节点、关系、分区和输出路径。区分用户事实与合理补充，不擅自增加业务关系。

Mermaid 适合自动布局和文档即代码，不承诺精确坐标。用户强调品牌化、复杂部署边界、像素级布局或高级展示时改用 SVG 或 Draw.io。

### 2. 选择图型

| 意图 | Mermaid 类型 |
| --- | --- |
| 流程、步骤、判断 | `flowchart` |
| 调用、消息、交互 | `sequenceDiagram` |
| 类、接口、继承 | `classDiagram` |
| 实体、数据库关系 | `erDiagram` |
| 状态变化 | `stateDiagram-v2` |
| 排期与进度 | `gantt` |
| Git 分支与合并 | `gitGraph` |
| 用户体验旅程 | `journey` |
| 占比 | `pie` |
| 层级思维结构 | `mindmap` |
| 里程碑 | `timeline` |
| 优先级矩阵 | `quadrantChart` |
| 数值趋势 | `xychart-beta` |
| 流量迁移 | `sankey-beta` |
| 系统模块框图 | `block-beta` |

- 静态系统分层优先 `block-beta`；带判断和流转关系时使用 `flowchart`。
- 调用关系复杂时使用 `sequenceDiagram`，不要在架构图中堆积箭头。
- 数据实体关系使用 `erDiagram`，不要用普通方框模拟。

### 3. 生成自然语言 DSL

按 `references/mermaid-dsl.md` 描述图型、主题、方向、节点或参与者、关系、分区、复杂度和检查要求。DSL 不强制落盘，不使用 JSON、JSON Schema 或 DiagramPlan。

### 4. 控制方向和复杂度

- 阶段流程优先 `LR`，层级和判断较多时优先 `TD`。
- 默认节点不超过 20，分区不超过 8，嵌套不超过 3 层。
- 单个标签尽量不超过 24 个中英文字符；过长时换行、精简或拆图。
- 避免多条回线、跨分区长线和大量中心发散连线。
- 自动布局出现拥挤时，优先减少关系、调整方向或拆图，不堆叠 `style` 修补。

### 5. 生成 Mermaid

每个交付文件默认只包含一个主 Mermaid block。Markdown 结构使用：标题、简短说明、完整 Mermaid fence、必要说明。

浅色主题：

```text
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Noto Sans SC, Microsoft YaHei, sans-serif","primaryColor":"#FFFFFF","primaryBorderColor":"#2563EB","primaryTextColor":"#172033","lineColor":"#64748B","background":"#F6F8FB"}}}%%
```

深色主题：

```text
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Noto Sans SC, Microsoft YaHei, sans-serif","primaryColor":"#172033","primaryBorderColor":"#60A5FA","primaryTextColor":"#F8FAFC","lineColor":"#94A3B8","background":"#0F172A"}}}%%
```

一张图只使用一个主色和不超过三种语义色。避免逐节点 `style`；需要语义样式时使用少量 `classDef`。

### 6. 校验和渲染

交付前运行：

```bash
python -X utf8 scripts/validate_mermaid.py <Markdown 文件或目录> --require-render
```

修改 skill 示例时运行：

```bash
python -X utf8 scripts/validate_mermaid.py examples --check-coverage --require-render
python -m unittest discover -s tests -v
```

校验后查看真实渲染，检查节点拥挤、文字截断、线条交叉、回线过长和大面积不均衡。renderer 不可用时只能报告“结构通过、渲染未验证”。

## 交付

交付 Mermaid 代码块或最终 Markdown 路径，并说明图型、主题和结构/渲染校验状态。不交付中间 DSL 或临时渲染文件，除非用户明确要求。
