# Mermaid 质量契约 v1.0

## 硬性门槛

- Markdown fence 完整，Mermaid 源码非空。
- 图类型与声明能力一致，语法可由固定版本 renderer 解析。
- 必须提供固定主题初始化配置；不得依赖环境默认配色。
- 默认节点不超过 20，subgraph/section 不超过 8，嵌套不超过 4 层。
- 单个节点标签建议不超过 24 个中英文字符；过长时主动换行或拆图。
- 方向与内容匹配：阶段流程优先 LR，层级/决策优先 TD，时序图按时间向下。
- 节点、参与者、实体和状态名称必须有意义。
- renderer 不可用时必须明确报告“结构通过、渲染未验证”，不得宣称完整通过。

## 交付命令

```bash
python -X utf8 scripts/validate_mermaid.py examples --require-render
```
