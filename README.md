# Plurality Wiki

> 多重意识体系统与相关心理健康主题的中文知识库与开源协作项目。  
> 在线版（GitHub Pages）：<https://kuliantnt.github.io/plurality_wiki/#/>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs status](https://img.shields.io/badge/Wiki-active-brightgreen.svg)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](#贡献)
[![Stars](https://img.shields.io/github/stars/kuliantnt/plurality_wiki?style=social)](https://github.com/kuliantnt/plurality_wiki/stargazers)
[![Build](https://github.com/kuliantnt/plurality_wiki/actions/workflows/ci.yml/badge.svg)](https://github.com/kuliantnt/plurality_wiki/actions)

---

📖 **提示**：如果你是普通读者，请查看 [README_wiki.md](./README_wiki.md)，这是面向公众的首页介绍；  
本文档主要面向开发者、贡献者与维护者。

---

## ✨ 项目目标

- 汇聚与整理多重意识体（Plurality）与相关心理健康主题的高质量中文资料；
- 采用一致的**条目规范**与**贡献流程**，确保可维护、可引用、可扩展；
- 面向大众读者与专业人士，兼顾可读性与严谨性（参考 E-E-A-T 原则）。

---

## 📦 仓库结构

```ini
plurality_wiki/
├─ README.md                # 仓库主页（面向开发者）
├─ README_wiki.md           # 网页首页（面向公众介绍）
├─ CONTRIBUTING.md          # 贡献指南（面向词条更新者/编辑者）
├─ AGENTS.md                # Codex/自动化与人类贡献者的协作约定
├─ index.md                 # Wiki 导航/索引（建议“顶部导航+完整索引”双层结构）
├─ glossary.md              # 术语表（可选）
├─ changelog.md             # 更新日志（可选）
├─ images/                  # 图片资源
├─ docs/                    # （可选）若使用 docsify/VitePress/VuePress 等静态站点
├─ tools/                   # 自动化维护工具
├─ .github/
│  ├─ ISSUE_TEMPLATE/       # Issue 模板（可选）
│  ├─ PULL_REQUEST_TEMPLATE.md  # PR 模板（可选）
│  └─ workflows/            # CI 工作流（Markdown lint/链接检查等）
└─ ...（按主题组织的词条 .md 文件）
```

> **约定**：条目一级标题统一采用 `中文名（English）` 格式；若为诊断/疾病，括号内用标准缩写，如“重度抑郁障碍（MDD）”。

---

## 🚀 快速开始（本地预览）

本仓库采用纯 Markdown + GitHub Pages（在线预览见页首链接）。如果你想在本地预览：

### 方式 A：任意静态服务器

```bash
# 例如使用 Python 简单服务器
cd plurality_wiki
python -m http.server 4173
# 浏览器打开 http://localhost:4173
```

### 方式 B：docsify 本地预览

```bash
npm i -g docsify-cli
docsify serve .
# 浏览器打开提示的本地地址
```

> ⚠️ **npm 权限受限？** 可改用指定 registry：

```bash
# 官方源（默认）
npx --yes --registry=https://registry.npmjs.org docsify-cli@latest serve . --port 4173
# 或使用 npmmirror 镜像
npx --yes --registry=https://registry.npmmirror.com docsify-cli@latest serve . --port 4173
```

### 方式 C：自动兜底脚本（优先 docsify，失败回退 Python）

```bash
python tools/docs_preview.py --port 4173
```

---

## 🧭 贡献（Contribution）

欢迎参与完善！首次贡献建议从 **[CONTRIBUTING.md](./CONTRIBUTING.md)** 开始。

### 简要流程

1. Fork 仓库 & 新建分支（如：`feat/add-did-partial`）。
2. 按**条目规范**撰写或修改文档，并**同步维护** `index.md` 与引用链接。
3. 本地预览（可选），自检通过后提交 PR。
4. 等待 Review 与合并。

### 提交信息规范（推荐）：Conventional Commits

- `feat:` 新增条目/新增章节
- `fix:` 错误修复（链接/引用/格式）
- `docs:` 文档与索引更新（不影响语义）
- `refactor:` 结构与命名重构（不改变内容含义）
- `chore:` 任务脚本、CI、批处理等维护项
- `style:` 空格/缩进/行尾等非语义变更

提交后建议执行以下脚本，检查链接：

```shell
python tools/check_links.py
```

### 更新日志脚本

```shell
# 1) 生成完整 CHANGELOG（从最早 tag 到最新 tag，每段 = PREV..CUR）
python tools/gen_changelog_by_tags.py

# 2) 只生成最近一段（上一个 tag..最新 tag），适合每次发版后更新
python tools/gen_changelog_by_tags.py --latest-only --output changelog_temp.md

# 3) 指定输出位置（默认仓库根目录）
python tools/gen_changelog_by_tags.py --output changelog.md
```

---

## 🧩 写作与风格（摘要版）

- 语言：**简体中文**优先；必要处可保留权威英文术语。
- 结构：一级标题=词条名称；二级/三级标题按内容层级递增。
- 证据：引用**权威来源**（ICD-11、DSM-5-TR、WHO/APA 官方材料、系统综述/指南/高质量综述）。
- 中立：避免夸张或未经验证的断言；区分“事实/证据”“假说/观点”。
- 同步：每次新增/更新条目请同步维护 `index.md` 索引与跳转链接。

---

## 🗺️ 路线图（Roadmap）

- [x] 梳理核心词条的最小完备集（DID, Partial DID, 去人格-现实解体障碍等）
- [x] 建立参考文献与术语表（Glossary）
- [ ] 完成样式统一（警示/信息框、引用块、表格模板）
- [X] 引入基础 CI 校验（Markdown lint/链接有效性）
- [ ] 重写前端页面（修复跳转问题）

---

## 🙌 致谢

感谢所有通过 Issue、PR、讨论参与贡献的人。
👉 欢迎加入贡献者名单（未来会新增 `Contributors.md` 进行致谢）。

---

## 📄 许可证

本项目采用 **MIT License**。请在转载或二次分发时保留版权与许可声明。
