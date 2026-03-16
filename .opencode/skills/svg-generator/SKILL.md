---
name: svg-generator
description: 根据自然语言描述生成 SVG 代码。支持流程图、卡片、图表、图标等常用图形，输出可直接在浏览器中查看的 SVG 文件。当用户提到 SVG、生成图片、图形、图标、流程图时触发。
---

# SVG 代码生成器

## 核心工作流

```
用户描述 → 解析需求 → 设计图形 → 生成 SVG 代码 → 验证输出 → 保存文件
```
详细流程如下：
1. 接收用户描述
    - 用户可能会描述需要的图类型（流程图、卡片、图表等）、布局（横向、纵向、网格等）、内容（文字、emoji）和风格（简约、专业、可爱等）。
    - 解析用户输入，提取关键信息以指导后续的图形设计和生成。
2. 解析用户需求
    - 思考需要绘制的图类型、结构、元素、布局和配色，如果不清楚的情况，请用户确认。
    - 评估元素数量，合理分组，避免单个图形承载过多内容
3. 根据分析结果，设计图的布局和元素
    - 确定图的整体结构和层次关系
    - 设计每个元素的样式（颜色、形状、大小等）
    - 确定元素之间的连接方式（线条、箭头等）
4. 生成SVG图代码
    - 使用 SVG 元素（rect, circle, path, text, line, polygon 等）构建图形
    - 应用 CSS 样式内嵌到 SVG 中
    - 根据风格选择应用滤镜、渐变和阴影效果
5. 针对生成的图进行验证，确保其符合用户需求和预期的视觉效果
    - **背景模式确认**：
      - 确认用户选择的背景模式（浅色/深色）
      - 未明确时默认使用浅色背景
      - 深色模式下文字和边框使用浅色系
    - **基础结构验证**（避免元素重叠和布局错乱）：
      - 检查图的结构和元素是否正确
      - 确保所有节点坐标计算准确，无重叠
      - 验证连接线起点/终点精确指向节点边缘（距边界 5px）
      - 检查文字与图形边界间距 ≥8px，避免文字溢出
      - **形状拼接验证**：避免双层叠加导致的圆角不协调问题，使用单层结构
    - **布局规约验证**（避免空白过多和拥挤）：
      - 画布尺寸紧凑合理，利用率 60%-80% 为宜
      - 节点间距合理，无过大或过小
      - 分支路径清晰，无路径交叉
      - 折线转折点不与节点重叠
      - **防线条混乱验证**：避免三条以上路径经过同一坐标点，连接线不穿过其他节点
    - **显示完整性保障**（避免显示不完整）：
      - 计算画布尺寸：`画布高度 = 标题高度(40) + 内容总高度 + 节点间距 × (节点数-1) + 图例说明区高度(如有) + 边距(60-80)`（图例应置于图形底部）
      - 确保所有节点、文字、连线、阴影、箭头都在 `viewBox` 范围内
      - 各边保留 ≥30-40px 边距，避免内容被裁剪
      - 复杂流程图使用折线、虚线等元素时，确保路径端点准确
    - **箭头与连接验证**（避免箭头混乱）：
      - 检查箭头大小一致（markerWidth=6, markerHeight=4）
      - 验证箭头指向准确，无偏移或错位
      - 检查折线路径节点顺序正确，无交叉混乱
      - 验证虚线仅用于异步流程，错误分支使用实线
    - **稳健性设计检查**：
      - 避免使用嵌套 transform，所有坐标使用绝对定位
      - 确保菱形判断节点中心坐标准确，分支从底部中心出发
      - 验证汇聚点位置在分支节点正下方，避免路径交叉
      - 图例应置于图形底部，避免与主流程重叠，预留专用图例区域
    - **样式与颜色验证**：
      - 确保颜色和样式符合选择的风格
      - 验证 SVG 代码的正确性和兼容性
      - 检查图的布局和元素之间的连接是否合理、线条是否清晰准确、图形是否清晰可读、颜色是否符合预期、排版是否整齐，有无文字显示不清晰等问题
      - 检查图中箭头是否清晰、连接是否正常、大小是否合适
      - 检查图片是否能够完整显示，是否有元素被截取，包括背景、图例、文字说明等
    - **复杂流程图验证**：
      - 分支流程使用不同颜色区分（错误分支用红色，主线用灰色/蓝色）
      - 条件判断节点使用菱形形状
      - 异步流程使用虚线连接（仅用于异步场景）
      - 汇聚点明确标注
      - 可选区域用虚线框表示
6. 输出最终的 SVG 代码，供用户使用和修改
    - 将 SVG 代码保存到指定路径，文件名以 `.svg` 结尾
    - 提供 SVG 代码字符串供用户复制使用


**核心原则：生成的 SVG 要简洁美观，符合现代设计规范，参考 assets/style-guide.md 规约文件。**

## 视觉风格规范

详细规范见 [assets/style-guide.md](./assets/style-guide.md)

### 背景模式

**重要：生成 SVG 时必须明确用户需要的背景模式，未明确时默认使用浅色背景**

#### 1. 浅色背景模式（默认）

适用于：浅色主题文档、PPT、网页等

参考示例：`examples/test.svg`, `examples/complex-flow.svg`

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

参考示例：`examples/rd-lifecycle-flow.svg`, `examples/rd-timeline.svg`

| 用途 | 颜色代码 |
|------|----------|
| 背景色 | `#1a1a2e` |
| 卡片背景 | `#16213e` |
| 标题文字 | `#ffffff` |
| 正文文字 | `#aaaaaa` 或 `#888888` |
| 边框色 | `#333333` |
| 箭头颜色 | `#666666` 或 `#555555` |

**深色模式配色速查（基于实际示例）**：
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
- 阴影颜色调整为 `rgba(0,0,0,0.4)`
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
| 阴影 | `0 3px 6px rgba(0,0,0,0.1)` | `0 3px 6px rgba(0,0,0,0.4)` |
| 边框宽度 | 2px | 2-3px |
| 字体 | `PingFang SC, Microsoft YaHei, sans-serif` | `PingFang SC, Microsoft YaHei, sans-serif` |
| 线条粗细 | 2px | 2px |
| 箭头大小 | markerWidth=6, markerHeight=4 | markerWidth=6, markerHeight=4 |

### 布局规范（重要）

#### 1. 形状拼接规范（避免圆弧不协调）

**问题说明**：当一个形状内部包含另一个形状（如带标题栏的卡片）时，如果分别设置圆角会导致边界不协调。

**正确做法 - 使用单层结构**：
```svg
<!-- 推荐：使用单一矩形，标题通过覆盖层实现 -->
<rect x="100" y="100" width="140" height="60" rx="8" 
      fill="#ffffff" stroke="#3498db" stroke-width="2"/>
<!-- 标题背景 -->
<path d="M100 108 Q100 100 108 100 L132 100 Q140 100 140 108 L140 118 Q140 126 132 126 L108 126 Q100 126 100 118 Z" 
      fill="#3498db"/>
<text x="120" y="118" text-anchor="middle" font-size="12" fill="#fff">标题</text>
```

**正确做法 - 简化版（推荐）**：
```svg
<!-- 推荐：简洁设计，不使用拼接 -->
<rect x="100" y="100" width="140" height="60" rx="8" 
      fill="#ffffff" stroke="#3498db" stroke-width="2"/>
<text x="120" y="125" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">节点名称</text>
```

**简化设计原则**：
- 避免使用双层形状叠加（一个带圆角的矩形+一个矩形标题栏）
- 如需区分标题区域，使用颜色填充而非叠加形状
- 标题文字使用粗体或不同颜色区分，不单独创建标题块

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

**紧凑布局示例**（drawio 格式，SVG 风格一致）：
- `examples/flowchart-insertion-sort-light.drawio` - 插入排序算法流程图（浅色模式）
- `examples/flowchart-insertion-sort-dark.drawio` - 插入排序算法流程图（深色模式）

#### 5. SVG 导出注意事项

**drawio 转 SVG 时的箭头颜色**：
- 浅色模式导出时箭头颜色保持 `#999999`
- 深色模式导出时箭头颜色保持 `#666666`
- 确保导出设置中保留原始颜色

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

### 常用图形模板

#### 1. 流程图节点

```svg
<!-- 圆角矩形卡片 -->
<rect x="100" y="100" width="140" height="60" rx="8" 
      fill="#fff" stroke="#3498db" stroke-width="2"
      filter="url(#shadow)"/>

<!-- 圆形节点 -->
<circle cx="200" cy="200" r="30" 
        fill="#fff" stroke="#3498db" stroke-width="2"/>
```

#### 2. 箭头连接

```svg
<!-- 灰色箭头（推荐用于连接线） -->
<marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
  <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
</marker>

<!-- 蓝色箭头（可用于强调流程主线） -->
<marker id="arrowhead-blue" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
  <polygon points="0 0, 6 2, 0 4" fill="#3498db"/>
</marker>

<!-- 红色箭头（错误分支） -->
<marker id="arrowhead-red" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
  <polygon points="0 0, 6 2, 0 4" fill="#e74c3c"/>
</marker>

<!-- 连接线 -->
<line x1="240" y1="130" x2="340" y2="130" 
      stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>
```

#### 3. 复杂流程图元素

```svg
<!-- 菱形判断节点 -->
<polygon points="200,100 240,140 200,180 160,140" 
         fill="#fff" stroke="#e67e22" stroke-width="2" filter="url(#shadow)"/>
<text x="200" y="145" text-anchor="middle" font-size="12" fill="#333">判断条件</text>

<!-- 折线连接（路径转向） -->
<path d="M 250 150 L 250 180 L 180 180 L 180 210" 
      fill="none" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>

<!-- 虚线连接（异步/错误分支） -->
<line x1="100" y1="130" x2="200" y2="130" 
      stroke="#e74c3c" stroke-width="2" stroke-dasharray="5,5"
      marker-end="url(#arrowhead-red)"/>

<!-- 虚线框（可选区域） -->
<rect x="50" y="200" width="200" height="120" rx="8" 
      fill="none" stroke="#999999" stroke-width="1" stroke-dasharray="5,5"/>
<text x="60" y="220" font-size="10" fill="#999">可选流程区域</text>

<!-- 汇聚点 -->
<circle cx="300" cy="400" r="6" fill="#666"/>
<text x="320" y="405" font-size="10" fill="#666">汇聚点</text>

<!-- 曲线连接（循环/回退） -->
<path d="M 250 200 C 250 250, 150 250, 150 300" 
      fill="none" stroke="#9b59b6" stroke-width="2" 
      stroke-dasharray="5,5" marker-end="url(#arrowhead-blue)"/>
```

#### 4. 背景装饰

```svg
<!-- 柔和背景 -->
<rect width="800" height="600" fill="#f8f9fa"/>
<!-- 光点装饰 -->
<circle cx="100" cy="100" r="20" fill="#3498db" opacity="0.1"/>
```

## 执行步骤

### 第 1 步：解析用户需求

用户可能提供：
- **图形类型**：流程图、卡片、图表、图标、关系图
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

### 第 3 步：生成 SVG 代码

根据需求生成完整的 SVG 文件：

```svg
<svg xmlns="http://www.w3.org/2000/svg" 
     width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <!-- 阴影滤镜 -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-opacity="0.1"/>
    </filter>
    <!-- 箭头标记 - 统一使用灰色箭头 -->
    <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
    </marker>
  </defs>
  
  <!-- 背景 -->
  <rect width="800" height="600" fill="#f8f9fa"/>
  
  <!-- 标题 -->
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333333">标题</text>
  
  <!-- 你的图形内容 -->
  ...
</svg>
```

#### 深色背景模板（参考 examples/rd-lifecycle-flow.svg）

```svg
<svg xmlns="http://www.w3.org/2000/svg" 
     width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <!-- 深色模式箭头 -->
    <marker id="arrowhead" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto">
      <polygon points="0 0, 5 2.5, 0 5" fill="#666"/>
    </marker>
  </defs>
  
  <!-- 深色背景 -->
  <rect width="800" height="600" fill="#1a1a2e"/>
  
  <!-- 标题 -->
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#ffffff">标题</text>
  
  <!-- 卡片示例 -->
  <rect x="100" y="80" width="140" height="60" rx="5" fill="#16213e" stroke="#3498db" stroke-width="2"/>
  <text x="170" y="115" text-anchor="middle" font-size="12" fill="#aaaaaa">节点内容</text>
  
  <!-- 你的图形内容 -->
  ...
</svg>
```

**深色背景配色速查表（基于实际示例）**：
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

将生成的 SVG 保存到用户指定的位置，文件名以 `.svg` 结尾。

## 示例

### 示例 1：横向三步流程图

用户输入：「生成一个三步流程图，从左到右分别是：需求分析 → 设计开发 → 测试上线」

生成：

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-opacity="0.1"/>
    </filter>
    <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
    </marker>
  </defs>
  
  <rect width="800" height="400" fill="#f8f9fa"/>
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333333">三步流程图</text>
  
  <!-- 步骤1：需求分析 -->
  <g transform="translate(100, 150)">
    <rect width="160" height="80" rx="8" fill="#fff" stroke="#3498db" stroke-width="2" filter="url(#shadow)"/>
    <text x="80" y="45" text-anchor="middle" font-size="14" fill="#666">🔍</text>
    <text x="80" y="65" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">需求分析</text>
  </g>
  
  <!-- 箭头1 - 使用统一灰色箭头 -->
  <line x1="270" y1="190" x2="350" y2="190" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- 步骤2：设计开发 -->
  <g transform="translate(360, 150)">
    <rect width="160" height="80" rx="8" fill="#fff" stroke="#2ecc71" stroke-width="2" filter="url(#shadow)"/>
    <text x="80" y="45" text-anchor="middle" font-size="14" fill="#666">🎨</text>
    <text x="80" y="65" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">设计开发</text>
  </g>
  
  <!-- 箭头2 - 使用统一灰色箭头 -->
  <line x1="530" y1="190" x2="610" y2="190" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- 步骤3：测试上线 -->
  <g transform="translate(620, 150)">
    <rect width="160" height="80" rx="8" fill="#fff" stroke="#e67e22" stroke-width="2" filter="url(#shadow)"/>
    <text x="80" y="45" text-anchor="middle" font-size="14" fill="#666">🚀</text>
    <text x="80" y="65" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">测试上线</text>
  </g>
</svg>
```

### 示例 2：纵向流程图

用户输入：「生成一个用户登录流程图」

参考 examples/red-packet-flow.svg 生成：

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-opacity="0.1"/>
    </filter>
    <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
    </marker>
  </defs>
  
  <rect width="800" height="600" fill="#f8f9fa"/>
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333333">用户登录流程图</text>
  
  <!-- 步骤1 -->
  <g transform="translate(330, 60)">
    <rect width="140" height="50" rx="8" fill="#fff" stroke="#3498db" stroke-width="2" filter="url(#shadow)"/>
    <text x="70" y="32" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">打开登录页面</text>
  </g>
  
  <!-- 箭头 -->
  <line x1="400" y1="110" x2="400" y2="135" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- 更多步骤... -->
</svg>
```

### 示例 3：架构图

用户输入：「生成一个系统架构图」

**注意**：分层架构图中箭头是可选的。当分层展示系统组件时，可以不加箭头表示流向，特别是当重点展示层次结构而非流程顺序时。如需表示数据流向，可添加箭头。

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-opacity="0.1"/>
    </filter>
    <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
    </marker>
  </defs>
  
  <rect width="1000" height="800" fill="#f8f9fa"/>
  <text x="500" y="30" text-anchor="middle" font-size="22" font-weight="bold" fill="#333333">系统架构图</text>
  
  <!-- 接入层 -->
  <g>
    <text x="100" y="70" font-size="14" font-weight="bold" fill="#3498db">① 接入层</text>
    <rect x="100" y="80" width="900" height="70" rx="8" fill="#fff" stroke="#e0e0e0" stroke-width="1"/>
    <!-- 组件... -->
  </g>
  
  <!-- 箭头到服务层（可选：分层架构图中箭头可根据需要添加） -->
  <!-- <line x1="500" y1="150" x2="500" y2="175" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/> -->
  
  <!-- 服务层 -->
  <g>
    <text x="100" y="195" font-size="14" font-weight="bold" fill="#2ecc71">② 服务层</text>
    <rect x="100" y="205" width="800" height="120" rx="8" fill="#fff" stroke="#e0e0e0" stroke-width="1"/>
    <!-- 组件... -->
  </g>
  
  <!-- 更多层级... -->
</svg>
```

### 示例 4：复杂流程图（包含分支、折线、虚线等）

用户输入：「生成一个包含分支判断的复杂流程图」

参考 examples/complex-flow.svg 生成，该示例展示：
- 菱形判断节点：条件分支
- 折线连接：路径转向
- 虚线连接：错误分支/异步流程
- 虚线框：可选区域
- 汇聚点：多分支汇合
- 图例说明：元素含义解释（置于图形底部，避免与主流程重叠）

**核心设计原则**：
1. 先计算内容所需空间，再确定画布尺寸
2. 使用不同颜色区分主线/错误分支
3. 复杂路径使用 `<path>` 元素实现折线
4. 确保所有元素在画布范围内，边距充足

完整代码见 examples/complex-flow.svg

## 示例文件

以下是可供参考的示例文件：

### 流程图
- `examples/flow-test.svg` - 测试流程图
- `examples/flow-user-sign-in.svg` - 用户登录流程图
- `examples/flow-red-packet-flow.svg` - 红包业务流程图
- `examples/flow-rd-lifecycle-flow.svg` - 研发流程生命周期图（深色模式）

### 时间线
- `examples/timeline-rd-timeline.svg` - 研发时间线（深色模式）

### 架构图
- `examples/architecture-red-packet-architecture.svg` - 红包系统架构图
- `examples/architecture-train-ticket-architecture.svg` - 火车票系统架构图

### 对比图
- `examples/compare-opencode-vs-openclaw.svg` - OpenCode vs OpenClaw 对比图

### 文章摘要图
- `examples/article-summary-openclaw-dark.svg` - 文章摘要图（深色）
- `examples/article-summary-wechat-openclaw-light.svg` - 微信文章摘要图（浅色）

## 触发条件

当用户提到以下内容时触发：
- SVG、图片、图形、图标
- 流程图、关系图、结构图
- 生成一个图、把文字变成图
- 静态配图（非动画）


### 兼容性检查清单

生成后请验证：
- [ ] 所有元素在 viewBox 范围内（含阴影）
- [ ] 箭头指向准确，无偏移
- [ ] 文字清晰可读，无重叠
- [ ] 使用标准 SVG 元素，无自定义标签
- [ ] 导入后可自由移动、编辑、删除元素

## 输出说明

生成的 SVG 代码可以直接：
1. 在浏览器中打开查看
2. 保存为 `.svg` 文件
3. 嵌入到 HTML 中使用
4. 导入到 Figma、Sketch 等设计工具
