---
name: xml-diagram
description: 根据自然语言描述生成 XML 格式（drawio）的图形文件。支持流程图、卡片、图表、图标等常用图形，输出可直接在 drawio 中打开编辑的 .drawio 文件。与 svg-generator 功能完全一致，但输出 drawio XML 格式。当用户提到 XML 绘图、drawio、生成图形、流程图时触发。
---

# XML 图形生成器（drawio 格式）

## 核心工作流

```
用户描述 → 解析需求 → 设计图形 → 生成 drawio XML → 验证输出 → 保存文件
```

详细流程如下：
1. 接收用户描述
    - 用户可能会描述需要的图类型（流程图、卡片、图表等）、布局（横向、纵向、网格等）、内容（文字、emoji）和风格（简约，专业、可爱等）。
    - 解析用户输入，提取关键信息以指导后续的图形设计和生成。
2. 解析用户需求
    - 思考需要绘制的图类型、结构、元素、布局和配色，如果不清楚的情况，请用户确认。
    - 评估元素数量，合理分组，避免单个图形承载过多内容
3. 根据分析结果，设计图的布局和元素
    - 确定图的整体结构和层次关系
    - 设计每个元素的样式（颜色、形状、大小等）
    - 确定元素之间的连接方式（线条、箭头等）
4. 生成 drawio XML 代码
    - 使用 drawio 的 mxGraph XML 格式构建图形
    - 应用 CSS 样式内嵌到 SVG 中
    - 根据风格选择应用滤镜和阴影效果
5. 针对生成的图进行验证，确保其符合用户需求和预期的视觉效果
    - **背景模式确认**：
      - 确认用户选择的背景模式（浅色/深色）
      - 未明确时默认使用浅色背景
      - 深色模式下文字和边框使用浅色系
    - **基础结构验证**（避免元素重叠和布局错乱）：
      - 检查图的结构和元素是否正确
      - 确保所有节点坐标计算准确，无重叠
      - 验证连接线起点/终点精确指向节点边缘
      - 检查文字与图形边界间距 ≥8px，避免文字溢出
    - **布局规约验证**（避免空白过多和拥挤）：
      - 画布尺寸紧凑合理，利用率 60%-80% 为宜
      - 节点间距合理，无过大或过小
      - 分支路径清晰，无路径交叉
      - 折线转折点不与节点重叠
    - **显示完整性保障**（避免显示不完整）：
      - 计算画布尺寸：`画布高度 = 标题高度 + 内容总高度 + 节点间距 × (节点数-1) + 图例说明区高度(如有) + 边距`
      - 确保所有节点、文字、连线、箭头都在画布范围内
      - 各边保留 ≥30-40px 边距，避免内容被裁剪
    - **箭头与连接验证**（避免箭头混乱）：
      - 检查箭头样式统一
      - 验证箭头指向准确，无偏移或错位
      - 检查折线路径节点顺序正确，无交叉混乱
      - 验证虚线仅用于异步流程，错误分支使用实线
    - **稳健性设计检查**：
      - 避免使用嵌套坐标，所有坐标使用明确数值
      - 确保菱形判断节点中心坐标准确，分支从底部中心出发
      - 验证汇聚点位置在分支节点正下方，避免路径交叉
      - 图例应置于图形底部，避免与主流程重叠，预留专用图例区域
    - **样式与颜色验证**：
      - 确保颜色和样式符合选择的风格
      - 验证 drawio XML 代码的正确性和兼容性
      - 检查图的布局和元素之间的连接是否合理、线条是否清晰准确、图形是否清晰可读、颜色是否符合预期、排版是否整齐
      - 检查图中箭头是否清晰、连接是否正常、大小是否合适
      - 检查图片是否能够完整显示，是否有元素被截取
    - **复杂流程图验证**：
      - 分支流程使用不同颜色区分（错误分支用红色，主线用灰色/蓝色）
      - 条件判断节点使用菱形形状
      - 异步流程使用虚线连接（仅用于异步场景）
      - 汇聚点明确标注
      - 可选区域用虚线框表示
6. 输出最终的 drawio XML 文件，供用户使用和修改
    - 将 drawio XML 保存到指定路径，文件名以 `.drawio` 结尾
    - 提供 drawio XML 代码字符串供用户复制使用

**核心原则：生成的 drawio 图形要简洁美观，符合现代设计规范，与 svg-generator 风格保持一致。**

## 视觉风格规范

### 背景模式

**重要：生成图形时必须明确用户需要的背景模式，未明确时默认使用浅色背景**

#### 1. 浅色背景模式（默认）

适用于：浅色主题文档、PPT、网页等

参考示例：浅色流程图、浅色架构图

| 用途 | 颜色代码 |
|------|----------|
| 背景色 | `#f8f9fa` |
| 卡片背景 | `#ffffff` |
| 标题文字 | `#333333` |
| 正文文字 | `#666666` 或 `#999999` |
| 边框色 | `#e0e0e0` |
| 箭头颜色 | `#999999` 或 `#666` |

#### 2. 深色背景模式

适用于：深色主题文档、演示文稿、代码编辑器主题等

参考示例：深色流程图、深色时间线

| 用途 | 颜色代码 |
|------|----------|
| 背景色 | `#1a1a2e` |
| 卡片背景 | `#16213e` |
| 标题文字 | `#ffffff` |
| 正文文字 | `#aaaaaa` 或 `#888888` |
| 边框色 | `#333333` |
| 箭头颜色 | `#666666` 或 `#555555` |

**深色模式配色速查**：
| 用途 | 颜色代码 |
|------|----------|
| 主色（蓝） | `#3498db` |
| 成功（绿） | `#2ecc71` |
| 警告（橙） | `#e67e22` |
| 错误（红） | `#e74c3c` |
| 紫色 | `#9b59b6` |
| 青色 | `#1abc9c` |
| 黄色 | `#f39c12` |
| 青色2 | `#00cec9` |

**深色背景下的特殊处理**：
- 文字使用浅色系确保对比度
- 节点边框适当加粗（2-3px）以增强可见性
- 建议使用圆角卡片提升视觉层次

### 配色方案

| 用途 | 颜色代码 |
|------|----------|
| 主色（蓝色） | `#3498db` |
| 辅助色（绿色） | `#2ecc71` |
| 强调色（橙色） | `#e67e22` |
| 警示色（红色） | `#e74c3c` |
| 背景色 | `#f8f9fa` |
| 文字色 | `#333333` 或 `#666666` |
| 边框色 | `#e0e0e0` |
| 箭头颜色 | `#999999` 或 `#3498db`（灰色/蓝色） |

### 图形规范

| 项目 | 浅色模式默认值 | 深色模式默认值 |
|------|---------------|---------------|
| 画布尺寸 | 800×600 | 800×600 |
| 圆角半径 | 8px（卡片） | 8px（卡片） |
| 阴影 | 柔和阴影 | 无阴影或淡阴影 |
| 边框宽度 | 2px | 2-3px |
| 字体 | PingFang SC, Microsoft YaHei, sans-serif | PingFang SC, Microsoft YaHei, sans-serif |
| 线条粗细 | 2px | 2px |

### 布局规范（重要）

#### 1. 形状拼接规范（避免圆弧不协调）

**问题说明**：当一个形状内部包含另一个形状（如带标题栏的卡片）时，如果分别设置圆角会导致边界不协调。

**正确做法 - 使用单层结构**：
```xml
<!-- 推荐：使用单一圆角矩形，标题通过不同颜色或位置区分 -->
<mxCell id="node1" value="节点名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=14;fontStyle=1;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
</mxCell>
```

**简化设计原则**：
- 避免使用双层形状叠加（一个带圆角的矩形+一个矩形标题栏）
- 如需区分标题区域，使用颜色填充而非叠加形状
- 标题文字使用粗体或不同颜色区分，不单独创建标题块
- drawio 中直接使用 `fontStyle=1` 让文字加粗，或使用不同 `fontColor` 区分标题

#### 2. 线条布局规范（避免混乱与重叠）

**节点间距规则**：
- 横向节点间距：≥ 40px
- 纵向节点间距：≥ 30px
- 分支节点间距：分支点前垂直距离 ≥ 50px

**连接线规范**：
- 连接线端点距节点边界：≥ 5px
- 折线转折点：使用整数坐标
- 避免三条以上路径经过同一坐标点
- 优先使用直线，其次折线，谨慎使用曲线
- 使用 `edgeStyle=orthogonalEdgeStyle` 确保折线正交

**分支路径规则**：
- 双分支左右偏转角度：30-45°
- 分支展开角度合理，避免交叉
- 汇聚点位于所有分支节点的公共下方

**防重叠检查**：
- 连接线不穿过其他节点
- 文字与图形边界间距 ≥ 8px
- 图例与主流程保持 ≥ 30px 间距

#### 3. 紧凑布局规范（优化流程图布局）

**核心原则**：在保证可读性的前提下，最大化画布利用率（70-80%），减少空白区域，创建简洁紧凑的流程图。

**节点尺寸规范**：
- 菱形判断节点：高度 50-60px，宽度 100-140px
- 矩形操作节点：高度 35-40px，宽度 100-140px  
- 圆形开始/结束节点：直径 40-50px
- 文字字体大小：节点内文字 11-13px，标签文字 10-11px

**间距规范**：
- 垂直节点间距：50-60px（主线流程）
- 水平节点间距：40-60px（并行流程）
- 分支节点间距：分支点前垂直距离 ≥ 50px
- 图例区域高度：100-120px（位于画布底部）

**画布计算**：
```
画布高度 = 标题高度(40) + 内容总高度 + 节点间距 × (节点数-1) + 图例说明区高度(100-120) + 边距(40)
画布宽度 = 边距(40) + 最大节点宽度 × 列数 + 列间距 × (列数-1) + 边距(40)
```

**紧凑布局检查清单**：
- [ ] 菱形节点高度 ≤ 60px
- [ ] 矩形节点高度 ≤ 40px
- [ ] 垂直间距 50-60px（非70-80px）
- [ ] 画布利用率 ≥ 70%（内容区域/画布总面积）
- [ ] 图例区域高度 ≤ 120px
- [ ] 无过大空白区域

**紧凑布局示例**：
- `examples/flowchart-insertion-sort-light.drawio` - 插入排序算法流程图（浅色模式）
- `examples/flowchart-insertion-sort-dark.drawio` - 插入排序算法流程图（深色模式）

#### 5. XML 注释规范（重要 - 避免 XML 语法错误）

**禁止在 XML 注释中使用双连字符 `--`**：
- ❌ `<!-- arr[j] = arr[j-1], j-- -->` （无效，XML 禁止注释中出现 `--`）
- ✅ `<!-- arr[j] = arr[j-1], j decreases -->` （有效）
- ✅ 直接不写注释，或使用单行注释

**验证方法**：使用 XML 解析器验证文件是否有效

#### 4. 附属节点布局规范（重要 - 避免元素重叠）

**核心原则**：当一个主节点有附属子节点（如工具箱、示例列表、说明文字）时，必须将子节点放在主节点的**外部**，不能与主节点边框重叠。

**常见错误示例**：
- ❌ 工具箱节点放在主节点下方，与边框重叠
- ❌ 示例列表放在主节点右侧但紧贴，导致文字溢出
- ❌ 说明文字放在主节点旁边，与其他元素重叠

**正确布局方式**：
- 子节点应该放在主节点的**外侧**（左侧或右侧），使用垂直列表排列
- 子节点与主节点之间保持 ≥ 10px 间距
- 如果子节点较多，考虑使用虚线框包围

```
正确示例：
┌─────────┐    ┌─────────┐
│  MCP    │    │  Skill  │
└─────────┘    └─────────┘
↑              ↑
│子节点列表    │子节点列表
（左侧）       （右侧）
```

**关系图布局检查清单**：
- [ ] 主节点（如 MCP、Skill）的附属节点是否放在外部（左侧/右侧）
- [ ] 附属节点与主节点之间是否有足够间距（≥ 10px）
- [ ] 多个附属节点是否垂直排列，不与上下元素重叠
- [ ] 说明文字区域是否与主节点区域分开
- [ ] 图例是否放在角落（建议左下角或右下角），避免与主流程重叠

#### 4. 图例与说明区域布局规范

**图例放置规则**：
- 优先放置在画布的**左下角**或**右下角**
- 如果放在底部中央，应使用**虚线框**包围，与主流程分开
- 图例尺寸应精简，避免占用过多空间

**说明文字区域**：
- 避免与图例重叠
- 可以使用虚线框包围，形成独立区域
- 放置在画布底部，与主节点区域保持距离

## drawio XML 格式规范

### 基础结构

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

### 常用元素格式

#### 1. 浅色模式圆角矩形卡片

```xml
<mxCell id="node1" value="节点名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=14;fontStyle=1;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
</mxCell>
```

#### 2. 深色模式圆角矩形卡片

```xml
<mxCell id="node1" value="节点名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#16213e;strokeColor=#3498db;strokeWidth=2;fontColor=#aaaaaa;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
</mxCell>
```

#### 3. 菱形判断节点

```xml
<mxCell id="node2" value="判断?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e67e22;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="80" height="80" as="geometry" />
</mxCell>
```

#### 4. 圆形节点

```xml
<mxCell id="node3" value="开始" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3498db;strokeWidth=2;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry" />
</mxCell>
```

#### 5. 箭头连接线

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#999999;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### 6. 虚线连接（异步/可选流程）

```xml
<mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#9b59b6;strokeWidth=2;dashed=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="node2" target="node3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### 7. 红色箭头（错误分支）

```xml
<mxCell id="edge3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#e74c3c;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="node2" target="node4">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### 8. 虚线框（可选区域）

```xml
<mxCell id="optional" value="可选流程" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8f9fa;strokeColor=#999999;strokeWidth=1;dashed=1;fontColor=#999999;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="50" y="200" width="200" height="120" as="geometry" />
</mxCell>
```

#### 9. 汇聚点

```xml
<mxCell id="join" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#666666;strokeColor=#666666;strokeWidth=0;" vertex="1" parent="1">
  <mxGeometry x="300" y="400" width="12" height="12" as="geometry" />
</mxCell>
```

### 样式属性说明

| 属性 | 说明 | 常用值 |
|------|------|--------|
| rounded | 圆角 | 0=无, 1=有 |
| whiteSpace | 文本换行 | wrap |
| html | HTML渲染 | 1 |
| fillColor | 填充颜色 | #ffffff, #16213e 等 |
| strokeColor | 边框颜色 | #3498db, #e74c3c 等 |
| strokeWidth | 边框宽度 | 2 |
| fontColor | 文字颜色 | #333333, #aaaaaa 等 |
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
- **布局描述**：横向、纵向、网格、环形
- **内容**：文字、emoji、颜色偏好
- **风格**：简约、专业、可爱
- **背景模式**：浅色/深色（重要：必须明确，未明确时默认浅色）

### 背景模式确认

**关键步骤**：生成前必须确认用户需要的背景模式

1. 询问用户：「需要浅色背景还是深色背景的图？」
2. 如用户未指定，默认使用**浅色背景**
3. 适用场景参考：
   - 浅色背景：文档、PPT、网页展示
   - 深色背景：代码截图、IDE配套图、深色主题设计稿

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
9. **表格对比** - 数据表格可视化

### 第 3 步：生成 drawio XML 代码

根据需求生成完整的 drawio 文件：

#### 浅色背景模板

```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="600" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- 背景 -->
        <mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8f9fa;strokeColor=#e0e0e0;" vertex="1" parent="1">
          <mxGeometry x="0" y="0" width="800" height="600" as="geometry" />
        </mxCell>
        
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

#### 深色背景模板

```xml
<mxfile host="app.diagrams.net">
  <diagram name="页面-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="600" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- 深色背景 -->
        <mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1a1a2e;strokeColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="0" y="0" width="800" height="600" as="geometry" />
        </mxCell>
        
        <!-- 标题 -->
        <mxCell id="title" value="图形标题" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap=1;rounded=0;fontSize=20;fontStyle=1;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="300" y="20" width="200" height="30" as="geometry" />
        </mxCell>
        
        <!-- 图形内容 -->
        <!-- 卡片示例 -->
        <mxCell id="node1" value="节点内容" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#16213e;strokeColor=#3498db;strokeWidth=2;fontColor=#aaaaaa;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="100" y="80" width="140" height="60" as="geometry" />
        </mxCell>
        
        ...
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**深色背景配色速查表**：
| 元素 | 颜色代码 |
|------|----------|
| 背景 | `#1a1a2e` |
| 卡片背景 | `#16213e` |
| 标题文字 | `#ffffff` |
| 正文文字 | `#aaaaaa` / `#888888` |
| 边框 | `#333333` |
| 箭头 | `#666` |
| 主色边框 | `#3498db` |
| 成功色 | `#2ecc71` |
| 错误色 | `#e74c3c` |

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

## 架构图规范

### 分层结构

架构图应采用分层设计，从上到下：
1. 接入层（客户端、CDN、负载均衡、网关）
2. 服务层（业务服务、认证服务、消息队列）
3. 数据层（Redis、MySQL、MongoDB）
4. 基础层（Docker、K8s、监控）

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

### 1. 背景模式确认

生成前必须确认：
- [ ] 已询问用户需要浅色还是深色背景
- [ ] 背景色与内容颜色形成良好对比
- [ ] 深色模式下文字使用浅色系（#ffffff、#aaaaaa、#888888）

### 2. 基础结构验证

- [ ] 节点圆角一致（rounded=1）
- [ ] 边框宽度适中（strokeWidth=2）
- [ ] 文字清晰可读，与背景对比度足够
- [ ] 箭头样式统一
- [ ] **形状拼接验证**：避免双层叠加导致的圆角不协调问题，使用单层结构
- [ ] **连接线验证**：确保连接线端点精确指向节点边缘，不偏移

### 3. 布局规约验证

- [ ] 画布尺寸合适，无过多空白（利用率 60%-80%）
- [ ] 节点间距合理，无拥挤或过大间距
- [ ] 分支路径清晰，无路径交叉
- [ ] 折线转折点不与节点重叠
- [ ] **防线条混乱验证**：
  - 避免三条以上路径经过同一坐标点
  - 连接线不穿过其他节点
  - 分支角度合理（30-45°），避免交叉
- [ ] 图例位于底部，与主流程无重叠

### 4. 图形完整显示验证

- [ ] 图形能够完整显示，避免元素超出画布范围
- [ ] 所有节点在画布范围内
- [ ] 连接线端点距节点边界距离合适
- [ ] 文字与图形边界间距足够

### 5. 颜色与样式验证

- [ ] 颜色符合配色规范
- [ ] 错误分支使用红色实线（非虚线）
- [ ] 异步流程使用虚线（紫色或灰色）
- [ ] 边框宽度合适（浅色模式：2px，深色模式：2-3px）

## 输出说明

生成的 drawio XML 文件可以直接：
1. 在 drawio 中打开查看和编辑
2. 保存为 .drawio 文件
3. 导出为 PNG、SVG、PDF 等格式
4. 嵌入到文档中使用

## 触发条件

当用户提到以下内容时触发：
- XML、drawio、绘图
- 流程图、关系图、结构图、架构图
- 生成一个图、把文字变成图
- drawio 编辑

## 与 svg-generator 的对应关系

本 skill 与 svg-generator 功能完全一致，区别在于输出格式：

| svg-generator | xml-diagram |
|---------------|-------------|
| 输出 SVG 格式 | 输出 drawio XML 格式 |
| `.svg` 文件 | `.drawio` 文件 |
| 可在浏览器打开 | 可在 drawio 中编辑 |
| 相同配色方案 | 相同配色方案 |
| 相同布局规范 | 相同布局规范 |
| 相同验证清单 | 相同验证清单 |
