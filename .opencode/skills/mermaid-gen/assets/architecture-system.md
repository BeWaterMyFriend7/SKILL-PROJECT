# Mermaid 架构与框图规则 v1.0

Mermaid 的优势是自动布局和文档可维护性，不追求像素级高级视觉。

## 推荐结构

- 系统模块：使用 `flowchart` + `subgraph`，嵌套不超过 3 层。
- 系统框图：优先 `block-beta`，列数不超过 4。
- 调用链：关系复杂时改用 `sequenceDiagram`，不要在 flowchart 中堆积交叉边。
- 数据关系：使用 `erDiagram`，不要用普通方框模拟实体关系。

## 约束

- 单图节点超过 20 时拆图。
- subgraph 标题简短，同级模块数量保持 2-6。
- 不使用大量 `style` 临时覆盖；统一通过 init themeVariables 和少量 classDef 表达语义。
- 用户要求精确坐标、品牌级高级视觉或复杂嵌套部署边界时，应改用 SVG 或 Draw.io。
