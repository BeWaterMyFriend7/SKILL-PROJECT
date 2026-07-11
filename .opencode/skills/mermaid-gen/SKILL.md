---
name: mermaid-gen
description: 生成 Mermaid 源码或包含 Mermaid fence 的 Markdown 图表，适用于用户明确要求 Mermaid、Markdown 图表、文档即代码或可 diff 图形。支持 flowchart、sequence、class、ER、state、gantt、gitGraph、journey、pie、mindmap、timeline、quadrant、xy、sankey 和 block。优先保证语法与文档可维护性，不用于 Draw.io 可编辑 XML 或像素级高级 SVG 视觉。
---

# Mermaid 图表生成器

本 skill 是完全自包含的 Mermaid 渲染模块。所有规则、参考、示例和校验脚本都位于本文件夹内，禁止读取其他 skill 的文件。

## 接口

输入：用户的图表语义、可选图类型、方向和主题。
输出：`mermaid` 代码块或保存到 `output/mermaid/` 的 Markdown 文件。

先读取 `assets/routing.md`。明确要求 SVG 或 Draw.io 时停止使用本 skill。

## 强制流程

```text
用户输入
-> 本地路由判断
-> DiagramPlan
-> 图类型选择
-> 复杂度预算
-> Mermaid 源码
-> 结构/语法/渲染校验
-> 交付
```

### 1. 整理 DiagramPlan

按 `assets/diagram-plan.schema.json` 整理类型、主题、方向、标题、节点、关系和分区。

### 2. 选择图类型

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
| 系统框图 | `block-beta` |

详细语法只读取本目录的 `references/mermaid-syntax.md` 和对应 `examples/*.md`。

### 3. 主题和复杂度

- 使用 `assets/visual-tokens.md` 中的本地颜色和字体。
- 输出固定 `%%{init: ...}%%`，不要依赖 renderer 默认主题。
- 默认节点不超过 20，分区不超过 8，嵌套不超过 4 层。
- 单标签建议不超过 24 个中英文字符；超出时换行、缩写或拆图。
- 不使用大量临时 `style`；语义样式用少量 `classDef`。
- 用户要求精确布局、品牌化或高级展示时应改用 SVG。

### 4. 输出格式

````markdown
# 图表标题

简要描述。

```mermaid
%%{init: {"theme": "base", "themeVariables": {}}}%%
<Mermaid 源码>
```

## 说明

- 关键节点或关系说明。
````

### 5. 校验

交付前运行：

```bash
python -X utf8 scripts/validate_plan.py <diagram-plan.json>
python -X utf8 scripts/validate_mermaid.py <Markdown 文件或目录> --require-render
```

若 renderer 不可用，只能报告“结构通过、渲染未验证”，不得宣称完整通过。

## 输出说明

交付时说明图类型、主题、文件路径和结构/渲染校验状态。
