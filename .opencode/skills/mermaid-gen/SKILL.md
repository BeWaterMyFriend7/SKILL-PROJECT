---
name: mermaid-gen
description: 使用 Mermaid 语法生成各种类型的图表。支持流程图(flowchart)、时序图(sequence diagram)、类图(class diagram)、ER图(er diagram)、状态图(state diagram)、甘特图(gantt chart)、Git图(git graph)、用户旅程图(user journey)、饼图(pie chart)、思维导图(mindmap)、时间线(timeline)、象限图(quadrant chart)、XY图表(xy chart)、桑基图(sankey)、框图(block diagram)等。当用户提到 mermaid、流程图、时序图、类图、ER图、甘特图、思维导图、饼图、状态图、时间线、桑基图、象限图、用户旅程、Git图、框图、生成图表、画一个图等时触发。
---

# Mermaid 图表生成

## 工作流程

1. 识别用户描述对应的图表类型
2. 提取参与者、节点、实体或状态
3. 确定元素间关系和连接
4. 生成 Mermaid 代码块输出

## 图表类型选择

| 用户意图 | 图表类型 | 关键词 |
|---------|---------|--------|
| 流程/步骤/决策 | Flowchart | 流程、步骤、判断 |
| 交互/调用/消息 | Sequence Diagram | 时序、交互、调用、消息 |
| 类/接口/继承 | Class Diagram | 类图、继承、接口 |
| 实体/数据库/关系 | ER Diagram | ER、实体、数据库表 |
| 状态变化/生命周期 | State Diagram | 状态、流转、生命周期 |
| 排期/计划/进度 | Gantt Chart | 甘特、排期、进度 |
| 分支/合并 | Git Graph | git、分支、合并 |
| 占比/分布 | Pie Chart | 饼图、占比、比例 |
| 脑图/层级结构 | Mindmap | 思维导图、脑图、层级 |
| 里程碑/版本 | Timeline | 时间线、里程碑 |
| 优先级/评估矩阵 | Quadrant Chart | 象限、优先级、矩阵 |
| 趋势/对比数值 | XY Chart | 趋势、柱状图、折线图 |
| 流向/转化漏斗 | Sankey | 桑基、流向、转化 |
| 系统框图/模块 | Block Diagram | 框图、模块、方块图 |

## 输出

以 ` ```mermaid ` 代码块直接输出，或保存为 `.md` 文件至 `output/mermaid/`。

文件命名：`<图类型>-<描述>.md`

### 输出模板
```markdown
# <图表标题>

<简要描述>

\`\`\`mermaid
<Mermaid 代码>
\`\`\`

## 说明
- 节点说明
- 关键关系解释
```

## 验证清单

- [ ] 语法正确，Mermaid 可解析
- [ ] 节点和关系名称清晰有意义
- [ ] 图表方向（TD/LR）适合内容布局
- [ ] 代码块使用 ` ```mermaid ` 包裹

## 参考

- 各类型语法速查见 `references/mermaid-syntax.md`
- 完整示例见 `examples/` 目录下对应文件
