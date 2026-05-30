---
name: xml-diagram
description: 根据自然语言描述生成 drawio XML 格式的图形文件。支持流程图、架构图（应用架构、部署架构、系统架构、业务架构）、对比图、时间线图、状态流转图、时序图、ER图、文章总结图、卡片、图表等常用图形，输出可直接在 drawio 中打开编辑的 .drawio 文件。当用户提到 drawio、XML绘图、生成图形、流程图、架构图、时序图、ER图、文章总结等时触发。使用此 skill 生成可编辑的专业图形。
---

# XML 图形生成器（drawio 格式）

## 核心工作流

```
用户描述 → 解析需求 → 设计图形 → 生成 drawio XML → 验证 → 保存文件
```

## 执行步骤

### 第 1 步：解析需求

用户可能提供：图形类型（流程图/卡片/图表/架构图/对比图/时间线/状态流转/时序图/ER图/文章总结）、布局（横向/纵向/网格）、内容（文字/emoji）、风格（简约/专业/可爱）、背景模式（浅色/深色）

**关键**：必须确认背景模式，未明确时默认浅色

### 第 2 步：生成图形

参考示例文件：
- 流程图：`examples/flow-*.drawio`
- 架构图：`examples/architecture-*.drawio`
- 时间线：`examples/timeline-*.drawio`
- 对比图：`examples/comparison-*.drawio`
- 时序图：`examples/sequence-*.drawio`
- ER图：`examples/er-*.drawio`
- 状态图：`examples/state-*.drawio`
- 文章总结：`examples/article-*.drawio`

专业流程图示例（带标题栏卡片设计）：
- `examples/flow-rd-lifecycle.drawio` - 研发全生命周期流程图（深色）
- `examples/flow-red-packet.drawio` - 红包业务流程图

专业架构图示例（分层设计）：
- `examples/architecture-red-packet.drawio` - 红包系统架构图

### 第 3 步：验证清单

- [ ] 背景模式正确（浅色：#f8f9fa，深色：#1a1a2e）
- [ ] 节点无重叠，间距合理（纵向≥50px，横向≥40px）
- [ ] 连接线端点精确指向节点边缘
- [ ] 画布利用率 60%-80%
- [ ] 箭头样式统一（灰色#999999）
- [ ] 错误分支用红色实线，异步流程用虚线
- [ ] 图例在底部角落，与主流程分开

---

# 第一部分：统一风格规范

## 1.1 配色规范

### 浅色模式（默认）
| 用途 | 颜色 | 说明 |
|------|------|------|
| 背景 | #f8f9fa | 主背景色 |
| 卡片 | #ffffff | 节点/容器填充 |
| 边框 | #e0e0e0 | 默认边框 |
| 标题文字 | #333333 | 主标题（fontColor） |
| 正文文字 | #666666 | 内容文字（fontColor） |
| 辅助文字 | #999999 | 次要信息 |
| 箭头 | #999999 | 默认连接线 |
| 阴影 | shadow=1 | 需要时启用 |

### 深色模式
| 用途 | 颜色 | 说明 |
|------|------|------|
| 背景 | #1a1a2e | 主背景色 |
| 卡片 | #16213e | 节点/容器填充 |
| 边框 | #333333 | 默认边框 |
| 标题文字 | #ffffff | 主标题 |
| 正文文字 | #aaaaaa | 内容文字 |
| 辅助文字 | #aaaaaa | 次要信息 |
| 箭头 | #666666 | 默认连接线 |
| 阴影 | shadow=0 | 极淡或无阴影 |

### 状态色（统一）
| 用途 | 颜色 | 浅色背景 | 深色背景 |
|------|------|----------|----------|
| 步骤1/主色(蓝) | #3498db | #e3f2fd | #16213e |
| 步骤2/成功(绿) | #2ecc71 | #e8f5e9 | #16213e |
| 步骤3/警告(橙) | #e67e22 | #fff3e0 | #16213e |
| 错误(红) | #e74c3c | #fce4ec | #16213e |
| 紫色 | #9b59b6 | #f3e8ff | #16213e |

## 1.2 形状绘制规范

### 基础形状（drawio style 对应）

```xml
<!-- 圆角卡片（最常用，推荐 rounded=1）-->
<mxCell id="card1" value="卡片文字" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=14;fontStyle=1;shadow=1;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry"/>
</mxCell>

<!-- 标题栏一体式卡片（用两个 mxCell 叠加，或使用 value 的 &#xa; 换行分隔） -->
<!-- 方式1：双层叠加 -->
<mxCell id="card2" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="160" height="100" as="geometry"/>
</mxCell>
<mxCell id="card2-header" value="标题" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=none;fontColor=#ffffff;fontSize=13;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="160" height="28" as="geometry"/>
</mxCell>

<!-- 方式2：使用分隔线（推荐） -->
<mxCell id="card3" value="目标检测&#xa;────────────────&#xa;车辆/行人/障碍物检测" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=11;fontStyle=1;align=left;spacingLeft=12;spacingTop=8;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="320" width="160" height="80" as="geometry"/>
</mxCell>

<!-- 菱形判断节点（使用 rhombus 形状） -->
<mxCell id="decision1" value="条件?" 
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="80" height="80" as="geometry"/>
</mxCell>

<!-- 圆形状态节点（ellipse 形状） -->
<mxCell id="state1" value="" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=#3498db;aspect=fixed;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 结束状态：同心圆（双层椭圆叠加） -->
<mxCell id="end-outer" value="" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#2ecc71;strokeWidth=2;aspect=fixed;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="24" height="24" as="geometry"/>
</mxCell>
<mxCell id="end-inner" value="" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#2ecc71;strokeColor=none;aspect=fixed;" 
  vertex="1" parent="1">
  <mxGeometry x="104" y="104" width="16" height="16" as="geometry"/>
</mxCell>

<!-- 圆柱体/数据库 -->
<mxCell id="db1" value="数据库" 
  style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fce4ec;strokeColor=#e74c3c;strokeWidth=2;fontColor=#333333;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="350" width="60" height="60" as="geometry"/>
</mxCell>

<!-- 六边形/消息队列 -->
<mxCell id="q1" value="消息队列" 
  style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#f3e8ff;strokeColor=#9b59b6;strokeWidth=2;fontColor=#333333;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x="400" y="200" width="100" height="40" as="geometry"/>
</mxCell>
```

### 形状速查表

| 形状 | drawio style | 推荐尺寸 | 用途 |
|------|-------------|----------|------|
| 圆角矩形 | `rounded=1` | 140×60 | 通用节点/状态 |
| 菱形 | `rhombus` | 80×80 | 判断/分支 |
| 圆形 | `ellipse;aspect=fixed` | 20×20 | 状态点 |
| 圆柱体 | `shape=cylinder3` | 60×60 | 数据库 |
| 六边形 | `shape=hexagon` | 100×40 | 消息队列 |
| 文本 | `text;html=1` | 按内容 | 标签/标题 |
| 分隔线 | `line;html=1` | 按宽度 | 视觉分隔 |
| 平行四边形 | `shape=parallelogram` | 100×40 | 输入/输出 |

## 1.3 箭头规范

### 箭头样式定义（drawio edge style）

```xml
<!-- 标准实线箭头（最常用） -->
<mxCell id="edge1" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" 
  edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 蓝色激活箭头 -->
<mxCell id="edge-blue" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3498db;strokeWidth=2;endArrow=classic;endFill=1;" 
  edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 虚线连接（异步/回调） -->
<mxCell id="edge-dashed" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#9b59b6;strokeWidth=2;dashed=1;endArrow=classic;" 
  edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 红色错误分支（必须用实线！） -->
<mxCell id="edge-error" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#e74c3c;strokeWidth=2;endArrow=classic;endFill=1;" 
  edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 无箭头连接线 -->
<mxCell id="edge-noarrow" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=1;endArrow=none;" 
  edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 带标签的连接线 -->
<mxCell id="edge-label" value="标签文字" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;labelBackgroundColor=#ffffff;fontColor=#666666;fontSize=10;" 
  edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 箭头使用规则

| 场景 | 箭头颜色 | 样式 | drawio 关键属性 |
|------|----------|------|----------------|
| 普通连接 | #999999(浅)/#666666(深) | 实线 | `endArrow=classic;endFill=1` |
| 激活/进行中 | #3498db | 实线 | `endArrow=classic;endFill=1` |
| 返回消息 | #999999 | 实线 | `endArrow=classic;endFill=1` |
| 错误分支 | #e74c3c | **实线（非虚线）** | `endArrow=classic;endFill=1` |
| 异步流程 | #9b59b6 | 虚线 | `dashed=1;endArrow=classic` |

**关键原则**：
- 必须使用 `source` 和 `target` 属性关联节点 ID，让 drawio 自动计算连接路径
- 使用 `edgeStyle=orthogonalEdgeStyle` 保证正交布线，避免交叉
- 连接线标签使用 `labelBackgroundColor` 确保文字清晰
- 错误分支**绝对不能**用虚线
- 同一图中箭头风格统一

---

# 第二部分：图形类型规范

## 2.1 架构图规范

### 分层结构
1. 接入层（客户端、CDN、网关）
2. 服务层（业务服务、认证、消息队列）
3. 数据层（Redis、MySQL、MongoDB）
4. 基础层（Docker、K8s、监控）

### 布局要点

**1. 元素对齐与均匀分布**：
- 每层内的元素使用**相同宽度**
- 元素与容器左右边距**对称**，避免单侧留白
- 间距计算公式：`(容器宽度 - 元素数量 × 元素宽度) / (元素数量 + 1)`
- 示例：容器900px，5个元素140px：`间距 = (900 - 5×140) / 6 = 16.67`

**2. 元素不能超出容器**：
- 确保元素在分层背景框内部
- 元素 y 坐标 = 容器 y + (容器高度 - 元素高度) / 2（垂直居中）

**3. 标题与内容分隔**：
- 使用分隔线区分标题和内容
- 标题使用 `fontStyle=1` 加粗
- 格式：`标题&#xa;────────────&#xa;内容描述`

**4. 层标签设计**：
- 使用与该层主要功能匹配的颜色
- 位置在分层背景框上方

### 架构图类型
- **应用架构图**：展示应用系统的组件及其交互关系
- **部署架构图**：展示系统在物理或虚拟环境中的部署方式
- **系统架构图**：展示整个系统的高级结构和主要组件
- **业务架构图**：展示业务流程、组织结构和能力模型

### 参考布局（4元素均匀分布）
```xml
<!-- 容器: x=100, width=900 -->
<!-- 元素: width=180, 间距=(900-4×180)/5=36 -->
<mxCell x="136" .../>  <!-- 100+36*1 -->
<mxCell x="352" .../>  <!-- 100+36*2 -->
<mxCell x="568" .../>  <!-- 100+36*3 -->
<mxCell x="784" .../>  <!-- 100+36*4 -->
```

### 分层容器模板
```xml
<!-- 服务层容器 -->
<mxCell id="layer-svc" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e0e0e0;strokeWidth=1;dashed=0;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="220" width="1000" height="150" as="geometry"/>
</mxCell>
<!-- 层标签 -->
<mxCell id="layer-svc-label" value="② 应用层 (Application Layer)" 
  style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=14;fontStyle=1;fontColor=#2ecc71;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="195" width="300" height="25" as="geometry"/>
</mxCell>

<!-- 层内服务节点 -->
<mxCell id="svc1" value="用户服务&#xa;────────&#xa;注册登录/身份认证" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=11;fontStyle=0;align=left;spacingLeft=12;spacingTop=8;shadow=1;" 
  vertex="1" parent="1">
  <mxGeometry x="120" y="240" width="180" height="80" as="geometry"/>
</mxCell>

<!-- 服务间连接 -->
<mxCell id="edge-svc1-svc2" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=1.5;endArrow=classic;endFill=1;" 
  edge="1" parent="1" source="svc1" target="svc2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 2.2 对比图规范

### 布局原则
- 左右对称布局，中间留出对比空间
- 每侧使用相同的模块设计，左侧蓝色系，右侧绿色或橙色系
- 中间添加"VS"或明确的对比标识
- 对比项逐行对齐，便于读者比较

### 结构模板
```xml
<!-- 左侧面板 - 蓝色系 -->
<mxCell id="left-panel" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#3498db;strokeWidth=2;dashed=0;" 
  vertex="1" parent="1">
  <mxGeometry x="60" y="80" width="380" height="400" as="geometry"/>
</mxCell>

<!-- 左侧标题 -->
<mxCell id="left-title" value="OpenCode" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=18;fontStyle=1;fontColor=#3498db;" 
  vertex="1" parent="1">
  <mxGeometry x="60" y="50" width="380" height="30" as="geometry"/>
</mxCell>

<!-- VS 分隔 -->
<mxCell id="vs-label" value="VS" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=3;fontColor=#e67e22;fontSize=18;fontStyle=1;aspect=fixed;" 
  vertex="1" parent="1">
  <mxGeometry x="462" y="250" width="60" height="60" as="geometry"/>
</mxCell>

<!-- 右侧面板 - 绿色系 -->
<mxCell id="right-panel" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f5e9;strokeColor=#2ecc71;strokeWidth=2;dashed=0;" 
  vertex="1" parent="1">
  <mxGeometry x="544" y="80" width="380" height="400" as="geometry"/>
</mxCell>

<!-- 对比项（左右各一行，y 坐标对齐） -->
<mxCell id="left-item1" value="✔ 功能A" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=1;fontColor=#333333;fontSize=12;align=left;spacingLeft=10;" 
  vertex="1" parent="1">
  <mxGeometry x="80" y="100" width="340" height="30" as="geometry"/>
</mxCell>
<mxCell id="right-item1" value="✔ 功能A" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#2ecc71;strokeWidth=1;fontColor=#333333;fontSize=12;align=left;spacingLeft=10;" 
  vertex="1" parent="1">
  <mxGeometry x="564" y="100" width="340" height="30" as="geometry"/>
</mxCell>
```

## 2.3 时间线图规范

### 布局原则
- 横向时间线：从左到右表示时间流逝，适合展示项目阶段、发展历程
- 纵向时间线：从上到下表示时间流逝，适合展示事件序列、版本历史
- 节点使用圆形或小卡片表示时间点
- 连接线使用实线串连时间点
- 每个时间点包含时间标签和事件描述

### 横向时间线模板
```xml
<!-- 横向时间轴线 -->
<mxCell id="timeline-axis" value="" 
  style="endArrow=classic;html=1;strokeColor=#3498db;strokeWidth=3;endFill=1;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="80" y="200" as="sourcePoint"/>
    <mxPoint x="750" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 时间节点（圆点） -->
<mxCell id="node1" value="" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=#ffffff;strokeWidth=2;aspect=fixed;" 
  vertex="1" parent="1">
  <mxGeometry x="145" y="190" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 时间标签 -->
<mxCell id="label1" value="2024-Q1" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;fontColor=#333333;" 
  vertex="1" parent="1">
  <mxGeometry x="115" y="170" width="80" height="20" as="geometry"/>
</mxCell>

<!-- 事件描述卡片（在时间线下方） -->
<mxCell id="event1" value="项目启动&#xa;需求分析完成" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=1;fontColor=#666666;fontSize=10;align=left;spacingLeft=8;spacingTop=5;" 
  vertex="1" parent="1">
  <mxGeometry x="115" y="225" width="80" height="45" as="geometry"/>
</mxCell>
```

## 2.4 状态流转图规范（重要）

### 节点类型
- **初始状态**：实心小圆（填充状态色，直径 16-20px）
- **结束状态**：空心圆包围实心圆（绿色，外层 24px，内层 16px）
- **状态**：圆角矩形（rx=6），带边框
- **判断**：菱形（80×80），填充白色或卡片色

### 连接线规范（关键）
- **水平/垂直直线优先**：利用 drawio 的 `orthogonalEdgeStyle` 自动布线
- **分支使用折线**：先直线走到分支点，再转向（drawio 自动处理）
- **箭头指向清晰**：使用 `source`/`target` 关联节点
- **条件标注**：在连接线上用 `value` 属性标注"是"/"否"

### 布局检查点
- 所有状态节点在网格上对齐
- 连接线不穿过其他节点
- 分支有足够的垂直间距（≥50px）
- 条件标注位置不与线交叉
- 使用 `orthogonalEdgeStyle` 确保 drawio 自动避免交叉

### 示例布局
```xml
<!-- 状态节点（水平排列） -->
<mxCell id="state-a" value="订单创建" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=13;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x="130" y="80" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="state-b" value="支付处理" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=13;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x="320" y="80" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="state-c" value="支付验证" 
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=11;" 
  vertex="1" parent="1">
  <mxGeometry x="680" y="60" width="80" height="80" as="geometry"/>
</mxCell>

<!-- 连接（drawio 自动正交布线） -->
<mxCell id="edge-ab" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" 
  edge="1" parent="1" source="state-a" target="state-b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 判断分支 - 否（红色实线） -->
<mxCell id="edge-c-no" value="否" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#e74c3c;strokeWidth=2;endArrow=classic;endFill=1;labelBackgroundColor=#ffffff;fontColor=#e74c3c;fontSize=10;" 
  edge="1" parent="1" source="state-c" target="state-cancel">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 2.5 时序图规范（重要）

### 布局原则
- **生命线等距分布**：每条生命线间距 200-250px
- **消息从上到下按时间顺序排列**
- **激活条**：细矩形，顶部对齐消息起点
- **返回消息在调用下方**

### 连接线规范（关键）
- **消息线尽量水平**：利用 drawio 的直角连接
- **消息从上到下按时间顺序排列**
- **返回消息在发起消息的下方**
- **箭头指向右表示调用，指向左表示返回**
- **避免消息线交叉**：drawio 的 `orthogonalEdgeStyle` 自动处理

### 时序图模板
```xml
<!-- 生命线（垂直虚线） -->
<mxCell id="lifeline-a" value="" 
  style="endArrow=none;html=1;strokeColor=#999999;strokeWidth=1;dashed=1;dashPattern=5 5;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="150" y="80" as="sourcePoint"/>
    <mxPoint x="150" y="420" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 角色标签 -->
<mxCell id="actor-a" value="用户界面" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;fontColor=#333333;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="55" width="100" height="25" as="geometry"/>
</mxCell>

<!-- 激活条 -->
<mxCell id="active-a" value="" 
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#3498db;strokeWidth=1;" 
  vertex="1" parent="1">
  <mxGeometry x="135" y="100" width="30" height="80" as="geometry"/>
</mxCell>

<!-- 调用消息 - 从 A 到 B -->
<mxCell id="msg1" value="login(username, password)" 
  style="endArrow=classic;endFill=1;html=1;strokeColor=#3498db;strokeWidth=2;labelBackgroundColor=#f8f9fa;fontColor=#333333;fontSize=11;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="165" y="120" as="sourcePoint"/>
    <mxPoint x="355" y="120" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 返回消息 - 从 B 到 A -->
<mxCell id="msg2" value="返回结果" 
  style="endArrow=classic;endFill=1;html=1;strokeColor=#999999;strokeWidth=2;labelBackgroundColor=#f8f9fa;fontColor=#666666;fontSize=11;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="355" y="200" as="sourcePoint"/>
    <mxPoint x="165" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

## 2.6 ER图规范

### 图形元素
- **实体**：圆角矩形（带顶部标题栏），浅色背景
- **属性**：实体内的行，使用分隔线区分
- **关系**：菱形连接符（可简化标注在线上的文字）
- **连接线**：实线，可选基数标注

### 约束表示
- 主键：加粗或 (PK) 标识
- 外键：斜体或 (FK) 标识
- 基数：在连接线上用 `value` 标注（1, N）

### ER图模板
```xml
<!-- 实体：用户 -->
<mxCell id="entity-user" value="用户 (User)&#xa;────────────&#xa;+ id: int (PK)&#xa;+ username: varchar(50)&#xa;+ email: varchar(100)" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=11;fontStyle=0;align=left;spacingLeft=12;spacingTop=5;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="95" as="geometry"/>
</mxCell>

<!-- 实体：订单 -->
<mxCell id="entity-order" value="订单 (Order)&#xa;────────────&#xa;+ order_id: int (PK)&#xa;+ user_id: int (FK)&#xa;+ order_date: datetime" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=11;fontStyle=0;align=left;spacingLeft=12;spacingTop=5;" 
  vertex="1" parent="1">
  <mxGeometry x="400" y="100" width="200" height="95" as="geometry"/>
</mxCell>

<!-- 关系连接 + 基数标注 -->
<mxCell id="edge-user-order" value="1..N" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;labelBackgroundColor=#f8f9fa;fontColor=#666666;fontSize=10;" 
  edge="1" parent="1" source="entity-user" target="entity-order">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 关系菱形（可选） -->
<mxCell id="rel-places" value="下单" 
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=1;fontColor=#333333;fontSize=10;" 
  vertex="1" parent="1">
  <mxGeometry x="275" y="202" width="50" height="40" as="geometry"/>
</mxCell>
```

## 2.7 文章总结图规范

### 布局原则
- **卡片流程式布局**：从左到右排列步骤卡
- **每张卡片包含**：步骤编号（标题栏）、标题、详细描述
- **箭头连接**：表示步骤顺序
- **底部注意事项框**：整图底部

### 浅色模式模板
```xml
<!-- 标题 -->
<mxCell id="title" value="文章标题" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#333333;" 
  vertex="1" parent="1">
  <mxGeometry x="250" y="10" width="300" height="30" as="geometry"/>
</mxCell>

<!-- 步骤1卡片（带标题栏） -->
<mxCell id="step1-body" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;shadow=1;" 
  vertex="1" parent="1">
  <mxGeometry x="80" y="90" width="160" height="100" as="geometry"/>
</mxCell>
<mxCell id="step1-header" value="Step 1" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=none;fontColor=#ffffff;fontSize=12;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x="80" y="90" width="160" height="28" as="geometry"/>
</mxCell>
<mxCell id="step1-title" value="准备工具" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fontColor=#333333;" 
  vertex="1" parent="1">
  <mxGeometry x="80" y="125" width="160" height="20" as="geometry"/>
</mxCell>
<mxCell id="step1-desc" value="下载安装 WorkBuddy" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=10;fontColor=#666666;" 
  vertex="1" parent="1">
  <mxGeometry x="80" y="150" width="160" height="20" as="geometry"/>
</mxCell>

<!-- 步骤间箭头 -->
<mxCell id="arrow-1-2" 
  style="endArrow=classic;endFill=1;html=1;strokeColor=#999999;strokeWidth=2;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="240" y="140" as="sourcePoint"/>
    <mxPoint x="300" y="140" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 注意事项框 -->
<mxCell id="notes-box" value="⚠️ 注意事项&#xa;────────────&#xa;• 注意事项1&#xa;• 注意事项2&#xa;• 注意事项3" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e0e0e0;strokeWidth=1;fontColor=#666666;fontSize=10;align=left;spacingLeft=15;spacingTop=8;" 
  vertex="1" parent="1">
  <mxGeometry x="80" y="360" width="640" height="90" as="geometry"/>
</mxCell>
```

### 深色模式要点
- 卡片背景：`fillColor=#16213e`（代替 #ffffff）
- 标题栏保持原色（如 #3498db）
- 文字：`fontColor=#ffffff`（标题）、`fontColor=#aaaaaa`（描述）
- 注意事项框边框：`strokeColor=#333333`

## 2.8 独立卡片规范

### 适用场景
- 信息展示卡片（用户信息卡、产品卡、统计数据卡）
- 功能入口卡片（仪表盘、导航页）
- 步骤引导卡片（单张强调卡）

### 基础卡片模板
```xml
<!-- 标准信息卡 -->
<mxCell id="card-info" value="用户信息&#xa;────────────&#xa;姓名：张三&#xa;部门：技术部&#xa;角色：管理员" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=12;align=left;spacingLeft=15;spacingTop=8;shadow=1;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="220" height="120" as="geometry"/>
</mxCell>

<!-- 统计数字卡 -->
<mxCell id="card-stat" value="总用户数&#xa;────────────&#xa;12,458&#xa;↑ 12.5%" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#3498db;strokeWidth=1;fontColor=#333333;fontSize=12;align=center;verticalAlign=middle;shadow=1;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="250" width="160" height="100" as="geometry"/>
</mxCell>

<!-- 功能入口卡（带图标） -->
<mxCell id="card-entry" value="📊 数据分析&#xa;────────────&#xa;查看业务报表与趋势分析" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#2ecc71;strokeWidth=2;fontColor=#333333;fontSize=12;align=left;spacingLeft=15;spacingTop=8;shadow=1;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="380" width="220" height="90" as="geometry"/>
</mxCell>
```

### 卡片网格布局
```xml
<!-- 2×2 卡片网格：间距30px，每行高度对齐 -->
<!-- 行1 -->
<mxCell id="card-1-1" ... x="100" y="100" width="220" height="120"/>
<mxCell id="card-1-2" ... x="350" y="100" width="220" height="120"/>
<!-- 行2 -->
<mxCell id="card-2-1" ... x="100" y="250" width="220" height="120"/>
<mxCell id="card-2-2" ... x="350" y="250" width="220" height="120"/>
```

### 配色建议
| 卡片类型 | 边框色 | 浅色背景 |
|---------|--------|---------|
| 信息展示 | #3498db（蓝） | #e3f2fd |
| 统计数据 | #2ecc71（绿） | #e8f5e9 |
| 功能入口 | #9b59b6（紫） | #f3e8ff |
| 警告提示 | #e67e22（橙） | #fff3e0 |
| 错误/危险 | #e74c3c（红） | #fce4ec |

## 2.9 图表规范（条形图/饼图/折线图）

drawio 没有原生图表组件，通过基础形状组合实现：

### 条形图
```xml
<!-- Y轴 -->
<mxCell id="chart-axis-y" value="" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=2;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry"><mxPoint x="100" y="60" as="sourcePoint"/><mxPoint x="100" y="300" as="targetPoint"/></mxGeometry>
</mxCell>
<!-- X轴 -->
<mxCell id="chart-axis-x" value="" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=2;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry"><mxPoint x="100" y="300" as="sourcePoint"/><mxPoint x="500" y="300" as="targetPoint"/></mxGeometry>
</mxCell>
<!-- 柱形（用矩形 + fillColor） -->
<mxCell id="bar-1" value="Q1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=#3498db;fontColor=#ffffff;fontSize=10;verticalAlign=bottom;" vertex="1" parent="1">
  <mxGeometry x="130" y="180" width="50" height="120" as="geometry"/>
</mxCell>
<mxCell id="bar-2" value="Q2" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#2ecc71;strokeColor=#2ecc71;fontColor=#ffffff;fontSize=10;verticalAlign=bottom;" vertex="1" parent="1">
  <mxGeometry x="210" y="140" width="50" height="160" as="geometry"/>
</mxCell>
<mxCell id="bar-3" value="Q3" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e67e22;strokeColor=#e67e22;fontColor=#ffffff;fontSize=10;verticalAlign=bottom;" vertex="1" parent="1">
  <mxGeometry x="290" y="200" width="50" height="100" as="geometry"/>
</mxCell>
```

### 饼图（扇形组合）
饼图通过多个重叠的扇形（pie shape）或弧形（arc shape）实现：
```xml
<!-- 使用 drawio 的 pie 形状 -->
<mxCell id="pie-slice-1" value="40%" style="shape=pie;part=0.4;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=#ffffff;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="150" height="150" as="geometry"/>
</mxCell>
<!-- 图例 -->
<mxCell id="legend-1" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="280" y="110" width="15" height="15" as="geometry"/>
</mxCell>
<mxCell id="legend-1-label" value="产品A (40%)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="300" y="108" width="100" height="20" as="geometry"/>
</mxCell>
```

### 折线图
使用 drawio 的 `<mxCell>` 连接多段折线，或使用 `shape=curvedConnector`：
```xml
<!-- 折线（用 edge 连接数据点） -->
<mxCell id="line-chart" value="" style="curved=1;endArrow=none;html=1;strokeColor=#3498db;strokeWidth=2;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="130" y="200"/><mxPoint x="210" y="140"/>
      <mxPoint x="290" y="180"/><mxPoint x="370" y="120"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 图表配色原则
- 使用标准状态色系（蓝→绿→橙→紫→红）循环
- 每个数据系列保持颜色一致
- 数值标注用 `fontColor=#666666`
- 坐标轴用 `#333333`

---

# 第三部分：代码模板

## 基础结构（浅色模式）
```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" pageWidth="800" pageHeight="600" pageBackground="#f8f9fa">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- 背景提示：使用 pageBackground 或在 root 下添加背景矩形 -->
        
        <!-- 标题 -->
        <mxCell id="title" value="图表标题" 
          style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="300" y="10" width="200" height="30" as="geometry"/>
        </mxCell>
        
        <!-- 图形元素放在这里 -->
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 基础结构（深色模式）
```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" pageWidth="800" pageHeight="600" pageBackground="#1a1a2e">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- 标题 - 深色 -->
        <mxCell id="title" value="图表标题" 
          style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#ffffff;" 
          vertex="1" parent="1">
          <mxGeometry x="300" y="10" width="200" height="30" as="geometry"/>
        </mxCell>
        
        <!-- 深色图形元素：fillColor=#16213e, strokeColor=#333333, fontColor=#ffffff/#aaaaaa -->
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 常用元素速查

### 文本标签
```xml
<mxCell id="text1" value="标签内容" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=14;fontColor=#333333;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="100" height="30" as="geometry"/>
</mxCell>
```

### 分隔线
```xml
<mxCell id="divider1" value="" 
  style="line;html=1;strokeColor=#e0e0e0;strokeWidth=1;fill=1;dashed=0;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="1" as="geometry"/>
</mxCell>
```

### 图标/Emoji
```xml
<mxCell id="icon1" value="🚀" 
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=24;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="40" height="40" as="geometry"/>
</mxCell>
```

---

# 第四部分：布局规范

## 节点尺寸
- 菱形（判断）：80×80px
- 矩形（状态/步骤）：140-160px宽，50-60px高
- 卡片（服务）：180-200px宽，80-115px高
- 步骤卡（文章总结）：160px宽，100px高
- 圆形（状态点）：16-20px直径
- 圆形（结束状态）：24px（外层）/ 16px（内层）
- 数据库（圆柱体）：60×60px

## 间距
- 垂直：50-60px
- 水平：40-60px
- 分支点前：≥50px
- 图例区域：100-120px

## 画布计算
```
画布高度 = 标题40 + 内容总高 + 间距×(节点数-1) + 图例120 + 边距40
画布宽度 = 边距40 + 最大宽×列数 + 列间距×(列数-1) + 边距40
```

## 重要规约

### XML 注释禁止双连字符
- ❌ `<!-- j-- -->`
- ✅ `<!-- j decreases -->`

### 错误分支
- 必须用红色实线（#e74c3c）
- 不可用虚线

### 异步流程
- 用虚线表示
- 颜色用紫色（#9b59b6）

---

## 输出

保存为 `.drawio` 文件至 `output/drawio/` 目录（或用户指定位置），可直接在 drawio/diagrams.net 中打开编辑或导出为 PNG/SVG/PDF。

文件命名规范：`<图类型>-<描述>[-dark|-light].drawio`

## 触发条件

当用户提到：
- drawio、XML绘图、生成图形
- 流程图、架构图、对比图、时间线图、状态流转图、时序图、ER图
- 文章总结、教程图、步骤图
- 生成一个图、把文字变成图
- 需要可编辑的图形文件
