# Mermaid 语法参考

本 skill 使用 Mermaid CLI `11.16.0` 验证。每个 Mermaid block 第一行使用 `SKILL.md` 中的浅色或深色固定主题。

## 通用规则

- 标签含括号、冒号、斜杠或其他标点时优先使用引号，例如 `A["资格校验（库存/规则）"]`。
- 节点 id 使用简短 ASCII 字母、数字和连字符，展示名称可以使用中文。
- 标签尽量不超过 24 个中英文字符；节点默认不超过 20 个。
- 优先使用 `LR` 或 `TD` 单向布局；结构过密时拆图，不依靠大量 `style` 修补。
- `block-beta`、`xychart-beta`、`sankey-beta` 属于版本相关语法，必须真实渲染验证。

## Flowchart

- 方向：`TD`、`LR`、`RL`、`BT`。
- 节点：`[矩形]`、`([圆角])`、`((圆形))`、`{判断}`、`[[子程序]]`。
- 连线：`-->` 实线箭头，`---` 无箭头，`-.->` 虚线箭头，`-->|条件|` 带标签箭头。
- `subgraph 标题 ... end` 表达分区，嵌套不超过 3 层。

## Sequence diagram

- 请求：`->>`；返回：`-->>`；失败终止：`-x`；异步：`-)`。
- 参与者：`participant A as 服务`；用户角色可使用 `actor U as 用户`。
- 条件：`alt / else / end`；可选：`opt / end`；循环：`loop / end`。
- 激活区间：`activate A` 和 `deactivate A`。

## Class diagram

- 继承 `<|--`，组合 `*--`，聚合 `o--`，关联 `-->`，依赖 `<..`。
- 基数写在关系两端，例如 `订单 "1" *-- "*" 订单项`。
- 可见性：`+` public、`-` private、`#` protected、`~` package。

## ER diagram

- 基数：`||` 恰好一，`|o` 零或一，`}o` 零或多，`}|` 一或多。
- 字段行格式为 `类型 字段名 PK/FK`，PK/FK 标记可省略但关系基数不可省略。

## State diagram

- 使用 `stateDiagram-v2`。
- `[*]` 表示初始或终止状态，转换格式为 `状态A --> 状态B : 触发条件`。

## Gantt

- 必须包含 `title` 和 `dateFormat`。
- 状态：`crit`、`done`、`active`、`milestone`。
- 依赖：`after taskId`；时长使用 `d`、`w`、`M`。

## 其他图型

- `journey`：`任务: 1-5评分: 参与者`。
- `gitGraph`：使用 `commit`、`branch`、`checkout`、`merge`。
- `pie`：`"类别" : 数值`，建议不超过 8 类。
- `mindmap`：缩进表达层级，根节点使用 `root((主题))`。
- `timeline`：`时间段 : 事件1 : 事件2`。
- `quadrantChart`：数据点坐标范围为 0-1。
- `xychart-beta`：`bar` 和 `line` 数量应与 x 轴类别一致。
- `sankey-beta`：每行 `源节点,目标节点,非负流量`，非 ASCII 标签需实测。
- `block-beta`：使用 `columns N`，列数建议 2-4；节点可用 `节点["标题"]:占用列数`。
