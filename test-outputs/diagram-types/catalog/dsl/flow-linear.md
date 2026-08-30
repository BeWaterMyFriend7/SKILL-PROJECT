# 线性流程 DSL：企业付款审批流程

生成方式：fresh-catalog-v1
规格哈希：b0840d889bb3654622c421723d62d08788985f1d37d6a8d42076551d443e16d9

## 原始自然语言需求

绘制从付款申请、材料校验、负责人审批、财务复核到银行支付和结果归档的线性流程。

## 可执行蓝图

- 图形类型：flow-linear（线性流程）
- 核心结论：付款申请经过逐级校验和审批后执行支付并完整归档。
- 视觉骨架：线性流程
- 视觉主题：Tech Blue｜科技蓝（默认）
- 布局：horizontal-flow
- 主叙事轴：x
- 视觉合同：enterprise-v2
- 附加模块：focus-node、footer-band、top-band
- 图标策略：仅在入口、焦点或关键区域按内容少量使用自包含线性图标，不设置硬上限

## 结构颜色映射

- axis-main: #3B6EDC（来源：main-blue）
- axis-cross: #2AA7C8（来源：data-cyan）
- side-rail: #2D56B3（来源：deep-blue）
- focus: #5B8FF9（来源：medium-blue）
- data-flow: #2AA7C8（来源：data-cyan）
- group: #5B8FF9（来源：medium-blue）
- connector: #3B6EDC（来源：main-blue）

## 质量预期

页面标题、区域、卡片和辅助信息层级清楚；唯一焦点承载核心结论；同类组件颜色一致；连线不穿越节点；XML/SVG 节点、角色和几何语义一致。
