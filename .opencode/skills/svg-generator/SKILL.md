---
name: svg-generator
description: 生成浏览器可直接展示、缩放和嵌入网页或文档的高质量静态 SVG 矢量图。用于用户明确要求 SVG、矢量图、网页配图或展示型架构图；支持业务、应用、系统、技术、部署、数据架构，以及流程、生命周期、状态、时序、ER、依赖、知识关系、对比、决策矩阵、SWOT、时间线、路线图和总结图。不用于 Draw.io 可编辑 XML、Mermaid 或照片插画。
---

# SVG 图形生成器

生成自包含 UTF-8 SVG。用户未指定目录时保存到项目根目录 `output/svg/`；需要拖拽编辑时改用 `xml-diagram`。

## 必读资源

- 分析需求和编写图形描述前读取 `references/svg-dsl.md`。
- 规划布局、颜色、连线和检查项时读取 `references/quality-rules.md`。
- 选择配色和图标时读取 `references/theme-tokens.md`、`references/icon-policy.md`。
- 读取与图形类型同名的 `templates/*.svg`，再参考同类型 `examples/*.svg`；禁止只替换标题后交付。

## 强制流程

```text
分析需求 → 详细自然语言 DSL → 匹配模板 → 计算布局 → 生成 SVG
        → 严格源文件校验 → 浏览器渲染检查 → 修正并交付
```

### 1. 分析需求

确定图形目的、受众、图形类型、显示模式、阅读方向、内容层级、核心关系和输出路径。主题识别、一次询问和默认回退按 `references/theme-tokens.md` 执行，并区分用户明确内容、合理补充和不可擅自推断的业务事实。

图形类型从以下目录选择：

- 架构：业务、应用/系统、技术、部署、数据；
- 流程与行为：线性流程、分支流程、生命周期、状态、时序；
- 关系：ER、依赖关系、知识关系；
- 信息表达：对比、决策矩阵、SWOT、时间线、路线图、总结图。

不生成系统上下文图；中心系统与外部角色关系优先改为应用架构或依赖关系图。

### 2. 生成详细自然语言 DSL

按 `references/svg-dsl.md` 写清画布、层级、分区、节点、布局、尺寸、连线、主题和检查要求。DSL 不强制落盘，不使用 JSON、JSON Schema 或 DiagramPlan 作为中间格式。

### 3. 匹配模板

- 业务架构读取 `templates/architecture-business.svg`。
- 应用或系统架构读取 `templates/architecture.svg`。
- 技术架构读取 `templates/architecture-technical.svg`。
- 部署架构读取 `templates/architecture-deployment.svg`。
- 数据架构读取 `templates/architecture-data.svg`。
- 其他类型读取同名模板。

用户内容与模板不同，可以增减层和卡片，但必须保留模板的层级、间距和设计语言，不机械保留空层。

### 4. 计算布局

先计算区域、标题、卡片、文字和必要连线所需空间，再确定画布。

- 架构图默认整体纵向分层、层内横向排列；一级标题可在容器顶部居中，二级标题与三级卡片分离。
- 三级卡片默认高 `28-34px`，同组等宽、等高、等距；内容过多时规则换行或扩展画布。
- 架构图默认不画箭头，通过层级、容器、分组和空间顺序表达关系。只有调用、流量或主数据流不可缺少时才保留少量正交连线。
- 同层内容铺满可用区域，不得集中在左侧；左右、上下留白与内容量匹配。
- 时序图必须包含完整参与者、生命线、横向消息、返回消息和起止语义。
- 流程图必须包含起点、终点和完整判断出口；关系图必须预留连线通道。

### 5. 生成 SVG

- `width`、`height` 与 `viewBox` 一致。
- 根节点使用 `role="img"` 和 `aria-labelledby`，包含 `<title>`、`<desc>`。
- 使用唯一 id；引用的 marker、filter、gradient、clipPath 必须存在。
- 使用字体 fallback，不嵌入外部字体、位图、CSS 或远程资源。
- 多行文字使用 `<tspan>`，不使用 `foreignObject`。
- 为主要节点、连线和辅助文字分别添加 `data-role="node"`、`data-role="edge"`、`data-text-role="auxiliary"`。
- 只使用统一默认视觉风格。浅色和深色只切换颜色变量，几何结构、文字和关系保持一致。
- 按 `background → regions → edges → nodes → labels → legend` 分层，保证文字和节点位于连线之上。

### 6. 严格校验和渲染

交付前运行：

```bash
python -X utf8 scripts/validate.py output/svg/文件名.svg --strict --render
```

修改 skill 内模板或示例时运行：

```bash
python -X utf8 scripts/validate.py . --strict
python -m unittest discover -s tests -v
```

校验后查看真实渲染结果，检查颜色搭配、布局均衡、元素重叠、文字清晰度、线条混乱和大面积空白。失败时调整布局或内容，不得通过缩小字体、删除必要节点或扩大空画布规避。

## 统一视觉风格

使用纯色画布、两级表面色、统一圆角、清晰边框、极轻阴影和小面积主色强调。禁止网格背景、多重渐变、重阴影、彩虹分层、霓虹描边、装饰噪声、图标风格混用和无语义箭头。深色主题依靠表面层级和边框亮度建立质感。

## 交付

交付最终 `.svg` 路径，并说明图形类型、浅色或深色主题及严格校验结果。不要交付临时 PNG、中间 DSL 或其他中间文件，除非用户明确要求。
