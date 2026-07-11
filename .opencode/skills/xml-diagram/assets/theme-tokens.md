# Draw.io 主题映射

权威颜色与尺寸定义见本目录 `visual-tokens.md`。本文件只说明如何把标记映射到 draw.io 样式，避免产生第二套配色。

| 角色 | draw.io 样式 |
| --- | --- |
| 画布 | `background=#F6F8FB` |
| 普通卡片 | `fillColor=#FFFFFF;strokeColor=#D8E1EA;fontColor=#172033` |
| 次级卡片 | `fillColor=#EEF3F8;strokeColor=#D8E1EA;fontColor=#172033` |
| 主焦点 | `fillColor=#EFF6FF;strokeColor=#2563EB;fontColor=#1D4ED8` |
| 外部依赖 | `fillColor=#FFF7ED;strokeColor=#D97706;fontColor=#9A3412` |
| 数据与存储 | `fillColor=#ECFEFF;strokeColor=#0891B2;fontColor=#155E75` |
| 错误路径 | `strokeColor=#DC2626;dashed=0` |
| 异步路径 | `strokeColor=#7C3AED;dashed=1` |

## 约束

- 默认字体：`Inter, Noto Sans SC, Microsoft YaHei, sans-serif`。
- 浅色卡片优先深色文字，不允许亮色填充配低对比白字。
- 同图强调色不超过 3 种；中性色不计入强调色。
- 用户品牌色必须记录为显式覆盖，不能静默改写本地标记。
