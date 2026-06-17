# 主题标记规则

所有颜色必须来自主题标记表或用户明确给出的品牌色。默认不允许临时编造颜色。

## 标准主题

适用于技术架构图、部署架构图、流程图、时序图、实体关系图、状态图和总结图。

```yaml
浅色:
  bg: "#f8fafc"
  container_bg: "#f1f5f9"
  card: "#ffffff"
  border: "#cbd5e1"
  layer_border: "#cbd5e1"
  title: "#0f172a"
  text: "#334155"
  subtext: "#64748b"
  muted: "#94a3b8"
  arrow: "#94a3b8"
  shadow: "1"
  label_bg: "#f8fafc"

深色:
  bg: "#0f172a"
  container_bg: "#111827"
  card: "#1e293b"
  border: "#334155"
  layer_border: "#334155"
  title: "#f8fafc"
  text: "#cbd5e1"
  subtext: "#94a3b8"
  muted: "#64748b"
  arrow: "#64748b"
  shadow: "0"
  label_bg: "#0f172a"

语义色:
  primary: "#3498db"
  success: "#2ecc71"
  warning: "#e67e22"
  danger: "#e74c3c"
  purple: "#9b59b6"
  teal: "#1abc9c"
  gold: "#f39c12"
  gray: "#95a5a6"
```

## 浅色现代化用法

浅色背景下不要大面积使用高饱和实心色块配白字。优先使用浅底、语义色边框、深色文字：

```yaml
浅色语义浅底:
  primary_bg: "#e8f3ff"
  primary_border: "#3498db"
  primary_text: "#1d4ed8"
  success_bg: "#eafaf1"
  success_border: "#2ecc71"
  success_text: "#15803d"
  warning_bg: "#fff4e6"
  warning_border: "#e67e22"
  warning_text: "#9a3412"
  danger_bg: "#fdecec"
  danger_border: "#e74c3c"
  danger_text: "#b91c1c"
  purple_bg: "#f3e8ff"
  purple_border: "#9b59b6"
  purple_text: "#6b21a8"
  teal_bg: "#e6fffb"
  teal_border: "#1abc9c"
  teal_text: "#0f766e"
```

规则：

```text
浅色模式的能力卡片、标签和状态块优先使用浅底方案。
只有深色标题条、主强调按钮式节点或小面积徽标可以使用语义实心色块。
使用 #2ecc71、#e67e22、#1abc9c、#95a5a6 等偏亮填充时，正文不要使用 #ffffff。
```

## 分层背景

```yaml
浅色分层:
  access: "#e3f2fd"
  service: "#e8f5e9"
  data: "#fce4ec"
  infra: "#eceff1"
  gateway: "#ffebee"
  external: "#fff3e0"

深色分层:
  access: "#16213e"
  service: "#16213e"
  data: "#16213e"
  infra: "#16213e"
  gateway: "#1e293b"
  external: "#1e293b"
```

## 使用映射

| 标记 | 用途 |
| --- | --- |
| `bg` | 画布背景 |
| `container_bg` | 区域容器背景 |
| `card` | 节点和卡片填充 |
| `border` | 默认边框 |
| `layer_border` | 分层容器边框 |
| `title` | 页面标题文字 |
| `text` | 正文文字 |
| `subtext` | 次要文字 |
| `muted` | 脚注和弱文字 |
| `arrow` | 默认连线 |
| `shadow` | 阴影开关 |
| `label_bg` | 连线标签背景 |
| `primary` | 主体节点、主流程 |
| `success` | 成功、服务、能力 |
| `warning` | 警告、设计、外部系统 |
| `danger` | 错误、风险、失败 |
| `purple` | 异步、队列、测试 |
| `teal` | 通信、部署、存储访问 |

## 强制约束

```text
节点填充只能使用卡片标记或语义色。
区域容器填充使用容器背景标记或分层背景色。
正文文字使用标题、正文、次要文字或弱文字标记。
标题条可使用语义色，但文字必须高对比。
深色模式阴影标记固定为 0。
连线标签背景必须与画布背景一致。
同一张图语义色不超过 8 种。
大面积背景禁止使用高饱和语义色。
```

## 对比度

```text
正文文字与背景对比度必须清晰。
浅色块不能使用低对比白字。
深色模式禁止使用 #666666 以下灰度作为正文。
标签背景和文字颜色必须成对选择。
```

## 图例语义

```text
主色 = 用户 / 前端 / 需求 / 主体
成功色 = 服务 / 能力 / 成功
警告色 = 外部系统 / 设计 / 警告
错误色 = 错误 / 风险 / 失败
紫色 = 测试 / 异步 / 对比对象
青色 = 部署 / 发布 / 通信 / 存储访问
灰色 = 基础设施 / 中性边界
```
