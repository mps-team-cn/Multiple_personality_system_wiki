# Plurality Wiki

> 多重意识体系统与相关心理健康主题的中文知识库与开源协作项目。
> 在线版（GitHub Pages）：<https://kuliantnt.github.io/plurality_wiki/#/>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs status](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://kuliantnt.github.io/plurality_wiki/#/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/kuliantnt/plurality_wiki?style=social)](https://github.com/kuliantnt/plurality_wiki/stargazers)
[![CI 状态](https://img.shields.io/github/actions/workflow/status/kuliantnt/plurality_wiki/ci.yml?label=CI&logo=github)](https://github.com/kuliantnt/plurality_wiki/actions/workflows/ci.yml)

---

📖 **提示**：如果你是普通读者，请查看 [Main_Page.html](./Main_Page.html)；本文档主要面向开发者与贡献者。

---

## ✨ 项目目标

- 汇聚与整理多重意识体（Plurality）与相关心理健康主题的高质量中文资料；
- 采用一致的**条目规范**与**贡献流程**，确保可维护、可引用、可扩展；
- 面向大众读者与专业人士，兼顾可读性与严谨性（参考 E-E-A-T 原则）。

---

### 手动执行（本地）

```bash

# 1) 自动修复

python tools/fix_md.py

# 2) 校验（需安装 markdownlint-cli）

markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
```

> Windows 可用 `py tools/fix_md.py`。
> 需 Python 3.10+。

---

## 📦 仓库结构

```ini
plurality_wiki/
├─ README.md
├─ Main_Page.html
├─ CONTRIBUTING.md
├─ AGENTS.md
├─ index.md
├─ glossary.md
├─ changelog.md
├─ tools/
│  ├─ fix_md.py               # ← 一键修复脚本
│  └─ pdf_export/...
├─ .github/
│  └─ workflows/
│     └─ markdown_format.yml  # ← CI 自动执行脚本与校验
└─ entries/...                 # 主题词条
```

---

## 🤖 自动化维护

根目录下的 `tools/` 目录集中存放了协助批量处理、检查与发布的脚本，可与 CI 流程搭配使用：

| 脚本/模块 | 功能摘要 | 常用用法 |
| --- | --- | --- |
| `tools/fix_md.py` | 批量修复 Markdown 常见 Lint 问题，涵盖行尾空格、标题前后空行、围栏语言补全等 | 详见上文“🧰 一键修复 Markdown”章节，可运行 `python tools/fix_md.py` 或 `python tools/fix_md.py --dry-run` |
| `tools/check_links.py` | 扫描 Markdown 文档中疑似内部链接的写法，禁止 `./`、`../` 等相对路径并提示改为 `entries/.../*.md` | `python tools/check_links.py --root .`，必要时加 `--whitelist` 允许额外根目录文档 |
| `tools/docs_preview.py` | 本地预览辅助：优先尝试 `docsify-cli`，失败时自动回退到 `python -m http.server` | `python tools/docs_preview.py --port 4173`（默认端口 4173，可通过 `--wait` 调整 docsify 启动检测） |
| `tools/gen_changelog_by_tags.py` | 按 Git 标签时间顺序生成 `CHANGELOG.md`，并按 Conventional Commits 类型分组 | `python tools/gen_changelog_by_tags.py --output changelog.md`，或加 `--latest-only` 仅生成最近区间，或加  `--latest-to-head` 生成“最新标签..HEAD”简化版 changelog，便于手工编辑 |
| `tools/pdf_export/` | Pandoc 驱动的整站 PDF 导出工具，支持封面、目录、忽略列表与中文字体配置 | 运行 `python tools/pdf_export/export_to_pdf.py` 或 `python -m pdf_export`，更多参数见 `tools/pdf_export/README_pdf_output.md` |

如需新增脚本，请保持功能说明与示例用法同步更新本章节，方便贡献者快速定位维护工具。

### 词条最后更新时间索引

- `scripts/gen-last-updated.mjs` 会遍历 `entries/` 下的所有 Markdown 词条，读取 Git 最后提交时间与提交哈希，并生成 `assets/last-updated.json` 索引文件；
- GitHub Actions 工作流 [`.github/workflows/last-updated.yml`](.github/workflows/last-updated.yml) 在推送 `main` 分支或手动触发时自动运行上述脚本并提交最新索引；
- 前端在 `index.html` 内置 Docsify 插件，会在每篇词条标题下渲染形如 `🕒 最后更新：2025/10/02 12:34:56（abc1234）` 的提示，其中时间来自 Git 提交历史、哈希取前 7 位；
- `tools/pdf_export/` 的导出流程会读取同一份索引，并在离线 PDF 中的每篇词条标题下展示相同的最后更新时间提示；
- 如需强制刷新缓存，可重新触发工作流或在部署平台清除静态资源缓存。

---

## 🚀 本地预览

### A. 任意静态服务器

```bash
python -m http.server 4173

# http://localhost:4173

```

### B. docsify

```bash
npm i -g docsify-cli
docsify serve .
```

---

## 🧭 贡献（Contribution）

欢迎参与完善！首次贡献请阅读 **[CONTRIBUTING.md](./CONTRIBUTING.md)**。

### 提交流程（简要）

1. Fork & 新建分支；
2. 按规范撰写/修改，**同步更新 index.md 与交叉链接**；
3. 本地执行 `python tools/fix_md.py` 与 `markdownlint`；
4. 提交 PR，等待 Review。

---

## 🗺️ 路线图（Roadmap）

- [x] 基础 CI（Markdown lint/链接检查）
- [ ] 样式统一与模板完善
- [ ] 前端页面优化与跳转修复
