# 🧭 Multiple Personality System Wiki 管理员操作指南（优化版）

本指南为 **Multiple Personality System Wiki** 维护者与协作者提供基础操作与维护流程。
目标是确保贡献内容符合规范、CI 通过、结构一致。
详细写作要求请参阅 [**contributing/index.md**](contributing/index.md) 与 [**AGENTS.md**](../AGENTS.md) 。

---

## 1️⃣ GitHub 基础操作

### 1.1 克隆与同步仓库

```bash

# 克隆仓库

git clone https://github.com/mps-team-cn/Multiple_Personality_System_wiki.git

# 进入目录

cd Multiple_Personality_System_wiki

# 同步主分支

git checkout main
git pull origin main
```

### 1.2 新建分支

所有改动应在独立分支进行，命名遵循：

| 类型        | 说明         |
| --------- | ---------- |
| feat/xxx  | 新增功能或词条    |
| fix/xxx   | 修复错误       |
| docs/xxx  | 文档更新       |
| chore/xxx | 配置、脚本或依赖维护 |

```bash
git checkout -b feat/new-entry
```

---

## 2️⃣ 提交与命名规范

提交信息遵循 **Conventional Commits** ：

```bash
git add entries/DID.md
git commit -m "feat: 新增解离性身份障碍（DID）条目"
```

**类型说明：**

* `feat:` 新增条目或功能
* `fix:` 修复错误、链接或格式
* `docs:` 文档内容变更
* `chore:` 配置、脚本或 CI 修改
* `style:` 空格、缩进、行尾等非语义修改

---

## 3️⃣ Pull Request（PR）流程

1. 推送分支

   ```bash
   git push origin feat/new-entry
   ```

2. 在 GitHub 上创建 PR：

   * 选择目标分支为 `main`
   * 填写 PR 模板（动机、变更点、风险、测试结果等）

3. 自检清单：

   * ✅ 所有断言均有引用（含 ICD/DSM）
   * ✅ 引用注明来源与日期
   * ✅ “最后更新”字段已更新
   * ✅ Lint / CI 通过

4. 审核与合并：

   * 至少一位管理员 Review
   * 确认无冲突后合并至 `main`
   * 合并后可删除源分支

---

## 4️⃣ 分支与版本管理

| 分支类型               | 用途     | 说明            |
| ------------------ | ------ | ------------- |
| `main`             | 稳定发布   | CI 通过、PDF 可导出 |
| `feat/*` / `fix/*` | 临时开发   | 合并后应删除        |
| `dev`（可选）          | 大型改动测试 | 合并完成后同步 main  |

---

## 5️⃣ 使用 Sveltia CMS 管理词条

### 📝 访问 CMS 后台

**在线版本**（推荐）：

- 访问 `[https://mpswiki.pages.dev/admin/`](https://mpswiki.pages.dev/admin/`)
- 使用 GitHub 账号登录
- 需要有仓库协作者权限

**本地版本**：

- 启动本地服务器：`python -m http.server 8000 --directory docs`
- 访问 `[http://localhost:8000/admin/`](http://localhost:8000/admin/`)
- 点击 "Work with Local Repository" 选择仓库目录

详细使用指南请参阅 [local-dev-server.md](../local-dev-server.md)

### ✨ CMS 核心功能

#### 搜索

- **快捷键**: `Ctrl+F` (Windows/Linux) 或 `Command+F` (macOS)
- **全文搜索**: 可搜索词条标题和正文内容
- **即时结果**: 输入即显示匹配结果

#### 筛选

- 点击 **Filter** 按钮
- 选择主题分类（7 个）或标签（4 个）
- 快速定位特定类型的词条

#### 分组

- 点击 **Group** 按钮
- 按主题分类或标签分组显示
- 便于查看词条分布

#### 排序

- 点击 **Sort** 按钮
- 支持按标题、更新时间、主题排序
- 支持升序/降序

### 🎯 使用 CMS 新增词条

1. 点击右上角蓝色 **"New"** 按钮
2. 填写以下字段：
   - **标题**: 格式必须为"中文（English/缩写）"
   - **主题分类**: 从 7 个选项中选择一个
   - **标签**: 添加相关标签（用于交叉引用）
   - **更新时间**: 自动设置为当前日期
   - **正文内容**: 使用 Markdown 编写
3. 点击 **"Save"** 保存
4. 填写提交信息（简要说明新增内容）
5. 点击 **"Publish"** 提交到 GitHub

### 📝 使用 CMS 编辑词条

1. 在列表中搜索或浏览找到词条
2. 点击词条标题进入编辑界面
3. 修改相关字段
4. 点击 **"Save"** 保存
5. 填写更新说明
6. 点击 **"Publish"** 提交更改

### 🎨 主题分类说明

创建或编辑词条时必须选择以下 7 个主题之一：

| 分类 | 说明 | 词条数 |
|------|------|--------|
| 理论与分类 | 结构性解离理论等 | 22 |
| 诊断与临床 | DID、解离障碍等 | 31 |
| 系统运作 | 切换、共意识等 | 48 |
| 角色与身份 | Admin、Alter 等 | 30 |
| 文化与表现 | 影视作品描绘 | 17 |
| 创伤与疗愈 | CPTSD、创伤治疗 | 5 |
| 实践指南 | Tulpa 创造等 | 5 |

---

## 6️⃣ 常见任务指南（手动方式）

### 🔹 6.1 手动新增词条

1. 复制 [TEMPLATE_ENTRY.md](TEMPLATE_ENTRY.md)
2. 填写完整内容（含 Frontmatter：`title`、`tags`、`updated`）
3. 将文件保存至 `docs/entries/` 目录
4. 标签索引由 MkDocs Material tags 插件自动生成，无需手动更新

> 💡 **推荐使用 CMS**: 上述步骤可通过 Sveltia CMS 界面完成，无需手动创建文件

### 🔹 6.2 更新已有词条

* 修改后同步更新 `index.md`、`Glossary.md`
* 检查引用与标签一致性

### 🔹 6.3 运行一键本地维护脚本

如果你是管理员或审稿人，可直接执行以下脚本进行本地全流程维护（含搜索索引更新）：

```bash
tools\run_local_updates.bat
```

遇到依赖相关问题，可以先执行

```bash
pip install -r requirements.txt
```

等效于以下手动操作顺序：

```bat
@REM 更新日志
python tools/gen_changelog_by_tags.py --latest-to-head
@REM 生成 PDF 和目录索引
python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
@REM 修正 Markdown 格式
python tools/fix_markdown.py
@REM 检查 Markdown 格式
markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
```

> **注意**：MkDocs Material 迁移后，标签索引由 `tags` 插件自动生成，无需手动工具维护。

✅ 建议在每次合并前执行一次。

---

## 7️⃣ 发布与更新日志

### 7.1 手动标记版本

```bash
git tag v1.3.4
git push origin v1.3.4
```

### 7.2 自动生成更新日志

使用工具脚本生成：

```bash
python tools/gen_changelog_by_tags.py --latest-to-head
```

输出文件：`CHANGELOG.md`
详见 [tools/README.md](tools/README.md)。

---

## 8️⃣ 审核要点（管理员）

合并前请检查以下项目：

| 检查项     | 要求                   |
| ------- | -------------------- |
| 🧩 结构   | 文件路径、命名与目录一致         |
| 📚 内容   | 引用可靠（ICD/DSM/学术文献）   |
| 🔗 链接   | 无断链、相对路径正确           |
| 🧹 格式   | Markdownlint、CI 全部通过 |
| 🗓️ 元数据 | Frontmatter、更新时间正确   |

---

## 9️⃣ 附录：推荐环境

| 工具               | 推荐版本  | 说明       |
| ---------------- | ----- | -------- |
| Python           | ≥3.10 | 运行工具脚本   |
| Node.js          | ≥18   | 运行更新脚本   |
| markdownlint-cli | 最新    | Lint 校验  |
| tectonic         | 最新    | PDF 导出引擎 |

---

### ✅ 建议后续改进

1. 可在 CI 中加入 `tools/run_local_updates.bat` 自动运行流程，减少人工误差。
2. 将生成日志、PDF、Lint 等合并到一个 `make all` 或 `npm run full-update` 中，实现跨平台一键构建。
