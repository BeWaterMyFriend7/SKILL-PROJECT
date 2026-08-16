---
name: xml-diagram
description: 生成可在 Draw.io/diagrams.net 中继续编辑的 UTF-8 `.drawio` XML 图形。用于业务/应用/技术/部署/数据架构图、流程图、状态图、生命周期图、时序图、ER/依赖/知识关系图、对比、决策矩阵、SWOT、时间线、路线图和总结图；不用于 Mermaid、静态 SVG、位图插画、统计图表或 UI 原型。
---

# Draw.io XML 图形生成器

生成可编辑、可复核的 Draw.io XML。禁止从用户自然语言直接跳到 XML；必须先完成需求分析和详细图形 DSL。

## 工作流程

### 1. 分析需求

明确用途、受众、核心结论、内容范围、图形类型、主要实体或步骤、阅读方向和显示模式。主题选择与默认回退按 `references/theme-tokens.md` 执行，并区分用户确认内容、合理推断和待确认事实。

完成条件：能够用一段自然语言说明“这张图向谁说明什么，按什么顺序阅读”。

### 2. 生成详细 DSL

读取 `references/diagram-dsl.md`、`references/theme-tokens.md` 和 `references/icon-policy.md`。DSL 必须覆盖叙事、布局、区域、节点、关系、颜色语义、图标策略、假设和质量预期，并明确模板名称、布局模式、间距和画布策略。

完成条件：只阅读 DSL 即可还原图形，XML 阶段不再猜测业务语义或布局意图。

### 3. 精确选择模板并生成 XML

按图形类型精确匹配一个模板：

| 图形类型 | 模板 |
| --- | --- |
| 业务、应用、技术、部署架构 | `templates/architecture.drawio` |
| 数据架构 | `templates/architecture-data.drawio` |
| 线性流程 | `templates/flow-linear.drawio` |
| 分支或异常流程 | `templates/flow-branching.drawio` |
| 状态图 | `templates/state.drawio` |
| 生命周期 | `templates/lifecycle.drawio` |
| 时序图 | `templates/sequence.drawio` |
| ER 图 | `templates/relationship-er.drawio` |
| 依赖关系 | `templates/relationship-dependency.drawio` |
| 知识关系 | `templates/relationship-knowledge.drawio` |
| 对比 | `templates/comparison.drawio` |
| 决策矩阵 | `templates/decision-matrix.drawio` |
| SWOT | `templates/swot.drawio` |
| 时间线或里程碑 | `templates/timeline.drawio` |
| 路线图 | `templates/roadmap.drawio` |
| 总结图 | `templates/summary.drawio` |

必须读取并复用模板骨架：保留标准画布、必要语义元素、正确的 `mxGeometry` 写法和基础布局，再替换内容、增删节点并动态调整坐标。禁止只参考配色后凭空重建一份相似 XML。

强制设置：

- UTF-8 无 BOM；
- `mxGraphModel` 显式设置 `grid="0"`；
- 每个 `mxGeometry` 包含 `as="geometry"`；
- 可见节点只使用 `width/height`，禁止 `w/h`；
- 可见节点宽高为正数；
- ID 唯一，边引用存在节点；
- 标题不用下划线或装饰横线；
- 浅色和深色使用相同坐标、尺寸、圆角、间距和连线；
- 架构一级标题置于对应容器外部上方，左侧对齐并保持 8～12px 紧密间距；
- 架构二级卡片标题使用独立、居中的标题条，内容标签从标题条下方开始；
- 架构同级卡片等宽、等高、等距，末行不足时整体居中，容器高度随实际内容行数调整；
- 架构图默认减少箭头；
- 架构主骨架和附加模块按 `references/diagram-dsl.md` 执行；
- 图标按 `references/icon-policy.md` 执行；
- 数据架构先根据需求对候选层执行保留、合并、删除、拆分或新增，禁止输出空层；
- 数据架构必须复用通用架构图的一级标题、一级容器、二级分组卡片、独立标题条和内容标签规范；示例层级只是候选内容，不得据此另造视觉骨架；
- 数据治理、安全、运维等贯穿能力使用同款架构分组区域表达，不使用窄而高的彩色长柱；
- 数据架构只保留一条主数据流或少量必要的实时/离线分支，详细表级或字段级血缘应拆为关系图；
- 时序图包含起点、终点、所有参与者的完整生命线、请求链和返回链。

### 4. 执行自动检查

读取 `references/quality-rules.md`，运行：

```bash
python -X utf8 scripts/validate.py <file-or-directory> --strict
```

错误和严格模式警告必须修复。不得通过删除必要内容或缩小字体规避问题。

### 5. 渲染检查并交付

将 `.drawio` 渲染或在 diagrams.net 中打开，检查颜色、布局、重叠、字体、线条、图例和空白。发现问题时返回 DSL 或布局阶段修正。

环境无法渲染时，必须明确说明“仅完成 XML 和结构检查，未完成视觉验收”，不得声称最终视觉质量已通过。

## 输出

默认只交付最终 `.drawio`。用户要求时再交付 DSL 或预览。输出到用户指定目录；未指定时输出到当前任务目录，不把运行产物写进本 skill。
