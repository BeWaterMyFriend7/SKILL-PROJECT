---
name: drawio-diagram
description: 根据自然语言描述生成 drawio 格式的图形文件。支持流程图、卡片、图表、图标、架构图等常用图形，输出可直接在 drawio 中打开编辑的 .drawio 文件。当用户提到 drawio、绘图、流程图、架构图、结构图时触发。
---

# drawio 图形生成器

## 核心工作流

```
用户描述 → 解析需求 → 设计图形 → 生成 drawio XML → 验证输出 → 保存文件
```

详细流程如下：
1. 接收用户描述
    - 用户可能会描述需要的图类型（流程图、卡片、图表、架构图等）、布局（横向、纵向、网格等）、内容（文字、emoji）和风格（简约、专业、可爱等）。
    - 解析用户输入，提取关键信息以指导后续的图形设计和生成。
2. 解析用户需求
    - 思考需要绘制的图类型、结构、元素、布局和配色，如果不清楚的情况，请用户确认。
    - 评估元素数量，合理分组，避免单个图形承载过多内容
3. 根据分析结果，设计图的布局和元素
    - 确定图的整体结构和层次关系
    - 设计每个元素的样式（颜色、形状、大小等）
    - 确定元素之间的连接方式（线条、箭头等）
4. 生成 drawio 图形代码
    - 使用 drawio 的 mxGraph XML 格式构建图形
    - 应用符合规范的样式（颜色、边框、阴影等）
    - 根据风格选择应用滤镜和阴影效果
5. 针对生成的图进行验证,通过元素数字计算结果进行验证或者打开drawio程序，利用drawio程序打开图形验证，确保其符合用户需求和预期的视觉效果
    - **基础结构验证**（避免元素重叠和布局错乱）：
      - 检查图的结构和元素是否正确
      - 确保所有节点坐标计算准确，无重叠
      - 验证连接线起点/终点精确指向节点边缘
      - 检查文字与图形边界间距充足，避免文字溢出
    - **显示完整性保障**（避免显示不完整）：
      - 计算画布尺寸，确保内容完整显示
      - 确保所有节点、文字、连线、箭头都在画布范围内
      - 各边保留足够边距，避免内容被裁剪
    - **箭头与连接验证**（避免箭头混乱）：
      - 检查箭头样式统一
      - 验证箭头指向准确，无偏移或错位
      - 检查折线路径节点顺序正确，无交叉混乱
      - 验证虚线仅用于异步流程，错误分支使用实线
    - **样式与颜色验证**：
      - 确保颜色和样式符合选择的风格
      - 验证 drawio XML 代码的正确性和兼容性
      - 检查图的布局和元素之间的连接是否合理、线条是否清晰准确、图形是否清晰可读、颜色是否符合预期、排版是否整齐
      - 检查图中箭头是否清晰、连接是否正常、大小是否合适
      - 检查图片是否能够完整显示，是否有元素被截取
6. 输出最终的 drawio 文件，供用户使用和修改
    - 将 drawio XML 保存到指定路径，文件名以 `.drawio` 结尾
    - 生成的 drawio 文件可以直接在 drawio 中打开查看和编辑

**核心原则：生成的 drawio 图形要简洁美观，符合现代设计规范，与 svg-generator 风格保持一致。**

## 视觉风格规范

### 配色方案

| 用途 | 颜色代码 |
|------|----------|
| 主色（蓝色） | #3498db |
| 辅助色（绿色） | #2ecc71 |
| 强调色（橙色） | #e67e22 |
| 警示色（红色） | #e74c3c |
| 紫色 | #9b59b6 |
| 青色 | #1abc9c |
| 背景色 | #f8f9fa |
| 卡片背景 | #ffffff |
| 文字色 | #333333 或 #666666 |
| 边框色 | #e0e0e0 |
| 箭头颜色 | #999999 或 #3498db（灰色/蓝色） |

### 图层颜色

| 图层类型 | 边框颜色 | 填充颜色 |
|---------|---------|---------|
| 客户端层 | #3498db | #E3F2FD |
| 网络层 | #e67e22 | #FFF3E0 |
| 服务层 | #2ecc71 | #E8F5E9 |
| 数据层 | #e74c3c | #FCE4EC |
| 基础层 | #95a5a6 | #ECEFF1 |

### 图形规范

| 项目 | 默认值 |
|------|--------|
| 画布尺寸 | 800×600 |
| 圆角半径 | 8px（卡片） |
| 阴影 | 柔和阴影效果 |
| 边框宽度 | 2px |
| 字体 | PingFang SC, Microsoft YaHei, sans-serif |
| 线条粗细 | 2px |

## drawio XML 格式规范

### 基础结构

drawio 使用 mxGraph XML 格式，基本结构如下：

```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1420" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="600" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 图形元素 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 常用元素格式

#### 1. 圆角矩形卡片

```xml
<mxCell id="node1" value="节点名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=14;fontStyle=1;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
</mxCell>
```

#### 2. 菱形判断节点

```xml
<mxCell id="node2" value="判断?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="80" height="80" as="geometry" />
</mxCell>
```

#### 3. 圆形节点

```mxCell id="node3" value="开始" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry" />
</mxCell>
```

#### 4. 箭头连接线

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### 5. 虚线连接（异步/可选流程）

```xml
<mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#9b59b6;strokeWidth=2;dashed=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="node2" target="node3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### 6. 红色箭头（错误分支）

```xml
<mxCell id="edge3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#e74c3c;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="node2" target="node4">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 样式属性说明

| 属性 | 说明 | 常用值 |
|------|------|--------|
| rounded | 圆角 | 0=无, 1=有 |
| whiteSpace | 文本换行 | wrap |
| html | HTML渲染 | 1 |
| fillColor | 填充颜色 | #ffffff, #E3F2FD 等 |
| strokeColor | 边框颜色 | #3498db, #e74c3c 等 |
| strokeWidth | 边框宽度 | 2 |
| fontColor | 文字颜色 | #333333, #666666 |
| fontSize | 字体大小 | 12, 14, 16 等 |
| fontStyle | 字体样式 | 0=普通, 1=粗体 |
| dashed | 虚线 | 0=实线, 1=虚线 |
| shadow | 阴影 | 0=无, 1=有 |
| edgeStyle | 连线样式 | orthogonalEdgeStyle=正交, elbowEdgeStyle=肘部 |

### 分层架构图容器

```xml
<!-- 容器背景 -->
<mxCell id="layer1" value="" style="rounded=1;whiteSpace=wrap=1;html=1;fillColor=#E3F2FD;strokeColor=#3498db;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="80" width="900" height="80" as="geometry" />
</mxCell>

<!-- 图层标签 -->
<mxCell id="label1" value="① 接入层" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap=1;rounded=0;fontColor=#3498db;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="110" y="85" width="100" height="20" as="geometry" />
</mxCell>
```

## 执行步骤

### 第 1 步：解析用户需求

用户可能提供：
- **图形类型**：流程图、卡片、图表、图标、关系图、架构图
- **布局描述**：横向、纵向、网格、环形、分层
- **内容**：文字、emoji、颜色偏好
- **风格**：简约、专业、可爱

### 第 2 步：选择模板或新建

常用模板：
1. **横向流程图** - 步骤从左到右排列
2. **纵向流程图** - 步骤从上到下排列
3. **循环流程图** - 首尾相连的闭环
4. **卡片网格** - 多张卡片并列
5. **对比图** - 左右对比布局
6. **时间线** - 垂直或水平时间轴
7. **饼图/柱状图** - 数据可视化
8. **架构图** - 系统、部署、应用架构图，架构图要分层显示
9. **泳道图** - 多角色/多部门流程图
10. **思维导图** - 中心发散的层级结构

### 第 3 步：生成 drawio XML 代码

根据需求生成完整的 drawio 文件：

```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="600" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- 标题 -->
        <mxCell id="title" value="图形标题" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap=1;rounded=0;fontSize=20;fontStyle=1;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="300" y="20" width="200" height="30" as="geometry" />
        </mxCell>
        
        <!-- 图形内容 -->
        ...
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 第 4 步：保存文件

将生成的 drawio 保存到用户指定的位置，文件名以 `.drawio` 结尾。

## 箭头规范

### 箭头样式

| 样式 | 属性值 |
|------|--------|
| 灰色箭头（推荐） | strokeColor=#999999 |
| 蓝色箭头 | strokeColor=#3498db |
| 红色箭头 | strokeColor=#e74c3c |
| 紫色箭头 | strokeColor=#9b59b6 |

### 线条样式

| 样式 | 使用场景 | 属性 |
|------|---------|------|
| 实线 | 主线流程、正确分支、错误分支 | dashed=0 |
| 虚线 | 异步/回调/可选流程 | dashed=1 |

**重要原则**：
- 错误分支必须使用实线，用颜色（红色）区分，不可用虚线
- 虚线仅用于表示异步、回调、定时任务等非同步场景

### 箭头端点样式

```xml
<!-- 经典箭头 -->
endArrow=classic;endFill=1;

<!-- 空心箭头 -->
endArrow=classicEmpty;endFill=0;

<!-- 菱形端点 -->
endArrow=diamond;endFill=1;
```

## 流程图规范

### 画布尺寸计算规则

```
画布高度 = 标题高度 + 内容总高度 + 节点间距 × (节点数-1) + 边距
画布宽度 = 边距 + 最大节点宽度 × 列数 + 列间距 × (列数-1) + 边距
```

### 节点排列

- 横向流程：节点水平排列，间距 40-60px
- 纵向流程：节点垂直排列，间距 30-50px

### 连接线类型

#### 直线连接
```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;" edge="1" parent="1" source="node1" target="node2">
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

#### 曲线连接（循环/回退）
```xml
<mxCell id="edge3" style="edgeStyle=elbowEdgeStyle;rounded=1;html=1;strokeColor=#9b59b6;strokeWidth=2;dashed=1;endArrow=classic;" edge="1" parent="1" source="node3" target="node1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 分支与汇聚

#### 菱形判断节点
```xml
<mxCell id="decision" value="判断条件" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="200" y="150" width="80" height="80" as="geometry" />
</mxCell>
```

#### 分支连线标注
在连线旁边添加标注：
```xml
<mxCell id="label1" value="是" style="text;html=1;strokeColor=none;fillColor=none;align=center;fontColor=#666666;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="220" y="230" width="30" height="20" as="geometry" />
</mxCell>
```

#### 虚线框表示可选区域
```xml
<mxCell id="optional" value="可选流程" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8f9fa;strokeColor=#999999;strokeWidth=1;dashed=1;fontColor=#999999;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="50" y="200" width="200" height="120" as="geometry" />
</mxCell>
```

#### 汇聚点
```xml
<mxCell id="join" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#666666;strokeColor=#666666;strokeWidth=0;" vertex="1" parent="1">
  <mxGeometry x="300" y="400" width="12" height="12" as="geometry" />
</mxCell>
```

## 架构图规范

### 分层结构

架构图应采用分层设计，从上到下：
1. 接入层（客户端、CDN、负载均衡、网关）
2. 服务层（业务服务、认证服务、消息队列）
3. 数据层（Redis、MySQL、MongoDB）
4. 基础层（Docker、K8s、监控）

### 图层标识样式

```xml
<mxCell id="label1" value="① 接入层" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap=1;rounded=0;fontColor=#3498db;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="110" y="90" width="100" height="20" as="geometry" />
</mxCell>
```

### 分层容器样式

```xml
<mxCell id="layer1" value="" style="rounded=1;whiteSpace=wrap=html=1;fillColor=#E3F2FD;strokeColor=#3498db;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="80" width="900" height="80" as="geometry" />
</mxCell>
```

### 架构图组件模板

#### 服务节点
```xml
<mxCell id="service1" value="服务名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#2ecc71;strokeWidth=2;fontColor=#333333;fontSize=12;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="150" y="100" width="100" height="40" as="geometry" />
</mxCell>
```

#### 数据库节点
```xml
<mxCell id="db1" value="数据库" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=5;fillColor=#FCE4EC;strokeColor=#e74c3c;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="300" y="350" width="60" height="50" as="geometry" />
</mxCell>
```

#### 队列节点
```xml
<mxCell id="queue1" value="消息队列" style="shape=hexagon;whiteSpace=wrap;html=1;fillColor=#F3E5F5;strokeColor=#9b59b6;strokeWidth=2;fontColor=#333333;fontSize=12;perimeter=hexagonPerimeter;" vertex="1" parent="1">
  <mxGeometry x="400" y="200" width="100" height="40" as="geometry" />
</mxCell>
```

### 箭头使用规则

**分层架构图中箭头是可选的**：

1. **无箭头架构图**：当重点展示系统层次结构和组件分层时，可以不加箭头。

2. **带箭头架构图**：当需要表示数据流向、调用关系或处理顺序时，可添加箭头。箭头应使用统一灰色（#999999）。

```xml
<mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="layer1" target="layer2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## 验证清单

生成 drawio 后，请检查：
- [ ] 箭头样式统一（strokeWidth=2, endArrow=classic）
- [ ] 箭头颜色使用灰色 #999999、蓝色 #3498db 或红色 #e74c3c
- [ ] 节点圆角一致（rounded=1）
- [ ] 文字清晰可读，字体大小适中
- [ ] 图形能够完整显示，避免元素超出画布范围
- [ ] 颜色符合配色规范
- [ ] 分支流程使用不同颜色区分（错误分支用红色）
- [ ] 虚线仅用于异步流程
- [ ] 连接线起点/终点准确指向节点边缘

## 输出说明

生成的 drawio 文件可以直接：
1. 在 drawio 中打开查看
2. 保存为 .drawio 文件
3. 导出为 PNG、SVG、PDF 等格式
4. 嵌入到文档中使用

## 触发条件

当用户提到以下内容时触发：
- drawio、绘图
- 流程图、关系图、结构图
- 架构图、系统图
- 生成一个图、把文字变成图
