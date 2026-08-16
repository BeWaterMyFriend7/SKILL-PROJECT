# 代码变更方案：XML 与 SVG 绘图 Skill 配色及布局优化（精简版）

**Plan ID:** diagram-skills-theme-layout-optimization-20260816-174654-r7
**创建时间:** 2026-08-16 17:46:54 +08:00
**修订时间:** 2026-08-16 23:26:45 +08:00
**状态:** IMPLEMENTED
**风险等级:** 中

---

## 1️⃣ 要做什么 (What)

### 目标

统一 `xml-diagram` 和 `svg-generator` 的主题、配色询问、图标及布局规则，同时保持现有纵向分层架构。

### 范围

**包含：**

- 提供科技蓝 `tech-blue`、活力多彩 `vibrant`、稳健聚焦 `focused` 三套多色主题，科技蓝为默认。
- 支持用户指定主题、品牌色或 `primary/secondary/tertiary/accent` 色槽。
- 完全没有颜色信号时询问一次；仍未指定或要求直接生成时使用 `tech-blue/light`。
- 保留纵向分层主骨架；AI 可按内容少量加入顶部信息带、辅助列、说明卡片、编号流程、焦点节点或底部总结带。
- 图标按需使用；普通图通常 0～4 个仅作为克制建议，不设硬上限，实际数量由内容复杂度、信息价值与可读性决定。
- 同步更新两个 Skill 的入口文档、DSL、主题与图标规则、模板、示例、校验器和测试。

**不包含：**

- 不根据业务节点名称自动选择主题或颜色。
- 不新增替代纵向分层的主布局。
- 不使用外部 URL、Emoji、图标字体、品牌 Logo、位图背景或重装饰效果。
- 不修改其他 Skill、项目 README 或用户已有生成文件。

### 验收标准

- [x] XML/SVG 使用相同的三套主题、色槽和派生规则。
- [x] 已指定主题或颜色时不询问；未指定时只询问一次，随后按规则回退科技蓝。
- [x] 用户颜色优先，缺失色槽可确定性补齐且满足对比度要求。
- [x] 颜色跟随结构角色，不跟随节点名称。
- [x] 默认纵向分层和主阅读方向不变；附加模块通常为 0～2 个。
- [x] 图标按内容适量使用，Draw.io 离线可见，SVG 无外部资源；不得机械地按固定数量裁剪。
- [x] 所有相关文档和示例使用新主题名，不保留旧草案键。
- [x] XML/SVG 严格校验和单测通过，SVG 代表图真实渲染通过。

### 待决策问题

无。

---

## 2️⃣ 怎么做 (How)

### 当前实现

- 入口：`.opencode/skills/xml-diagram/SKILL.md`、`.opencode/skills/svg-generator/SKILL.md`。
- 当前颜色规则分散在质量规则、模板和示例中，缺少统一的主题选择与用户配色流程。
- 架构图已有纵向分层骨架，本次只在该骨架内增加可选内容。

### 主题定义

参考图只用于提取配色，不复制其中的业务内容、图标或布局。

| 主题 | Primary | Secondary | Tertiary | Accent |
|---|---|---|---|---|
| 科技蓝 `tech-blue`（默认） | `#2E69E1` | `#1A388D` | `#819FDE` | `#1A388D` |
| 活力多彩 `vibrant` | `#1B9CDE` | `#A039B9` | `#39A95B` | `#FE9022` |
| 稳健聚焦 `focused` | `#1F5CD7` | `#12939D` | `#4B9654` | `#FF6B1A` |

每个基础色派生 `strong/soft/border`；XML 与 SVG 对同一输入必须产生相同结果。旧草案键不作为别名保留。

### 主题选择

优先级：用户逐槽颜色 > 用户明确主题 > 可明确映射的视觉描述 > 询问结果 > 默认科技蓝。

1. 已有主题、合法颜色、品牌色或明确视觉描述：直接使用。
2. 完全没有颜色信号：询问一次“科技蓝（默认）/活力多彩/稳健聚焦/自定义颜色”。
3. 用户回复“默认、随便、你决定、直接生成”或仍未选择：使用 `tech-blue/light`，不再追问。
4. 用户要求不提问或环境不支持交互：直接使用默认主题，并在结果中说明。

### 颜色、图标与布局

- 结构色分别用于主结构、辅助结构、并列结构和唯一焦点；状态色只表达真实状态。
- 图标只用于有明确导航、识别或焦点价值的位置；普通图通常 0～4 个但不设硬上限。数量较多时必须通过密度、重叠和可读性检查。Draw.io 优先原生形状，必要时使用内嵌单色 SVG；SVG 使用内联路径。
- 主体继续使用 `vertical-stack`。AI 仅在内容有明确信号时加入：`top-band`、`aux-column`、`callout`、`numbered-flow`、`focus-node`、`footer-band`。
- 附加模块通常 0～2 个，不得改变主层顺序、造成重叠或依靠扩大画布解决拥挤。

### 必须保持

- Draw.io XML 可编辑、离线可见，ID、父子结构和 `mxGeometry` 合法。
- SVG 自包含，保留 ARIA、`title/desc`，不使用 `foreignObject`。
- 浅色/深色模式只改变颜色，不改变几何。
- 不降低现有字号、对比度、间距和结构校验标准。

### 行为变化

| 当前 | 目标 |
|---|---|
| 固定、分散的 palette | 三套统一多色主题 + 用户逐槽覆盖 |
| 无统一主题确认流程 | 无颜色信号时只询问一次，再回退科技蓝 |
| 架构图只有标准纵向层 | 保留主骨架，按内容少量增加附加模块 |
| 图标规则不统一 | 少量、自包含、Draw.io 离线可见 |

---

## 3️⃣ 改哪些 (Where)

### 文件白名单

| 动作 | 文件 | 修改内容 |
|---|---|---|
| 修改 | `.opencode/skills/xml-diagram/SKILL.md`、`.opencode/skills/svg-generator/SKILL.md` | 统一主题识别、一次询问、默认回退、布局和图标流程 |
| 新增 | 两侧 `references/theme-tokens.md` | 主题名称、色值、覆盖优先级和派生规则 |
| 新增 | 两侧 `references/icon-policy.md` | 图标数量、来源和可移植性规则 |
| 修改 | XML `references/diagram-dsl.md`、SVG `references/svg-dsl.md` | 增加主题、四个色槽、附加模块和图标字段 |
| 修改 | 两侧 `references/quality-rules.md` | 统一颜色、询问、布局与图标约束 |
| 新增 | 两侧 `scripts/palette.py` | 确定性生成主题和用户配色 token |
| 修改 | XML `templates/*.drawio`、SVG `templates/*.svg` | 切换默认科技蓝；架构模板预留可选模块 |
| 修改 | XML `examples/*.drawio`、SVG `examples/*.svg` | 更新配色，并用代表例展示少量图标和附加模块 |
| 修改 | 两侧 `scripts/validate.py` 及 `tests/` | 校验主题键、颜色、图标、布局和跨格式一致性 |

除上述文件外不修改其他文件。

### 实施顺序

1. 定义两侧共享的主题键、色值、交互规则和测试向量。
2. 更新 `SKILL.md`、主题文档、DSL、图标策略和质量规则。
3. 实现 palette、校验器和测试。
4. 更新模板与示例，执行全量验证和真实渲染检查。

### 影响范围

- 新生成文件的默认配色及主题确认行为会变化。
- 架构模板可按内容增加少量附加模块和图标。
- 已生成文件和其他 Skill 不受影响。

---

## 4️⃣ 如何验证 (Verify)

### 验收与验证

| 验收结果 | 验证方式 | 预期结果 |
|---|---|---|
| 主题一致 | 两侧分别生成三套主题 | 基础色与派生 token 一致 |
| 询问流程正确 | 测试明确主题、自定义颜色、无主题、默认/直接生成和非交互场景 | 只在完全无信号时询问一次 |
| 用户颜色有效 | 测试单色、部分色槽和完整色槽 | 用户颜色保留，缺失色确定性补齐 |
| 文档一致 | 搜索两侧 Skill 全目录 | 无旧主题键残留 |
| 图标可移植 | 离线打开并导出 Draw.io；渲染 SVG | 图标可见、无外部资源，数量与内容匹配且不损害可读性 |
| 布局稳定 | 对比无附加模块时的 geometry | 主层顺序和主要几何不变 |
| 全量合法 | 运行严格校验、单测和代表图渲染 | 全部通过 |

### 实施结果

- XML：20 个单测通过；严格校验通过 37 个 Draw.io 文件。
- SVG：24 个单测通过；严格校验通过 40 个 SVG 文件。
- SVG 代表图：Chrome 真实渲染通过，尺寸为 1200×720。
- Skill 结构：`xml-diagram` 与 `svg-generator` 均通过 `quick_validate.py`。
- 跨格式：两侧 `palette.py` 内容一致，并由 XML 测试校验主题与明暗模式输出一致。
- 图标策略：普通图 0～4 个仅为克制建议，校验器未设置数量硬阈值。
- 自定义颜色：保留用户基础色，同时保证浅色/深色派生填充和边框对背景可见。
- Draw.io 图标：内嵌 SVG 会解码并解析，拒绝损坏 XML、远程引用、嵌套图片、脚本和外部字体/CSS。
- 主题与布局：只允许三套主题键；五类 SVG 架构模板均声明 `vertical-stack` 和可选模块集合。

### 执行命令

~~~powershell
Set-Location '.opencode/skills/xml-diagram'
python -X utf8 scripts/palette.py --theme tech-blue --mode light
python -X utf8 scripts/validate.py . --strict
python -m unittest discover -s tests -v

Set-Location '../svg-generator'
python -X utf8 scripts/palette.py --theme vibrant --mode light
python -X utf8 scripts/validate.py . --strict
python -m unittest discover -s tests -v
python -X utf8 scripts/validate.py examples --strict --render
~~~

### 停止条件

- 需要修改白名单外文件。
- 用户基础色无法在不被修改的情况下满足必要对比度。
- 附加模块必须改变主层顺序或模板入口。
- Draw.io 可编辑性、SVG 可访问性或现有质量标准下降。

### 风险与回滚

| 风险 | 缓解 | 回滚 |
|---|---|---|
| 主题询问打断一次性生成 | 只询问一次；直接生成和非交互场景使用默认主题 | 恢复为自动使用 `tech-blue/light` |
| XML/SVG 配色结果不一致 | 共享测试向量 | 回滚不一致实现 |
| 图标影响 Draw.io 兼容性 | 优先原生形状，并按密度、重叠和信息价值检查 | 移除无必要或不兼容的内嵌图标 |
| 附加模块造成拥挤 | 通常限制为 0～2 个并做重叠检查 | 恢复标准纵向模板 |

---

## ✅ 审批

**状态:** IMPLEMENTED
**批准记录:** 用户于 2026-08-16 明确要求“实施吧”，并确认图标不设置硬上限。

已按文件白名单实施并完成验证。
