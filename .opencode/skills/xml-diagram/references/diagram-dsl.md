# 图形 DSL

## 目录

- 通用结构
- 自然语言要求
- 图形类型
- 布局与内容
- 连线计划
- 专项结构
- DSL 完成检查

## 通用结构

生成 XML 前在内部整理以下 YAML 风格 DSL。它是思考和生成契约，不要求默认保存为文件。

```yaml
diagram:
  type: architecture.business
  title: 电商平台业务架构
  subtitle: 可选副标题
  theme: light
  purpose: 向业务和技术评审人员说明平台场景、能力及核心业务对象。
  audience: 业务负责人、产品经理、架构师
  narrative: 从上到下阅读，先看业务场景，再看核心能力，最后看业务对象与资源。
  reading_direction: top-to-bottom
  canvas:
    width: 1200
    height: 760
    margin: 40
  layout:
    pattern: layered
    density: standard
    alignment: grid
  sections: []
  nodes: []
  edges: []
  legend: null
  assumptions:
    confirmed: []
    inferred: []
    needs_confirmation: []
  quality_expectations:
    edge_policy: minimal
    target_utilization: 0.65
    avoid_crossings: true
    avoid_large_empty_areas: true
```

统一字段名称：

- 使用 `theme`，不使用 `mode`；
- 使用 `canvas.margin`，不使用顶层 `margin`；
- 边使用 `source` 和 `target`，不使用 `from` 和 `to`；
- 节点显示文本统一使用 `label`；
- `theme` 只能是 `light` 或 `dark`。

## 自然语言要求

- `purpose` 说明图形要帮助谁理解或决定什么。
- `narrative` 说明阅读顺序和核心结论，不写“展示系统架构”之类空泛短句。
- 节点名称使用明确实体，不使用“模块一”“处理器”等无业务含义名称。
- 节点说明回答“负责什么”，不重复标题。
- 连线标签使用“主体动作对象”式动词短语，如“提交订单”“发布事件”“查询库存”。
- 推断内容写入 `assumptions.inferred`，不得伪装为用户确认事实。
- 影响业务边界的未知内容写入 `needs_confirmation`。

## 图形类型

```text
architecture.business       业务架构图
architecture.application    应用架构图
architecture.technical      技术架构图
architecture.deployment     部署架构图

flow.linear                 线性步骤流程图
flow.structured             结构化复杂流程图
flow.state                  状态图
flow.lifecycle              生命周期图

interaction.sequence        时序图

relationship.er             ER 实体关系图
relationship.dependency     依赖关系图
relationship.knowledge      知识关系图

structured.comparison       对比图
structured.decision-matrix  决策矩阵
structured.swot             SWOT 分析图
structured.timeline         时间线或路线图
structured.summary          总结图
```

## 布局与内容

区域：

```yaml
sections:
  - id: capability
    label: 业务能力层
    role: primary-region
    order: 2
    layout: grid
    children: [user-domain, product-domain]
```

节点：

```yaml
nodes:
  - id: user-domain
    parent: capability
    kind: group-card
    label: 用户管理域
    description: 管理身份、资料、会员与权益。
    emphasis: primary
    items:
      - { id: identity, label: 注册认证, kind: tag }
      - { id: membership, label: 会员权益, kind: tag }
```

`group-card` 的 `label` 是语义标题。渲染 XML 时必须拆成两个元素：一个无文字的圆角卡片容器和一个独立纯文字标题 `mxCell`。标题位于卡片顶部安全区，内容标签从标题安全区下方开始。`tag` 可将矩形和内部文字保留为同一个 `mxCell`。

布局模式：

- `layered`：架构分层、依赖分层；
- `lanes`：跨角色流程和阶段；
- `flow`：线性流程、复杂流程、状态；
- `sequence`：横向参与者、纵向时间；
- `network`：知识关系和中心辐射；
- `grid`：对比、矩阵、SWOT、总结；
- `timeline`：时间线和生命周期。

先决定信息密度，再决定画布。内容不足时补充合理语义或询问用户，不使用大卡片和大留白伪装丰富；内容过多时分组、扩画布或拆图，不缩小字体。

## 连线计划

```yaml
edges:
  - id: submit-order
    source: client
    target: gateway
    relation: synchronous
    label: 提交订单
    importance: primary
    required: true
    routing: orthogonal
```

每条边必须说明：

- 为什么必须存在；
- 方向和关系类型；
- 是否属于主链路；
- 是否可由包含、分组或邻近关系替代；
- 标签是否足够简短明确。

关系类型：`normal`、`primary`、`async`、`error`、`return`、`dependency`、`state-transition`、`relationship`。

架构图默认 `edge_policy: minimal`。可由层级或包含表达的关系不画箭头。

## 专项结构

### 状态图

```yaml
state:
  direction: left-to-right
  initial: pending
  terminal: [completed, cancelled]
  main_path: [pending, paid, processing, completed]
  side_states: [cancelled, failed]
```

主状态沿一个轴排列；失败、取消和回退放在主轴外侧。每条转换必须有触发条件。双向转换不得使用完全重合路径。

### 时序图

```yaml
sequence:
  start: { label: 开始交互 }
  end: { label: 结束交互 }
  participants:
    - { id: user, label: 用户 }
    - { id: api, label: API 网关 }
    - { id: service, label: 认证服务 }
  messages:
    - { id: m1, source: user, target: api, type: sync, label: 提交登录, order: 1 }
    - { id: m2, source: api, target: service, type: sync, label: 校验凭证, order: 2 }
    - { id: m3, source: service, target: api, type: return, label: 返回结果, order: 3 }
  activations:
    - { participant: api, start: 1, end: 4 }
```

参与者横向排列；每个参与者都必须具有完整、可见的竖向生命线；时间自上而下；消息箭头横向连接；返回消息使用虚线；主要处理者使用激活条。时序图必须显式表示起点和终点，并用横向消息把起点接入首个参与者、把最终响应连接到终点。模板至少示范一次 A→B→C 调用和 C→B→A 返回，避免生成时漏掉末端参与者或下游消息。

### 关系图

```yaml
relationship:
  direction: left-to-right
  groups: [identity, transaction]
  hub_nodes: []
  show_transitive_dependencies: false
```

相关节点邻近放置，优先分层、分组或网格。默认不展示可推导的间接依赖，不允许随机散点和蜘蛛网式连接。

## DSL 完成检查

- 图形目的、受众、叙事和阅读方向明确；
- 图形类型属于支持范围；
- 每个区域和节点有稳定 ID、明确标签和职责；
- 所有边引用存在节点且有存在理由；
- 已规划颜色语义和图例需求；
- 已识别潜在交叉、拥挤和大面积空白；
- 状态图、时序图和关系图包含对应专项结构；
- XML 阶段不再需要猜测业务事实或布局。
