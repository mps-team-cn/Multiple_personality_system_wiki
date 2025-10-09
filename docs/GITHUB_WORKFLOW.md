# GitHub 提交流程指南（GITHUB_WORKFLOW.md）

本指南面向 **Multiple Personality System Wiki** 的贡献者，介绍如何通过 GitHub 提交内容。
推荐流程： **Fork 仓库 → 新建分支 → 修改提交 → Pull Request (PR)** 。

---

## 1. Fork 仓库

1. 打开主仓库：[Multiple Personality System Wiki](https://github.com/mps-team-cn/plurality_wiki)
2. 点击右上角 **Fork** 按钮，创建属于自己的副本。

   - Fork 后地址示例：

     ```text
     [https://github.com/你的用户名/plurality_wiki](https://github.com/你的用户名/plurality_wiki)
     ```

---

## 2. 克隆到本地

```bash

# 克隆自己 Fork 的仓库

git clone https://github.com/你的用户名/plurality_wiki.git

# 进入仓库目录

cd plurality_wiki
```

---

## 3. 新建分支

不要在 `main` 直接修改，请为每次修改新建分支。

分支命名规则：

- `feat/xxx`：新增条目或功能
- `fix/xxx`：修复问题
- `docs/xxx`：文档更新

示例：

```bash
git checkout -b feat/add-did-entry
```

---

## 4. 修改内容并提交

1. 修改或新增文件（必须放在 `entries/` 目录下）。
2. 保存后执行：

```bash
git add .
git commit -m "feat: 新增解离性身份障碍（DID）条目"
```

> 提交信息必须遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

---

## 5. 推送到自己的仓库

```bash
git push origin feat/add-did-entry
```

---

## 6. 发起 Pull Request (PR)

1. 打开你 Fork 的仓库页面（GitHub 网页端）。
2. 点击 **Compare & Pull Request** 。
3. 设置目标分支：

   - **base repository** : `mps-team-cn/plurality_wiki`
   - **base branch** : `main`

4. 填写 PR 模板，说明修改内容。
5. 提交后等待管理员审核。

---

## 7. 审核与合并

- 管理员会进行 **Review** ，检查引用、格式、Lint 等。
- 通过后，PR 会合并到主仓库。
- 如有问题，管理员会在 PR 下留言，贡献者可继续修改。

---

## 8. 同步上游更新（可选）

如果主仓库更新，需要将改动同步到自己 Fork：

```bash

# 添加上游仓库

git remote add upstream https://github.com/mps-team-cn/plurality_wiki.git

# 获取更新

git fetch upstream

# 合并到本地 main

git checkout main
git merge upstream/main

# 推送到自己的 fork

git push origin main
```

---

## 9. 提交流程图

```text
Fork → Clone → 新建分支 → 修改 & 提交 → Push → Pull Request → 审核合并
```
