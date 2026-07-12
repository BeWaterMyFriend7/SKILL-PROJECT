# Git 只读分析命令参考

以下命令用于收集证据，执行前仍需结合仓库状态判断。

```bash
# 当前状态和未合并文件
git status --short --branch
git diff --name-only --diff-filter=U
git ls-files -u

# 查看冲突三阶段内容
git show :1:path/to/file   # common-base
git show :2:path/to/file   # stage-2
git show :3:path/to/file   # stage-3

# 合并相关提交
cat "$(git rev-parse --git-path MERGE_HEAD)"
git merge-base HEAD MERGE_HEAD

# 文件历史与提交内容
git log --follow --date=iso -- path/to/file
git show --stat --summary <sha>
git show <sha> -- path/to/file
git blame <revision> -- path/to/file

# 比较两侧相对基线的变化
git diff <base>..<side-a> -- path/to/file
git diff <base>..<side-b> -- path/to/file

# 解决后检查
git diff --check
git diff --cached --check
git diff --name-only --diff-filter=U
```

## 注意

- rebase 中 `ours/theirs` 的直觉含义容易与分支名称相反，因此报告使用 stage 编号和实际提交来源。
- `git blame` 只能说明最后修改行的提交，不能单独证明业务目的。
- `git log --follow` 对复杂重命名和拆分并不总是完整，应结合符号搜索和提交 diff。
