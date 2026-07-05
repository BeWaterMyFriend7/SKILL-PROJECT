# code-merge-helper

代码合并助手 - 分析 Git 冲突，追溯改动原因，提供合并方案。

**支持平台：** OpenCode、Codex、Cursor、Aider 等兼容 Agent Skills 规范的 AI 编程工具。

**系统要求：**
- Git 2.0+
- Python 3.7+ （验证脚本，无第三方依赖）

## 核心原则

**只分析 → 不改代码 → 等待审批**

## 一、快速开始

### 调用方式

**OpenCode / Cursor / Aider:**
```text
/code-merge-helper

分析当前冲突，生成报告，不修改代码。
```

**Codex:**
```text
$code-merge-helper

分析当前冲突，生成报告，不修改代码。
```

分析阶段始终以 `WAITING_FOR_APPROVAL` 结束。批准后按报告操作步骤执行。

### 输出位置

```text
.code/merge-review/合并<source>到<target>-<YYYYMMDD-HHMMSS>.md
```

## 二、报告结构（5 章简洁版）

```
Git 合并冲突分析报告
├── 1️⃣ 冲突概览
│   └── 所有冲突索引表（文件、类型、风险、方案）
│
├── 2️⃣ 冲突分析（核心）
│   ├── C-01: 文件路径
│   │   ├── 发生了什么？（三方对比）
│   │   ├── 推荐方案（含代码）
│   │   └── 理由
│   └── C-02: ...
│
├── 3️⃣ 操作步骤
│   └── 可执行的 bash 命令序列
│
├── 4️⃣ 验证清单
│   └── Checkbox 验证列表
│
└── 5️⃣ 风险与回滚
    ├── 风险评估
    └── 回滚命令
```

**特点：**
- 📄 **5-8 页** - 简洁易读
- ⏱️ **5 分钟** - 快速审批
- ✅ **直观** - Emoji + 风险标记
- 🎯 **实用** - 直接可执行

## 三、核心流程

```
1. 识别冲突
   - 哪些文件冲突了？
   - 冲突点是什么？

2. 追溯原因
   - 两边为什么改？
   - 改动的目的是什么？

3. 评估方案
   - 保留谁的改动？
   - 能否合并两边？

4. 分析影响
   - 会影响哪些功能？
   - 需要什么验证？

5. 输出报告
   - 文件：.code/merge-review/合并分析-YYYYMMDD-HHMMSS.md
   - 状态：等待审批
```

## 四、安装

### OpenCode
```text
# 全局
~/.config/opencode/skills/code-merge-helper/

# 项目级
<project>/.opencode/skills/code-merge-helper/
```

### Codex
```text
~/.codex/skills/code-merge-helper/
```

### 通用 Agent Skills
```text
<repo>/.agents/skills/code-merge-helper/
```

## 五、与其他 Skill 的协作

- **code-change-plan**：当合并涉及大规模重构或新功能引入时，建议先用 `code-change-plan` 生成变更方案，再在合并分析报告中引用该方案的 plan-id。
- 如果在执行 code-change-plan 过程中发现需要先解决合并冲突，应暂停并建议使用本 Skill 完成三方合并分析。

## 六、目录结构

```text
code-merge-helper/
├── SKILL.md                         # 核心执行规范
├── README.md                        # 本文件
├── requirements.txt                 # Python 依赖（仅标准库）
├── assets/
│   ├── merge-resolution-report.md  # 简洁报告模板
│   └── plan-amendment.md           # 修订模板
├── references/
│   ├── analysis-rules.md           # 分析规则
│   ├── git-command-reference.md    # Git 命令参考
│   └── verification-matrix.md      # 验证矩阵
├── evals/
│   └── scenarios.md                # 测试场景
└── scripts/
    ├── validate_merge_plan.py      # 方案验证脚本
    └── write_utf8.py               # UTF-8 文件写入工具

Python 要求：Python 3.7+ （无第三方依赖）
```

## 七、自检

```bash
python scripts/run_evals.py
```

检查：文件完整性、Schema 合法性、脚本语法、模板完整性、参考文档覆盖。
