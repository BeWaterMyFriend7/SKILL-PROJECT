---
name: xml-diagram
description: 根据用户自然语言输入生成可在 drawio 或 diagrams.net 中编辑的 XML 架构图、简约步骤流程图、对比图、时间线图、生命周期图、文章总结图和分析图。适用于用户要求生成 drawio、XML 图形、可编辑图形、架构图、业务架构、应用架构、技术架构、部署架构、简约流程图、步骤图、少分支流程、时序图、实体关系图、状态图、对比图、项目时间线、项目生命周期、文章总结、卡片总结等场景。输出必须是稳定、美观、可编辑的 .drawio 文件。
---

# XML 图形生成器

本技能的目标是根据用户输入生成可编辑的 `.drawio` 文件。输出重点是：结构清晰、布局稳定、风格统一、文字清晰、元素不重叠、画布不空旷、图例完整。

## 核心原则

禁止直接从自然语言一步生成 XML。必须先规划，再生成：

```text
用户输入 -> 意图识别 -> 模板选择 -> 内容充实 -> 中间结构 -> 布局计划 -> 样式计划 -> 连线计划 -> 校验修正 -> XML
```

## 模板优先

生成任何图形前，先选择最接近的 `templates/*.drawio` 作为视觉骨架。

- 模板决定：画布比例、标题位置、容器层级、卡片样式、图例位置、箭头风格和默认间距。
- 模型决定：图形逻辑、分层名称、节点内容、关系说明和可选区域。
- 布局规约决定：坐标、尺寸、换行和安全间距。
- 校验规约决定：是否需要修复重叠、遮挡、空白过大、颜色不清和连线混乱。
- 没有完全匹配的模板时，使用最接近的 `examples/*.drawio` 作为参考，但仍必须遵守同一套规约。

## 资源加载

按任务需要读取以下资源，不要一次加载无关文件：

- `assets/design-system.md`：全局视觉设计、颜色角色和禁止项。
- `assets/theme-tokens.md`：浅色/深色主题、语义色和对比度规则。
- `assets/typography-rules.md`：页面标题、区域标题、卡片标题、标签文字规则。
- `assets/component-rules.md`：页面、区域容器、分组卡片、小标签、说明和图例组件规则。
- `assets/layout-rules.md`：布局算法、间距、安全区、画布利用率和不同图类型结构。
- `assets/edge-rules.md`：正交连线、主流程、异步线、错误线和存储线规则。
- `assets/legend-rules.md`：图例触发条件、位置、类型和尺寸。
- `assets/validation-rules.md`：最终校验项、失败处理和修正顺序。
- `assets/dsl-schema.md`：生成 XML 前必须先整理的中间结构。

## 模板映射

| 用户意图 | 优先模板 |
| --- | --- |
| 业务架构、能力地图、业务领域 | `templates/architecture/business-layered.drawio` |
| 应用架构、前端后端、外部系统 | `templates/architecture/application-pipeline.drawio` |
| 技术架构、系统架构、分层技术视图 | `templates/architecture/technical-layered.drawio` |
| 部署架构、网络拓扑、集群和云区域 | `templates/architecture/deployment-region.drawio` |
| 简约流程、步骤图、少分支流程 | `templates/flow/simple-step-flow.drawio` |
| 时序图、登录链路、消息调用链路 | `templates/sequence/sequence-login.drawio` |
| 项目路线图、研发时间线 | `templates/project/roadmap-timeline.drawio` |
| 项目生命周期、阶段流转、交付流程 | `templates/project/lifecycle-flow.drawio` |
| 里程碑看板 | `templates/project/milestone-board.drawio` |
| 对比分析、左右对比 | `templates/analysis/comparison-vs.drawio` |
| 决策矩阵 | `templates/analysis/decision-matrix.drawio` |
| 优势劣势机会威胁分析 | `templates/analysis/swot.drawio` |
| 文章总结 | `templates/summary/article-summary.drawio` |
| 知识结构图 | `templates/summary/knowledge-map.drawio` |
| 卡片总结 | `templates/summary/card-summary.drawio` |

## 中间结构

生成 XML 前，必须先整理中间结构。最小结构如下：

```yaml
diagram:
  type: technical_architecture
  mode: light
  palette: standard
  title: "图形标题"
  subtitle: "可选副标题"
  sections: []
  nodes: []
  edges: []
  legends: []
```

## 内容充实

架构图必须先做内容充实，再进入坐标布局。不要用空容器、大卡片或大画布掩盖信息不足。

```text
1. 从用户输入提取确定内容。
2. 按图类型补齐候选维度。
3. 标注哪些内容是合理假设，哪些内容需要用户确认。
4. 先压实语义，再计算画布大小。
```

架构图常用补齐维度：

```text
业务架构：用户/角色、业务场景、核心能力、业务对象、运营治理、风险控制。
应用架构：入口端、网关、核心服务、数据存储、外部系统、运维观测。
技术架构：接入、协议、服务框架、中间件、数据层、基础设施、安全与监控。
部署架构：区域、网络边界、负载均衡、计算节点、数据组件、缓存/消息、监控告警。
```

若用户输入不足但主题明确，可以补充通用模块；若涉及真实业务边界、产品职责、合规要求或专有系统名称，先问用户确认。

## 执行步骤

1. 识别图类型、主题模式、输出文件名、区域划分、主流程、异步流程、存储关系和图例需求。
2. 按模板映射选择最接近的模板。
3. 读取模板和必要规约。架构图、项目图和分析图通常需要读取字体、组件、布局、连线、图例和校验规则。
4. 进入内容充实阶段：如果架构图只有少量模块或会造成大面积空白，先基于用户主题头脑风暴场景、能力、服务、数据、治理、监控等候选内容；通用且低风险的补充可以直接采用，涉及业务事实或取舍不明确时先向用户确认。
5. 按“页面 -> 区域容器 -> 分组卡片 -> 小标签 -> 说明”的层级整理中间结构。
6. 根据模板骨架计算布局，保证卡片不进入区域标题安全区、不超出区域边界。
7. 使用主题标记配色，除非用户明确提供品牌色，否则不要引入标记表外颜色。
8. 使用正交连线。错误路径必须是红色实线；虚线只用于异步、回调、消息事件。
9. 简约步骤流程图最多使用 8 个主步骤，优先使用编号卡片；主线只保留必要箭头，禁止复杂分支和多重回环。
10. 按图例规约判断是否必须生成图例。
11. 生成 XML 后执行校验，失败必须修正后再输出。
12. 保存 `.drawio` 到 `output/drawio/`，文件名使用清晰的中文或拼音描述。

## 强制视觉规则

- 画布利用率目标为 60%-80%。
- 低于 50% 视为留白过多，必须缩小画布或重新居中；高于 85% 视为内容过满，必须扩展画布或拆分区域。
- 页面边距至少 32px，任何内容距离画布边缘不得小于 30px。
- 区域标题必须有独立安全区，高度至少 44px，节点不得进入该区域。
- 任意两个元素最小间距 24px；分组卡片间距至少 28px；区域间距至少 36px。
- 卡片层级必须明确，禁止把区域容器、分组卡片和小标签做成同一视觉层级。
- 架构图的一级内容标题、分层标题和区域标题必须是纯文本，不要给标题单独添加矩形框线或填充底色。
- 架构图的三级内容必须绘制为可编辑的小矩形标签，不得只写成卡片内部的纯文字、换行文字或项目符号。
- 时序图必须包含横向参与者、竖向生命线和激活条；多消息链路不得只画参与者与横向消息线。
- 满足以下任一条件必须生成图例：使用 4 种以上语义色；存在实线、虚线、主流程、错误线区别；存在阶段色、角色色或系统边界色。
- 图例不得覆盖主内容，必须与节点保持至少 24px 距离。
- 深色模式禁止阴影；浅色模式只允许轻微阴影。
- XML 注释不得包含 `--`。

## XML 与编码硬性规则

- 所有 `.drawio`、`.md`、`.py` 文件必须按 UTF-8 读取和写入。
- 禁止用 PowerShell 的 `Get-Content`/`Set-Content` 修复中文 drawio 文件；这会在无 BOM 文件上触发 ANSI/GBK 误解码风险。
- 若必须脚本化处理文件，使用严格 UTF-8：Python 使用 `Path.read_text(encoding="utf-8")` 和 `write_text(encoding="utf-8", newline="\n")`；PowerShell 使用 `[System.IO.File]::ReadAllText(path, [System.Text.UTF8Encoding]::new($false, $true))`。
- 禁止把 UTF-8 字节按 GBK 解码后再写回；一旦出现常见中文 mojibake 片段或 Unicode 替换字符，视为中文编码损坏，必须重新生成或从可信源恢复文本。
- 每个 `mxGeometry` 都必须写成 `<mxGeometry ... as="geometry" />`；缺少 `as="geometry"` 会导致 draw.io 报 `Could not add object mxGeometry`。
- 连线、标签、泳道、背景、容器的几何信息也必须遵守同一规则，不要只检查普通矩形。
- 输出不得包含内嵌图片；本技能只从用户输入生成可编辑 drawio XML。

## 最终规约检查

交付前必须逐项检查：

```text
1. 文件能以严格 UTF-8 读取，不存在乱码、替换字符或 mojibake 片段。
2. XML 可解析，根节点为 mxfile 或 mxGraphModel。
3. 每个 mxCell 有唯一 id。
4. 每个 mxGeometry 都包含 as="geometry"。
5. 连线 source 和 target 引用存在。
6. 错误/失败路径是红色实线，虚线只用于异步、回调或消息事件。
7. 元素不重叠，卡片不进入区域标题安全区。
8. 画布利用率控制在 50%-85%，目标 60%-80%。
9. 浅色和深色模式文字对比度清晰，浅色语义色块不要用白字。
10. 图例不遮挡主内容，且解释实际出现的颜色或线型。
11. 架构图三级内容都是小矩形标签，一级/区域标题没有框线或填充。
12. 时序图包含参与者、生命线、激活条和按时间排列的消息线。
13. examples 文件命名遵守“一级类别[-二级类别]-背景风格-业务说明[-其他].drawio”。
14. 运行 validate_drawio.py 和 check_contrast.py 后再交付。
```

## 输出要求

输出时说明生成的 `.drawio` 路径和使用的模板。若脚本可用，交付前运行：

```bash
python -X utf8 scripts/validate_drawio.py output/drawio/文件名.drawio --fail-on-warning
python -X utf8 scripts/check_contrast.py output/drawio/文件名.drawio --fail-on-warning
```

## 示例和模板

`templates/` 用作可复用骨架，`examples/` 用作具体视觉参考。生成结果如果偏离模板风格，应修正布局和样式，不要新增临时例外规则。
