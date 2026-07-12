# code-change-plan

代码变更分析及计划 Skill - 将需求转换为可执行的代码变更方案。

**支持平台：** OpenCode、Codex、Cursor、Aider 等兼容 Agent Skills 规范的 AI 编程工具。

## 核心原则

**先分析 → 再设计 → 产出方案 → 等待审批**

只负责生成变更方案，不修改业务代码。

## 一、快速开始

### 调用方式

**OpenCode / Cursor / Aider:**
```text
/code-change-plan

需求：实现用户登录功能
- 支持用户名密码登录
- 返回 JWT token
```

**Codex:**
```text
$code-change-plan

需求：实现用户登录功能
- 支持用户名密码登录
- 返回 JWT token
```

### 输出位置

```text
.code/change-plans/<需求描述>-<YYYYMMDD-HHMMSS>.md
```

## 二、报告结构（4 章简洁版）

```
代码变更方案
├── 1️⃣ 要做什么 (What)
│   ├── 需求列表 (checkbox)
│   ├── 验收标准
│   └── 待决策问题
│
├── 2️⃣ 怎么做 (How)
│   ├── 技术方案
│   ├── 关键决策
│   └── 流程对比
│
├── 3️⃣ 改哪些 (Where)
│   ├── 文件清单（白名单）
│   └── 影响范围
│
└── 4️⃣ 如何验证 (Verify)
    ├── 验证步骤
    ├── 验证清单
    └── 风险与回滚
```

**特点：**
- 📄 **3-5 页** - 简洁易读
- ⏱️ **3 分钟** - 快速审批
- ✅ **直观** - Emoji + Checkbox
- 🎯 **实用** - 直接可执行

## 三、执行方式

人工审核方案后，将状态改为 `APPROVED`，然后新建 AI 助手会话：

```text
读取并执行以下代码变更方案：
.code/change-plans/<plan-id>.md

要求：
1. 按文件清单修改代码
2. 每步完成后运行对应验证
3. 发现问题立即停止
4. 验证全部通过后报告完成
```

## 四、目录结构

```text
code-change-plan/
├── SKILL.md                         # 核心执行规范
├── README.md                        # 本文件
├── requirements.txt                 # Python 依赖（仅标准库）
├── assets/
│   ├── change-plan-template.md     # 简洁方案模板
│   └── change-plan-amendment.md    # 修订模板
├── references/
│   ├── workflow-detail.md          # 详细工作流程
│   ├── report-structure.md         # 报告结构说明
│   └── quality-checklist.md        # 质量检查清单
└── scripts/
    ├── validate_change_plan.py     # 方案验证脚本
    ├── check_utf8.py               # UTF-8 编码检查
    └── write_utf8.py               # UTF-8 文件写入工具

Python 要求：Python 3.7+ （无第三方依赖）
```

## 五、安装

### OpenCode
```text
# 全局
~/.config/opencode/skills/code-change-plan/

# 项目级
<project>/.opencode/skills/code-change-plan/
```

### Codex
```text
~/.codex/skills/code-change-plan/
```

### 通用 Agent Skills
```text
<repo>/.agents/skills/code-change-plan/
```

## 六、与其他 Skill 的协作

- **code-merge-helper**：当变更涉及分支合并且存在冲突时，建议暂停本方案执行，先使用 `code-merge-helper` 完成三方合并分析。合并完成后再回到本方案继续执行。

## 七、Windows 环境注意

- 本 Skill 所有 `.md` 文件均为 UTF-8 编码
- 若在 PowerShell 中用 `Get-Content` 读到乱码，改用 `[System.IO.File]::ReadAllText("<path>", [System.Text.Encoding]::UTF8)`
- Skill 仅生成方案，不修改业务代码

## 八、自检

```bash
python scripts/validate_change_plan.py
```

检查方案文件的完整性和结构合法性。
