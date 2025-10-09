# Multiple Personality System Wiki 贡献与开发约定（AGENTS.md）

本文件定义了本项目的贡献规则与开发约定，适用于人工贡献者与自动化工具（代理/脚本）。
所有贡献应严格遵循以下要求，以保持条目结构与站点一致性。

---

## 1. 通用约定

### 1.1 语言规范

- 所有条目、说明文档与提交信息统一使用简体中文。
- 一级标题采用 `中文名（English/缩写）` 格式；若为诊断/疾病，括号内必须使用标准缩写。

### 1.2 文件与目录规范

**重要** ：本项目已从 Docsify 迁移至 MkDocs Material，请遵循以下新的目录结构：

- **词条** ：
  - 存放位置：`docs/entries/` 目录（MkDocs 构建源）
  - 不得新建二级子目录，分类信息统一通过 Frontmatter `tags` 字段声明
- **词条 Frontmatter** ：每篇词条必须在文件开头声明 `---` 包裹的 YAML，至少包含 `title` / `tags` / `updated` 三个字段。
- **词条加粗规范** ：加粗内容前后都需要加空格，格式为 ` **加粗内容** `，以便于 MkDocs 正确识别。
- **文档** ：
  - MkDocs 文档：统一放在 `docs/` 目录（包括 `index.md`、`README.md`、`Glossary.md` 等）
  - 贡献指南：`docs/contributing/`（拆分为多个专题文档）
  - 开发者文档：`docs/ADMIN_GUIDE.md`、`docs/GITHUB_WORKFLOW.md`、`docs/TEMPLATE_ENTRY.md` 等
- **脚本与工具** ：所有脚本或自动化工具，统一放在 `tools/` 子目录。
- **工具文档** ：脚本更新或维护后，必须同步更新 `docs/tools/README.md`，保证工具与说明一致。

### 1.3 索引与链接规范

- 新增或修改词条时，必须同步维护：
  - docs/Glossary.md → 术语表（如适用）
  - 对应主题的总览页面（如适用）
  - **对应的 Guide 条目** → 当创建或更新专业术语、治疗方法、诊断标准等条目时，必须同步更新相关的导览条目（如 `Mental-Health-Guide.md`、`Core-Concepts-Guide.md`、`Clinical-Diagnosis-Guide.md` 等）中的引用和链接
- 条目内链接规范：
  - **词条间链接（同目录）** ：使用相对路径 `Admin.md`
  - **跨目录链接** ：
    - 从词条引用其他目录：`../contributing/index.md`
    - 从其他目录引用词条：`../entries/Admin.md`
  - MkDocs 会自动处理 `.md` 扩展名转换为 HTML
  - **禁止** 使用绝对路径（如 `/docs/entries/DID.md`）
  - 禁止使用模糊链接或锚点不明确的链接

---

## 2. 站点配置与前端规则

**当前框架** ：MkDocs Material

- **配置文件** ：
  - `mkdocs.yml` - 主配置文件（站点元信息、主题、插件、导航结构）
  - `requirements.txt` - Python 依赖清单
  - `.cfpages-build.sh` - Cloudflare Pages 构建脚本
- **静态资源** ：
  - 主目录：`docs/assets/`（CSS、JS、图片、JSON 数据等）
  - 自定义样式：`docs/assets/extra.css`
  - 自定义脚本：`docs/assets/extra.js`
  - **资源子目录** ：
    - `docs/assets/figures/` - 图表、流程图、示意图、SVG 等
    - `docs/assets/images/` - 一般图片（封面、截图等）
    - `docs/assets/icons/` - 小图标、装饰性素材
  - 资源引用：使用相对于 `docs/` 的路径（如 `assets/icons/favicon.svg`）

### 2.1 提示块语法

- 请在需要强调补充信息时使用 Material for MkDocs 的提示块语法。
- 常用语法示例如下，注意缩进需使用四个空格：

```markdown
!!! note
    This is a note.

!!! tip
    This is a tip.

!!! warning
    This is a warning.

!!! danger
    This is a danger.

!!! success
    This is a success.

!!! info
    This is an info.

!!! quote
    This is a quote.

??? question "What is the meaning of life, the universe, and everything?"
    42.
```

---

## 3. 工具与脚本

- 所有工具位于 `tools/` 目录，相关文档放置在 `docs/tools/README.md`。
- **PDF 导出工具** （`tools/pdf_export/`）：
  - **环境** ：Python ≥ 3.10
  - **规范** ：
    - 使用 `pathlib.Path`，禁止字符串拼接路径。
    - 保持函数化/`dataclass`/类型注解。
    - 注意 LaTeX/Markdown 转换的跨平台兼容与转义。
  - **文档同步** ：修改导出逻辑需同步更新 `docs/tools/README.md`。

---

## 4. 提交与版本管理

- **提交信息前缀（Conventional Commits）** ：
  - `feat:` 新增条目或功能
  - `fix:` 修复错误或错别字
  - `docs:` 文档说明调整
  - `refactor:` 代码重构或结构调整
  - `chore:` 构建/配置/依赖更新
  - `style:` 空格/缩进/行尾等非语义变更
- **Pull Request 说明** ：必须包含动机、主要变更、潜在风险、相关条目/链接。
- **忽略文件** ：提交前检查 `ignore.md` 维护是否正确。

---

## 5. Python 环境配置

### 5.1 系统要求

- Python 3.8 或更高版本
- pip 或虚拟环境支持

### 5.2 推荐配置方式

#### 方式一：虚拟环境（推荐）

适用于 Debian/Ubuntu 等外部管理 Python 环境的系统：

```bash
# 1. 安装 venv 支持（如需要）
sudo apt install python3.12-venv  # 或对应的 Python 版本

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt
```

**后续使用**：每次使用项目工具前，需先激活虚拟环境：

```bash
source venv/bin/activate
```

#### 方式二：系统级安装

适用于非托管 Python 环境：

```bash
# 直接安装依赖
pip install -r requirements.txt
```

### 5.3 常见问题解决

#### `pip: command not found`

```bash
# 方法 1：使用 python3 -m pip
python3 -m pip install -r requirements.txt

# 方法 2：安装 pip
python3 -m ensurepip --default-pip

# 方法 3：系统包管理器安装
sudo apt install python3-pip
```

#### `externally-managed-environment` 错误

这是 Debian/Ubuntu 系统的安全特性，请使用虚拟环境（见 5.2 方式一）。

**不推荐**：使用 `--break-system-packages` 可能破坏系统 Python 环境。

---

## 6. 测试与检查

- **MkDocs 本地预览** （推荐）：

  ```bash
  # 安装依赖（在虚拟环境中）
  pip install -r requirements.txt

  # 启动本地服务器（支持热重载）
  mkdocs serve

  # 访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)
  ```

- **构建测试** ：

  ```bash
  # 构建静态站点
  mkdocs build

  # 严格模式构建（有警告则失败）
  mkdocs build --strict
  ```

- **Python 语法检查** ：

  ```bash
  python -m compileall tools/pdf_export/export_to_pdf.py
  ```

---

## 7. 自动化维护规则（代理/脚本必须遵循）

- ✅ 必须遵循贡献指南（`docs/contributing/`）与词条模板（`docs/TEMPLATE_ENTRY.md`）
- ✅ 必须保持小步提交（最小可审查单位）
- ✅ 词条必须遵守markdownlint规范
- ✅ 必须在 PR 描述中说明生成/重写内容的方法与来源（正则/脚本名/范围等）
- ✅ 必须在脚本更新时同步维护 `docs/tools/README.md`
- ❌ 禁止生成无法追溯的证据
- ❌ 禁止破坏索引、交叉引用或有效链接
- ⚠️ 大规模格式化操作必须附带回滚指引

---

## 8. Markdown 自动修复与校验

> 自动执行优先；手动修改后需手动执行。

### 8.1 自动执行（CI）

- CI 会在 `push` / `pull_request` 时运行以下步骤：

  1. 执行 `python tools/fix_markdown.py` 自动修复；
  2. 执行 `markdownlint` 校验；若有未修复项，CI 失败并提示。
- 详见 `.github/workflows/markdown_format.yml`。

### 8.2 手动执行（本地）

```bash

# 执行自动修复

python tools/fix_markdown.py

# 可选：仅查看将修改哪些文件

python tools/fix_markdown.py --dry-run

# 运行 markdownlint（需已安装 markdownlint-cli）

# MkDocs 项目检查

markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"

# 或检查所有 Markdown

markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor" --ignore "site"
```

k### 7.3 规则说明与例外

- 脚本会自动修复：MD012 / MD022 / MD040 / MD009 / MD034 / MD047 / MD028
- **需人工处理** ：

  - MD024 重复标题（请调整为唯一标题或降级层级）
  - MD052 参考式链接缺失定义（补 `[n]: [https://...`）](https://...`）)
  - MD042 / MD051 徽章空链接与无效锚点（修正为有效 URL/锚点）
