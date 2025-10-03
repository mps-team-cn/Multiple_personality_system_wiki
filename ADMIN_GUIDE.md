# Plurality Wiki 管理员操作指南

本指南为本仓库维护者与协作者提供基础操作流程，确保贡献内容能够有序合并并符合规范。
详细的内容约定与写作规范请参阅 **[CONTRIBUTING.md](./CONTRIBUTING.md)**。

---

## 1. 基本 GitHub 操作

### 1.1 克隆与同步仓库

```bash
# 克隆仓库
git clone https://github.com/kuliantnt/plurality_wiki.git

# 进入仓库目录
cd plurality_wiki

# 同步主分支
git checkout main
git pull origin main
```

### 1.2 新建分支

为每个功能或修复建立独立分支，分支命名遵循约定：

* `feat/xxx`：新增功能或词条
* `fix/xxx`：修复错误
* `docs/xxx`：文档更新
* `chore/xxx`：配置、脚本等维护

```bash
git checkout -b feat/new-entry
```

---

## 2. 提交规范

遵循 **Conventional Commits** 格式：

* `feat:` 新增条目或章节
* `fix:` 修复链接、格式等
* `docs:` 仅文档改动
* `chore:` 脚本、CI 或配置
* `style:` 空格、缩进等非语义改动

示例：

```bash
git add entries/诊断与临床/DID.md
git commit -m "feat: 新增解离性身份障碍（DID）条目"
```

---

## 3. Pull Request 使用流程

1. **推送分支**

   ```bash
   git push origin feat/new-entry
   ```

2. **在 GitHub 创建 PR**

   * 选择要合并到 `main` 的分支。
   * 填写 PR 模板，包括改动动机、主要变更、风险说明等。

3. **自检清单**

   * 所有断言均有引用，含 ICD/DSM 对照
   * 引用含版本与访问日期
   * “最后更新”字段已更新
   * Lint / CI 已通过

4. **代码评审**

   * 至少一位管理员或维护者进行 Review
   * 通过后合并至 `main`

---

## 4. 分支管理原则

* `main`：始终保持可发布、可访问状态
* 功能分支（`feat/*`、`fix/*`）：合并后删除，保持仓库整洁
* 长期维护分支（如 `dev`）：仅在大规模改动时使用

---

## 5. 常见任务

### 5.1 更新已有词条

* 在新分支修改条目
* 更新 `最后更新：YYYY-MM-DD`
* 同步修改 `index.md` 与 `README.md`

### 5.2 新增条目

* 复制 [TEMPLATE_ENTRY.md](./TEMPLATE_ENTRY.md)
* 按要求填写内容
* 放入对应目录（如 `entries/诊断与临床/`）

### 5.3 发布与日志

* 合并 PR 后，更新 `CHANGELOG.md`
* 使用标签（tag）标记版本号，例如：

  ```bash
  git tag v1.3.3
  git push origin v1.3.3
  ```

---

## 6. 审核要点（管理员）

管理员在合并前需重点检查：

* 是否符合 **贡献指南（CONTRIBUTING.md）**
* 引用与数据是否权威、完整
* 链接路径是否正确，索引是否同步
* CI / Lint 检查是否通过
