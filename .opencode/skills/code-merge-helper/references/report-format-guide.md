# 报告与 JSON 格式填写指南

> 配合 `assets/merge-resolution-report.md` 模板使用。SKILL.md 仅保留流程与约束，本章提供各章节的详细填写规范。

---

## 报告各章节填写规范

### 1. 合并上下文

| 字段 | 说明 | 数据来源 |
|---|---|---|
| 仓库/目录 | 绝对路径 | `git rev-parse --show-toplevel` |
| Git 操作 | merge / rebase / cherry-pick | 检测 `.git/MERGE_HEAD` 等元数据 |
| 当前分支 | 分支名 | `git branch --show-current` |
| 当前 HEAD | 完整 SHA | `git rev-parse HEAD` |
| 操作对象提交 | 合入的提交 SHA | `cat .git/MERGE_HEAD` |
| stage-2 来源 | 当前分支侧，注明分支名 | `HEAD` |
| stage-3 来源 | 合入分支侧，注明分支名 | `MERGE_HEAD` |
| common-base | 共同祖先 SHA | `git merge-base HEAD MERGE_HEAD` |
| 工作区既有改动 | 无 / 列出文件 | `git status --short` |

### 2. 执行摘要

简明扼要，1 分钟内可读完。重点突出：高风险项数、需人工决策数、总体策略一句话。

### 3. 冲突清单

每行一个冲突。类型可选：文本、结构、语义、接口消费者、重命名/删除、生成文件、依赖、配置、接口、数据迁移、测试、文档。

风险 4-5 的行加粗标记。

### 4. 冲突详细分析

每个冲突独立一节（C-01, C-02...）。

**项目逻辑**：不超出冲突文件 + 1 跳调用链。写清楚「这个符号在系统中做什么」。

**三方变化对比**：每行一句话描述行为差异。证据来源列可以是「提交 SHA + 文件名」或「测试用例名」。

**提交追溯**：证据等级只有三种——
- **事实**：提交 diff + 测试 + 文档三者一致
- **高置信**：提交 diff + 关联 issue/PR 一致，但缺测试
- **低置信**：仅有提交 diff，无其他佐证

**候选方案**：至少评估 A/B/C 三种。推荐方案需写明「为什么其他方案不行」。

### 5. 行为保留矩阵

每个行为 ID 必须对应至少一个验证项。来源标注为 stage-2 / stage-3 / 新增。

### 6. 逐文件实施清单

**这是白名单**。执行阶段只能修改此表列出的文件。

操作类型：修改 / 新增 / 删除 / 重命名 / 重新生成。

禁止事项写「不得删除 XX 测试」「不得修改 YY 接口签名」等具体约束。

### 7. 影响范围评估

核心扫描结果写在此表。扩展扫描结果按风险标注触发条件。

### 8. 执行顺序

按依赖关系排序：源定义/接口 → 业务实现 → 配置/迁移 → 生成文件/锁文件 → 测试 → 文档。

### 9. 验证计划

层级：结构 / 静态 / 针对性 / 集成 / 全量 / 人工。

必须执行的验证项用「是」，可选用「否」。

### 10. 人工决策项 ⭐

**这是审批人最关注的部分，必须详尽。**

每个 HD-xx 包含以下完整信息：

**涉及功能**：一句话，用业务语言而非技术语言。例如「Sidecar 启动时的服务发现策略」而非「main.go 中的 init 函数」。

**数据流/流程**：ASCII 流程图，5-8 个节点为佳。例如：
```
Nacos 拉取 → 解析 → 快照落盘 → 热加载 → eBPF Map 写入 → sidecar 生效
```

**改动点明细**：每个改动点一条记录。修改目的要写「为什么改」而非「改了什么」。例如「统一端口管理，减少配置项」而非「删除了 dnsListen 变量」。

**合并建议**：2-3 句。第一句说推荐哪个方案，第二句说核心理由，第三句（可选）说注意事项。

**影响范围**：分直接和间接。直接是改动的文件/函数，间接是被影响的调用方/配置/测试。

**功能影响**：三个维度缺一不可——正面效果、不合并后果、回滚建议。

**待决策问题**：单选或判断题，审批人可以直接回答「是/否」或「选 A/B」。

### 11. 停止条件

必须覆盖：现场漂移、范围扩张、符号不存在、验证失败、新风险。

### 12. 残余风险与回滚

回滚步骤要**可执行**：具体的 git 命令或文件恢复路径，不要写「恢复到合并前」。

### 13. 人工审批

审批状态默认 `WAITING_FOR_APPROVAL`，**不可自行改为 APPROVED**。

审批人确认后手动修改状态和批准范围。

### 14. 执行指引

此章节供 Agent 执行时参考，无需审批人关注。内容从 SKILL.md 和 Executor 规则中提取，确保 Agent 无需加载其他 Skill 即可执行。

---

## 附录 A JSON block 字段规范

> JSON block 嵌入在报告末尾的 ` ```json ` fenced code block 中，按 `assets/merge-plan.schema.json` 约束。
> 验证脚本从 Markdown 文件中自动提取该 block 进行结构校验。

| 字段 | 必填 | 说明 |
|---|---|---|
| `schema_version` | ✅ | 固定 `"1.0"` |
| `plan_id` | ✅ | 与报告中的 plan-id 一致 |
| `status` | ✅ | Planner 写 `"WAITING_FOR_APPROVAL"` |
| `report_path` | ✅ | 相对仓库根的路径 |
| `generated_at` | ✅ | ISO 8601 时间戳 |
| `repository.root` | ✅ | 仓库绝对路径 |
| `repository.head` | ✅ | 当前 HEAD SHA |
| `repository.existing_worktree_changes` | | 工作区既有改动文件列表 |
| `git_snapshot.operation` | ✅ | `"merge"` / `"rebase"` / `"cherry-pick"` |
| `git_snapshot.operation_head` | | 操作对象提交 SHA |
| `git_snapshot.conflict_files` | ✅ | 冲突文件路径数组 |
| `git_snapshot.stages` | ✅ | 每个冲突文件的三阶段 Blob |
| `approval.status` | ✅ | Planner 写 `"WAITING_FOR_APPROVAL"` |
| `approval.scope` | ✅ | 批准后写 `["ALL"]` 或具体 ID 列表 |
| `approval.approver` | | 批准后填写 |
| `approval.approved_at` | | 批准后填写 |
| `decisions[].id` | ✅ | `"D-01"` 格式 |
| `decisions[].strategy` | ✅ | 保留策略描述 |
| `decisions[].preserve[].behavior_id` | ✅ | `"B-01"` 格式 |
| `decisions[].preserve[].validation_ids` | ✅ | 关联的验证项 ID |
| `allowed_changes[].id` | ✅ | `"A-01"` 格式 |
| `allowed_changes[].path` | ✅ | 文件路径 |
| `allowed_changes[].action` | ✅ | modify / add / delete / rename / regenerate |
| `allowed_changes[].instructions` | ✅ | 修改说明 |
| `allowed_changes[].must_preserve` | | 必须保留的行为 ID |
| `allowed_changes[].must_not` | | 禁止事项 |
| `execution_steps[].order` | ✅ | 从 1 开始的连续整数 |
| `execution_steps[].action_ids` | ✅ | 本步骤包含的动作 ID |
| `validations[].id` | ✅ | `"V-01"` 格式 |
| `validations[].level` | ✅ | structural / static / targeted / integration / full / manual |
| `validations[].required` | ✅ | true / false |
| `stop_conditions` | ✅ | 停止条件列表 |
| `prohibited_actions` | ✅ | 禁止操作列表 |
