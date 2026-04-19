---
name: prototype-design-xml
description: 原型设计 Skill。根据需求文档生成 drawio XML 格式的可编辑原型图，支持在 drawio 中二次编辑。当用户提到原型设计、XML原型、drawio原型时触发。生成可直接在 drawio 中打开编辑的 .drawio 文件。
---

# 原型设计（XML格式）

## 执行步骤

### 第 1 步：读取需求

- 读取 `output/doc/requirements-analysis-review.md`
- 或读取用户提供的需求文档
- 无文档时：先进行需求分析

### 第 2 步：原型设计

在 `output/design-output/` 下输出：
- drawio XML 格式的原型文件（.drawio）
- 配套资源文件
- 项目 README 手册

### 第 3 步：验证测试

确保 XML 格式正确，可在 drawio 中正常打开

## 设计规范

- 简约大气，避免过于花哨
- 参考 `reference/design-rule.md`
- 参考 `xml-diagram` skill 的配色和布局规范

## 配色规范

### 浅色模式（默认）
| 用途 | 颜色 |
|------|------|
| 背景 | #f8f9fa |
| 卡片 | #ffffff |
| 边框 | #e0e0e0 |
| 文字 | #333333/#666666 |

### 深色模式
| 用途 | 颜色 |
|------|------|
| 背景 | #1a1a2e |
| 卡片 | #16213e |
| 边框 | #333333 |
| 文字 | #ffffff/#aaaaaa |

### 状态色
| 用途 | 颜色 |
|------|------|
| 主色(蓝) | #3498db |
| 成功(绿) | #2ecc71 |
| 警告(橙) | #e67e22 |
| 错误(红) | #e74c3c |

## 布局规范

### 页面尺寸
- Web端：16:9 比例
- 宽度：800-1200px
- 高度：根据内容自适应

### 节点尺寸
- 卡片：高度60-80px，宽度根据内容
- 按钮：高度35-40px，宽度80-120px
- 输入框：高度35-40px，宽度自定义

### 间距规则
- 组件间距：20-30px
- 卡片内边距：15-20px
- 页面边距：30-40px

## 代码模板

### 基础画布
```xml
<mxfile host="app.diagrams.net">
  <diagram name="原型">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" pageWidth="1000" pageHeight="600">
      <root>
        <mxCell id="0"/><mxCell id="1" parent="0"/>
        <!-- 页面元素 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 页面标题
```xml
<mxCell value="页面标题" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;routed=0;fontSize=20;fontStyle=1;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="400" y="20" width="200" height="40" as="geometry"/>
</mxCell>
```

### 卡片容器
```xml
<mxCell id="card1" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e0e0e0;strokeWidth=1;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="80" width="300" height="200" as="geometry"/>
</mxCell>
```

### 卡片标题
```xml
<mxCell value="卡片标题" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;routed=0;fontSize=14;fontStyle=1;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="115" y="95" width="270" height="30" as="geometry"/>
</mxCell>
```

### 按钮
```xml
<mxCell id="btn1" value="按钮文字" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3498db;strokeColor=#2980b9;strokeWidth=1;fontColor=#ffffff;fontSize=14;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="200" y="250" width="100" height="36" as="geometry"/>
</mxCell>
```

### 输入框
```xml
<mxCell id="input1" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e0e0e0;strokeWidth=1;fontColor=#333333;fontSize=14;" vertex="1" parent="1">
  <mxGeometry x="115" y="140" width="270" height="35" as="geometry"/>
</mxCell>
```

### 输入框标签
```xml
<mxCell value="标签" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;routed=0;fontSize=12;fontColor=#666666;" vertex="1" parent="1">
  <mxGeometry x="115" y="118" width="60" height="20" as="geometry"/>
</mxCell>
```

### 列表项
```xml
<mxCell id="item1" value="列表项内容" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#f0f0f0;strokeWidth=1;fontColor=#333333;fontSize=13;align=left;spacingLeft=10;" vertex="1" parent="1">
  <mxGeometry x="115" y="180" width="270" height="40" as="geometry"/>
</mxCell>
```

### 分隔线
```xml
<mxCell value="" style="line;html=1;strokeColor=#e0e0e0;strokeWidth=1;fill=1;dashed=0;" vertex="1" parent="1">
  <mxGeometry x="115" y="220" width="270" height="1" as="geometry"/>
</mxCell>
```

## 输出

- 可编辑的 .drawio 文件
- 可在 drawio 中打开二次编辑
- 可导出为 PNG/SVG/PDF

## 触发条件

当用户提到：
- 原型设计、界面原型
- XML原型、drawio原型
- 生成原型图
- 需要可编辑的原型文件