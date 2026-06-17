---
name: prototype-design-xml
description: 原型设计 Skill。根据需求文档生成 drawio XML 格式的可编辑原型图，支持在 drawio 中二次编辑。当用户提到原型设计、XML原型、drawio原型、界面原型、可编辑原型、生成原型图、drawio原型图、protype drawio时触发。生成可直接在 drawio 中打开编辑的 .drawio 文件。
---

# 原型设计（drawio XML 格式）

## 执行步骤

### 第 1 步：读取需求

- 默认读取 `output/doc/requirements-analysis-review.md`
- 或读取用户指定的需求文档
- 无文档时先进行需求分析

### 第 2 步：原型设计

在 `output/design-output/` 下输出：
- drawio XML 格式原型文件（.drawio）
- 配套资源文件
- 项目 README 手册

### 第 3 步：验证测试

确保 XML 格式正确，可在 drawio 中正常打开。

## 设计规范

- 参考 `reference/design-rule.md` 获取设计规约
- 配色和布局遵循 `xml-diagram` skill 的共享设计系统

### 配色规范

**浅色模式（默认）**
| 用途 | 颜色 |
|------|------|
| 背景 | #f8f9fa |
| 卡片 | #ffffff |
| 边框 | #e0e0e0 |
| 文字 | #333333/#666666 |

**深色模式**
| 用途 | 颜色 |
|------|------|
| 背景 | #1a1a2e |
| 卡片 | #16213e |
| 边框 | #333333 |
| 文字 | #ffffff/#aaaaaa |

**状态色**
| 主色(蓝) | 成功(绿) | 警告(橙) | 错误(红) |
|----------|----------|----------|----------|
| #3498db | #2ecc71 | #e67e22 | #e74c3c |

### 布局规范

- Web端 16:9，宽度 800-1200px
- 组件间距 20-30px，页面边距 30-40px
- 卡片高度 60-80px，按钮 35-40px，输入框 35-40px

### 常用 XML 代码模板

见 `xml-diagram` skill 的 `assets/style-guide.md` 获取完整组件模板。

**基础画布结构：**
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

## 输出

- 可编辑的 .drawio 文件
- 可在 drawio 中打开二次编辑并导出为 PNG/SVG/PDF
