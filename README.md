# Plurality Wiki

> 多重意识体系统与相关心理健康主题的中文知识库与开源协作项目。
> 在线版本：<https://plurality-wiki.pages.dev/>

- [查看标签索引](docs/tags.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs status](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://plurality-wiki.pages.dev/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/kuliantnt/plurality_wiki?style=social)](https://github.com/kuliantnt/plurality_wiki/stargazers)
[![工作流 状态](https://img.shields.io/github/actions/workflow/status/kuliantnt/plurality_wiki/ci.yml?label=CI&logo=github)](https://github.com/kuliantnt/plurality_wiki/actions/workflows/docs_quality.yml)

---

📖 **提示** ：如果你是普通读者，请访问在线版本 [plurality-wiki.pages.dev](https://plurality-wiki.pages.dev/)；本文档主要面向开发者与贡献者。

---

## ✨ 项目目标

- 汇聚与整理多重意识体（Plurality）与相关心理健康主题的高质量中文资料；
- 采用一致的 **条目规范** 与 **贡献流程** ，确保可维护、可引用、可扩展；
- 面向大众读者与专业人士，兼顾可读性与严谨性（参考 E-E-A-T 原则）。

---

## 🛠️ 技术栈

### 前端框架

- **MkDocs Material** - 现代化静态站点生成器
- **Material Design** - 响应式 UI 组件
- **Python 3.10+** - 构建环境

### 核心插件

- `mkdocs-material` - Material Design 主题
- `mkdocs-git-revision-date-localized-plugin` - 自动获取 Git 更新时间
- `mkdocs-minify-plugin` - HTML/CSS/JS 压缩
- `mkdocs-glightbox` - 图片灯箱效果
- `pymdown-extensions` - Markdown 增强扩展

### 自动化工具

- **Python** - 内容处理、索引生成、校验
- **GitHub Actions** - CI/CD 自动化
- **Cloudflare Pages** - 静态站点托管

---

## 📦 仓库结构

```ini
plurality_wiki/
├─ README.md                     # 开发者说明
├─ CONTRIBUTING.md               # 贡献指南
├─ mkdocs.yml                    # MkDocs 配置文件
├─ requirements-mkdocs.txt       # Python 依赖清单
├─ requirements.txt              # 工具依赖清单
├─ .cfpages-build.sh             # Cloudflare Pages 构建脚本
├─ .gitignore                    # Git 忽略配置
├─ .markdownlint*                # Markdown 规范配置
│
├─ docs/                         # MkDocs 文档目录
│  ├─ index.md                   # 首页（Material 风格）
│  ├─ README.md                  # 关于本站
│  ├─ Preface.md                 # 前言
│  ├─ Glossary.md                # 术语表
│  ├─ tags.md                    # 标签索引
│  ├─ changelog.md               # 变更日志
│  │
│  ├─ entries/                   # 词条正文（142+ 个 Markdown 文件）
│  │
│  ├─ contributing/              # 贡献指南（拆分版本）
│  │  ├─ index.md                # 贡献指南总览
│  │  ├─ 编写规范.md             # 语言、格式规范
│  │  ├─ 学术引用.md             # 引用格式、证据分级
│  │  ├─ 诊断临床规范.md         # 病理学内容要求
│  │  ├─ 技术约定.md             # 文件结构、链接管理
│  │  └─ PR流程.md              # 提交流程、检查清单
│  │
│  ├─ assets/                    # 静态资源
│  │  ├─ extra-material.css      # Material 主题样式
│  │  ├─ extra.js                # 自定义脚本
│  │  ├─ favicon.svg             # 站点图标
│  │  └─ last-updated.json       # 词条更新时间索引
│  │
│  ├─ dev/                       # 开发文档
│  │  ├─ README.md               # 开发文档索引
│  │  ├─ AGENTS.md               # 贡献与开发约定
│  │  ├─ CLOUDFLARE_PAGES.md    # Cloudflare Pages 部署说明
│  │  ├─ MIGRATION_REPORT.md    # Docsify → MkDocs 迁移报告
│  │  ├─ HOMEPAGE_FIX.md        # 首页修复记录
│  │  ├─ THEME_GUIDE.md         # 主题配置指南
│  │  ├─ CSS_GUIDE.md           # 样式开发指南
│  │  └─ INDEX_GUIDE.md         # 索引配置指南
│  │
│  ├─ tools/                     # 工具文档
│  │  └─ README.md               # 工具使用说明
│  │
│  ├─ ADMIN_GUIDE.md             # 维护者手册
│  ├─ GITHUB_WORKFLOW.md         # GitHub 提交流程
│  ├─ TEMPLATE_ENTRY.md          # 词条模板
│  └─ VALIDATION_REPORT.md       # 校对报告（脚本生成）
│
├─ legacy/                       # Docsify 旧版文件存档
│  ├─ README.md                  # 旧版文件说明
│  ├─ index.html                 # Docsify 入口
│  ├─ index.md                   # Docsify 首页
│  ├─ _sidebar.md                # Docsify 侧边栏
│  ├─ _navbar.md                 # Docsify 导航栏
│  └─ ...                        # 其他 Docsify 文件
│
├─ releases/                     # 历史 PDF 版本存档
│  ├─ README.md                  # 版本说明
│  └─ 多意识体wiki v_*.pdf       # 历史版本 PDF
│
├─ entries/                      # 原始词条目录（与 docs/entries/ 同步）
│
├─ tools/                        # 本地维护工具
│  ├─ core/                      # 核心共享模块
│  │  ├─ config.py               # 配置管理
│  │  ├─ frontmatter.py          # Frontmatter 解析
│  │  ├─ logger.py               # 日志系统
│  │  └─ utils.py                # 通用工具函数
│  ├─ processors/                # 内容处理器
│  │  ├─ markdown.py             # Markdown 处理器（整合 3 个工具）
│  │  ├─ links.py                # 链接处理器
│  │  └─ tags.py                 # 标签处理器
│  ├─ generators/                # 生成器模块
│  ├─ validators/                # 校验器模块
│  ├─ cli/                       # CLI 接口
│  ├─ deprecated/                # 已废弃工具（保留历史）
│  ├─ fix_markdown.py            # Markdown 自动修复（主入口）
│  ├─ check_links.py             # 链接检查（上下文感知）
│  ├─ gen-validation-report.py   # 校验词条结构
│  ├─ gen_changelog_by_tags.py   # 基于标签生成变更日志
│  └─ pdf_export/                # PDF 导出工具
│
├─ scripts/
│  └─ gen-last-updated.mjs       # 更新词条时间索引
│
└─ .github/
   ├─ ISSUE_TEMPLATE/
   ├─ PULL_REQUEST_TEMPLATE.md
   └─ workflows/
      ├─ docs_quality.yml        # Markdown/链接检查 CI
      └─ last-updated.yml        # 自动生成 last-updated.json
```

---

## 🤖 自动化维护

根目录下的 `tools/` 目录集中存放了协助批量处理、检查与发布的脚本，可与 CI 流程搭配使用。更完整的说明与后续更新请参见 [`docs/tools/README.md`](docs/tools/README.md)。

### 核心工具

- **`python tools/fix_markdown.py`**：Markdown 格式自动修复
  - 整合了 3 个独立工具（fix_md.py + fix_bold_format.py + fix_list_bold_colon.py）
  - 支持 13 条 Markdownlint 规则 + 5 条中文排版规则
  - 支持预览模式：`--dry-run`

- **`python tools/check_links.py --root .`**：链接有效性检查
  - 上下文感知验证（支持 entries、docs_root、docs_subdir 等不同上下文）
  - 支持尖括号包裹的链接格式 `[text](<url>)`
  - 自动排除文档示例和模板文件

- **`python tools/gen-validation-report.py`**：词条结构校验
  - 读取 CONTRIBUTING.md 与 TEMPLATE_ENTRY.md 生成校对报告

- **`python tools/gen_changelog_by_tags.py --latest-to-head`**：变更日志生成
  - 基于 Git 标签自动生成版本日志

### 已废弃工具

- ~~`python tools/generate_tags_index.py`~~：**[已废弃]** MkDocs Material 的 tags 插件自动处理
- ~~`python tools/build_search_index.py`~~：**[已废弃]** MkDocs 内置搜索功能

---

## 🚀 本地开发

### 环境准备

```bash

# 1. 安装 Python 依赖

pip install -r requirements-mkdocs.txt

# 2. 本地预览（支持热重载）

mkdocs serve

# 访问 http://127.0.0.1:8000

```

### 构建静态站点

```bash

# 构建到 site/ 目录

mkdocs build

# 严格模式构建（有警告则失败）

mkdocs build --strict
```

### 旧版 Docsify 预览（已弃用）

```bash

# 方式 A: 简单 HTTP 服务器

python -m http.server 4173

# 方式 B: Docsify CLI

npm i -g docsify-cli
docsify serve .
```

**注意** ：推荐使用 MkDocs Material 版本，Docsify 版本仅作备份保留。

---

## 🧭 贡献（Contribution）

欢迎参与完善！首次贡献请阅读 **[CONTRIBUTING.md](./CONTRIBUTING.md)** ，并参考下列关键文档：

- [GitHub 提交流程指南](docs/GITHUB_WORKFLOW.md)
- [词条模板](docs/TEMPLATE_ENTRY.md)
- [维护者手册](docs/ADMIN_GUIDE.md)

### 提交流程（简要）

1. Fork & 新建分支；
2. 按规范撰写/修改词条到 `docs/entries/` 目录；
3. **同步更新索引** ：
   - 标签索引由 MkDocs 自动生成，无需手动运行脚本
   - 更新 `docs/index.md` 导航（如需要）
4. **本地验证** ：
   - 执行 `python tools/fix_markdown.py` 自动修复格式
   - 执行 `markdownlint "docs/**/*.md"` 检查
   - 运行 `mkdocs serve` 本地预览
5. 提交 PR，等待 Review。

---

## 🚀 部署

本项目使用 **Cloudflare Pages** 进行部署，详细配置请查看 [CLOUDFLARE_PAGES.md](docs/dev/CLOUDFLARE_PAGES.md)。

**构建配置** ：

```yaml

# Cloudflare Pages 设置

Build command: bash .cfpages-build.sh
Build output directory: site
Environment variables: PYTHON_VERSION=3.11
```

**在线地址** ：<https://plurality-wiki.pages.dev/>

---

## 🗺️ 路线图（Roadmap）

### 已完成 ✅

- [x] 基础 CI（Markdown lint/链接检查）
- [x] 前端框架迁移（Docsify → MkDocs Material）
- [x] 响应式设计与移动端优化
- [x] 深色模式支持
- [x] 搜索功能增强
- [x] 自动化工具重构（tools/ 目录模块化）
- [x] Cloudflare Pages 部署配置
- [x] PDF 导出功能（基于 topic 字段分组）

### 进行中 🚧

- [ ] 完善文档更新（README、AGENTS、CONTRIBUTING 等）
- [ ] 词条内容扩充与质量提升

### 计划中 📋

- [ ] 多版本文档支持（使用 mike）
- [ ] 评论系统集成（Giscus）
- [ ] PWA 离线访问支持
- [ ] 性能优化（图片压缩、CDN 加速）
