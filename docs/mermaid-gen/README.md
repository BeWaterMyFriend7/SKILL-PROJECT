# mermaid-gen 使用说明

## 第一部分：Skill 使用说明

### 适用场景

- 在 Markdown 中维护流程、时序、ER、状态、甘特、框图等图形。
- 需要自动布局、可版本管理且可由 Mermaid CLI 真实渲染的图形。
- 精确坐标和高级视觉使用 `svg-generator`；需要 Draw.io 编辑时使用 `xml-diagram`。

### 快速使用

```text
请使用 mermaid-gen 绘制用户登录时序图，并输出为 Markdown。
```

### 支持的图类型

- 流程图、框图
- 时序图、状态图、类图
- ER 图
- 甘特图、时间线、用户旅程图
- 饼图、XY 图、象限图
- 思维导图、Git 图、桑基图
- 更多

### 核心流程

1. 分析需求并选择 Mermaid 图型。
2. 规划节点、关系、分区、方向和复杂度。
3. 生成一个完整 Mermaid block。
4. 检查围栏、主题和图型语义。
5. 使用固定版本 Mermaid CLI 渲染，并在拥挤或交叉时调整方向、简化关系或拆图。

## 第二部分：Skill 示例输出

> 现在有一个抢红包系统，请使用 mermaid-gen 绘制系统框图、用户抢红包主要流程图、用户抢红包时序图、ER 图、红包活动状态图和系统开发计划。

测试环境：Mermaid CLI 11.16.0，Chrome Headless。

### 文件索引

| 图形类型 | Markdown |
| --- | --- |
| 系统框图 | [architecture-red-packet.md](markdown/architecture-red-packet.md) |
| 主要流程图 | [flow-red-packet.md](markdown/flow-red-packet.md) |
| 时序图 | [sequence-red-packet.md](markdown/sequence-red-packet.md) |
| ER 图 | [er-red-packet.md](markdown/er-red-packet.md) |
| 状态图 | [state-red-packet.md](markdown/state-red-packet.md) |
| 开发计划 | [gantt-red-packet.md](markdown/gantt-red-packet.md) |

### 渲染截图

#### 系统框图

![系统框图](images/architecture-red-packet.png)

#### 主要流程图

![主要流程图](images/flow-red-packet.png)

#### 时序图

![时序图](images/sequence-red-packet.png)

#### ER 图

![ER 图](images/er-red-packet.png)

#### 状态图

![状态图](images/state-red-packet.png)

#### 开发计划

![开发计划](images/gantt-red-packet.png)

### 验证范围

- Markdown 围栏完整且每个文件只有一个 Mermaid block。
- 图型、固定主题和类型专属语义检查通过。
- 所有案例使用 Mermaid CLI 11.16.0 完成真实渲染。
