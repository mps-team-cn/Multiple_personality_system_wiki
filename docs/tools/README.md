# 自动化维护工具清单

> 本目录用于集中维护仓库中各类自动化脚本的说明与使用示例，便于在 README 与 docs 之间保持一致。

## 工具概览

| 脚本/模块 | 功能摘要 | 常用用法 |
| --- | --- | --- |
| `tools/fix_md.py` | 批量修复 Markdown 常见 Lint 问题，涵盖行尾空格、标题前后空行、围栏语言补全等 | `python tools/fix_md.py` 或 `python tools/fix_md.py --dry-run` |
| `tools/check_links.py` | 扫描 Markdown 文档中疑似内部链接写法，禁止 `./`、`../` 等相对路径 | `python tools/check_links.py --root .`，必要时配合 `--whitelist` |
| `tools/docs_preview.py` | 本地预览辅助：优先尝试 `docsify-cli`，失败时回退 `python -m http.server` | `python tools/docs_preview.py --port 4173`（可用 `--wait` 调整检测时间） |
| `tools/gen_changelog_by_tags.py` | 按 Git 标签时间顺序生成 `changelog.md` 并按提交类型分组 | `python tools/gen_changelog_by_tags.py --output changelog.md`，可加 `--latest-only`/`--latest-to-head` |
| `tools/pdf_export/` | Pandoc 驱动的整站 PDF 导出工具，支持封面、忽略列表与中文字体 | `python tools/pdf_export/export_to_pdf.py` 或 `python -m pdf_export` |
| `tools/gen-validation-report.py` | 校验词条结构并生成 `docs/VALIDATION_REPORT.md` | `python tools/gen-validation-report.py` |
| `tools/retag_and_related.py` | 批量重建 Frontmatter 标签并生成“相关词条”区块 | `python tools/retag_and_related.py` 或 `python tools/retag_and_related.py --dry-run --limit 5` |
| `tools/run_local_updates.sh` / `tools/run_local_updates.bat` | 串联常用维护脚本，一键完成日常更新任务 | `bash tools/run_local_updates.sh` 或 `tools\run_local_updates.bat`（均支持 `--skip-*` 选项） |
| `generate_tags_index.py` | 扫描 Frontmatter 标签并生成 `tags.md` 索引 | `python generate_tags_index.py` |

如需新增脚本，请保持功能说明与示例用法同步更新本章节，方便贡献者快速定位维护工具。

## 使用建议

### 🏃 一键执行日常维护

```bash

# macOS / Linux 默认执行全部步骤

bash tools/run_local_updates.sh

# macOS / Linux 仅跳过 PDF 导出与 markdownlint

bash tools/run_local_updates.sh --skip-pdf --skip-markdownlint

# Windows 等效执行方式

tools\run_local_updates.bat

# Windows 同样可叠加跳过参数

tools\run_local_updates.bat --skip-pdf --skip-markdownlint
```

> 两个脚本都会自动切换到仓库根目录，并依次调用 changelog 生成、标签重建、最后更新时间索引、PDF 导出、标签索引、Markdown 修复与 lint。

### 🧰 一键修复 Markdown

```bash

# 1) 自动修复

python tools/fix_md.py

# 2) 校验（需安装 markdownlint-cli）

markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
```

> Windows 可用 `py tools/fix_md.py`，运行环境需 Python 3.10 及以上。

### 词条最后更新时间索引

- `scripts/gen-last-updated.mjs` 会遍历 `entries/` 下的所有 Markdown 词条，读取 Git 最后提交时间与提交哈希，并生成 `assets/last-updated.json` 索引文件；
- GitHub Actions 工作流 [`.github/workflows/last-updated.yml`](../../.github/workflows/last-updated.yml) 在推送 `main` 分支或手动触发时自动运行上述脚本并提交最新索引；
- 前端在 `index.html` 内置 Docsify 插件，会在每篇词条标题下渲染形如 `🕒 最后更新：2025/10/02 12:34:56（abc1234）` 的提示；
- `tools/pdf_export/` 的导出流程同样会读取该索引，并在离线 PDF 中展示相同的最后更新时间提示；
- 如需强制刷新缓存，可重新触发工作流或在部署平台清除静态资源缓存。

### 标签索引维护

- `python generate_tags_index.py` 会解析词条 Frontmatter 中的 `tags`，按标签分组生成 `tags.md`；
- 更新或新增词条后务必重新运行该脚本，确保索引与仓库内容一致；
- CI 会在 PR 中执行脚本并检查 `tags.md` 是否最新。

### PDF 导出目录生成逻辑

- `tools/pdf_export/` 在导出 PDF 时会优先读取仓库根目录的 `index.md`，目录页与章节书签都会遵循该文件的分组与顺序；
- 若 `index.md` 缺失或未收录全部词条，未出现在目录中的文档会自动归入“未索引词条”章节，确保不会遗漏内容；
- 目录中的词条链接会自动重写为 PDF 内部锚点，确保离线文档中的跳转行为与线上一致。
- 词条 Frontmatter 的 `updated` 字段支持 `YYYY-MM-DD` 字符串或 YAML 日期字面量，若留空、写成 `null`、布尔值或列表，导出脚本会终止并提示修正。

## 相关文档

- [导出 PDF 使用指南](../pdf_export/README_pdf_output.md)
- [贡献流程与规范](../TEMPLATE_ENTRY.md)
- [维护者手册](../ADMIN_GUIDE.md)
