# xml-diagram 使用说明

两套绘图 Skill 共享 `enterprise-v2` 视觉合同和 19 类自然语言新生目录。主题名称与配色固定，结构颜色会按主轴、交叉轴、侧栏、焦点和数据流受控映射。

## 生成与主题规则

- 用户未指定主题时询问一次；仍不指定则使用 Tech Blue｜科技蓝（默认）。
- 架构图保持纵向分层主骨架；流程、关系、矩阵和时间类选择相应视觉骨架。
- 图标由内容决定，不设硬上限，但只在具有导航、识别或焦点价值时使用。
- 所有文件都从自然语言请求重新生成，不从旧示例批量换色。

## 19 类新生示例

| 图形类型 | 主题 | Draw.io 源文件 | PNG 预览 |
| --- | --- | --- | --- |
| 应用架构 | Tech Blue｜科技蓝（默认） | [文件](drawio/architecture-application-tech-blue-light-enterprise.drawio) | [预览](images/architecture-application-tech-blue-light-enterprise.png) |
| 业务架构 | Vibrant ｜活力 | [文件](drawio/architecture-business-vibrant-light-enterprise.drawio) | [预览](images/architecture-business-vibrant-light-enterprise.png) |
| 数据架构 | Mint green｜清爽绿 | [文件](drawio/architecture-data-mint-green-light-enterprise.drawio) | [预览](images/architecture-data-mint-green-light-enterprise.png) |
| 部署架构 | Tech Blue｜科技蓝（默认） | [文件](drawio/architecture-deployment-tech-blue-light-enterprise.drawio) | [预览](images/architecture-deployment-tech-blue-light-enterprise.png) |
| 技术架构 | Steady Red & Blue｜稳重红蓝 | [文件](drawio/architecture-technical-steady-red-blue-light-enterprise.drawio) | [预览](images/architecture-technical-steady-red-blue-light-enterprise.png) |
| 对比图 | Vibrant ｜活力 | [文件](drawio/comparison-vibrant-light-enterprise.drawio) | [预览](images/comparison-vibrant-light-enterprise.png) |
| 决策矩阵 | Mint green｜清爽绿 | [文件](drawio/decision-matrix-mint-green-light-enterprise.drawio) | [预览](images/decision-matrix-mint-green-light-enterprise.png) |
| 分支流程 | Vibrant ｜活力 | [文件](drawio/flow-branching-vibrant-light-enterprise.drawio) | [预览](images/flow-branching-vibrant-light-enterprise.png) |
| 线性流程 | Tech Blue｜科技蓝（默认） | [文件](drawio/flow-linear-tech-blue-light-enterprise.drawio) | [预览](images/flow-linear-tech-blue-light-enterprise.png) |
| 生命周期 | Vibrant ｜活力 | [文件](drawio/lifecycle-vibrant-light-enterprise.drawio) | [预览](images/lifecycle-vibrant-light-enterprise.png) |
| 依赖关系 | Steady Red & Blue｜稳重红蓝 | [文件](drawio/relationship-dependency-steady-red-blue-light-enterprise.drawio) | [预览](images/relationship-dependency-steady-red-blue-light-enterprise.png) |
| ER 关系 | Mint green｜清爽绿 | [文件](drawio/relationship-er-mint-green-light-enterprise.drawio) | [预览](images/relationship-er-mint-green-light-enterprise.png) |
| 知识关系 | Mint green｜清爽绿 | [文件](drawio/relationship-knowledge-mint-green-light-enterprise.drawio) | [预览](images/relationship-knowledge-mint-green-light-enterprise.png) |
| 路线图 | Steady Red & Blue｜稳重红蓝 | [文件](drawio/roadmap-steady-red-blue-light-enterprise.drawio) | [预览](images/roadmap-steady-red-blue-light-enterprise.png) |
| 时序图 | Tech Blue｜科技蓝（默认） | [文件](drawio/sequence-tech-blue-light-enterprise.drawio) | [预览](images/sequence-tech-blue-light-enterprise.png) |
| 状态图 | Tech Blue｜科技蓝（默认） | [文件](drawio/state-tech-blue-light-enterprise.drawio) | [预览](images/state-tech-blue-light-enterprise.png) |
| 总结图 | Vibrant ｜活力 | [文件](drawio/summary-vibrant-light-enterprise.drawio) | [预览](images/summary-vibrant-light-enterprise.png) |
| SWOT 分析 | Steady Red & Blue｜稳重红蓝 | [文件](drawio/swot-steady-red-blue-light-enterprise.drawio) | [预览](images/swot-steady-red-blue-light-enterprise.png) |
| 时间线 | Steady Red & Blue｜稳重红蓝 | [文件](drawio/timeline-steady-red-blue-light-enterprise.drawio) | [预览](images/timeline-steady-red-blue-light-enterprise.png) |

## 验证

本目录源文件与测试截图来自同一请求清单。完整流程会清理旧目标、生成 DSL 和两种源文件、严格校验、真实渲染，并记录 SHA-256；详情见 `test-outputs/diagram-types/catalog/verification-report.json`。
