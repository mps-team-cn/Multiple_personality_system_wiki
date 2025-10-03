# Plurality Wiki 贡献与开发约定（AGENTS.md）

本文件定义了本项目的贡献规则与开发约定，供人类贡献者与自动化工具（如代理/脚本）使用。
所有贡献应严格遵循以下要求，以保持条目结构与站点一致性。

---

## 1. 通用约定

- **语言**：所有条目、说明文档与提交信息统一使用简体中文。
- **词条目录**：
  - 所有词条（Markdown 文档）必须存放在仓库根目录下的 `entries/` 子目录；严禁在其他目录编写词条。
  - `entries/` 下可根据主题建立二级目录（如 `entries/诊断与临床/`、`entries/系统体验与机制/`）。
- **命名规范**：
  - 文件名采用“首字母大写 + 英文短横线”的英文文件名（如 `Borderline-Personality-Disorder-BPD.md`）。
  - 一级标题统一采用 `中文名（English/缩写）` 格式；诊断/疾病在括号内使用标准缩写。
- **目录索引同步**：
  - 新增或修改词条时，必须同步维护：
    - `index.md` → 全局目录索引
    - `glossary.md` → 术语表（如适用）
    - `assets/last-updated.json` → 词条最后更新时间索引；如有词条变动，请运行 `node scripts/gen-last-updated.mjs` 重新生成
- **链接规范**：
  - **所有条目内链接必须使用完整路径**（如 `entries/系统角色与类型/Admin.md`），禁止相对或模糊链接。

---

## 2. 站点配置与前端规则

- 站点文件位于仓库根目录，必须包含：
  - `index.html`、`_sidebar.md`、`_coverpage.md`、`.nojekyll`
- 静态资源引用使用相对路径（如 `./assets/xxx.png`），禁止以 `/` 开头的绝对路径。

---

## 3. PDF 导出脚本（`tools/pdf_export/`）

- **环境**：Python ≥ 3.10
- **规范**：
  - 使用 `pathlib.Path`，禁止字符串拼接路径。
  - 保持函数化/`dataclass`/类型注解。
  - 注意 LaTeX/Markdown 转换的跨平台与转义。
- **文档同步**：修改导出逻辑需同步更新 `tools/pdf_export/README_pdf_output.md`。

---

## 4. 提交与版本管理

- **提交信息前缀（Conventional Commits）**：
  - `feat:` 新增条目或功能
  - `fix:` 修复错误或错别字
  - `docs:` 文档说明调整
  - `refactor:` 代码重构或结构调整
  - `chore:` 构建/配置/依赖更新
  - `style:` 空格/缩进/行尾等非语义变更
- **Pull Request 说明**：包含动机、主要变更、潜在风险、相关条目/链接。
- **忽略文件**：提交前检查 `ignore.md` 维护是否正确。

---

## 5. 测试与检查

- Python 快速语法检查：

  ```bash
  python -m compileall tools/pdf_export/export_to_pdf.py
  ```

- Markdown 本地预览：

  ```bash
  npx docsify serve .
  ```

---

## 6. 自动化维护规则（代理/脚本必须遵循）

- **遵循规范**：严格按照《CONTRIBUTING.md》以及《TEMPLATE_ENTRY.md》执行写作规范、条目模板、提交流程与自检清单。
- **最小可审查单位**：小步提交，小主题 PR（如“统一标题层级/修复链接/更新参考文献”）。
- **可追溯性**：自动生成/重写内容须在 PR 描述中说明来源与方法（正则/脚本名/范围等）。
- **不造证据**：引用需指向可核验的权威文献（ICD-11、DSM-5-TR、WHO/APA 指南、综述等）。
- **不破坏链接**：涉及重命名/路径调整，须同步更新索引与交叉引用。
- **可回滚**：大规模格式化/统一风格，应附回滚脚本或复原指引。

---

## 7. Markdown 自动修复与校验（**必须**）

> 自动执行优先；手动修改后需手动执行。

### 7.1 自动执行（CI）

- CI 会在 `push` / `pull_request` 上运行以下步骤：

  1. 执行 `python tools/fix_md.py` 自动修复；
  2. 执行 `markdownlint` 校验；若有未修复项，CI 失败并提示。

> 详见 `.github/workflows/markdown_format.yml`。

### 7.2 手动执行（本地）

```sh

# 执行自动修复

python tools/fix_md.py

# 可选：仅查看将修改哪些文件

python tools/fix_md.py --dry-run

# 运行 markdownlint（需已安装 markdownlint-cli）

markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
```

### 7.3 规则说明与例外

- 脚本会自动修复：MD012/MD022/MD040/MD009/MD034/MD047/MD028
- **需人工处理**：

  - MD024 重复标题（请调整为唯一标题或降级层级）
  - MD052 参考式链接缺失定义（补 `[n]: [https://...`）](https://...`）)
  - MD042/MD051 徽章空链接与无效锚点（修正为有效 URL/锚点）
