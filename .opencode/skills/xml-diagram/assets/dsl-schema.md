# 中间结构规则

生成 XML 前必须先整理中间结构。中间结构是语义、布局、样式、连线和校验之间的约定。

## 顶层结构

```yaml
diagram:
  type: business_architecture
  mode: light
  palette: standard
  template: templates/architecture/business-layered.drawio
  title: "业务架构图"
  subtitle: "可选副标题"
  canvas:
    width: 1200
    height: 860
    margin: 32
  sections: []
  nodes: []
  edges: []
  legends: []
  annotations: []
  assumptions: []
  enrichment:
    confirmed: []
    inferred: []
    needs_confirmation: []
```

图类型建议：

```text
business_architecture = 业务架构图
application_architecture = 应用架构图
technical_architecture = 技术架构图
deployment_architecture = 部署架构图
simple_step_flow = 简约步骤流程图
sequence_diagram = 时序图
roadmap_timeline = 项目路线图
lifecycle_flow = 生命周期流程图
comparison = 对比图
summary = 总结图
```

## 区域

```yaml
sections:
  - id: sec_capability
    title: "业务能力层"
    kind: section_container
    semantic: capability
    bounds:
      x: 40
      y: 160
      width: 1120
      height: 240
    headerHeight: 44
    paddingX: 28
    paddingY: 24
    children: [card_user, card_order]
```

## 内容充实

架构图必须在 `enrichment` 中记录内容来源：

```yaml
enrichment:
  confirmed:
    - "用户明确要求：电商平台业务架构"
  inferred:
    - "补充用户、商品、订单、支付、物流、营销等常见业务域"
    - "补充监控、权限、风控等治理能力"
  needs_confirmation:
    - "是否需要包含会员等级和积分体系"
```

规则：

```text
confirmed 是用户明确给出的内容。
inferred 是根据图类型和常见架构模式补充的内容。
needs_confirmation 是影响业务事实或边界的内容，不能静默写成确定事实。
如果 inferred 为空且架构图节点很少，先补充内容，不要直接生成稀疏画布。
```

## 分组卡片

```yaml
nodes:
  - id: card_user
    parent: sec_capability
    kind: group_card
    title: "用户管理域"
    semantic: primary
    bounds:
      x: 80
      y: 228
      width: 220
      height: 120
    items:
      - "注册登录"
      - "信息管理"
      - "权限控制"
```

## 小标签

小标签用于第 3 层内容。架构图中的小标签必须作为子单元绘制成矩形，不得只作为卡片内的结构化文本。非架构图只有在内容极少且不需要编辑标签时，才允许内联文字。

```yaml
items:
  - id: tag_login
    parent: card_user
    kind: item_tag
    label: "注册登录"
    semantic: neutral
    bounds:
      x: 12
      y: 42
      width: 72
      height: 22
```

架构图分组卡片的 `items` 推荐使用对象数组：

```yaml
nodes:
  - id: card_user
    kind: group_card
    title: "用户管理域"
    items:
      - { id: tag_login, label: "注册登录", kind: item_tag }
      - { id: tag_profile, label: "资料维护", kind: item_tag }
      - { id: tag_auth, label: "权限控制", kind: item_tag }
```

## 连线

```yaml
edges:
  - id: e_user_to_order
    from: card_user
    to: card_order
    type: normal
    label: "调用"
```

## 时序图参与者

```yaml
participants:
  - id: browser
    title: "浏览器"
    bounds:
      x: 80
      y: 120
      width: 140
      height: 48
    lifeline:
      x: 150
      y1: 168
      y2: 680
    activations:
      - { y1: 220, y2: 560 }
```

时序图消息：

```yaml
messages:
  - id: msg_login
    from: browser
    to: gateway
    type: sync
    label: "提交登录"
    y: 230
  - id: msg_login_return
    from: gateway
    to: browser
    type: return
    label: "返回 Token"
    y: 520
```

时序图激活条：

```yaml
activations:
  - id: act_gateway_login
    participant: gateway
    y1: 220
    y2: 560
  - id: act_auth_verify
    participant: auth_service
    y1: 300
    y2: 500
```

连线类型：

```text
普通
主流程
异步
错误
成功
返回
带标签
层间连接
生命线
激活条
```

## 图例

```yaml
legends:
  - id: legend_main
    type: color
    placement: right
    items:
      - { label: "前端/用户", color: primary }
      - { label: "服务/能力", color: success }
```

## 规划检查

渲染 XML 前确认：

```text
每个节点都有稳定标识。
除页面标题和图例外，每个节点都有父级。
每个区域都有标题安全区。
每个卡片都在区域边界内。
每条连线都引用存在的节点标识。
已判断是否需要图例。
架构图第 3 层内容已拆成小矩形标签。
时序图已包含生命线和必要激活条。
```
