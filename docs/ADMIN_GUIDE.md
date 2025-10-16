# 🧭 Multiple Personality System Wiki 管理员操作指南

本指南专为 **Multiple Personality System Wiki** 的管理员与维护者设计，涵盖分支管理、PR 审核、版本发布、CMS 管理等专属操作流程。

!!! info "面向对象"
    本文档面向拥有仓库写入权限的管理员。普通贡献者请参阅 [贡献指南](contributing/index.md)。

!!! tip "相关文档"

    - [贡献指南](contributing/index.md) - 通用贡献流程
    - [PR 提交流程](contributing/pr-workflow.md) - 详细提交步骤
    - [AGENTS.md](../AGENTS.md) - 项目开发约定
    - [工具文档](tools/README.md) - 自动化工具说明

---

## 📋 快速导航

1. [分支与版本管理](#1-分支与版本管理)
2. [PR 审核要点](#2-pr-审核要点)
3. [版本发布流程](#3-版本发布流程)
4. [Sveltia CMS 管理](#4-sveltia-cms-管理)
5. [自动化维护工具](#5-自动化维护工具)
6. [CI/CD 监控](#6-cicd-监控)
7. [应急处理](#7-应急处理)

---

## 1️⃣ 分支与版本管理

### 1.1 分支策略

| 分支类型               | 用途         | 管理权限 | 说明                       |
| ------------------ | ---------- | ---- | ------------------------ |
| `main`             | 生产环境稳定版本   | 管理员  | 受保护分支，CI 通过后才可合并         |
| `dev`              | 开发集成分支     | 管理员  | 可选，用于大型功能测试             |
| `feat/*`           | 功能开发分支     | 所有人  | 合并后自动删除                  |
| `fix/*`            | Bug 修复分支   | 所有人  | 合并后自动删除                  |
| `docs/*`           | 文档更新分支     | 所有人  | 合并后自动删除                  |
| `chore/*`          | 工具/配置维护分支  | 管理员  | 合并后自动删除                  |
| `hotfix/*`         | 紧急修复分支     | 管理员  | 直接基于 main 创建，优先处理        |

### 1.2 分支保护规则

`main` 分支保护设置：

- ✅ 需要 PR 审核才能合并
- ✅ 需要至少 1 位管理员批准
- ✅ 需要 CI 通过
- ✅ 需要分支与 main 保持最新
- ✅ 禁止强制推送
- ✅ 禁止删除分支

### 1.3 合并后清理

管理员职责：

```bash

# 合并 PR 后删除远程分支

git push origin --delete feat/branch-name

# 本地清理

git fetch -p
git branch -d feat/branch-name
```

!!! tip "自动化建议"
    可在 GitHub 仓库设置中启用"合并后自动删除分支"选项。

---

## 2️⃣ PR 审核要点

### 2.1 审核检查清单

合并前必须确认以下所有项：

#### 📚 内容质量

- [ ] 所有断言均有可靠引用
- [ ] 病理学内容包含 ICD-11 与 DSM-5-TR 双重引用
- [ ] 引用格式正确（来源、版本、日期）
- [ ] 原文摘录 ≤25 词 + 中文翻译
- [ ] 无明显事实错误或误导性内容

#### 🔗 结构与链接

- [ ] 文件路径符合项目规范（词条在 `docs/entries/`）
- [ ] 内部链接使用相对路径
- [ ] 所有链接可访问（无 404）
- [ ] Frontmatter 完整（title、tags、updated、topic）
- [ ] 相关 Guide 已同步更新（见 [AGENTS.md](../AGENTS.md#13-索引与链接规范)）

#### 🧹 格式规范

- [ ] `python tools/fix_markdown.py` 已执行
- [ ] `markdownlint` 检查通过
- [ ] `mkdocs build --strict` 构建成功
- [ ] CI/CD 全部通过

#### 📝 提交规范

- [ ] Commit 信息符合 Conventional Commits
- [ ] PR 描述完整（动机、变更、影响、测试）
- [ ] 关联相关 Issue（如有）

### 2.2 常见问题处理

| 问题类型     | 处理方式                                  |
| -------- | ------------------------------------- |
| 链接错误     | 要求贡献者修正相对路径                           |
| 格式问题     | 运行 `fix_markdown.py` 后提交                |
| 引用缺失     | 要求补充引用或标注来源                           |
| Frontmatter 不完整 | 要求补全必需字段                              |
| CI 失败    | 查看日志，指导贡献者修复                          |
| 冲突       | 要求贡献者 rebase main 分支                  |

### 2.3 审核评论模板

```markdown

## 审核意见

感谢您的贡献！以下是需要调整的地方：

### ✅ 已通过检查

- 内容质量良好
- 引用格式规范

### ⚠️ 需要修改

1. **链接问题**：[line 42] 请使用相对路径 `../entries/DID.md`
2. **格式问题**：请运行 `python tools/fix_markdown.py` 修复格式
3. **引用缺失**：[line 88] 请补充 ICD-11 引用

### 📝 建议改进（可选）

- 建议补充相关词条的交叉引用

请修改后重新提交，感谢配合！
```

---

## 3️⃣ 版本发布流程

### 3.1 发布前准备

!!! danger "发布前必须执行"

    1. 核对 `docs/changelog.md` 内容完整性
    2. 确认 `docs/index.md` 版本号正确
    3. 运行完整构建测试
    4. 确保 main 分支最新

### 3.2 版本号规范

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

| 版本号          | 说明                    | 示例          |
| ------------ | --------------------- | ----------- |
| `MAJOR.x.x`  | 不兼容的 API 修改            | `2.0.0`     |
| `x.MINOR.x`  | 向后兼容的功能新增             | `1.3.0`     |
| `x.x.PATCH`  | 向后兼容的 Bug 修复          | `1.2.1`     |
| `x.x.x-beta` | 预发布版本                 | `1.3.0-beta.1` |

### 3.3 发布步骤

#### Step 1: 更新 Changelog

```bash

# 自动生成 changelog（从最新标签到当前）

python tools/gen_changelog_by_tags.py --latest-to-head

# 手动编辑 docs/changelog.md，确认：

# - 版本号正确

# - 日期准确

# - 变更分类清晰（feat/fix/docs/chore）

# - 重要变更已高亮

```

#### Step 2: 创建 Git 标签

```bash

# 创建标签

git tag v1.4.0 -m "Release v1.4.0"

# 推送标签

git push origin v1.4.0
```

#### Step 3: 发布 GitHub Release

使用 GitHub CLI（推荐）：

```bash

# 创建新 Release

gh release create v1.4.0 \
  --title "v1.4.0 - 标题" \
  --notes-file docs/changelog.md

# 或编辑现有 Release

gh release edit v1.4.0 \
  --notes-file docs/changelog.md
```

或在 GitHub 网页端操作：

1. 访问 <https://github.com/mps-team-cn/Multiple_Personality_System_wiki/releases/new>
2. 选择标签 `v1.4.0`
3. 复制 `docs/changelog.md` 对应版本内容到 Release Notes
4. 点击 "Publish release"

#### Step 4: 验证发布

- [ ] GitHub Release 页面显示正常
- [ ] Cloudflare Pages 自动部署成功
- [ ] 线上版本号正确
- [ ] 主要功能正常工作

### 3.4 回滚操作

如需回滚发布：

```bash

# 删除远程标签

git push --delete origin v1.4.0

# 删除本地标签

git tag -d v1.4.0

# 删除 GitHub Release（网页端操作）

```

---

## 4️⃣ Sveltia CMS 管理

### 4.1 访问权限管理

#### 在线 CMS

- **URL**: <https://wiki.mpsteam.cn/admin/>
- **认证**: GitHub OAuth
- **权限**: 需要仓库 Collaborator 权限

#### 添加协作者

1. 访问 <https://github.com/mps-team-cn/Multiple_Personality_System_wiki/settings/access>
2. 点击 "Add people"
3. 输入 GitHub 用户名
4. 选择权限级别（建议：Write）

### 4.2 CMS 配置文件

配置文件位置：`docs/admin/config.yml`

关键配置项：

```yaml
backend:
  name: github
  repo: mps-team-cn/Multiple_Personality_System_wiki
  branch: main

media_folder: "docs/assets/images"
public_folder: "../assets/images"

collections:

  - name: "entries"

    label: "词条"
    folder: "docs/entries"
    # ... 其他配置
```

!!! warning "修改配置后需要"

    - 测试 CMS 功能正常
    - 确认词条保存路径正确
    - 验证 Frontmatter 格式符合 MkDocs 要求

### 4.3 CMS 使用指南

详细使用方法请参阅：

- [Sveltia CMS 本地开发指南](dev/LOCAL_DEV_SERVER.md)
- [CMS 配置说明](https://github.com/sveltia/sveltia-cms#readme)

### 4.4 主题分类管理

当前 7 个主题分类：

| 分类      | 对应 Guide 文件                         | 词条数（参考） |
| ------- | ----------------------------------- | ------- |
| 理论与分类   | `Theory-Classification-Guide.md`    | ~22     |
| 诊断与临床   | `Clinical-Diagnosis-Guide.md`       | ~31     |
| 系统运作    | `System-Operations-Guide.md`        | ~48     |
| 角色与身份   | `Roles-Identity-Guide.md`           | ~30     |
| 文化与表现   | `Cultural-Media-Guide.md`           | ~17     |
| 创伤与疗愈   | `Trauma-Healing-Guide.md`           | ~5      |
| 实践指南    | `Practice-Guide.md`                 | ~5      |

!!! tip "维护提醒"
    新增词条时，务必同步更新对应的 Guide 文件。

---

## 5️⃣ 自动化维护工具

### 5.1 一键本地维护脚本

**Windows 批处理脚本**：

```bash
tools\run_local_updates.bat
```

等效操作：

```bash

# 1. 生成 changelog

python tools/gen_changelog_by_tags.py --latest-to-head

# 2. 导出 PDF（可选）

python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"

# 3. 修复 Markdown 格式

python tools/fix_markdown.py

# 4. Lint 检查

markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
```

!!! note "关于标签索引"
    MkDocs Material 的 `tags` 插件会自动生成标签索引页面，无需手动维护 `tags.md`。

### 5.2 格式化工具

#### Markdown 自动修复

```bash

# 修复所有文件

python tools/fix_markdown.py

# 查看修复预览（不实际修改）

python tools/fix_markdown.py --dry-run

# 修复特定文件

python tools/fix_markdown.py docs/entries/DID.md
```

**修复内容**：

- 加粗链接格式
- 列表项空格
- 链接括号格式
- 冒号格式
- 多余空行

#### Markdownlint 检查

```bash

# 检查所有文档

markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "site"

# 检查并自动修复

markdownlint "docs/**/*.md" --fix
```

### 5.3 构建与预览

```bash

# 本地预览（支持热重载）

mkdocs serve

# 严格模式构建（有警告即失败）

mkdocs build --strict

# 普通构建

mkdocs build
```

### 5.4 PDF 导出

```bash

# 使用 tectonic 引擎导出 PDF

python tools/pdf_export/export_to_pdf.py \
  --pdf-engine=tectonic \
  --cjk-font="Microsoft YaHei"
```

详见 [工具文档](tools/README.md#pdf-导出工具)。

---

## 6️⃣ CI/CD 监控

### 6.1 GitHub Actions 工作流

主要 CI 流程：

| 工作流文件                      | 触发条件                   | 主要任务                 |
| -------------------------- | ---------------------- | -------------------- |
| `markdown_format.yml`      | push / PR              | Markdown 格式检查        |
| `build.yml`                | push / PR              | MkDocs 构建测试          |
| `deploy.yml`               | push to main           | 部署到 Cloudflare Pages |
| `release.yml`              | 新标签推送                  | 创建 GitHub Release    |

### 6.2 Cloudflare Pages 部署

**部署配置**：

- **构建命令**: `bash .cfpages-build.sh`
- **构建输出目录**: `site`
- **环境变量**: 见 Cloudflare Pages 控制台

**监控地址**：

- **生产环境**: <https://wiki.mpsteam.cn>
- **预览部署**: 每个 PR 都会生成预览链接

### 6.3 CI 失败处理

| 失败类型         | 常见原因             | 解决方法                      |
| ------------ | ---------------- | ------------------------- |
| Markdown Lint | 格式不符合规范          | 运行 `fix_markdown.py` 修复    |
| Build Failed | 链接失效/Frontmatter 错误 | 检查错误日志，修复对应问题             |
| Deploy Failed | Cloudflare 配置问题    | 检查构建脚本与 Cloudflare Pages 配置 |

---

## 7️⃣ 应急处理

### 7.1 紧急回滚

如果发现 main 分支有严重问题：

```bash

# 1. 创建 hotfix 分支

git checkout -b hotfix/critical-fix main

# 2. 修复问题并测试

# ...

# 3. 快速合并（跳过常规 PR 流程）

git checkout main
git merge hotfix/critical-fix --no-ff
git push origin main

# 4. 补充 PR 记录（事后）

```

### 7.2 数据备份

定期备份关键文件：

- `docs/entries/` - 所有词条
- `docs/changelog.md` - 版本历史
- `mkdocs.yml` - 站点配置
- `docs/admin/config.yml` - CMS 配置

!!! tip "自动备份"
    Git 本身就是版本控制系统，所有历史都可恢复。建议定期检查 `.gitignore` 确保重要文件已纳入版本控制。

### 7.3 冲突解决

当多个 PR 同时修改同一文件：

```bash

# 1. 让后提交的 PR 作者 rebase main

git checkout feat/branch-name
git fetch origin
git rebase origin/main

# 2. 手动解决冲突

# ...

# 3. 继续 rebase

git add .
git rebase --continue

# 4. 强制推送（仅限个人分支）

git push origin feat/branch-name --force-with-lease
```

### 7.4 联系信息

遇到技术问题可联系：

- **GitHub Issues**: <https://github.com/mps-team-cn/Multiple_Personality_System_wiki/issues>
- **讨论区**: <https://github.com/mps-team-cn/Multiple_Personality_System_wiki/discussions>

---

## 📚 附录

### A. 推荐开发环境

| 工具               | 推荐版本      | 说明               |
| ---------------- | --------- | ---------------- |
| Python           | ≥ 3.10    | 运行工具脚本           |
| Node.js          | ≥ 18      | 运行 npm 脚本（可选）    |
| markdownlint-cli | 最新        | Markdown 格式检查    |
| tectonic         | 最新        | PDF 导出引擎         |
| MkDocs           | ≥ 1.5     | 静态站点生成器          |
| gh               | 最新        | GitHub CLI（发布管理） |

### B. 常用命令速查

```bash

# 环境准备

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 本地开发

mkdocs serve
python tools/fix_markdown.py
markdownlint "docs/**/*.md"

# 发布流程

python tools/gen_changelog_by_tags.py --latest-to-head
git tag v1.4.0 -m "Release v1.4.0"
git push origin v1.4.0
gh release create v1.4.0 --notes-file docs/changelog.md
```

### C. 关键文档索引

| 文档类别   | 文档路径                                  |
| ------ | ------------------------------------- |
| 贡献指南   | `docs/contributing/index.md`          |
| PR 流程  | `docs/contributing/pr-workflow.md`    |
| 编写规范   | `docs/contributing/writing-guidelines.md` |
| 开发约定   | `AGENTS.md`                           |
| 工具文档   | `docs/dev/Tools-Index.md`                |
| 词条模板   | `docs/TEMPLATE_ENTRY.md`              |
| GitHub 工作流 | `docs/GITHUB_WORKFLOW.md`             |

---

!!! success "文档版本"
    最后更新：2025-01-12
    如有疑问，请在 GitHub Issues 中提问。
