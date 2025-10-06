# Plurality Wiki

> 多重意识体系统与相关心理健康主题的中文知识库与开源协作项目。
> 在线版（GitHub Pages）：<https://kuliantnt.github.io/plurality_wiki/#/>

- [查看标签索引](tags.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs status](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://kuliantnt.github.io/plurality_wiki/#/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/kuliantnt/plurality_wiki?style=social)](https://github.com/kuliantnt/plurality_wiki/stargazers)
[![工作流 状态](https://img.shields.io/github/actions/workflow/status/kuliantnt/plurality_wiki/ci.yml?label=CI&logo=github)](https://github.com/kuliantnt/plurality_wiki/actions/workflows/docs_quality.yml)

---

📖 **提示**：如果你是普通读者，请查看网页版本 [GitHUB pages](https://kuliantnt.github.io/plurality_wiki/#/)或[cloud Flare Page](https://plurality-wiki.pages.dev/)；本文档主要面向开发者与贡献者。

---

## ✨ 项目目标

- 汇聚与整理多重意识体（Plurality）与相关心理健康主题的高质量中文资料；
- 采用一致的**条目规范**与**贡献流程**，确保可维护、可引用、可扩展；
- 面向大众读者与专业人士，兼顾可读性与严谨性（参考 E-E-A-T 原则）。

---

## 📦 仓库结构

```ini
plurality_wiki/
├─ README.md                  # 开发者说明
├─ CONTRIBUTING.md            # 贡献指南
├─ index.html                 # Docsify 入口
├─ _sidebar.md / _navbar.md   # Docsify 导航配置
├─ 404.html / _404.md         # 404 页面（HTML + Markdown 版）
├─ Main_Page.html             # 旧版主页面（保留历史内容）
├─ Glossary.md                # 术语表
├─ Preface.md                 # 前言
├─ index.md                   # 全局目录索引
├─ changelog.md               # 版本更新记录
├─ docs/                      # 贡献流程补充文档与自动报告
│  ├─ ADMIN_GUIDE.md
│  ├─ GITHUB_WORKFLOW.md
│  ├─ TEMPLATE_ENTRY.md
│  ├─ VALIDATION_REPORT.md    # 校对与审核记录（脚本生成）
│  └─ tools/...
├─ entries/                   # 词条正文（全部放在根目录，依靠 Frontmatter tags 分类）
├─ tags.md                    # 按标签自动生成的索引页
├─ assets/                    # 静态资源与 last-updated.json
├─ scripts/
│  └─ gen-last-updated.mjs    # 更新词条时间索引
├─ tools/                     # 本地维护工具
│  ├─ gen-validation-report.py # 校验词条结构并生成报告
│  ├─ fix_md.py               # Markdown 自动修复脚本
│  └─ pdf_export/...
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ workflows/
│     ├─ docs_quality.yml     # Markdown/链接检查 CI
│     └─ last-updated.yml     # 自动生成 last-updated.json
├─ AGENTS.md                  # 贡献与开发约定
└─ ignore.md、.nojekyll、.markdownlint* 等配置文件
```

---

## 🤖 自动化维护

根目录下的 `tools/` 目录集中存放了协助批量处理、检查与发布的脚本，可与 CI 流程搭配使用。更完整的说明与后续更新请参见 [`docs/tools/README.md`](docs/tools/README.md)。

- `python tools/gen-validation-report.py`：读取《CONTRIBUTING.md》与《docs/TEMPLATE_ENTRY.md》，生成 `docs/VALIDATION_REPORT.md` 校对报告。
- `python tools/generate_tags_index.py`：扫描 `entries/` 前置元数据，输出 `tags.md` 标签索引。
- `python tools/check_links.py --root .`：校验所有 Markdown 文件的内部链接是否遵循 `entries/*.md` 绝对路径写法，并提示潜在断链。

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

欢迎参与完善！首次贡献请阅读 **[CONTRIBUTING.md](./CONTRIBUTING.md)**，并参考下列关键文档：

- [GitHub 提交流程指南](docs/GITHUB_WORKFLOW.md)
- [词条模板](docs/TEMPLATE_ENTRY.md)
- [维护者手册](docs/ADMIN_GUIDE.md)

### 提交流程（简要）

1. Fork & 新建分支；
2. 按规范撰写/修改，**同步更新 tags.md（运行 `python tools/generate_tags_index.py`）、index.md 与交叉链接**；
3. 本地执行 `python tools/fix_md.py` 与 `markdownlint`；
4. 提交 PR，等待 Review。

---

## 🗺️ 路线图（Roadmap）

- [x] 基础 CI（Markdown lint/链接检查）
- [ ] 样式统一与模板完善
- [ ] 前端页面优化与跳转修复
