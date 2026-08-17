# svg-generator 使用说明

`svg-generator` 生成可直接在浏览器、网页和文档中展示的自包含 SVG，适合架构、流程、时序、关系、规划和结构化信息图。需要在 Draw.io 中拖拽编辑时使用 `xml-diagram`。

## 快速使用

```text
请使用 svg-generator 绘制智慧零售平台的技术架构图。
使用稳健聚焦深色主题，保持纵向分层，并输出自包含 SVG。
```

未提供颜色信号时，Skill 会询问一次主题；仍未指定则使用默认科技蓝浅色模式。

## 主题

| 主题 | 键 | 适合的视觉感受 |
| --- | --- | --- |
| 科技蓝（默认） | `tech-blue` | 清晰、专业、统一 |
| 活力多彩 | `vibrant` | 多角色、多分支、强调区分 |
| 稳健聚焦 | `focused` | 克制、结构化、突出重点 |

每个主题都包含 primary、secondary、tertiary、accent 多个结构色。用户可以覆盖部分或全部色槽；浅色与深色版本保持相同内容和几何结构。

## 生成流程

1. 明确图形类型、核心结论、内容层级和阅读方向。
2. 选择主题与显示模式，生成自然语言 DSL。
3. 匹配 SVG 模板并计算画布、区域、卡片和连线。
4. 生成可访问、自包含 SVG，执行严格源文件校验。
5. 使用真实浏览器渲染，修正重叠、文字、连线和空白。

架构图固定使用 `vertical-stack` 纵向分层。顶部信息带、辅助列、说明卡片、编号流程、焦点节点和底部总结带只在内容需要时加入。图标通常 0～4 个，但不设置硬上限。

## 智慧零售示例集

以下 10 类示例均重新生成浅色和深色版本，共 20 个 SVG 文件。

| 图形类型 | 主题 | 浅色 | 深色 |
| --- | --- | --- | --- |
| 业务架构 | 科技蓝 | [文件](svg/architecture-business-tech-blue-light-smart-retail.svg) | [文件](svg/architecture-business-tech-blue-dark-smart-retail.svg) |
| 技术架构 | 稳健聚焦 | [文件](svg/architecture-technical-focused-light-smart-retail.svg) | [文件](svg/architecture-technical-focused-dark-smart-retail.svg) |
| 部署架构 | 科技蓝 | [文件](svg/architecture-deployment-tech-blue-light-smart-retail.svg) | [文件](svg/architecture-deployment-tech-blue-dark-smart-retail.svg) |
| 数据架构 | 稳健聚焦 | [文件](svg/architecture-data-focused-light-smart-retail.svg) | [文件](svg/architecture-data-focused-dark-smart-retail.svg) |
| 分支流程 | 活力多彩 | [文件](svg/flow-branching-vibrant-light-smart-retail.svg) | [文件](svg/flow-branching-vibrant-dark-smart-retail.svg) |
| 时序图 | 科技蓝 | [文件](svg/sequence-tech-blue-light-smart-retail.svg) | [文件](svg/sequence-tech-blue-dark-smart-retail.svg) |
| ER 图 | 稳健聚焦 | [文件](svg/relationship-er-focused-light-smart-retail.svg) | [文件](svg/relationship-er-focused-dark-smart-retail.svg) |
| 核心能力 | 活力多彩 | [文件](svg/summary-vibrant-light-smart-retail.svg) | [文件](svg/summary-vibrant-dark-smart-retail.svg) |
| 交付里程碑 | 科技蓝 | [文件](svg/timeline-tech-blue-light-smart-retail.svg) | [文件](svg/timeline-tech-blue-dark-smart-retail.svg) |
| 演进路线图 | 稳健聚焦 | [文件](svg/roadmap-focused-light-smart-retail.svg) | [文件](svg/roadmap-focused-dark-smart-retail.svg) |

## 主题截图

### 科技蓝

![科技蓝浅色业务架构](images/architecture-business-tech-blue-light-smart-retail.png)

![科技蓝深色业务架构](images/architecture-business-tech-blue-dark-smart-retail.png)

### 活力多彩

![活力多彩浅色流程](images/flow-branching-vibrant-light-smart-retail.png)

![活力多彩深色流程](images/flow-branching-vibrant-dark-smart-retail.png)

### 稳健聚焦

![稳健聚焦浅色技术架构](images/architecture-technical-focused-light-smart-retail.png)

![稳健聚焦深色技术架构](images/architecture-technical-focused-dark-smart-retail.png)

其他截图覆盖部署、数据、时序、ER、总结、时间线和路线图，位于 [images](images/)。

## 验证结果

- Skill 内 21 个示例和文档侧 20 个 SVG 文件均通过严格校验。
- 文档截图由本机 Chrome 从对应 SVG 文件重新渲染。
- 已检查可访问性元数据、外部资源、浅色/深色一致性、主题色角色、元素重叠、文字对比度、连线和画布利用率。
