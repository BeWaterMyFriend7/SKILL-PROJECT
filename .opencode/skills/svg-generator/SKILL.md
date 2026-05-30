---
name: svg-generator
description: 根据自然语言描述生成 SVG 代码。支持流程图、架构图（应用架构、部署架构、系统架构、业务架构）、对比图、时间线图、状态流转图、时序图、ER图、文章总结图、卡片、图表等常用图形，输出可直接在浏览器中查看的 SVG 文件。当用户提到 SVG、生成图片、图形、图标、流程图、架构图、时序图、ER图、文章总结等时触发。
---

# SVG 代码生成器

## 核心工作流

```
用户描述 → 解析需求 → 设计图形 → 生成 SVG → 验证 → 保存文件
```

## 执行步骤

### 第 1 步：解析需求

用户可能提供：图形类型、布局、内容、风格、背景模式

**关键**：必须确认背景模式，未明确时默认浅色

### 第 2 步：生成图形

参考示例：`examples/*.svg`

### 第 3 步：验证清单

- [ ] 背景模式正确
- [ ] 节点无重叠，间距合理
- [ ] 连接线端点精确指向节点边缘（距边界≥5px）
- [ ] 画布利用率 60%-80%
- [ ] 箭头样式统一
- [ ] 箭头不交叉、不混乱，清晰可读
- [ ] 错误分支用红色实线，异步流程用虚线

---

# 第一部分：统一风格规范

## 1.1 配色规范

### 浅色模式（默认）
| 用途 | 颜色 | 说明 |
|------|------|------|
| 背景 | #f8f9fa | 主背景色 |
| 卡片 | #ffffff | 节点/容器填充 |
| 边框 | #e0e0e0 | 默认边框 |
| 标题文字 | #333333 | 主标题 |
| 正文文字 | #666666 | 内容文字 |
| 辅助文字 | #999999 | 次要信息 |
| 箭头 | #999999 | 默认连接线 |
| 阴影 | rgba(0,0,0,0.1) | 0 3px 6px |

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
| 阴影 | rgba(0,0,0,0.1) | 极淡阴影，仅必要时使用 |

### 状态色（统一）
| 用途 | 颜色 | 浅色背景 | 深色背景 |
|------|------|----------|----------|
| 步骤1/主色(蓝) | #3498db | #e3f2fd | #16213e |
| 步骤2/成功(绿) | #2ecc71 | #e8f5e9 | #16213e |
| 步骤3/警告(橙) | #e67e22 | #fff3e0 | #16213e |
| 错误(红) | #e74c3c | #fce4ec | #16213e |
| 紫色 | #9b59b6 | #f3e8ff | #16213e |

### 渐变方案（架构图专用）
```xml
<!-- 蓝色渐变 - 前端/客户端层 -->
<linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#2979ff"/>
  <stop offset="100%" stop-color="#2962ff"/>
</linearGradient>

<!-- 绿色渐变 - 后端/服务层 -->
<linearGradient id="greenGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#00c853"/>
  <stop offset="100%" stop-color="#00b248"/>
</linearGradient>

<!-- 橙色/黄色渐变 - 外部系统/第三方 -->
<linearGradient id="yellowGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#ffab00"/>
  <stop offset="100%" stop-color="#ff9100"/>
</linearGradient>
```

## 1.2 形状绘制规范

### 基础形状
```xml
<!-- 圆角卡片（推荐 rx=6-8） -->
<rect x="100" y="100" width="140" height="60" rx="8" 
      fill="#ffffff" stroke="#3498db" stroke-width="2"/>

<!-- 标题栏一体式卡片 -->
<g>
  <rect x="100" y="100" width="160" height="100" rx="8" fill="#ffffff" stroke="#3498db" stroke-width="2"/>
  <rect x="100" y="100" width="160" height="28" rx="8" fill="#3498db"/>
  <text x="180" y="119" text-anchor="middle" fill="#ffffff" font-weight="bold">标题</text>
</g>

<!-- 菱形判断节点（推荐 60x40） -->
<polygon points="200,100 230,130 200,160 170,130" 
         fill="#ffffff" stroke="#e67e22" stroke-width="2"/>

<!-- 圆形状态节点 -->
<circle cx="100" cy="100" r="8" fill="#3498db"/>
<!-- 结束状态：空心圆包围实心圆 -->
<circle cx="100" cy="100" r="10" fill="none" stroke="#2ecc71" stroke-width="2"/>
<circle cx="100" cy="100" r="5" fill="#2ecc71"/>
```

## 1.3 箭头规范

### 箭头标记定义
```xml
<!-- 浅色模式 - 标准箭头 -->
<marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
  <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
</marker>

<!-- 深色模式 - 标准箭头 -->
<marker id="arrowhead-dark" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto">
  <polygon points="0 0, 5 2.5, 0 5" fill="#666666"/>
</marker>

<!-- 彩色箭头（用于特殊场景） -->
<marker id="arrowBlue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#3498db"/>
</marker>
```

### 箭头使用规则
| 场景 | 箭头颜色 | 样式 |
|------|----------|------|
| 普通连接 | #999999(浅)/#666(深) | 实线 |
| 激活/进行中 | #3498db | 实线 |
| 返回消息 | #999999 | 实线 |
| 错误分支 | #e74c3c | 实线（非虚线） |
| 异步流程 | #9b59b6 | 虚线 |

**关键原则**：
- 箭头必须从源节点的边缘正确发出
- 箭头端点距目标节点边界 ≥5px
- 避免箭头交叉，必要时使用折线
- 同一图中箭头大小统一

---

# 第二部分：图形类型规范

## 2.1 架构图规范

### 分层结构
1. 接入层（客户端、CDN、网关）
2. 服务层（业务服务、认证、消息队列）
3. 数据层（Redis、MySQL、MongoDB）
4. 基础层（Docker、K8s、监控）

### 布局要点
- **元素对齐与均匀分布**：每层内的元素使用相同宽度，元素与容器左右边距对称
- **元素不能超出容器**：确保元素在分层背景框内部
- **层标签设计**：使用与该层主要功能匹配的颜色，位置在分层背景框上方

### 架构图类型
- **应用架构图**：展示应用系统的组件及其交互关系
- **部署架构图**：展示系统在物理或虚拟环境中的部署方式
- **系统架构图**：展示整个系统的高级结构和主要组件
- **业务架构图**：展示业务流程、组织结构和能力模型

## 2.2 对比图规范

### 布局原则
- 左右对称布局，中间留出对比空间
- 每侧使用相同的模块设计
- 颜色区分：左侧蓝色系，右侧绿色或橙色系
- 中间添加"VS"或明确的对比标识

## 2.3 时间线图规范

### 布局原则
- 横向时间线：从左到右表示时间流逝
- 纵向时间线：从上到下表示时间流逝
- 节点使用圆形或卡片表示时间点
- 连接线使用实线连接时间点
- 每个时间点包含时间标签和事件描述

## 2.4 状态流转图规范（重要）

### 节点类型
- **初始状态**：实心圆（填充状态色）
- **结束状态**：空心圆包围实心圆（绿色）
- **状态**：圆角矩形（rx=6），带边框
- **判断**：菱形（填充白色或卡片色）

### 连接线规范（重���）
- **水平/垂直直线优先**：避免斜线
- **分支使用折线**：先直线走到分支点，再转向
- **箭头指向清晰**：从不清晰区域指向清晰区域
- **条件标注**：在箭头旁标注"是"/"否"，不要跨在其他元素上

### 布局检查点
- 所有状态节点在网格上对齐
- 连接线不穿过其他节点
- 分支有足够的垂直间距（≥50px）
- 条件标注位置不与线交叉

### 正确示例
```svg
<!-- 垂直对齐的状态 -->
<rect x="150" y="80" width="140" height="50" rx="6" fill="#ffffff" stroke="#3498db"/>
<rect x="400" y="80" width="140" height="50" rx="6" fill="#ffffff" stroke="#3498db"/>

<!-- 分支连接：先水平，再垂直，避免斜线 -->
<line x1="290" y1="105" x2="400" y2="105" stroke="#999999" stroke-width="2"/>
<!-- 判断后分支：向下走一步再转向 -->
<line x1="470" y1="130" x2="470" y2="150" stroke="#999999" stroke-width="2"/>
<line x1="470" y1="150" x2="520" y2="150" stroke="#999999" stroke-width="2"/>
```

## 2.5 时序图规范（重要）

### 布局原则
- **生命线等距分布**：每条生命线间距 200-250px
- **消息从上到下按时间顺序排列**
- **激活条（Rectangle）**：表示对象活跃期间，顶部对齐消息起点
- **返回消息在调用下方**：保持时间顺序

### 连接线规范（关键）
- **消息线必须水平**：不使用折线
- **消息从上到下按时间顺序排列**
- **返回消息在发起消息的下方**
- **箭头指向右表示调用，指向左表示返回**
- **避免消息线交叉**

### 正确示例
```svg
<!-- 生命线等距 -->
<line x1="150" y1="80" x2="150" y2="400" stroke="#999999" stroke-width="1" stroke-dasharray="5,5"/>
<line x1="400" y1="80" x2="400" y2="400" stroke="#999999" stroke-width="1" stroke-dasharray="5,5"/>
<line x1="650" y1="80" x2="650" y2="400" stroke="#999999" stroke-width="1" stroke-dasharray="5,5"/>

<!-- 激活条：顶部对齐消息起点 -->
<rect x="135" y="120" width="30" height="80" fill="#e3f2fd" stroke="#3498db"/>

<!-- 消息：水平直线，从左到右按时间顺序排列 -->
<line x1="170" y1="140" x2="380" y2="140" stroke="#3498db" stroke-width="2" marker-end="url(#arrowBlue)"/>
<text x="275" y="125" text-anchor="middle" fill="#333" font-size="11">方法调用()</text>

<!-- 返回消息：在调用下方，水平直线返回 -->
<line x1="380" y1="200" x2="170" y2="200" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="275" y="185" text-anchor="middle" fill="#666" font-size="11">返回结果</text>
```

## 2.6 ER图规范

### 图形元素
- **实体**：圆角矩形（带顶部标题栏）
- **属性**：连接实体的小圆角矩形
- **关系**：菱形
- **连接线**：实线

### 约束表示
- 主键：加粗或PK标识
- 外键：斜体或FK标识
- 基数：在连接线端标注（1, N）

## 2.7 文章总结图规范

### 布局原则
- **卡片流程式布局**：从左到右或从上到下排列
- **每张卡片包含**：步骤编号、标题、详细描述
- **箭头连接**：表示步骤顺序
- **底部注意事项框**：整图底部，使用虚线边框

### 结构模板
```svg
<!-- 背景 -->
<rect width="800" height="500" fill="#f8f9fa"/>

<!-- 标题 -->
<text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333333">文章标题</text>
<text x="400" y="55" text-anchor="middle" font-size="11" fill="#666666">副标题</text>

<!-- 步骤卡片组 -->
<g transform="translate(80, 90)">
  <!-- 步骤1 -->
  <rect width="160" height="100" rx="8" fill="#ffffff" stroke="#3498db" stroke-width="2"/>
  <rect x="0" y="0" width="160" height="28" rx="8" fill="#3498db"/>
  <text x="80" y="19" text-anchor="middle" fill="#ffffff">Step 1</text>
  <text x="80" y="55" text-anchor="middle" font-weight="bold">标题</text>
  <text x="80" y="75" text-anchor="middle">描述</text>
</g>

<!-- 箭头连接 -->
<line x1="250" y1="140" x2="290" y2="140" stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>

<!-- 更多步骤... -->

<!-- 注意事项框 -->
<g transform="translate(80, 360)">
  <rect width="640" height="110" rx="8" fill="#ffffff" stroke="#e0e0e0"/>
  <text x="30" y="25" font-weight="bold">⚠️ 注意事项</text>
  <text x="30" y="50">• 注意事项1</text>
  <text x="30" y="70">• 注意事项2</text>
</g>

<!-- 底部信息 -->
<text x="400" y="495" text-anchor="middle" fill="#999999">来源/作者</text>
```

### 深色模式文章总结图
```svg
<rect width="800" height="500" fill="#1a1a2e"/>

<!-- 步骤卡片 - 使用 #16213e 作为卡片色 -->
<g transform="translate(80, 90)">
  <rect width="160" height="100" rx="5" fill="#16213e" stroke="#3498db" stroke-width="2"/>
  <rect x="0" y="0" width="160" height="28" rx="5" fill="#3498db"/>
  <text x="80" y="19" text-anchor="middle" fill="#ffffff">Step 1</text>
  <text x="80" y="55" text-anchor="middle" fill="#ffffff">标题</text>
  <text x="80" y="75" text-anchor="middle" fill="#aaaaaa">描述</text>
</g>
```

---

# 第三部分：代码模板

## 基础结构（浅色模式）
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <filter id="shadow">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-opacity="0.1"/>
    </filter>
    <marker id="arrowhead" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#999999"/>
    </marker>
  </defs>
  <rect width="800" height="600" fill="#f8f9fa"/>
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333333">标题</text>
  <!-- 图形内容 -->
</svg>
```

## 基础结构（深色模式）
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <filter id="shadow-dark" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.1"/>
    </filter>
    <marker id="arrowhead-dark" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto">
      <polygon points="0 0, 5 2.5, 0 5" fill="#666666"/>
    </marker>
  </defs>
  <rect width="800" height="600" fill="#1a1a2e"/>
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#ffffff">标题</text>
  <!-- 图形内容 -->
</svg>
```

---

# 第四部分：布局规范

## 节点尺寸
- 菱形：60px宽，40px高
- 矩形：140-160px宽，50-60px高（状态），100px高（步骤卡）
- 圆形：16-20px直径（状态点），12px（时间点）

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

---

# 触发条件

当用户提到：
- SVG、图片、图形、图标、流程图
- 架构图、对比图、时间线图、状态流转图、时序图、ER图
- 文章总结、教程图、步骤图
- 生成一个图、把文字变成图
- 需要浏览器可查看的图形