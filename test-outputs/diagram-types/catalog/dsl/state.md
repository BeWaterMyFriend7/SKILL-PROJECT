# 状态图 DSL：订单状态流转

生成方式：fresh-catalog-v1
规格哈希：fea3dc7d4c0aa87737b106d99da117d12538405dc3b630fbd69027d2f98e7110

## 原始自然语言需求

绘制订单从待支付、已支付、处理中、已完成到已关闭的状态变化，并体现取消与退款路径。

## 可执行蓝图

- 图形类型：state（状态图）
- 核心结论：订单围绕支付和履约主链路流转，异常状态拥有明确退出路径。
- 视觉骨架：闭环状态
- 视觉主题：Tech Blue｜科技蓝（默认）
- 布局：mixed-axis
- 主叙事轴：mixed
- 视觉合同：enterprise-v2
- 附加模块：focus-node、footer-band、top-band
- 图标策略：仅在入口、焦点或关键区域按内容少量使用自包含线性图标，不设置硬上限

## 结构颜色映射

- axis-main: #5B8FF9（来源：medium-blue）
- axis-cross: #3B6EDC（来源：main-blue）
- side-rail: #2D56B3（来源：deep-blue）
- focus: #3B6EDC（来源：main-blue）
- data-flow: #2AA7C8（来源：data-cyan）
- group: #5B8FF9（来源：medium-blue）
- connector: #3B6EDC（来源：main-blue）

## 质量预期

页面标题、区域、卡片和辅助信息层级清楚；唯一焦点承载核心结论；同类组件颜色一致；连线不穿越节点；XML/SVG 节点、角色和几何语义一致。
