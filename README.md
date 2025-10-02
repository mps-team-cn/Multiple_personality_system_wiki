# Plurality Wiki

> 多重意识体系统与相关心理健康主题的中文知识库与开源协作项目。  
> 在线版（GitHub Pages）：<https://kuliantnt.github.io/plurality_wiki/#/>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs status](https://img.shields.io/badge/Wiki-active-brightgreen.svg)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](#贡献)

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
├─ AGENTS.md                # 给 Codex/自动化与人类贡献者的协作约定
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

### 方式 B：docsify 本地预览（如使用 docsify）

```bash
npm i -g docsify-cli
docsify serve .
# 浏览器打开提示的本地地址
```

> ⚠️ **npm 权限受限？** 可以改用 `npx --yes --registry=…` 指定可访问的 registry：

```bash
# 官方源（默认）
npx --yes --registry=https://registry.npmjs.org docsify-cli@latest serve . --port 4173
# 若遇到权限/网络限制，可切换至 npmmirror 镜像
npx --yes --registry=https://registry.npmmirror.com docsify-cli@latest serve . --port 4173
```

### 方式 C：自动兜底脚本（优先 docsify，失败回退 Python）

```bash
python tools/docs_preview.py --port 4173
```

> 脚本会先尝试多 registry 的 `docsify-cli`，无法启动时自动改用 `python -m http.server`。
>
> 如果你采用了其他站点生成器（如 VuePress/VitePress 等），请在 PR 中同步更新说明。

---

## 🧭 贡献（Contribution）

欢迎你参与完善！首次贡献建议从 Wiki 版的《贡献指南》开始：
见 **[CONTRIBUTING.md](./CONTRIBUTING.md)**。

### 简要流程

1. Fork 仓库 & 新建分支（如：`feat/add-did-partial`）。
2. 按**条目规范**撰写或修改文档，并**同步维护** `index.md` 与引用链接。
3. 本地预览（可选），自检通过后提交 PR。
4. 等待 Review 与合并。

### 提交信息规范（推荐）：Conventional Commits

```yaml
feat: 新增条目「部分解离性身份障碍（Partial DID, 6B65）」
fix: 修复 PDF 导航目录重复的问题
docs: 调整 index.md 索引与链接
refactor: 统一小节标题层级
```

提交后建议执行以下脚本，检查是否有链接问题

```shell
python tools/check_links.py
```

---

## 🧩 写作与风格（摘要版）

- 语言：**简体中文**优先；必要处可保留权威英文术语。
- 结构：一级标题=词条名称；二级/三级标题按内容层级递增。
- 证据：引用**权威来源**（ICD-11、DSM-5-TR、WHO/APA 官方材料、系统综述/指南/高质量综述）。
- 中立：避免夸张或未经验证的断言；区分“事实/证据”“假说/观点”。
- 同步：每次新增/更新条目请同步更新 `index.md` 目录索引与跳转链接。

> 完整版规则、模板与示例请见 Wiki 页的《贡献指南》。

---

## 🗺️ 路线图（Roadmap）

- [ ] 梳理核心词条的**最小完备集**（DID, Partial DID, 去人格-现实解体障碍等）
- [x] 建立**参考文献与术语表**（Glossary）
- [ ] 完成**样式统一**（警示/信息框、引用块、表格模板）
- [ ] 引入**基础 CI 校验**（Markdown lint/链接有效性）
- [ ] 重写**前端页面**(已知跳转问题)

---

## 📄 许可证

本项目采用 **MIT License**。请在转载或二次分发时保留版权与许可声明。
