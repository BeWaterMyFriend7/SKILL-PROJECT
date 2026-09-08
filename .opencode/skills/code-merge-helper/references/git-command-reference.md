# Git 只读取证

先确认操作类型，再选择命令；缺失的操作引用不是空提交，也不是可以猜测的来源。
示例中的路径和提交必须替换为已核实值。文件路径含空格时按当前 shell 引号规则传参。

```text
git status --short --branch
git diff --name-only --diff-filter=U
git ls-files -u
git rev-parse HEAD
git rev-parse --verify MERGE_HEAD
git rev-parse --verify CHERRY_PICK_HEAD
git rev-parse --verify REBASE_HEAD
git rev-parse --git-path rebase-merge
git rev-parse --git-path rebase-apply
```

只读取当前存在的操作引用。linked worktree 中不要假设 .git 是目录；通过 --git-path 定位操作状态。
merge 的双方提交确认后用 `git merge-base --all <当前提交> <合入提交>`。
cherry-pick/rebase 用 `git show --no-patch --format=%H%n%P <正在应用的提交>` 确认提交及父提交；有多个父提交时核实 mainline，不能默认选第一个。

有冲突索引时按实际存在的 stage 读取：

```text
git show :1:path/to/file
git show :2:path/to/file
git show :3:path/to/file
git log --follow --date=iso -- path/to/file
git show <commit> -- path/to/file
git diff <实际基线> <对应侧提交> -- path/to/file
```

上述 stage 项是文件 blob；删除/新增冲突中部分 stage 可能不存在。提交历史辅助解释目的，blame、时间或作者不能单独证明目的。
重命名时核对每侧路径，不能假设三侧路径相同。

## 后续解决验证（报告中的执行要求）

`git diff --check` 和 `git diff --cached --check` 检查各自 diff，不足以证明全部文件没有冲突标记。
另检查本次解决文件中的标记，并排除文档示例或合法分隔符；不能只凭搜索命中认定错误。
编辑后尚未暂存时，未合并索引仍存在。只有在已获授权且精确暂存已审核文件后，才要求 `git ls-files -u` 为空。
继续 merge/rebase/cherry-pick 的条件和命令按当前操作与用户授权决定，不提供通用的 add/commit/push 序列。
