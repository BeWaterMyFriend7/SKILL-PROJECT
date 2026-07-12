# code-merge-helper 输出示例

## 调用方式

```
/code-merge-helper

分析当前 merge 冲突，生成报告，不修改代码。
```

**场景：** 将 `feature/login` 分支合并到 `main` 时出现冲突

---

## 输出文件

**文件名：** `.code/merge-review/合并feature-login到main-20260704-150230.md`

**文件内容：**

```markdown
# Git 合并冲突分析报告

**Plan ID:** MG-20260704-001  
**创建时间:** 2026-07-04 15:02:30  
**操作:** feature/login → main  
**冲突文件数:** 3  
**高风险冲突:** 1  
**状态:** 等待审批

---

## 1️⃣ 冲突概览

| 文件 | 类型 | 风险 | 推荐方案 |
|------|------|------|---------|
| src/services/user.service.ts | 逻辑冲突 | ⚠️ 中 | 语义融合 |
| src/routes/api.ts | 文本冲突 | ✅ 低 | 保留 feature 侧 |
| **package.json** | **依赖冲突** | **🔴 高** | **需人工决策** |

**说明：**
- **stage-2:** 当前分支（main）
- **stage-3:** 合入分支（feature/login）
- **common-base:** 共同祖先（commit a1b2c3d）

---

## 2️⃣ 冲突分析

### 🔸 C-01: src/services/user.service.ts（中风险）

**发生了什么？**
- **stage-2 (main):** 张三在 7月1日 添加了 Redis 缓存逻辑（提交 `a1b2c3d`）→ 目的：优化查询性能
- **stage-3 (feature/login):** 李四在 7月3日 添加了密码字段过滤（提交 `e4f5g6h`）→ 目的：安全加固，防止密码泄露
- **common-base:** 简单的数据库查询，无缓存，无字段过滤

**推荐方案：语义融合（保留两边改动）**
```typescript
async findById(id: string): Promise<User> {
  // 1. 先查缓存（来自 main）
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  
  // 2. 查询数据库
  const user = await db.users.findOne({ id });
  if (!user) return null;
  
  // 3. 过滤敏感字段（来自 feature/login）✅ 新增
  delete user.password;
  delete user.passwordHash;
  
  // 4. 写入缓存（来自 main）
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);
  
  return user;
}
```

**理由：** 两个改动互不冲突，缓存优化和安全加固都应该保留，只需确保缓存前先过滤敏感字段。

---

### 🔸 C-02: src/routes/api.ts（低风险）

**发生了什么？**
- **stage-2 (main):** 无修改
- **stage-3 (feature/login):** 添加了 `/auth/login` 路由
- **common-base:** 原有路由定义

**推荐方案：保留 feature 侧**
```typescript
// 保留 feature/login 分支的新增路由
router.post('/auth/login', authController.login);
```

**理由：** 新增路由，不影响现有功能，直接保留即可。

---

### 🔸 C-03: package.json（高风险）🔴

**发生了什么？**
- **stage-2 (main):** 添加 `redis@4.5.0` 依赖（用于缓存）
- **stage-3 (feature/login):** 添加 `jsonwebtoken@9.0.2` 和 `bcrypt@5.1.1` 依赖（用于认证）
- **common-base:** 无这些依赖

**❓ 需要人工决策：**
> Redis 版本选择 4.5.0 还是 4.6.0？
> - 选项 A: redis@4.5.0 → 稳定版，兼容 Node.js 16+
> - 选项 B: redis@4.6.0 → 最新版，支持新特性，但要求 Node.js 18+

**推荐方案：** 合并所有依赖，Redis 版本根据 Node.js 版本确定
```json
{
  "dependencies": {
    "redis": "4.5.0",
    "jsonwebtoken": "9.0.2",
    "bcrypt": "5.1.1"
  }
}
```

**理由：** 三个依赖互不冲突，都应保留。Redis 版本建议使用 4.5.0（如果 Node.js >= 18 可升级到 4.6.0）。

---

## 3️⃣ 操作步骤

```bash
# 1. 确认 Git 状态
git status --short

# 2. 解决冲突（按上述方案编辑文件）
# - 编辑 src/services/user.service.ts（按 C-01 方案语义融合）
# - 编辑 src/routes/api.ts（按 C-02 方案保留 feature 侧）
# - 编辑 package.json（按 C-03 方案合并依赖，确认 Redis 版本）

# 3. 安装依赖
npm install

# 4. 验证编译
npm run build

# 5. 运行测试
npm test

# 6. 检查冲突标记已清除
git diff --check

# 7. 完成合并
git add .
git commit -m "合并 feature/login 到 main

- 语义融合 user.service.ts（缓存 + 密码过滤）
- 新增登录路由
- 合并依赖：redis, jsonwebtoken, bcrypt
"
```

---

## 4️⃣ 验证清单

- [ ] 所有冲突文件已按方案编辑
- [ ] 冲突标记（`<<<<<<<`, `=======`, `>>>>>>>`）已全部清除
- [ ] 依赖安装成功（npm install）
- [ ] 编译无错误（npm run build）
- [ ] 单元测试通过（npm test）
- [ ] 用户查询功能正常（包含缓存逻辑）
- [ ] 密码字段被正确过滤
- [ ] 登录接口可用（/auth/login）
- [ ] Redis 连接正常

---

## 5️⃣ 风险与回滚

### 风险
- 🔴 **高风险：** Redis 版本不兼容可能导致启动失败 → 缓解：先在开发环境验证，确认 Node.js 版本兼容性
- ⚠️ **中风险：** 缓存 + 密码过滤的组合逻辑未经充分测试 → 缓解：重点测试 user.service.ts 的 findById 方法
- ⚠️ **中风险：** 缓存中可能已存在包含密码的旧数据 → 缓解：合并后清空 Redis 缓存（`redis-cli FLUSHDB`）
- ✅ **低风险：** 新增登录路由不影响现有功能 → 缓解：确保路由路径无冲突

### 回滚方案
```bash
# 如果还在合并过程中（未 commit）
git merge --abort
npm install  # 恢复 package.json

# 如果已经 commit（未 push）
git reset --hard HEAD~1
npm install

# 如果已经 push
git revert HEAD
git push
```

---

## ✅ 审批

**状态:** WAITING_FOR_APPROVAL

**待决策问题：**
- [ ] 确认 Node.js 版本（决定 Redis 版本选择 4.5.0 vs 4.6.0）
- [ ] 确认是否需要在合并后清空 Redis 缓存

**审批通过后执行：**
按照第 3 章"操作步骤"执行合并。

---

**报告结束**
```

---

## 控制台输出

```
✓ 合并冲突分析报告已生成

【操作】将 feature/login 合并到 main
【冲突】3 个文件（高风险 1 个）
【方案】语义融合（保留两边改动）
【决策】Redis 版本需确认（4.5.0 vs 4.6.0）
【状态】等待审批

文件：.code/merge-review/合并feature-login到main-20260704-150230.md

请审核报告后按操作步骤执行。
```
