# 多意识体系统 Wiki（Multiple Personality System Wiki）

> 多意识体系统与相关心理健康主题的中文知识库与开源协作项目。
> 本 Wiki 致力于提供中立、客观的信息。所有更新仅面向使用者，不涉及或受社区争议、政治事件、意识形态等因素影响。
> 在线版本：<https://wiki.mpsteam.cn/>

[![Cloudflare Pages](https://img.shields.io/badge/Cloudflare%20Pages-deployed-brightgreen?logo=cloudflare)](https://wiki.mpsteam.cn/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/mps-team-cn/Multiple_personality_system_wiki?style=social)](https://github.com/mps-team-cn/Multiple_personality_system_wiki/stargazers)

---

📖 提示：普通读者请访问在线站点 [wiki.mpsteam.cn](https://wiki.mpsteam.cn/)。本文件主要面向开发者与贡献者。

---

## ✨ 项目目标

- 汇聚与整理多意识体（Multiple Personality System）与相关心理健康主题的高质量中文资料；
- 采用一致的条目规范与贡献流程，确保可维护、可引用、可扩展；
- 面向大众读者与专业人士，兼顾可读性与严谨性（参考 E-E-A-T 原则）。

---

## 🛠️ 技术栈

### 前端与运行环境

- MkDocs Material（静态站点生成器）
- Python ≥ 3.10（构建与工具链）

### 核心插件与特性

- `mkdocs-material` · `pymdown-extensions` · 丰富的 Markdown 语法与组件
- `mkdocs-git-revision-date-localized-plugin` · 基于 Git 的更新时间显示
- `mkdocs-minify-plugin` · HTML/CSS/JS 压缩
- `mkdocs-glightbox` · 图片灯箱
- `mkdocs-exclude` · 构建排除
- `mkdocs-exclude-search` · 搜索索引排除
- `search + jieba` · 中文分词 + 自定义词典（`data/user_dict.txt`）

### 内容管理与部署

- Sveltia CMS（前端 CMS）→ 访问路径：`/admin`([在线后台](https://wiki.mpsteam.cn/admin/))
- Cloudflare Functions（`functions/api/auth.ts`）提供 GitHub OAuth 代理
- Cloudflare Pages：自动构建与部署（构建脚本：`.cfpages-build.sh`）

---

## 📦 仓库结构（精简）

```text
Multiple_personality_system_wiki/
├─ README.md                     # 本说明文件（面向开发者/贡献者）
├─ AGENTS.md                     # 贡献与开发约定（强制遵循）
├─ CONTRIBUTING.md               # 贡献指南（总览）
├─ mkdocs.yml                    # 站点配置（主题/插件/导航）
├─ requirements.txt              # Python 依赖
├─ .cfpages-build.sh             # Cloudflare Pages 构建脚本
│
├─ docs/
│  ├─ index.md                  # 站点首页
│  ├─ Preface.md                # 前言
│  ├─ Glossary.md               # 术语表
│  ├─ tags.md                   # 标签索引
│  ├─ changelog.md              # 变更日志
│  ├─ TEMPLATE_ENTRY.md         # 词条模板（必读）
│  ├─ ADMIN_GUIDE.md            # 管理员指南
│  ├─ GITHUB_WORKFLOW.md        # GitHub 工作流说明
│  ├─ dev/                      # 开发文档
│  ├─ admin/                    # Sveltia CMS（index.html / config.yml / admin.css）
│  ├─ assets/                   # CSS/JS/图标等静态资源（含 mid60 组件）
│  ├─ entries/                  # 词条目录（不创建子目录）
│  ├─ guide/                    # 索引和导览文件目录（不创建子目录）
│  └─ includes/                 # 片段（如缩写表）
│
├─ tools/                       # 维护脚本与辅助工具
│  ├─ fix_markdown.py           # Markdown 自动修复
│  ├─ check_links.py            # 链接规范检查
│  ├─ update_git_timestamps.py  # 从 Git 历史更新 updated 字段
│  └─ pdf_export/               # PDF 导出工具
│
├─ functions/api/auth.ts        # GitHub OAuth 代理（Sveltia CMS 登录）
├─ .github/workflows/           # CI（PR 质量检查 / 合并后自动修复）
└─ releases/                    # 历史版本产物（如 PDF）
```

---

## 🚀 快速开始

推荐使用虚拟环境（或使用 uv）。

### 方式一：虚拟环境（推荐）

```bash

# 1) 创建并激活虚拟环境

python3 -m venv venv
source venv/bin/activate

# 2) 安装依赖

pip install -r requirements.txt

# 3) 本地预览（热重载）

mkdocs serve

# 访问：http://127.0.0.1:8000

```

### 方式二：使用 uv（已提供 uv.lock）

```bash

# 安装依赖并创建隔离环境

uv sync

# 运行本地预览

uv run mkdocs serve
```

### 构建静态站点

```bash

# 标准构建（输出到 site/）

mkdocs build

# 严格模式（有警告即失败）

mkdocs build --strict

# 使用 uv 运行

uv run mkdocs build --strict
```

---

## 🤖 自动化与工具

根目录 `tools/` 提供内容维护工具；完整说明见：`docs/dev/Tools-Index.md`。

- `python3 tools/fix_markdown.py [路径]`：Markdown 自动修复（支持 `--dry-run`）
- `python3 tools/check_links.py [路径]`：链接规范检查（上下文感知）
- `python3 tools/update_git_timestamps.py`：根据 Git 历史更新时间戳
- PDF 导出：`python3 tools/pdf_export/export_to_pdf.py`

CI 双重保障（见 `.github/workflows/`）：

- PR 阶段：`pr-check.yml` 检查「链接规范 + Frontmatter」
- 合并后：`auto-fix-entries.yml` 自动更新时间戳、修复格式并二次校验

---

## 🧭 贡献（Contribution）

欢迎参与完善！首次贡献请阅读：

- 贡献指南：`docs/contributing/index.md`
- 词条模板：`docs/TEMPLATE_ENTRY.md`
- 开发约定：`AGENTS.md`

提交前建议自检：

- 词条放在 `docs/entries/`（不创建子目录）
- Frontmatter 包含 `title / topic / tags`（时间戳由 CI 维护）
- 已运行：`python3 tools/fix_markdown.py docs/entries/`
- 已运行：`python3 tools/check_links.py docs/entries/`
- 构建通过：`mkdocs build --strict`

新增或修改词条时，请同步更新对应主题 Guide（见 `AGENTS.md` 中的映射表）。

---

## 📦 部署

使用 Cloudflare Pages 自动构建与部署：

```yaml
Build command: bash .cfpages-build.sh
Build output directory: site
```

在线地址：<https://wiki.mpsteam.cn/>

---

## 📮 反馈与联系

- 信息反馈：support@mpsteam.cn（内容错误、改进建议、使用问题）
- 官方联系：contact@mpsteam.cn（合作洽谈、媒体咨询、其他事务）
- GitHub Issues：<https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues>

---

## ⭐ Star History

如果喜欢这个项目，请给个 Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=mps-team-cn/Multiple_personality_system_wiki&type=Date)](https://star-history.com/#mps-team-cn/Multiple_personality_system_wiki&Date)
