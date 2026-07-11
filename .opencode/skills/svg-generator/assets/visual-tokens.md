# SVG 视觉标记 v1.0

本文件是 `svg-generator` 文件夹内唯一的基础视觉值来源，不依赖其他 skill。

## 颜色

| 角色 | 浅色 | 深色 |
| --- | --- | --- |
| canvas | `#F6F8FB` | `#0F172A` |
| surface | `#FFFFFF` | `#172033` |
| surface-muted | `#EEF3F8` | `#1E293B` |
| border | `#D8E1EA` | `#334155` |
| text-strong | `#172033` | `#F8FAFC` |
| text | `#475569` | `#CBD5E1` |
| text-muted | `#64748B` | `#94A3B8` |
| primary | `#2563EB` | `#60A5FA` |
| success | `#16A34A` | `#4ADE80` |
| warning | `#D97706` | `#FBBF24` |
| error | `#DC2626` | `#F87171` |
| async | `#7C3AED` | `#A78BFA` |
| storage | `#0891B2` | `#22D3EE` |

## 字体

- 字体族：`Inter, "Noto Sans SC", "Microsoft YaHei", sans-serif`
- 页面标题：26px / 700
- 副标题：13px / 400
- 区域标题：18px / 700
- 卡片标题：15px / 600
- 正文：12px / 400
- 辅助文字：11px / 400
- 禁止小于 11px；仅坐标刻度可使用 10px。

## 形状与间距

- 页面边距：40px，硬下限 30px。
- 区域间距：36px；卡片间距：28px；标签间距：8px。
- 区域圆角：14px；卡片圆角：10px；标签圆角：6px。
- 区域边框：1.5px；卡片边框：1.5px；连线：2px。
- 浅色阴影：`0 4 14 rgba(15,23,42,.08)`；深色禁止阴影。
- 一张图默认只使用一个主色，额外语义色不超过三种。
