# code-merge-helper 输出示例

## 调用方式

~~~text
/code-merge-helper

分析当前 merge 冲突，生成报告，不修改代码或 Git 状态。
~~~

**场景：** 将 `feature/login` 合并到 `main`。

## 输出文件

`.code/merge-review/合并feature-login到main-20260824-150230.md`

~~~markdown
# Git 冲突解决方案

**状态：** WAITING_FOR_APPROVAL
**操作：** feature/login@e4f5g6h → main@a1b2c3d　**冲突：** 3　**风险：** 高

## 合并结论

合并后同时保留用户查询缓存和敏感字段过滤，并采用 feature 侧新增的登录路由。依赖需要合并，但 Redis 版本取决于生产 Node.js 版本，确认前不能处理依赖文件。

**需要决定：**

- 确认生产环境 Node.js 版本，以选择兼容的 Redis 版本。

## 关键冲突

| 功能/文件 | 冲突点 | 合并结果 | 风险或决策 |
|---|---|---|---|
| 用户查询 | main 增加缓存；feature 过滤密码 | 缓存只保存已过滤对象，读取旧缓存时再次过滤 | 高：旧缓存可能包含密码 |
| 登录路由 | main 保持原路由；feature 新增登录入口 | 保留登录入口并维持原路由顺序 | 低 |
| 依赖 | main 增加 Redis；feature 增加认证依赖 | 合并依赖 | 高：需要确认 Node.js 版本 |

---

## AI 冲突执行信息

### Git 依据

- **当前侧：** main（stage-2：`a1b2c3d`）
- **合入侧：** feature/login（stage-3：`e4f5g6h`）
- **共同基线：** `91ab234`
- `a1b2c3d` 引入 Redis 缓存；`e4f5g6h` 引入字段过滤和认证依赖。

### 文件解决动作

| 文件/位置 | 解决动作 | 必须保留 | 完成检查 |
|---|---|---|---|
| `src/services/user.service.ts:findById` | 过滤敏感字段后写缓存；读取旧缓存时再次过滤 | 缓存命中能力和所有返回路径不暴露密码 | 命中、未命中和旧缓存均无密码字段 |
| `src/routes/api.ts:router` | 保留登录路由并维持原顺序 | 现有路由行为 | 路由测试通过 |
| `package.json:dependencies` | 确认 Node.js 后合并三项依赖 | 两侧功能依赖和运行时兼容范围 | 安装、依赖树和构建通过 |

### 合并验证

| 验证对象 | 验证方式和预期结果 |
|---|---|
| main 缓存行为 | 缓存命中和未命中测试均通过 |
| feature 安全行为 | 密码过滤和登录路由测试通过 |
| 组合行为 | 预置含密码的旧缓存后查询，结果无密码且缓存可更新 |
| Git 状态 | `git diff --check` 和未合并索引检查均无问题 |

### 停止条件

- 生产 Node.js 版本尚未确认。
- stage 来源变化或出现报告之外的新冲突。
- 旧缓存兼容无法在不扩大范围的情况下解决。
- 任一单侧或组合行为验证失败。

### 恢复方式

当前仍在 merge 冲突处理中且尚未提交，可使用 `git merge --abort`。
~~~

## 控制台输出

~~~text
合并：同时保留缓存、密码过滤和登录路由；依赖版本待确认
冲突：3
风险：高
待决策：生产 Node.js 版本
状态：WAITING_FOR_APPROVAL
文件：.code/merge-review/合并feature-login到main-20260824-150230.md
~~~
