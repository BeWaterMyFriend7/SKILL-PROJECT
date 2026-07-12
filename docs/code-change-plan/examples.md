# code-change-plan 输出示例

## 调用方式

```
/code-change-plan

需求：实现用户登录功能
- 支持用户名/密码登录
- 登录成功后返回 JWT token
- token 有效期 7 天
```

---

## 输出文件

**文件名：** `.code/change-plans/新增用户登录功能-20260704-143052.md`

**文件内容：**

```markdown
# 代码变更方案：新增用户登录功能

**Plan ID:** CP-20260704-001  
**创建时间:** 2026-07-04 14:30:52  
**状态:** 等待审批  
**风险等级:** 中

---

## 1️⃣ 要做什么 (What)

### 需求
- [x] 支持用户名/密码登录
- [x] 登录成功返回 JWT token
- [x] Token 有效期 7 天
- [x] 登录失败返回明确错误信息

### 验收标准
- ✓ 正确的用户名密码可以登录成功，返回 200 + token
- ✓ 错误的密码返回 401 错误
- ✓ Token 包含用户 ID 和过期时间
- ✓ Token 可以用于访问受保护的接口

### 待决策问题
- [ ] Token 存储在 Cookie 还是返回 JSON 让前端自行存储？

---

## 2️⃣ 怎么做 (How)

### 技术方案
新增 `AuthService` 处理用户认证逻辑，使用 bcrypt 验证密码，使用 jsonwebtoken 生成 JWT。

### 关键决策
- **使用 JWT 而非 Session** → 原因：无状态，便于扩展，支持分布式部署
- **密码使用 bcrypt** → 原因：业界标准，安全性高，自动加盐
- **Token 存储在 HTTP-only Cookie** → 原因：防止 XSS 攻击，前端无法通过 JS 访问

### 流程对比
```
当前流程：无登录流程，所有接口都可直接访问

目标流程：
  用户输入账号密码 
    → AuthService.login() 验证 
    → 生成 JWT token 
    → 设置 HTTP-only Cookie 
    → 返回成功响应
  
  用户访问受保护 API 
    → AuthMiddleware 验证 token 
    → 通过则继续，失败则返回 401
```

---

## 3️⃣ 改哪些 (Where)

### 文件清单（只能改这些文件）

```
✏️ 修改
  - package.json (添加 bcrypt, jsonwebtoken 依赖)
  - src/routes/index.ts (注册登录路由)
  - src/app.ts (应用认证中间件到需要保护的路由)
  - .env.example (添加 JWT_SECRET 配置说明)

➕ 新增
  - src/services/auth.service.ts (认证服务)
  - src/routes/auth.routes.ts (登录路由)
  - src/middlewares/auth.middleware.ts (JWT 验证中间件)
  - tests/auth.test.ts (登录功能测试)

❌ 删除
  - (无)
```

### 影响范围
- **用户服务** - 影响程度：中 - 需要添加密码验证方法
- **API 路由** - 影响程度：低 - 需要保护的接口添加中间件
- **配置管理** - 影响程度：低 - 添加 JWT 密钥配置

---

## 4️⃣ 如何验证 (Verify)

### 验证步骤
```bash
# 1. 安装依赖
npm install

# 2. 编译检查
npm run build

# 3. 单元测试
npm test

# 4. 手动验证 - 登录成功
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'
# 期望结果：200 + Set-Cookie: token=xxx

# 5. 手动验证 - 登录失败
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
# 期望结果：401 + {"error": "Invalid credentials"}

# 6. 手动验证 - 访问受保护接口
curl http://localhost:3000/api/profile \
  -H "Cookie: token=<从步骤4获取的token>"
# 期望结果：200 + 用户信息
```

### 验证清单
- [ ] 编译无错误
- [ ] 正确密码登录成功
- [ ] 错误密码登录失败
- [ ] Token 可以验证通过
- [ ] Token 过期后验证失败
- [ ] 单元测试全部通过

### 风险与回滚

**风险：**
- ⚠️ **中风险：** JWT 密钥泄露会导致 token 可被伪造 → 缓解：密钥存储在环境变量，不提交到 git
- ⚠️ **中风险：** Token 无法主动撤销（JWT 特性） → 缓解：设置较短的有效期（7天），后续可引入黑名单机制
- ✅ **低风险：** 密码加密算法选择不当 → 缓解：使用 bcrypt（业界标准）

**回滚方案：**
```bash
# 如果已经 commit
git revert <commit-sha>

# 如果还没 commit
git checkout .
git clean -fd
```

---

## ✅ 审批

**状态:** WAITING_FOR_APPROVAL

**待处理事项：**
- [ ] 确认 Token 存储方式（Cookie vs JSON）
- [ ] 确认 JWT_SECRET 是否已在服务器环境配置

**审批通过后执行：**
```
读取并执行以下代码变更方案：
.code/change-plans/新增用户登录功能-20260704-143052.md

要求：
1. 按文件清单修改代码
2. 每步完成后运行对应验证
3. 发现问题立即停止
4. 验证全部通过后报告完成
```

---

**方案结束**
```

---

## 控制台输出

```
✓ 代码变更方案已生成

【需求】新增用户登录功能
【方案】添加 AuthService + JWT 认证
【影响】8 个文件（新增 4，修改 4）
【风险】中等（JWT 密钥管理）
【状态】等待审批

文件：.code/change-plans/新增用户登录功能-20260704-143052.md

请审核方案后执行。
```
