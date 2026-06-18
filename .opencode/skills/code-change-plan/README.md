# code-change-plan

这是一个用于代码修改前分析和设计的 Codex Skill。它只负责生成一个完整的 Markdown 变更方案，不修改业务代码，也不生成单独 JSON。

## 一、目录结构

```text
code-change-plan/
├── SKILL.md
├── README.md
├── assets/
│   ├── change-plan-template.md
│   └── change-plan-amendment.md
├── references/
│   ├── workflow-detail.md
│   ├── report-structure.md
│   └── quality-checklist.md
└── scripts/
    ├── validate_change_plan.py
    └── check_utf8.py
```

## 二、安装

复制到 Codex 全局 Skill 目录：

```text
C:\Users\BeWater\.codex\skills\code-change-plan\
```

安装完成后应存在：

```text
C:\Users\BeWater\.codex\skills\code-change-plan\SKILL.md
```

## 三、调用方式

在项目根目录启动 Codex，然后输入：

```text
$code-change-plan

请分析以下需求并生成完整代码变更方案，只生成一个 Markdown，不修改业务代码：
<需求内容>
```

## 四、推荐提示词

```text
$code-change-plan

请分析以下需求并产出完整的代码变更方案：

<需求内容>

要求：
1. 只分析和生成方案，不修改业务代码
2. 分析当前功能流程、调用链、数据流和配置流
3. 设计目标功能流程、调用链、数据流和配置流
4. 明确修改前后差异
5. 全项目评估代码、测试、配置、脚本、数据、接口、文档和监控影响
6. 列出需要删除、替换、迁移或限期兼容的旧逻辑
7. 不允许无规则保留新旧两套实现
8. 给出准确文件清单、实施顺序和验证命令
9. 把执行约束、停止条件和所有校验项写入同一个 Markdown
10. 初始审批状态必须为 WAITING_FOR_APPROVAL
```

## 五、输出位置

```text
.codex/change-plans/<plan-id>.md
```

方案包含 7 个章节：

1. 基本信息与需求分析：基线 + 业务目标 + 功能需求 + 验收标准 + 待决策项
2. 当前实现与差距：模块职责 + 当前流程 + 差距分析
3. 目标方案与对比：方案概述 + 设计决策 + 目标流程 + 修改前后对比
4. 影响范围与文件清单：修改单元 + 影响矩阵 + 旧逻辑退役 + 文件清单
5. 实施顺序：按依赖关系的步骤表
6. 测试、验证与完成：验证方案 + 追踪矩阵 + 发布回滚 + 完成条件
7. 执行契约与审批：执行规则 + 停止条件 + 风险 + 审批 + 执行提示词

## 六、执行方式

人工审核方案后，将状态改为：

```text
APPROVED
```

然后新建 Codex 会话，输入：

```text
读取并严格执行以下已批准的代码变更方案：

.codex/change-plans/<plan-id>.md

要求：
1. 严格按照修改单元、文件清单和实施顺序执行
2. 完整处理旧逻辑退役矩阵
3. 不得出现未经批准的新旧逻辑双活
4. 每个修改单元完成后运行局部验证
5. 完成后运行全部必需验证
6. 发现计划外影响时停止，并标记 PLAN_AMENDMENT_REQUIRED
7. 不执行 git add、git commit 或 git push
8. 最后报告实际修改、旧逻辑清理、验证结果、未执行项和残余风险
```

## 七、Windows 环境注意

- 本 Skill 所有 `.md` 文件均为 UTF-8 编码
- 若在 PowerShell 中用 `Get-Content` 读到乱码，改用 `[System.IO.File]::ReadAllText("<path>", [System.Text.Encoding]::UTF8)`
- Skill 仅生成方案，不修改业务代码；方案执行时参考执行契约中的 Windows 文件编辑指南（规则 12、13）

## 八、与其他 Skill 的协作

- **code-merge-helper**：当变更涉及分支合并且存在冲突时，建议暂停本方案执行，先使用 `code-merge-helper` 完成三方合并分析。合并完成后再回到本方案继续执行。
- 可以在合并分析报告（code-merge-helper 产出）的第 10 章人工决策项中引用本方案的 plan-id，建立追溯链。
