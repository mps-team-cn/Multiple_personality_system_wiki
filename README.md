# Plurality Wiki

> 多重意识体系统与相关心理健康主题的中文知识库与开源协作项目。
> 在线版（GitHub Pages）：<https://kuliantnt.github.io/plurality_wiki/#/>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs status](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://kuliantnt.github.io/plurality_wiki/#/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/kuliantnt/plurality_wiki?style=social)](https://github.com/kuliantnt/plurality_wiki/stargazers)
[![Build](https://github.com/kuliantnt/plurality_wiki/actions/workflows/ci.yml/badge.svg)](https://github.com/kuliantnt/plurality_wiki/actions)

---

📖 **提示**：如果你是普通读者，请查看 [Main_Page.md](./Main_Page.md)；本文档主要面向开发者与贡献者。

---

## ✨ 项目目标

- 汇聚与整理多重意识体（Plurality）与相关心理健康主题的高质量中文资料；
- 采用一致的**条目规范**与**贡献流程**，确保可维护、可引用、可扩展；
- 面向大众读者与专业人士，兼顾可读性与严谨性（参考 E-E-A-T 原则）。

---

## 🧰 一键修复 Markdown（自动 & 手动）

本仓库提供 `tools/fix_md.py` 用于**自动修复**常见 Markdown 风格与语法问题（MD012/MD022/MD040/MD009/MD034/MD047/MD028）。

### 自动执行（CI）

- 在 `push` / `pull_request` 时，CI 会运行：
  1. `python tools/fix_md.py`
  2. `markdownlint` 校验（如仍有问题则 CI 失败）

> 工作流示例见 `.github/workflows/markdown_format.yml`。

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
├─ Main_Page.md
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
