# ER 关系 DSL：订单领域实体关系

生成方式：fresh-catalog-v1
规格哈希：02e3f205d1e9cd50d7e3510407b03fd132a43e219b7a907d82868ffb4ee67163

## 原始自然语言需求

绘制客户、订单、订单项、商品、支付单和地址之间的实体关系，突出订单聚合根。

## 可执行蓝图

- 图形类型：relationship-er（ER 关系）
- 核心结论：订单聚合客户、商品、支付和履约信息，形成一致的交易数据模型。
- 视觉骨架：关系数据
- 视觉主题：Mint green｜清爽绿
- 布局：network
- 主叙事轴：radial
- 视觉合同：enterprise-v2
- 附加模块：focus-node、footer-band
- 图标策略：仅在入口、焦点或关键区域按内容少量使用自包含线性图标，不设置硬上限

## 结构颜色映射

- axis-main: #2E8B57（来源：mint-green）
- axis-cross: #14B8A6（来源：teal-green）
- side-rail: #2E8B57（来源：mint-green）
- focus: #14B8A6（来源：teal-green）
- data-flow: #14B8A6（来源：teal-green）
- group: #2E8B57（来源：mint-green）
- connector: #14B8A6（来源：teal-green）

## 质量预期

页面标题、区域、卡片和辅助信息层级清楚；唯一焦点承载核心结论；同类组件颜色一致；连线不穿越节点；XML/SVG 节点、角色和几何语义一致。
