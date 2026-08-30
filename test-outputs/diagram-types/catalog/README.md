# 19 类绘图全流程目录

本目录是两套绘图 Skill 的端到端验证源。固定自然语言需求先生成 DSL，再经共享场景模型分别生成 SVG 与 Draw.io；不读取旧模板或旧示例。

## 重新生成与验证

```powershell
python test-outputs/diagram-types/catalog/verify_catalog.py
```

验证流程会清理声明目标、重新生成 19 类 × 2 格式源文件、检查 XML/SVG 语义与几何一致性、严格校验、真实渲染 38 张 PNG，并写入 `verification-report.json`。

| 图形类型 | 主题 | DSL | SVG | Draw.io | SVG PNG | Draw.io PNG |
| --- | --- | --- | --- | --- | --- | --- |
| 应用架构 | Tech Blue｜科技蓝（默认） | [DSL](dsl/architecture-application.md) | [SVG](svg/architecture-application-tech-blue-light-enterprise.svg) | [Draw.io](xml/architecture-application-tech-blue-light-enterprise.drawio) | [预览](images/svg/architecture-application-tech-blue-light-enterprise.png) | [预览](images/xml/architecture-application-tech-blue-light-enterprise.png) |
| 业务架构 | Vibrant ｜活力 | [DSL](dsl/architecture-business.md) | [SVG](svg/architecture-business-vibrant-light-enterprise.svg) | [Draw.io](xml/architecture-business-vibrant-light-enterprise.drawio) | [预览](images/svg/architecture-business-vibrant-light-enterprise.png) | [预览](images/xml/architecture-business-vibrant-light-enterprise.png) |
| 数据架构 | Mint green｜清爽绿 | [DSL](dsl/architecture-data.md) | [SVG](svg/architecture-data-mint-green-light-enterprise.svg) | [Draw.io](xml/architecture-data-mint-green-light-enterprise.drawio) | [预览](images/svg/architecture-data-mint-green-light-enterprise.png) | [预览](images/xml/architecture-data-mint-green-light-enterprise.png) |
| 部署架构 | Tech Blue｜科技蓝（默认） | [DSL](dsl/architecture-deployment.md) | [SVG](svg/architecture-deployment-tech-blue-light-enterprise.svg) | [Draw.io](xml/architecture-deployment-tech-blue-light-enterprise.drawio) | [预览](images/svg/architecture-deployment-tech-blue-light-enterprise.png) | [预览](images/xml/architecture-deployment-tech-blue-light-enterprise.png) |
| 技术架构 | Steady Red & Blue｜稳重红蓝 | [DSL](dsl/architecture-technical.md) | [SVG](svg/architecture-technical-steady-red-blue-light-enterprise.svg) | [Draw.io](xml/architecture-technical-steady-red-blue-light-enterprise.drawio) | [预览](images/svg/architecture-technical-steady-red-blue-light-enterprise.png) | [预览](images/xml/architecture-technical-steady-red-blue-light-enterprise.png) |
| 对比图 | Vibrant ｜活力 | [DSL](dsl/comparison.md) | [SVG](svg/comparison-vibrant-light-enterprise.svg) | [Draw.io](xml/comparison-vibrant-light-enterprise.drawio) | [预览](images/svg/comparison-vibrant-light-enterprise.png) | [预览](images/xml/comparison-vibrant-light-enterprise.png) |
| 决策矩阵 | Mint green｜清爽绿 | [DSL](dsl/decision-matrix.md) | [SVG](svg/decision-matrix-mint-green-light-enterprise.svg) | [Draw.io](xml/decision-matrix-mint-green-light-enterprise.drawio) | [预览](images/svg/decision-matrix-mint-green-light-enterprise.png) | [预览](images/xml/decision-matrix-mint-green-light-enterprise.png) |
| 分支流程 | Vibrant ｜活力 | [DSL](dsl/flow-branching.md) | [SVG](svg/flow-branching-vibrant-light-enterprise.svg) | [Draw.io](xml/flow-branching-vibrant-light-enterprise.drawio) | [预览](images/svg/flow-branching-vibrant-light-enterprise.png) | [预览](images/xml/flow-branching-vibrant-light-enterprise.png) |
| 线性流程 | Tech Blue｜科技蓝（默认） | [DSL](dsl/flow-linear.md) | [SVG](svg/flow-linear-tech-blue-light-enterprise.svg) | [Draw.io](xml/flow-linear-tech-blue-light-enterprise.drawio) | [预览](images/svg/flow-linear-tech-blue-light-enterprise.png) | [预览](images/xml/flow-linear-tech-blue-light-enterprise.png) |
| 生命周期 | Vibrant ｜活力 | [DSL](dsl/lifecycle.md) | [SVG](svg/lifecycle-vibrant-light-enterprise.svg) | [Draw.io](xml/lifecycle-vibrant-light-enterprise.drawio) | [预览](images/svg/lifecycle-vibrant-light-enterprise.png) | [预览](images/xml/lifecycle-vibrant-light-enterprise.png) |
| 依赖关系 | Steady Red & Blue｜稳重红蓝 | [DSL](dsl/relationship-dependency.md) | [SVG](svg/relationship-dependency-steady-red-blue-light-enterprise.svg) | [Draw.io](xml/relationship-dependency-steady-red-blue-light-enterprise.drawio) | [预览](images/svg/relationship-dependency-steady-red-blue-light-enterprise.png) | [预览](images/xml/relationship-dependency-steady-red-blue-light-enterprise.png) |
| ER 关系 | Mint green｜清爽绿 | [DSL](dsl/relationship-er.md) | [SVG](svg/relationship-er-mint-green-light-enterprise.svg) | [Draw.io](xml/relationship-er-mint-green-light-enterprise.drawio) | [预览](images/svg/relationship-er-mint-green-light-enterprise.png) | [预览](images/xml/relationship-er-mint-green-light-enterprise.png) |
| 知识关系 | Mint green｜清爽绿 | [DSL](dsl/relationship-knowledge.md) | [SVG](svg/relationship-knowledge-mint-green-light-enterprise.svg) | [Draw.io](xml/relationship-knowledge-mint-green-light-enterprise.drawio) | [预览](images/svg/relationship-knowledge-mint-green-light-enterprise.png) | [预览](images/xml/relationship-knowledge-mint-green-light-enterprise.png) |
| 路线图 | Steady Red & Blue｜稳重红蓝 | [DSL](dsl/roadmap.md) | [SVG](svg/roadmap-steady-red-blue-light-enterprise.svg) | [Draw.io](xml/roadmap-steady-red-blue-light-enterprise.drawio) | [预览](images/svg/roadmap-steady-red-blue-light-enterprise.png) | [预览](images/xml/roadmap-steady-red-blue-light-enterprise.png) |
| 时序图 | Tech Blue｜科技蓝（默认） | [DSL](dsl/sequence.md) | [SVG](svg/sequence-tech-blue-light-enterprise.svg) | [Draw.io](xml/sequence-tech-blue-light-enterprise.drawio) | [预览](images/svg/sequence-tech-blue-light-enterprise.png) | [预览](images/xml/sequence-tech-blue-light-enterprise.png) |
| 状态图 | Tech Blue｜科技蓝（默认） | [DSL](dsl/state.md) | [SVG](svg/state-tech-blue-light-enterprise.svg) | [Draw.io](xml/state-tech-blue-light-enterprise.drawio) | [预览](images/svg/state-tech-blue-light-enterprise.png) | [预览](images/xml/state-tech-blue-light-enterprise.png) |
| 总结图 | Vibrant ｜活力 | [DSL](dsl/summary.md) | [SVG](svg/summary-vibrant-light-enterprise.svg) | [Draw.io](xml/summary-vibrant-light-enterprise.drawio) | [预览](images/svg/summary-vibrant-light-enterprise.png) | [预览](images/xml/summary-vibrant-light-enterprise.png) |
| SWOT 分析 | Steady Red & Blue｜稳重红蓝 | [DSL](dsl/swot.md) | [SVG](svg/swot-steady-red-blue-light-enterprise.svg) | [Draw.io](xml/swot-steady-red-blue-light-enterprise.drawio) | [预览](images/svg/swot-steady-red-blue-light-enterprise.png) | [预览](images/xml/swot-steady-red-blue-light-enterprise.png) |
| 时间线 | Steady Red & Blue｜稳重红蓝 | [DSL](dsl/timeline.md) | [SVG](svg/timeline-steady-red-blue-light-enterprise.svg) | [Draw.io](xml/timeline-steady-red-blue-light-enterprise.drawio) | [预览](images/svg/timeline-steady-red-blue-light-enterprise.png) | [预览](images/xml/timeline-steady-red-blue-light-enterprise.png) |

`generation-manifest.json` 记录请求、主题、骨架、主轴、结构角色和源文件哈希；`verification-report.json` 记录渲染器、清理目标、语义配对结果及全部图片哈希。
