# Mermaid 语法参考

## 1. Flowchart (流程图)

方向：`TD`(默认)/`LR`/`RL`/`BT`

节点形状：
- `[矩形]` `[/圆角矩形/]` `((圆形))` `{菱形}` `[/平行四边形/]` `[[子程序]]`

连接线：
- `-->` 实线箭头 | `---` 无箭头 | `-.->` 虚线箭头 | `==>` 粗实线箭头 | `-- 标签 -->` 带标签

## 2. Sequence Diagram (时序图)

箭头类型：`->>` 实线实心 | `-->>` 虚线实心 | `->` 实线无填充 | `-->` 虚线无填充 | `-x` 叉尾 | `-)` 异步

激活区间：`activate B` ... `deactivate B`

## 3. Class Diagram (类图)

关系：`<|--` 继承 | `*--` 组合 | `o--` 聚合 | `<--` 关联 | `<..` 依赖
可见性：`+` public | `-` private | `#` protected | `~` package

## 4. ER Diagram (ER图)

基数：`||` 恰好一 | `|o` 零或一 | `}o` 零或多 | `}|` 一或多

## 5. State Diagram (状态图)

使用 `stateDiagram-v2` 语法，`[*]` 表示初始/结束状态。

## 6. Gantt Chart (甘特图)

任务状态：`crit`/`done`/`active`/`milestone`
日期格式：`YYYY-MM-DD`，时长用 `d`/`w`/`M`

## 7. Journey (用户旅程图)

满意度 1-5，格式：`步骤: 满意度: 参与者`

## 8. Git Graph (Git图)

使用 `commit`/`branch`/`checkout`/`merge` 命令

## 9. Pie Chart (饼图)

数值自动计算百分比，建议 6-8 个分类。

## 10. Mindmap (思维导图)

缩进表示层级，节点形状：`((圆形))` `[方形]` `(圆角)` `))云形((` `))](爆炸形)[(`
支持图标：`::icon(fa fa-star)`

## 11. Timeline (时间线)

格式：`时间段 : 事件1 : 事件2`

## 12. Quadrant Chart (象限图)

x/y 坐标范围 0-1，格式：`数据点: [x, y]`

## 13. XY Chart (XY图表)

同时支持 bar（柱状）和 line（折线）。

## 14. Sankey (桑基图)

格式：`源节点, 目标节点, 流量值`

## 15. Block Diagram (框图)

用 `columns N` 定义列数，节点格式：`名称 block:显示名:占用列数`
