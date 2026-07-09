---
name: diff-review
description: Review the current diff for correctness bugs and reuse/simplification/efficiency cleanups. Supports two modes: single-agent (default) for quick reviews, and --multi for multi-agent collaboration (finder + verifier + completeness critic + reporter) to minimize missed findings.
---

# Diff Review

审查当前 git diff，发现正确性 bug 和代码简化/复用/效率改进点。

## 运行模式

| 模式 | 触发 | 流程 | 适用场景 |
|------|------|------|---------|
| **单智能体** | 默认（无 flag） | 上下文收集 -> 逐维度审查 -> 输出报告 | 日常小改动、diff < 200 行 |
| **多智能体（--multi）** | `--multi` flag | 上下文收集 -> 3 路并行查找 -> 对抗验证 -> 完整性审查 -> 综合报告 | 大改动、高风险变更、effort high/max |

**规则**：effort 设为 `high` 或 `max` 时，自动启用 `--multi` 模式。

---

## 0. 上下文收集（单智能体 & 多智能体共用）

### 检测 CodeGraph

首先检查项目根目录是否存在 `.codegraph/` 目录：

```bash
test -d .codegraph && echo "CODEGRAPH_AVAILABLE" || echo "CODEGRAPH_UNAVAILABLE"
```

### 路径 A：CodeGraph 可用

**必须**优先使用 CodeGraph MCP 工具收集上下文：

1. `git diff --name-only HEAD` 获取变更文件列表
2. 对变更文件中的核心符号，用 `codegraph_explore` 一次性获取完整上下文：
   ```
   codegraph_explore(query="<变更涉及的函数/类/模块名 空格分隔>", depth=2)
   ```
   - 默认 `depth=2`，high/max 时 `depth=3`
3. 对核心变更符号，用 `codegraph_callers` 追踪所有调用方：
   ```
   codegraph_callers(symbol="<变更的函数/方法名>")
   ```
4. 用 `codegraph_callees` 查看变更函数内部依赖：
   ```
   codegraph_callees(symbol="<变更的函数/方法名>")
   ```
5. high/max 时，用 `codegraph_impact` 做 N 跳影响传播分析：
   ```
   codegraph_impact(symbol="<核心变更符号>", depth=3)
   ```

### 路径 B：CodeGraph 不可用

使用传统工具：
1. `git diff --name-only HEAD` 获取变更文件列表
2. grep 搜索变更函数/类的调用方
3. glob 查找相关测试文件
4. Read 读取变更文件及其直接依赖

**不得跳过上下文收集直接审 diff** —— 至少读取变更文件全文和直接调用方。

收集完毕后，产出 **Context Brief**（变更文件清单 + 核心符号列表 + 调用关系摘要），供后续阶段使用。

---

## 1. 审查维度

### 1.1 正确性（Correctness）
- 空指针/nil 引用
- 边界条件（off-by-one、空集合、零值）
- 并发安全（race condition、死锁、缺少同步）
- 错误处理（吞掉错误、错误类型不匹配、缺少错误传播）
- 资源泄漏（未关闭的文件/连接/锁）
- 类型安全（类型断言无检查、溢出、截断）
- 逻辑错误（条件反转、短路逻辑误用、状态机非法转换）

### 1.2 简化与复用（Simplification & Reuse）
- 可消除的重复代码
- 可用标准库/现有工具函数替代的自定义实现
- 过度抽象（可内联的间接层）
- 死代码（零调用方的导出符号）
- 可简化的复杂条件表达式

### 1.3 效率（Efficiency）
- 不必要的分配/拷贝
- 循环内的重复计算
- 阻塞 IO 可改为异步
- 大对象值传递应改指针/引用
- N+1 查询模式

---

## 2. 模式 A：单智能体（默认）

### 流程

按 Step 0 收集上下文后，逐文件、逐维度审查 diff，产出发现列表。

### Effort Level

| Level | 上下文深度 | CodeGraph depth | 审查范围 |
|-------|-----------|-----------------|---------|
| **low** | 变更文件 + 直接调用方 | depth=1 | 仅高置信度正确性 bug |
| **medium** | 变更文件 + 1 跳调用链 | depth=2 | 正确性 + 简化复用 |
| **high** | 自动启用 --multi 模式 | -- | -- |
| **max** | 自动启用 --multi 模式 | -- | -- |

未指定 effort level 时默认 **medium**。

### 输出格式

```markdown
### [Severity] Title

- **File**: `path/to/file.ts:123`
- **Category**: correctness | simplification | efficiency
- **Confidence**: high | medium | low
- **Description**: <what the issue is>
- **Impact**: <what happens if not fixed>
- **Fix**: <concrete suggestion>

---
```

严重度标记：
- `CRITICAL`：运行时崩溃、数据丢失、安全漏洞
- `HIGH`：功能错误、资源泄漏
- `MEDIUM`：代码异味、不必要的复杂度
- `LOW`：风格改进、微小优化

---

## 3. 模式 B：多智能体（--multi）

### 整体架构

```
Context Brief
     |
     +---> Finder:Correctness  ----+
     |                             |
     +---> Finder:Simplify   ----+ |
     |                           | |
     +---> Finder:Efficiency ----+ |
         (3 路并行查找)             |
                                   v
                            Verifier (对抗验证)
                                   |
                                   v
                         Completeness Critic
                         (遗漏维度检查)
                                   |
                                   v
                              Reporter
                            (综合报告产出)
```

### Phase 1：并行查找（3 Finder agents）

同时启动 3 个独立 Agent，各自从不同维度审阅相同的 Context Brief + diff。每个 Agent 只能看到自己的维度，确保独立性。

**Finder 1: Correctness**

使用 Agent 工具启动，subagent_type="general-purpose"，description="Find correctness bugs"。

Prompt 要点：
- 仅审查正确性维度（空指针、边界、并发、错误处理、资源泄漏、类型安全、逻辑错误）
- 基于 Context Brief 和 git diff
- 对每个发现输出：文件+行号、严重度、置信度、问题描述、影响、修复建议
- 只报告确定或高置信的问题，不猜测

**Finder 2: Simplification & Reuse**

使用 Agent 工具启动，subagent_type="general-purpose"，description="Find simplification issues"。

Prompt 要点：
- 仅审查简化与复用维度（重复代码、标准库替代、过度抽象、死代码、复杂条件）
- 对每个发现输出：文件+行号、严重度、置信度、描述、影响、建议
- 只报告明确可改进的问题

**Finder 3: Efficiency**

使用 Agent 工具启动，subagent_type="general-purpose"，description="Find efficiency issues"。

Prompt 要点：
- 仅审查效率维度（分配/拷贝、循环计算、阻塞IO、值传递、N+1查询）
- 对每个发现输出：文件+行号、严重度、置信度、描述、影响、建议
- 只报告有实际性能影响的问题

收集所有 3 个 Finder 的发现，合并为 `all_findings` 列表（同一文件+同一行的发现去重，优先保留 正确性 > 简化 > 效率）。

### Phase 2：对抗验证（Verifier agent）

启动 Verifier agent，对 `all_findings` 中的每条发现尝试**反驳**：

使用 Agent 工具启动，subagent_type="general-purpose"，description="Verify each finding adversarially"。

Prompt 要点：
- 逐条审查 all_findings，尝试反驳
- 判断：CONFIRMED（证据充分）/ REFUTED（误报）/ UNCERTAIN（降级为 low confidence）
- 必须基于具体代码证据，不因「理论上可能」保留
- 输出格式：`[ID] VERDICT: ... | Reason: ... | Adjusted Confidence: ... | Adjusted Severity: ...`

过滤 REFUTED 发现，UNCERTAIN 降级保留。产出 `verified_findings`。

### Phase 3：完整性审查（Completeness Critic）

启动 Completeness Critic，检查遗漏：

使用 Agent 工具启动，subagent_type="general-purpose"，description="Check for missed findings"。

Prompt 要点：
- 基于 Context Brief + git diff + verified_findings
- 对照完整维度清单，逐项检查是否有遗漏
- 检查跨文件交互问题
- 检查缺失的测试覆盖
- 只报告确实遗漏的具体问题，不重复已有发现
- 无遗漏时明确说「无遗漏」

### Phase 4：综合报告（Reporter agent）

启动 Reporter agent，合成最终报告：

使用 Agent 工具启动，subagent_type="general-purpose"，description="Synthesize final review report"。

Prompt 要点：
- 综合 Context Brief + verified_findings + completeness_result
- 输出结构：
  1. 审查概要（模式、文件数、CodeGraph 状态）
  2. 发现清单（逐条 CONFIRMED/UNCERTAIN，含 Verifier 判定）
  3. 遗漏补充（Completeness Critic 新增）
  4. 统计摘要（按维度 x 严重度矩阵）
  5. 审查元数据（各阶段发现数、反驳数、新增数）

### --multi 最终输出

Reporter 产出完整 Markdown 报告为最终输出。主 Agent 在报告末尾追加元数据：

```markdown
---
## Multi-Agent Trace
- Mode: multi-agent
- Finder 1 (Correctness): {N} findings
- Finder 2 (Simplification): {N} findings
- Finder 3 (Efficiency): {N} findings
- Verifier: {N} confirmed, {N} refuted, {N} uncertain
- Completeness Critic: {N} additions
- Reporter: final synthesis
---
```

---

## 4. 标志

### --comment
将发现作为内联评论发布到对应的 PR/CR（适用时）。

### --fix
审查完成后，将高置信度的简化/复用/效率发现应用到工作树。正确性修复不自动应用。

### --multi
启用多智能体协作模式（3 路并行查找 -> 对抗验证 -> 完整性审查 -> 综合报告）。

---

## 5. 通用规则

- **不得**仅根据 diff 片段下结论 —— 必须读取完整函数上下文。
- **不得**在未检查调用方的情况下标记「可删除」。
- **必须**区分「确定是 bug」和「可能有问题」 —— 后者标记 `Confidence: low`。
- **必须**对每个发现给出具体修复建议。
- CodeGraph 可用但查询无结果时，回退到传统工具 —— 不跳过上下文收集。
- **多智能体模式**下，主 Agent 是编排者，不参与具体审查 —— 确保审查独立性。
