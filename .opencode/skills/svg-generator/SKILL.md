---
name: svg-generator
description: 生成浏览器可直接展示的高质量静态 SVG 矢量图，适用于用户明确要求 SVG、矢量图、网页嵌入图，或未指定媒介但要求高级、专业、精确排版的展示型架构图。支持业务/应用/技术/部署/系统架构、流程、时序、状态、ER、对比、时间线和总结图。不用于 Draw.io 可编辑 XML 或 Mermaid/Markdown 图表。
---

# SVG 图形生成器

本 skill 是完全自包含的 SVG 渲染模块。所有规范、模板、示例、脚本和 eval 都位于本文件夹内，禁止读取其他 skill 的文件。

## 接口

输入：用户的图形主题、内容、可选主题模式和布局偏好。
输出：浏览器可直接打开的 UTF-8 SVG 文件，默认保存到 `output/svg/`。

先读取 `assets/routing.md` 确认媒介边界。明确要求 Draw.io 或 Mermaid 时停止使用本 skill。

## 强制流程

禁止从自然语言直接拼接 SVG：

```text
用户输入
-> 本地路由判断
-> DiagramPlan
-> 模板/构图原型
-> 布局计划
-> SVG
-> 源文件校验
-> 渲染检查
-> 交付
```

### 1. 整理 DiagramPlan

按 `assets/diagram-plan.schema.json` 整理图类型、主题、密度、标题、画布、区域、节点、边、图例和假设。

架构图必须记录：

- 用户明确给出的内容；
- 根据常见架构模式补充的合理假设；
- 需要用户确认的真实业务边界。

### 2. 选择模板

- 架构图优先读取 `templates/architecture/` 中对应类型。
- 没有模板时使用最接近的 `examples/*.svg` 作为视觉参考。
- 模板只提供骨架，不得原样替换标题后交付。

### 3. 应用本地规范

按需读取：

- `assets/visual-tokens.md`：唯一的颜色、文字、间距、圆角和阴影来源；
- `assets/architecture-system.md`：五类架构图构图原型；
- `assets/style-guide.md`：SVG 元素、连线、文本换行和媒介特有规则；
- `assets/quality-contract.md`：交付阈值。

### 4. 生成 SVG

- `width`、`height`、`viewBox` 必须一致。
- 使用唯一 id；所有 marker/filter/clipPath 引用必须存在。
- 文本使用稳定字体 fallback，不嵌入外部字体。
- 架构图使用中性底色、一个主色和不超过三个语义色。
- 错误路径为红色实线；虚线只表示异步、回调和事件。
- 禁止连接线穿过节点，禁止自由散点布局和随机渐变。

### 5. 校验与渲染

交付前必须运行：

```bash
python -X utf8 scripts/validate_references.py
python -X utf8 scripts/validate_plan.py <diagram-plan.json>
python -X utf8 scripts/validate_svg.py output/svg/文件名.svg --fail-on-warning --require-render
```

还必须检查渲染结果：

- 100% 尺寸下文字清晰，无裁切、重叠和溢出；
- 25% 缩略图下标题、区域层次和主链路仍可辨认；
- 画布利用率目标 60%-80%，硬范围 50%-85%；
- 正文不小于 12px，辅助文字不小于 11px。

校验失败必须修正，不得通过删减必要内容或缩小字号规避。

## 架构图高级感基线

- 先压实语义，再决定画布和容器。
- 同级卡片尺寸、圆角、边框和标题基线一致。
- 不使用整图彩虹分层、大面积高饱和色块和重阴影。
- 内容不足时补充合理维度或缩小画布；内容过多时分区或拆图。
- 静态架构关系可不画箭头；动态调用和数据流必须有方向和短标签。

## 输出说明

交付时说明：

1. SVG 文件路径；
2. 使用的模板或构图原型；
3. 主题模式；
4. 校验结果。
