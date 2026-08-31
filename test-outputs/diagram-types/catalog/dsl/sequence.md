# 时序图 DSL：统一登录认证时序

生成方式：fresh-catalog-v1
规格哈希：6a3c13a9ebd4b6360b0538aa39c1f91687769d5edc1981c1e9cca641d05ceea6

## 原始自然语言需求

绘制用户、前端应用、认证中心、账户服务和审计平台参与的统一登录认证时序。

## 可执行蓝图

- 图形类型：sequence（时序图）
- 核心结论：登录请求经过身份校验和令牌签发后访问账户，并记录完整审计事件。
- 视觉骨架：交互时序
- 视觉主题：Tech Blue｜科技蓝（默认）
- 布局：horizontal-flow
- 主叙事轴：x
- 视觉合同：enterprise-v2
- 附加模块：focus-node、footer-band
- 图标策略：仅在入口、焦点或关键区域按内容少量使用自包含线性图标，不设置硬上限

## 结构颜色映射

- axis-main: #2AA7C8（来源：data-cyan）
- axis-cross: #3B6EDC（来源：main-blue）
- side-rail: #2D56B3（来源：deep-blue）
- focus: #5B8FF9（来源：medium-blue）
- data-flow: #3B6EDC（来源：main-blue）
- group: #5B8FF9（来源：medium-blue）
- connector: #3B6EDC（来源：main-blue）

## 质量预期

页面标题、区域、卡片和辅助信息层级清楚；唯一焦点承载核心结论；同类组件颜色一致；连线不穿越节点；XML/SVG 节点、角色和几何语义一致。
