---
name: code-merge-helper
description: 合并冲突决策：当用户要求分析 Git merge/rebase/cherry-pick 冲突、制定冲突方案或评估两侧改动时，只读追溯 common-base/stage-2/stage-3，输出自包含 Markdown 报告和附录 A JSON 执行契约；报告获批后才按第 14 章实施。
---

# Code Merge Helper

把冲突处理视为“三方语义决策”，产出**自包含的可执行契约**：报告获批后无需加载其他 Skill。

> 报告各章节的详细填写规范见 `references/report-format-guide.md`。

## 职责边界

**负责**：找冲突 → 分析逻辑 → 追溯目的 → 形成方案 → 评估影响 → 输出自包含 Markdown 报告（含附录 A JSON 执行契约）。

**禁止**：修改业务文件、解决冲突标记、git add/commit/push、自行标记已批准、替用户决定互斥规则、**输出后在同一 turn 内继续修改代码**。

产物写入 `.git/codex-merge-review/<plan-id>/`。

> plan-id 格式：`merge-YYYYMMDD-HHMMSS`（如 `merge-20260618-143052`），基于生成时间戳保证唯一性。

## 强制原则

- 统一使用 `common-base`、`stage-2`、`stage-3`，不用 `ours/theirs`。
- 提交作者/时间/信息只是证据，不能单独证明意图。
- 编译通过 ≠ 语义正确，方案必须覆盖两侧应保留行为。
- 生成文件/锁文件从源定义重新生成。
- 不可逆变更、安全冲突、接口不兼容、互斥规则 → 列入人工决策项。
- 报告与附录 A JSON 执行契约必须一致；由同一文件构造保证一致性。
- **所有输出文件与会话摘录必须保持可读 UTF-8**：报告 `.md` 以及任何中间产物。
  - Windows 环境禁止使用 PowerShell `Set-Content` / `Out-File` 直接覆写含中文的文件；必须通过 Python 临时脚本显式指定 `encoding="utf-8"`。
  - 在 Codex/PowerShell 会话中查看或摘录中文 Markdown 时，禁止用 `Get-Content`、`type`、`more` 直接输出到会话；使用 Python 读取并打印，例如：`python -c "from pathlib import Path; print(Path(r'<file>').read_text(encoding='utf-8'))"`。
  - 如果会话输出出现 `鍦`、`鈥`、`銆`、`锛`、`U+FFFD` 等乱码特征，立即停止使用该输出；必须重新用 Python 回读原文件后再总结、复制或写入。
  - 写入完成后必须回读校验：读取文件前 3 字节确认无 BOM `\xef\xbb\xbf`，全文不得出现 Unicode 替换字符 `\ufffd` 或可疑 mojibake 片段。
  - 校验命令：`python scripts/check_utf8.py --strict-mojibake <file>`
  - 校验失败 → 以 UTF-8 重新生成，不得输出含乱码的文件。

## 输入识别

记录：仓库根目录、分支、HEAD、Git 操作类型、操作对象、common-base、stage 来源、工作区既有改动、AGENTS.md。

信息不全不停止分析，无法确定的内容标注置信度。

## 标准流程

范围等级：
- **【仓库级】**
- **【核心（必扫）】** + 扩展（按风险触发）
- **【冲突文件】** + 1 跳调用链

### 0. 安全预检

`git status --short --branch` → `git diff --name-only --diff-filter=U` → 检测 merge/rebase/cherry-pick 元数据 → `scripts/collect_merge_context.py`。

### 1. 建立冲突清单

每个冲突记录：ID、文件、区间、类型、三方变化、耦合的自动合并文件。

### 2. 分析项目逻辑

限定冲突文件 + 直接调用者/被调用者（1 跳）。检查：完整函数/模块、调用链、关联测试、同提交配套修改、自动合并的组合错误。

### 3. 追溯修改来源

按冲突文件过滤提交历史。记录：SHA、作者、时间、diff、关联 issue/PR、修改目的、证据等级（事实/高置信/低置信）。

### 4. 形成候选方案

每冲突评估 5 种方案（保留 stage-2、保留 stage-3、语义融合、重构融合、升级人工决策）。推荐方案必须写明保留什么、舍弃什么及理由。

### 5. 评估影响范围

- **核心（必扫）**：冲突文件、1 跳调用链、单元测试、同提交配套文件。
- **扩展（按风险触发）**：风险 1-2 跳过；风险 3 加配置/脚本/文档；风险 4-5 加 CI/依赖/迁移/回滚；import 变化加依赖树；schema 变化加消费者兼容。

### 6. 跨冲突检查

一致性、接口匹配、重复注册/死代码、安全校验覆盖、行为倒退。**接口消费者扫描**：对冲突涉及的符号反向搜索所有引用，检测任一侧删除而另一侧仍有引用的情况。

### 7. 输出报告

按 `assets/merge-resolution-report.md` 模板输出单一 Markdown 文件。报告第 1-12 章供人审，第 14 章供 Agent 执行，附录 A 为 JSON 执行契约（按 `assets/merge-plan.schema.json` 约束），供脚本做确定性校验。

### 8. 自检并停止

```bash
python scripts/validate_merge_plan.py --plan <plan.md> --repo . --pre-merge
```

确认 `WAITING_FOR_APPROVAL`、决策完整、行为有验证项、记录 Blob 指纹、报告自包含。

> **完成后必须立即停止，不得在同一 turn 内修改代码。** 提示用户审批后 Agent 按第 14 章执行。

## 交接契约

报告的内容要求详见 `references/report-format-guide.md`。核心要点：

- 报告第 10 章人工决策项必须包含：功能、数据流、改动点明细（谁在什么时候为什么改）、合并建议、影响范围、功能影响、待决策问题。
- 报告第 14 章执行指引必须包含：前置校验、执行约束、范围守卫、分层验证、偏差处理、最终复核、执行结论。
- 附录 A JSON 执行契约必须记录 HEAD、操作对象、冲突集合和 stage Blob，Planner 不得写 `APPROVED`。

## 完成条件

- 显式冲突 + 潜在语义冲突（含接口消费者）均有决策。
- 行为保留矩阵完整，每个行为有关联验证项。
- 修改文件均进入白名单。
- 人工决策项信息完整。
- 报告通过 `--pre-merge` 校验，附录 A JSON 执行契约结构合法。
- 执行指引章节完整。
- **已停止修改，等待审批。**

## 执行中修正

当报告审批结果为 `APPROVED_WITH_CHANGES` 或执行中出现偏差（见报告第 14.5 节），使用 `assets/plan-amendment.md` 模板生成修正请求，而非全量重新分析。

规则：
- 保留原 plan-id 不变
- 仅更新变更涉及的章节和附录 A JSON block
- 修正后报告状态重置为 `WAITING_FOR_APPROVAL`
- 修正批准前停止一切修改

## 推荐调用

```
分析当前 merge 冲突，生成报告，不修改代码。
```

```
分析 feature/order-v2 合入 release/2.8 的冲突，重点检查接口兼容和数据库迁移。
```

```
报告已批准，按第 14 章执行指引修改代码，不暂存、不提交。
```
