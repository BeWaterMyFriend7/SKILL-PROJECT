---
name: xml-diagram
description: 根据自然语言描述生成 drawio XML 格式的图形文件。支持流程图、卡片、图表、图标、架构图等常用图形，输出可直接在 drawio 中打开编辑的 .drawio 文件。当用户提到 drawio、XML绘图、生成图形、流程图、架构图时触发。使用此 skill 生成可编辑的专业图形。
---

# XML 图形生成器（drawio 格式）

## 核心工作流

```
用户描述 → 解析需求 → 设计图形 → 生成 drawio XML → 验证 → 保存文件
```

## 执行步骤

### 第 1 步：解析需求

用户可能提供：图形类型（流程图/卡片/图表/架构图）、布局（横向/纵向/网格）、内容（文字/emoji）、风格（简约/专业/可爱）、背景模式（浅色/深色）

**关键**：必须确认背景模式，未明确时默认浅色

### 第 2 步：生成图形

参考示例文件：
- 流程图：`examples/flow-*.drawio`
- 架构图：`examples/architecture-*.drawio`
- 时间线：`examples/timeline-*.drawio`
- 对比图：`examples/compare-*.drawio`

专业流程图示例（带标题栏卡片设计）：
- `examples/flow-rd-lifecycle-flow.drawio` - 研发全生命周期流程图（深色）
- `examples/flow-red-packet-flow.drawio` - 红包业务流程图

专业架构图示例（分层设计）：
- `examples/architecture-red-packet-architecture.drawio` - 红包系统架构图

### 第 3 步：验证清单

- [ ] 背景模式正确（浅色：#f8f9fa，深色：#1a1a2e）
- [ ] 节点无重叠，间距合理（纵向≥50px，横向≥40px）
- [ ] 连接线端点精确指向节点边缘
- [ ] 画布利用率 60%-80%
- [ ] 箭头样式统一（灰色#999999）
- [ ] 错误分支用红色实线，异步流程用虚线
- [ ] 图例在底部角落，与主流程分开

## 配色规范

### 浅色模式（默认）
| 用途 | 颜色 |
|------|------|
| 背景 | #f8f9fa |
| 卡片 | #ffffff |
| 边框 | #e0e0e0 |
| 文字 | #333333/#666666 |
| 箭头 | #999999 |

### 深色模式
| 用途 | 颜色 |
|------|------|
| 背景 | #1a1a2e |
| 卡片 | #16213e |
| 边框 | #333333 |
| 文字 | #ffffff/#aaaaaa |
| 箭头 | #666666 |

### 状态色
| 用途 | 颜色 |
|------|------|
| 主色(蓝) | #3498db |
| 成功(绿) | #2ecc71 |
| 警告(橙) | #e67e22 |
| 错误(红) | #e74c3c |
| 紫色 | #9b59b6 |

## 代码模板

### 基础结构
```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" pageWidth="800" pageHeight="600">
      <root>
        <mxCell id="0"/><mxCell id="1" parent="0"/>
        <!-- 图形元素 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 圆角卡片
```xml
<mxCell id="node1" value="节点名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=14;fontStyle=1;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry"/>
</mxCell>
```

### 菱形判断节点
```xml
<mxCell id="node2" value="判断?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="80" height="80" as="geometry"/>
</mxCell>
```

### 箭头连接线
```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 虚线连接（异步）
```xml
<mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#9b59b6;strokeWidth=2;endArrow=classic;" edge="1" parent="1" source="node2" target="node3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 红色箭头（错误分支）
```xml
<mxCell id="edge3" style="edgeStyle=orthogonalEdgeStyle;strokeColor=#e74c3c;strokeWidth=2;endArrow=classic;" edge="1" parent="1" source="node2" target="node4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 布局规范

### 节点尺寸
- 菱形：50-60px高，100-140px宽
- 矩形：35-40px高，100-140px宽
- 圆形：40-50px直径
- 文字：节点内11-13px，标签10-11px

### 间距规则
- 垂直间距：50-60px
- 水平间距：40-60px
- 分支点前垂直距离：≥50px
- 图例区域：100-120px

### 画布计算
```
画布高度 = 标题40 + 内容总高 + 间距×(节点数-1) + 图例120 + 边距40
画布宽度 = 边距40 + 最大宽×列数 + 列间距×(列数-1) + 边距40
```

## 架构图规范

### 分层结构
1. 接入层（客户端、CDN、网关）
2. 服务层（业务服务、认证、消息队列）
3. 数据层（Redis、MySQL、MongoDB）
4. 基础层（Docker、K8s、监控）

### 架构图布局要点（重要）

**1. 元素对齐与均匀分布**：
- 每层内的元素使用**相同宽度**
- 元素与容器左右边距**对称**，避免单侧留白
- 间距计算公式：`(容器宽度 - 元素数量 × 元素宽度) / (元素数量 + 1)`
- 示例：容器900px，5个元素140px：`间距 = (900 - 5×140) / 6 = 16.67`

**2. 元素不能超出容器**：
- 确保元素在分层背景框内部
- 元素 y 坐标 = 容器 y + (容器高度 - 元素高度) / 2（垂直居中）
- 或元素 y 坐标 = 容器 y + 适当边距

**3. 标题与内容分隔**：
- 使用**分隔线**（─ 或 ────）区分标题和内容
- 标题使用 `fontStyle=1` 加粗，字号稍大
- 使用 `align=left` + `spacingLeft=12` + `spacingTop=8` 左对齐布局
- 格式：`标题&#xa;────────────&#xa;内容描述`
- 示例：`value="目标检测&#xa;────────────────&#xa;车辆/行人/障碍物检测"`

**4. 底部信息框对齐**：
- 标题与内容框**垂直居中**：标题 y = 内容框 y - 20
- 两个信息框**与上层容器对齐**：左边缘对齐或右边缘对齐
- 参考 red-packet 示例：tech_box 和 flow_box 在同一水平线上

**5. 层标签设计**：
- 使用与该层主要功能匹配的颜色
- 位置在分层背景框上方

**参考布局（4元素均匀分布）**：
```xml
<!-- 容器: x=100, width=900 -->
<!-- 元素: width=180, 间距=(900-4×180)/5=36 -->
<mxCell x="136" .../>  <!-- 100+36*1 -->
<mxCell x="352" .../>  <!-- 100+36*2 -->
<mxCell x="568" .../>  <!-- 100+36*3 -->
<mxCell x="784" .../>  <!-- 100+36*4 -->
```

**标题分隔线示例**：
```xml
<mxCell value="目标检测&#xa;────────────────&#xa;车辆/行人/障碍物" 
        style="fontSize=11;fontStyle=1;align=left;spacing=8;spacingLeft=12;spacingTop=8;"
        .../>
```

**组件模板**
```xml
<!-- 服务节点 -->
<mxCell id="s1" value="服务名称" style="rounded=1;fillColor=#E8F5E9;strokeColor=#2ecc71;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="150" y="100" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 数据库 -->
<mxCell id="db1" value="数据库" style="shape=cylinder3;fillColor=#FCE4EC;strokeColor=#e74c3c;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="300" y="350" width="60" height="50" as="geometry"/>
</mxCell>

<!-- 消息队列 -->
<mxCell id="q1" value="消息队列" style="shape=hexagon;fillColor=#F3E5F5;strokeColor=#9b59b6;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="400" y="200" width="100" height="40" as="geometry"/>
</mxCell>
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

## 输出

保存为 `.drawio` 文件，可直接在 drawio 中打开编辑或导出为 PNG/SVG/PDF

## 触发条件

当用户提到：
- drawio、XML绘图、生成图形
- 流程图、架构图、结构图、关系图
- 生成一个图、把文字变成图
- 需要可编辑的图形文件
