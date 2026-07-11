# Mermaid 视觉标记 v1.0

本文件只服务 `mermaid-gen`，不依赖其他 skill。

## 颜色

| 角色 | 浅色 | 深色 |
| --- | --- | --- |
| canvas | `#F6F8FB` | `#0F172A` |
| surface | `#FFFFFF` | `#172033` |
| border | `#D8E1EA` | `#334155` |
| text-strong | `#172033` | `#F8FAFC` |
| text | `#475569` | `#CBD5E1` |
| primary | `#2563EB` | `#60A5FA` |
| success | `#16A34A` | `#4ADE80` |
| warning | `#D97706` | `#FBBF24` |
| error | `#DC2626` | `#F87171` |
| async | `#7C3AED` | `#A78BFA` |

## 主题要求

- 字体族：`Inter, Noto Sans SC, Microsoft YaHei, sans-serif`。
- 使用 `%%{init: ...}%%` 固定 themeVariables，不依赖 renderer 默认主题。
- 每张图一个主色，额外语义色不超过三种。
- 错误使用红色实线语义；异步使用紫色虚线语义。
