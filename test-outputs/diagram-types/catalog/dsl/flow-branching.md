# 分支流程 DSL：智能订单处理流程

生成方式：fresh-catalog-v1
规格哈希：97909e4230dc39af55592da34512b77d22f9f86c54147527bdf6ba46ae3b296c

## 原始自然语言需求

绘制智能订单处理分支流程，从订单提交、库存校验进入风险判断，分别走自动履约、人工复核和失败补偿。

## 可执行蓝图

- 图形类型：flow-branching（分支流程）
- 核心结论：订单按库存与风险结果分流，并在异常路径完成补偿闭环。
- 视觉骨架：分支流程
- 视觉主题：Vibrant ｜活力
- 布局：horizontal-flow
- 主叙事轴：x
- 视觉合同：enterprise-v2
- 附加模块：focus-node、footer-band
- 图标策略：仅在入口、焦点或关键区域按内容少量使用自包含线性图标，不设置硬上限

## 结构颜色映射

- axis-main: #06B6D4（来源：cyan）
- axis-cross: #3B82F6（来源：blue）
- side-rail: #8B5CF6（来源：purple）
- focus: #8B5CF6（来源：purple）
- data-flow: #06B6D4（来源：cyan）
- group: #3B82F6（来源：blue）
- connector: #06B6D4（来源：cyan）

## 质量预期

页面标题、区域、卡片和辅助信息层级清楚；唯一焦点承载核心结论；同类组件颜色一致；连线不穿越节点；XML/SVG 节点、角色和几何语义一致。
