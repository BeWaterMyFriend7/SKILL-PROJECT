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
    └── validate_change_plan.py
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

方案中已包含：

- 需求分析
- 当前实现
- 目标方案
- 修改前后变化
- 全项目影响矩阵
- 旧逻辑退役矩阵
- 文件变更清单
- 实施步骤
- 测试验证
- 执行契约
- 完成状态
- 审批记录
- 后续直接执行提示词

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