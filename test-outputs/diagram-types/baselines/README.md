# 四主题全流程视觉基线

本目录用于审批两套绘图 Skill 的新视觉合同，不复用或批量换色旧示例。

完整链路为：自然语言需求（`requests.json`）→ 可执行 DSL → 结构角色配色映射 → 全新 SVG/Draw.io 源文件 → 严格校验 → Chrome/Draw.io 真实渲染 → SHA-256 验证报告。

## 一键重新生成与验证

在仓库根目录执行：

```powershell
python test-outputs/diagram-types/baselines/verify_baselines.py
```

脚本只清理本目录中四个已声明主题的 DSL、SVG、Draw.io 和 PNG 目标文件，然后从 `requests.json` 重新生成。它不会读取 `.opencode/skills/*/examples`，且会检查每个源文件中的 `fresh-dsl-v1` 标记、规格哈希以及 `legacyInputFiles: []`。

通过条件：

- 四套主题各自重新产生 DSL、SVG、Draw.io、SVG PNG、Draw.io PNG；
- SVG 通过 `--strict --render`，Draw.io 通过 `--strict`；
- PNG 分别由本机 Chrome/Edge 与 Draw.io 桌面版真实导出；
- [generation-manifest.json](generation-manifest.json) 的源文件哈希全部匹配；
- [verification-report.json](verification-report.json) 记录本次运行时间、清理目标、执行命令、渲染器和 20 个产物哈希。

## 审批预览

| 主题 | DSL | SVG 源文件 | Draw.io 源文件 | SVG PNG | Draw.io PNG |
| --- | --- | --- | --- | --- | --- |
| Tech Blue｜科技蓝（默认） | [DSL](dsl/tech-blue.md) | [SVG](svg/tech-blue.svg) | [Draw.io](xml/tech-blue.drawio) | [预览](images/svg/tech-blue.png) | [预览](images/xml/tech-blue.png) |
| Vibrant ｜活力 | [DSL](dsl/vibrant.md) | [SVG](svg/vibrant.svg) | [Draw.io](xml/vibrant.drawio) | [预览](images/svg/vibrant.png) | [预览](images/xml/vibrant.png) |
| Mint green｜清爽绿 | [DSL](dsl/mint-green.md) | [SVG](svg/mint-green.svg) | [Draw.io](xml/mint-green.drawio) | [预览](images/svg/mint-green.png) | [预览](images/xml/mint-green.png) |
| Steady Red & Blue｜稳重红蓝 | [DSL](dsl/steady-red-blue.md) | [SVG](svg/steady-red-blue.svg) | [Draw.io](xml/steady-red-blue.drawio) | [预览](images/svg/steady-red-blue.png) | [预览](images/xml/steady-red-blue.png) |

这四张是阶段一审批基线。视觉确认后，再用相同管线批量重建 19 种图形类型；旧的 19 类索引目前仍属于历史输出，不能作为新视觉合同的通过证据。
