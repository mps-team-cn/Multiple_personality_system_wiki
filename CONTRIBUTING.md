# Plurality Wiki 贡献指南（CONTRIBUTING.md）

本文件定义了 **Plurality Wiki** 的贡献规则与开发约定，适用于人类贡献者与自动化工具。
目标是保证条目内容的 **一致性、严谨性、可验证性**，并确保引用有清晰出处。

---

## 1. 通用约定

- **语言规范**

  - 所有条目、说明文档、提交信息统一使用简体中文。
  - 一级标题统一采用 `中文名（English/缩写）` 格式，若为诊断或疾病则在括号内使用标准缩写（如“解离性身份障碍（DID）”）。
  - 首次出现时必须标注**英文原名与缩写**。

- **文件结构**

  **重要**：本项目已从 Docsify 迁移至 MkDocs Material。

  - 所有词条文件统一存放在 `docs/entries/` 目录（MkDocs 构建源），不得再建立二级子目录。
  - 备份同步：`entries/` 根目录保留词条副本，便于工具兼容。
  - 每篇词条必须以 YAML Frontmatter 开头，并声明 `title`、`tags`、`updated` 字段。
  - 禁止在其他目录撰写词条。

- **Markdown 规范**

  - 一级标题：词条名
  - 二级及以下标题：依层级递增
  - 必要时在文首添加 **触发警示**（如涉及创伤、暴力、自伤、性侵等内容）。

- **提交规范**

  - 遵循 Conventional Commits 规范：

    - `feat:` 新增条目/新增章节
    - `fix:` 错误修复（链接/引用/格式）
    - `docs:` 文档与索引更新（不影响语义）
    - `refactor:` 结构与命名重构（不改变内容含义）
    - `chore:` 工具、CI、脚本维护项
    - `style:` 空格/缩进/行尾等非语义变更

---

## 2. 学术与引用规范

为确保条目**严谨、无歧义、可追溯**，所有断言必须配备引用。

### 2.1 证据与来源分级

- **一级来源（必选优先）**：

  - ICD-11 官方浏览器、Reference Guide、临床描述与诊断要求（CDDR）
  - DSM-5-TR 原文与 APA 官方资料

- **二级来源（可补充）**：

  - 权威综述（StatPearls, UpToDate, 教科书）

- **三级来源（仅限背景）**：

  - 社群 Wiki、媒体报道、博客、论坛

> **规则**：涉及诊断、病理学、流行病学断言，**必须引用至少 1 个一级来源**。

### 2.2 引用格式要求

- 每个可核查断言**就近给出引用**（脚注或段尾引用）。
- 引用须包含：**来源名称、版本、访问日期**。
- 如为中文翻译，必须同时给出英文原文（≤25 词），并标明译者/校对。

示例：

```yaml
ICD-11（6B64）：“…two or more distinct personality states…”（存在两个或以上身份状态）。
来源：WHO ICD-11 浏览器（MMS 2025-01，访问日期 2025-10-03）
```

---

## 3. 【诊断与临床】强制要求

凡涉及疾病、诊断、病理机制等条目，必须遵循以下规范：

1. **ICD-11 与 DSM-5-TR 双重对照**

   - 需明确给出 ICD-11 的诊断编码与定义。
   - 若 DSM 无对应诊断，则说明 DSM 的归类（如 Partial DID 在 DSM 属于 OSDD-1）。

2. **原文摘录**

   - 必须包含原文的中文翻译。
   - 示例：

     ```yaml
     ICD-11: “two or more distinct personality states…”
     中文：两个或以上身份状态。
     来源：ICD-11 Browser, 6B64, 访问日期 2025-10-03
     ```

3. **差异说明**

   - 若 ICD 与 DSM 的分类存在差异（如 ICD-11 有 Partial DID，DSM 无），必须在条目中**显式说明**。

---

## 4. 翻译与术语规范

- 采用 **中文名（English, 缩写）** 格式。
- 社群用语（如“人格职业”“幻想伙伴”）必须与临床术语分开，列入“同义词/社群用法”小节。
- 若存在多译名，需标明使用场景与来源（临床/社群/媒体）。

---

## 5. 图表与数据要求

- 图片、图表必须注明来源与许可。
- 数据表需标明统计口径、时间范围、样本来源。
- 对有争议的研究，需并列不同观点，并标注证据等级。

---

## 6. 技术与格式约定

- **最后更新时间**：Frontmatter 中的 `updated` 字段须与 `docs/assets/last-updated.json` 保持一致。
- **内部链接**：
  - MkDocs 项目：使用相对路径 `entries/Admin.md` 或 `../entries/Admin.md`
  - MkDocs 会自动处理 `.md` 扩展名转换为 HTML
  - 禁止使用模糊链接或锚点不明确的链接
- **目录同步**：更新或新增词条时，必须同步修改：
  - `docs/tags.md`（运行 `python tools/generate_tags_index.py`）
  - `docs/index.md` 首页导航
  - `docs/Glossary.md` 术语表（如适用）

---

## 7. PR 提交流程与检查清单

### 本地开发流程

1. **安装依赖**：

   ```bash
   pip install -r requirements-mkdocs.txt
   ```

2. **编辑词条**：

   - 在 `docs/entries/` 目录下创建或修改词条
   - 确保 Frontmatter 包含 `title`、`tags`、`updated` 字段

3. **本地验证**：

   ```bash
   # 自动修复格式
   python tools/fix_md.py

   # Markdown lint 检查
   markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "site"

   # 生成标签索引
   python tools/generate_tags_index.py

   # 本地预览
   mkdocs serve
   # 访问 http://127.0.0.1:8000
   ```

4. **构建测试**：

   ```bash
   # 严格模式构建
   mkdocs build --strict
   ```

### PR 提交检查清单

每个 PR 必须包含以下信息：

- [ ] 变更类型（feat/fix/docs/...）与影响范围
- [ ] 所有断言均有就近引用（含版本与访问日期）
- [ ] 【病理学】同时给出 ICD-11 与 DSM-5-TR 的锚点
- [ ] 【病理学】含原文摘录（≤25 词）+ 中文翻译 + 链接/页码
- [ ] 翻译注明译者/校对
- [ ] 图片/数据版权与许可明确
- [ ] 内部链接与目录正确；`python tools/generate_tags_index.py` 已执行
- [ ] 最后更新时间已更新（`docs/assets/last-updated.json`）
- [ ] `mkdocs serve` 本地预览无误
- [ ] `mkdocs build --strict` 构建成功
- [ ] CI / Lint 通过

---

## 8. 常用权威入口（建议引用时固定）

- WHO ICD-11 Browser（MMS 2025-01）
- WHO Clinical Descriptions and Diagnostic Requirements（CDDR, 2024 PDF）
- APA DSM-5-TR Fact Sheets 与官方页面
- StatPearls / UpToDate（作为二级来源）

---

## 9. 模板

请参考[导入模板](docs/TEMPLATE_ENTRY.md)
