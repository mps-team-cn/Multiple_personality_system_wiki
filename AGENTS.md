# Plurality Wiki 贡献与开发约定（AGENTS.md）

本文件定义了本项目的贡献规则与开发约定，供人类贡献者与自动化工具（如 Codex）使用。  
所有贡献应严格遵循以下要求，以保持条目结构与站点的一致性。

---

## 1. 通用约定

- **语言**：所有条目、说明文档与提交信息统一使用简体中文。
- **词条目录**：
  - 所有词条（Markdown 文档）必须存放在仓库根目录下的 `entries/` 子目录。
  - 严禁在其他目录编写词条文件。
  - `entries/` 下可根据主题建立二级目录（如 `entries/诊断与临床/`、`entries/系统体验与机制/`）。
- **命名规范**：
  - 一级标题统一采用 `中文名（English/缩写）` 格式。
  - 若为诊断或疾病，在括号内使用标准缩写（如 `重度抑郁障碍（MDD）`）。
- **目录索引同步**：
  - 新增或修改词条时，必须同步维护：
    - `index.md` → 全局目录索引  
    - `README.md` → 对应链接指向
- **文档结构**：
  - Markdown 一级标题：词条名称
  - 二级及以下标题：按内容层级递增
  - 若存在触发警示（⚠），必须置于文首

---

## 2. 站点配置与前端规则

- 所有站点文件放在 **仓库根目录**，必须包含：  
  - `index.html`  
  - `_sidebar.md`  
  - `_coverpage.md`  
  - `.nojekyll`（不可删除，避免 GitHub Pages 过滤下划线文件）  
- 所有静态资源引用必须使用相对路径（如 `./assets/xxx.png`），禁止使用以 `/` 开头的绝对路径，确保在 GitHub Pages 子路径下正常渲染。

---

## 3. PDF 导出脚本（`tools/pdf_export/`）

- **运行环境**：Python ≥ 3.10
- **代码规范**：
  - 使用 `pathlib.Path` 处理路径，禁止字符串拼接路径。
  - 保持函数拆分、`dataclass` 结构与类型标注。
  - 解析/生成 LaTeX、Markdown 时需考虑跨平台兼容性，并对用户输入做必要转义。
- **文档同步**：
  - 修改导出逻辑时，必须同步更新 `tools/pdf_export/README_pdf_output.md`。

---

## 4. 提交与版本管理

- **提交信息（Commit Message）建议前缀**：
  - `feat:` 新增条目或功能
  - `fix:` 修复错误或错别字
  - `docs:` 文档说明调整
  - `refactor:` 代码重构或结构调整
  - `chore:` 构建/配置/依赖更新
- **Pull Request 说明**：
  - 必须包含：改动动机、主要变更、潜在风险、相关条目或链接。
- **忽略文件**：
  - 提交前请检查 `ignore.md`，确保需要排除的文件已正确维护。

---

## 5. 测试与检查

- 修改 Python 代码后，至少运行：
  ```bash
  python -m compileall tools/pdf_export/export_to_pdf.py
````

确认无语法错误。

* 如引入额外依赖或命令行选项，必须在 `README.md` 或相关文档中注明。
* Markdown 新增/修改条目后，运行本地预览：

  ```bash
  npx docsify serve .
  ```

  确认页面能正常渲染。

---

## 6. 路线图（供 Codex 使用）

* [ ] 校验所有词条均位于 `entries/` 目录
* [ ] 校验 `index.md` 与 `README.md` 是否同步更新
* [ ] 自动检查 `.nojekyll` 是否存在
* [ ] PDF 导出脚本异常捕获与测试增强
* [ ] 集成 CI：提交时自动检查路径、Python 语法、Docsify 渲染

