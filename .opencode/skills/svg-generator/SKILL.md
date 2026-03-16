---
name: svg-generator
description: 根据自然语言描述生成 SVG 代码。支持流程图、卡片、图表、图标等常用图形，输出可直接在浏览器中查看的 SVG 文件。当用户提到 SVG、生成图片、图形、图标、流程图时触发。
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
- [ ] 箭头样式统一（markerWidth=6, markerHeight=4）
- [ ] 错误分支用红色实线，异步流程用虚线

## 配色规范

### 浅色模式（默认）
| 用途 | 颜色 |
|------|------|
| 背景 | #f8f9fa |
| 卡片 | #ffffff |
| 边框 | #e0e0e0 |
| 文字 | #333333/#666666 |
| 箭头 | #999999 |
| 阴影 | 0 3px 6px rgba(0,0,0,0.1) |

### 深色模式
| 用途 | 颜色 |
|------|------|
| 背景 | #1a1a2e |
| 卡片 | #16213e |
| 边框 | #333333 |
| 文字 | #ffffff/#aaaaaa |
| 箭头 | #666666 |
| 阴影 | 0 3px 6px rgba(0,0,0,0.4) |

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

### 圆角卡片
```svg
<rect x="100" y="100" width="140" height="60" rx="8" 
      fill="#ffffff" stroke="#3498db" stroke-width="2" filter="url(#shadow)"/>
<text x="170" y="135" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">节点名称</text>
```

### 菱形判断节点
```svg
<polygon points="200,100 240,140 200,180 160,140" 
         fill="#fff" stroke="#e67e22" stroke-width="2" filter="url(#shadow)"/>
<text x="200" y="145" text-anchor="middle" font-size="12" fill="#333">判断条件</text>
```

### 箭头连接
```svg
<line x1="240" y1="130" x2="340" y2="130" 
      stroke="#999999" stroke-width="2" marker-end="url(#arrowhead)"/>
```

### 虚线（异步/可选）
```svg
<line x1="100" y1="130" x2="200" y2="130" 
      stroke="#9b59b6" stroke-width="2" stroke-dasharray="5,5"
      marker-end="url(#arrowhead)"/>
```

### 红色箭头（错误分支）
```svg
<line x1="100" y1="130" x2="200" y2="130" 
      stroke="#e74c3c" stroke-width="2" marker-end="url(#arrowhead)"/>
```

## 布局规范

### 节点尺寸
- 菱形：50-60px高，100-140px宽
- 矩形：35-40px高，100-140px宽
- 圆形：40-50px直径

### 间距
- 垂直：50-60px
- 水平：40-60px
- 分支点前：≥50px
- 图例区域：100-120px

### 画布计算
```
画布高度 = 标题40 + 内容总高 + 间距×(节点数-1) + 图例120 + 边距40
画布宽度 = 边距40 + 最大宽×列数 + 列间距×(列数-1) + 边距40
```

## 触发条件

当用户提到：
- SVG、图片、图形、图标
- 流程图、关系图、结构图
- 生成一个图、把文字变成图
- 需要浏览器可查看的图形
