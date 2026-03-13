# XML 图形生成规范（drawio 格式）

## 概述

本规范定义了 drawio XML 图形生成的标准，包括视觉风格、图形元素、箭头样式等，确保生成的图形统一美观。与 svg-generator 风格保持一致。

## 1. 基础规范

### 1.1 画布尺寸

| 类型 | 默认尺寸 | 最大尺寸 |
|------|---------|---------|
| 小型图 | 600×400 | 800×600 |
| 中型图 | 800×600 | 1000×800 |
| 大型图 | 1000×800 | 1200×1000 |

### 1.2 视图框

drawio 使用 pageWidth 和 pageHeight 属性：
```xml
pageWidth="800" pageHeight="600"
```

### 1.3 根元素结构

```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="600" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 图形元素 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 2. 颜色规范

### 2.1 主色调

| 用途 | 颜色代码 |
|------|---------|
| 主色（蓝色） | `#3498db` |
| 辅助色（绿色） | `#2ecc71` |
| 强调色（橙色） | `#e67e22` |
| 警示色（红色） | `#e74c3c` |
| 紫色 | `#9b59b6` |
| 青色 | `#1abc9c` |
| 黄色 | `#f39c12` |
| 青色2 | `#00cec9` |

### 2.2 中性色 - 浅色模式

| 用途 | 颜色代码 |
|------|---------|
| 背景色 | `#f8f9fa` |
| 卡片背景 | `#ffffff` |
| 标题文字 | `#333333` |
| 正文文字 | `#666666` |
| 辅助文字 | `#999999` |
| 边框色 | `#e0e0e0` |

### 2.2.1 中性色 - 深色模式

| 用途 | 颜色代码 |
|------|---------|
| 背景色 | `#1a1a2e` |
| 卡片背景 | `#16213e` |
| 标题文字 | `#ffffff` |
| 正文文字 | `#aaaaaa` |
| 边框色 | `#333333` |
| 箭头颜色 | `#666666` |

### 2.3 图层颜色 - 浅色模式

| 图层类型 | 边框颜色 | 填充颜色 |
|---------|---------|---------|
| 客户端层 | `#3498db` | `#E3F2FD` |
| 网络层 | `#e67e22` | `#FFF3E0` |
| 服务层 | `#2ecc71` | `#E8F5E9` |
| 数据层 | `#e74c3c` | `#FCE4EC` |
| 基础层 | `#95a5a6` | `#ECEFF1` |

### 2.3.1 图层颜色 - 深色模式

| 图层类型 | 边框颜色 | 填充颜色 |
|---------|---------|---------|
| 客户端层 | `#3498db` | `#16213e` |
| 网络层 | `#e67e22` | `#16213e` |
| 服务层 | `#2ecc71` | `#16213e` |
| 数据层 | `#e74c3c` | `#16213e` |
| 基础层 | `#95a5a6` | `#16213e` |

## 3. 箭头规范

### 3.1 箭头样式属性

| 属性 | 说明 | 常用值 |
|------|------|--------|
| edgeStyle | 连线样式 | orthogonalEdgeStyle=正交 |
| strokeColor | 线条颜色 | #999999, #3498db |
| strokeWidth | 线条粗细 | 2 |
| endArrow | 箭头类型 | classic, diamond |
| endFill | 箭头填充 | 0=空心, 1=实心 |
| dashed | 虚线 | 0=实线, 1=虚线 |

### 3.2 箭头颜色

- **灰色箭头**：使用 `#999999`（推荐用于连接线）
- **蓝色箭头**：使用 `#3498db`（可用于强调流程主线）
- **红色箭头**：使用 `#e74c3c`（用于错误分支）
- **紫色箭头**：使用 `#9b59b6`（用于异步流程）

### 3.3 线条样式规范

| 样式类型 | 使用场景 | stroke-dasharray | 颜色 |
|---------|---------|------------------|------|
| 实线 | 主线流程、正确分支、错误分支 | dashed=0 | `#999999` 或 `#e74c3c` |
| 虚线 | 异步/回调流程 | dashed=1 | `#9b59b6` 或 `#999999` |

**重要原则**：
- 错误分支必须使用实线，用颜色（红色）区分，不可用虚线
- 虚线仅用于表示异步、回调、定时任务等非同步场景

## 4. 图形元素规范

### 4.1 节点基础样式

| 属性 | 说明 | 常用值 |
|------|------|--------|
| rounded | 圆角 | 0=无, 1=有 |
| whiteSpace | 文本换行 | wrap |
| fillColor | 填充颜色 | #ffffff, #16213e 等 |
| strokeColor | 边框颜色 | #3498db, #e74c3c 等 |
| strokeWidth | 边框宽度 | 2 |
| fontColor | 文字颜色 | #333333, #aaaaaa 等 |
| fontSize | 字体大小 | 12, 14, 16 等 |
| fontStyle | 字体样式 | 0=普通, 1=粗体 |
| shadow | 阴影 | 0=无, 1=有 |

### 4.2 节点形状

```xml
<!-- 圆角矩形 -->
style="rounded=1;whiteSpace=wrap;html=1;"

<!-- 菱形（判断节点） -->
style="rhombus;whiteSpace=wrap;html=1;"

<!-- 圆形 -->
style="ellipse;whiteSpace=wrap;html=1;"

<!-- 六边形（队列） -->
style="shape=hexagon;perimeter=hexagonPerimeter;"

<!-- 圆柱形（数据库） -->
style="shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=5;"
```

### 4.3 阴影设置

- 浅色模式：`shadow=1`
- 深色模式：`shadow=0`（不使用阴影）

## 5. 架构图规范

### 5.1 分层结构

架构图应采用分层设计，从上到下：
1. 接入层（客户端、CDN、负载均衡、网关）
2. 服务层（业务服务、认证服务、消息队列）
3. 数据层（Redis、MySQL、MongoDB）
4. 基础层（Docker、K8s、监控）

### 5.2 布局原则

1. **上下对齐**：每层标签与容器左对齐
2. **居中分布**：容器内元素均匀居中分布
3. **模块间距**：模块间保持合适间距
4. **底部区域协调**：底部补充区域与主架构区域宽度协调

## 6. 流程图规范

### 6.1 画布尺寸计算规则

```
画布高度 = 标题高度 + 内容总高度 + 节点间距 × (节点数-1) + 边距
画布宽度 = 边距 + 最大节点宽度 × 列数 + 列间距 × (列数-1) + 边距
```

### 6.2 节点排列

- 横向流程：节点水平排列，间距 40-60px
- 纵向流程：节点垂直排列，间距 30-50px

### 6.3 连接线类型

#### 直线连接
```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### 折线连接（路径转向）
```xml
<mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;" edge="1" parent="1" source="node2" target="node3">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <Object x="250" y="180" />
    </Array>
  </mxGeometry>
</mxCell>
```

#### 虚线连接（异步/可选流程）
```xml
<mxCell id="edge3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#9b59b6;strokeWidth=2;dashed=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="node2" target="node3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 6.4 分支与汇聚

#### 菱形判断节点
```xml
<mxCell id="decision" value="判断条件" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="200" y="150" width="80" height="80" as="geometry" />
</mxCell>
```

#### 汇聚点
```xml
<mxCell id="join" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#666666;strokeColor=#666666;strokeWidth=0;" vertex="1" parent="1">
  <mxGeometry x="300" y="400" width="12" height="12" as="geometry" />
</mxCell>
```

#### 虚线框（可选区域）
```xml
<mxCell id="optional" value="可选流程" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8f9fa;strokeColor=#999999;strokeWidth=1;dashed=1;fontColor=#999999;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="50" y="200" width="200" height="120" as="geometry" />
</mxCell>
```

## 7. 稳健性设计规范

### 7.1 避免元素重叠和布局错乱

**1. 坐标计算规则：**
- 节点宽度 = 文字宽度 + 24px（左右边距）
- 节点高度 = 文字行数 × 行高 + 24px（上下边距）
- 水平间距 ≥ 30px
- 垂直间距 ≥ 25px

**2. 避免重叠检查：**
- 节点间水平间距 ≥ 30px
- 节点间垂直间距 ≥ 25px
- 连接线不穿过其他节点
- 文字与图形边界间距 ≥ 8px

### 7.2 避免图形显示不完整

**1. 画布尺寸计算：**
```
画布宽度 = 边距(30-40)×2 + 内容总宽度 + 间距×(列数-1)
画布高度 = 标题区(60) + 内容总高度 + 间距×(行数-1) + 边距(30-40)
```

**2. 边距保障规则：**
- 所有元素距离画布边缘 ≥ 30px
- 标题距顶部边距 ≥ 20px

### 7.3 避免箭头混乱

**1. 箭头连接规则：**
- 连接线使用 source/target 属性指向节点
- 箭头大小统一
- 折线转折点使用 Array as="points" 定义

**2. 路径优化原则：**
- 优先使用直线连接
- 避免路径交叉
- 复杂路径使用折线点

## 8. 图例位置规范

**1. 图例放置原则：**
- 图例应置于图形最底部
- 图例宽度不宜超过画布宽度的 1/3
- 图例必须位于所有图形元素下方

**2. 布局计算：**
```
图例Y坐标 = 画布高度 - 图例高度 - 底部边距(30-40)
```

## 9. 验证清单

### 9.1 背景模式确认
- [ ] 已询问用户需要浅色还是深色背景
- [ ] 背景色与内容颜色形成良好对比

### 9.2 基础结构验证
- [ ] 节点圆角一致（rounded=1）
- [ ] 边框宽度适中（strokeWidth=2）
- [ ] 文字清晰可读
- [ ] 箭头样式统一

### 9.3 布局规约验证
- [ ] 画布尺寸合适，无过多空白
- [ ] 节点间距合理
- [ ] 分支路径清晰，无路径交叉
- [ ] 图例位于底部，与主流程无重叠

### 9.4 图形完整显示验证
- [ ] 图形能够完整显示
- [ ] 所有节点在画布范围内

### 9.5 颜色与样式验证
- [ ] 颜色符合配色规范
- [ ] 错误分支使用红色实线（非虚线）
- [ ] 异步流程使用虚线
