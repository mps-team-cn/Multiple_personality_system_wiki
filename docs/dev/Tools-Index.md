# 自动化维护工具清单

> **简化版工具索引** - 详细文档已拆分到各专题页面,便于快速查找和维护。

**重要更新**:本项目已从 Docsify 迁移至 MkDocs Material,部分工具的文件路径和使用方式有所调整。

## 🚀 快速开始

### 一键执行日常维护

```bash

# macOS / Linux

bash tools/run_local_updates.sh

# Windows

tools\run_local_updates.bat

# 查看帮助和可用选项

bash tools/run_local_updates.sh --help
```

**执行步骤**:变更日志生成 → PDF 导出 → Markdown 修复 → markdownlint 校验

**可选参数**:`--skip-changelog` `--skip-pdf` `--skip-fix-md` `--skip-markdownlint`

### 常见任务速查

| 任务 | 命令 |
|------|------|
| 修复 Markdown 格式 | `python3 tools/fix_markdown.py docs/entries/` |
| 检查链接规范 | `python3 tools/check_links.py docs/entries/` |
| 检查 Frontmatter | `python3 tools/check_frontmatter.py` |
| 检查标签规范 | `python3 tools/check_tags.py docs/entries/` |
| 清理临时远端分支 | `bash tools/cleanup-remote-branches.sh --dry-run` |
| 更新时间戳 | `python3 tools/update_git_timestamps.py` |
| 标准化标签 | `python3 tools/tag_normalization.py --execute` |
| 生成分区索引 | `python3 tools/build_partitions_cn.py` |
| 生成 SEO URL 列表 | `python3 tools/generate_seo_urls.py` |
| 提交到 Google Indexing API | `python3 tools/submit_to_google_indexing.py` |
| 提交到 IndexNow | `python3 tools/submit_to_indexnow.py --recent 50` |
| 本地预览 | `mkdocs serve` |
| 构建静态站点 | `mkdocs build` |

## 📦 核心自动化工具(CI 集成)

这些工具已集成到 GitHub Actions 工作流,在 PR 检查和合并后自动运行。

| 工具 | 功能 | CI 阶段 | 详细文档 |
|------|------|---------|---------|
| **fix_markdown.py** | 修复 Markdown 格式问题(13 条 Markdownlint 规则 + 6 条中文排版规则) | 合并后 | [查看详情](#markdown-处理器) |
| **check_links.py** | 检查内部链接规范和完整性 | PR + 合并后 | [查看详情](#链接检查工具) |
| **check_frontmatter.py** | 验证词条 Frontmatter 必需字段 | PR | [查看详情](#frontmatter-检查工具) |
| **update_git_timestamps.py** | 根据 Git 历史自动更新 `updated` 字段 | 合并后 | [查看详情](#git-时间戳更新工具) |
| **build_partitions_cn.py** | 生成七大主题分区索引页 | 构建时 | [查看详情](#主题分区索引生成) |

👉 **详细配置和规则说明**:[核心工具详解](Tools-Core.md)

## 🛠️ 手动维护工具(按需使用)

这些工具用于特定维护任务,需要手动运行。

### SEO 优化

| 工具 | 功能 | 使用频率 |
|------|------|---------|
| **check_descriptions.py** | 统计词条 description 字段覆盖率 | 🔍 SEO 审计时 |
| **add_descriptions.py** | 批量为核心词条添加 SEO 描述 | 📝 内容优化时 |
| **generate_seo_urls.py** | 生成高权重 URL 列表用于搜索引擎提交 | 📊 SEO 策略规划时 |
| **submit_to_google_indexing.py** | 使用 Google Indexing API 批量提交 URL | 🚀 新内容发布时 |
| **submit_to_indexnow.py** | 使用 IndexNow 协议推送 URL 到 Bing/Yandex 等 | 🚀 内容更新时(已集成 CI) |

### 搜索优化(jieba 词典管理)

| 工具 | 功能 | 使用频率 |
|------|------|---------|
| **generate_user_dict_from_entries.py** | ⭐ 从词条 Frontmatter 生成 jieba 词典(推荐) | 📝 日常维护 |
| **analyze_search_index.py** | 分析搜索索引,统计词频和 n-gram 分布 | 🔍 词典更新时 |
| **extract_dict_candidates.py** | 从索引提取候选词(可配置阈值) | 📝 词典生成时 |
| **auto_review_candidates.py** | 自动审核候选词并生成优化词典 | ✅ 质量控制时 |
| **test_dict_segmentation.py** | 测试词典的分词效果 | 🧪 验证效果时 |

👉 **完整指南**: [AI 辅助生成搜索词典指南](AI-Dictionary-Generation.md)

### 标签管理

| 工具 | 功能 | 使用频率 |
|------|------|---------|
| **tag_normalization.py** | 批量标准化词条标签,统一分面标签规范 | 🏷️ 标签体系调整时 |
| **check_tags.py** | 校验 Frontmatter 标签是否符合 Tagging Standard v2.0（含前缀、格式与别名识别） | ✅ 日常提交/PR |

### 版本管理

| 工具 | 功能 | 使用频率 |
|------|------|---------|
| **gen_changelog_by_tags.py** | 按 Git 标签生成结构化 changelog | 📅 发布前 |

### 文档导出

| 工具 | 功能 | 使用频率 |
|------|------|---------|
| **pdf_export/** | Pandoc 驱动的整站 PDF 导出 | 📄 归档时 |

注意：
- 为提升 LaTeX 兼容性，PDF 导出会移除 Markdown 删除线（`~~text~~`）标记并将 admonition 标题图标替换为纯文字。
- 标签筛选需遵循标签规范；`dx:` 仅用于诊断/分类，不应作为泛“相关主题”标签使用。
- `check_tags.py` 会同时检查完整标签别名与“名称部分别名”，例如 `dx:PTSD`、`dx:解离性身份障碍` 会被提示改为规范标签。

👉 **详细用法和配置选项**:[手动工具指南](Tools-Manual.md)

## 🧪 开发者工具

### 验证与测试

| 工具 | 功能 |
|------|------|
| **gen-validation-report.py** | 校验词条结构并生成验证报告 |
| **test_dict_segmentation.py** | 测试 jieba 词典分词效果 |

### 部署运维

| 工具 | 功能 |
|------|------|
| **delete-cf-pages-project.js** | Cloudflare Pages 项目批量删除工具 |
| **cleanup-remote-branches.ps1 / cleanup-remote-branches.sh** | 清理符合指定前缀的本地与远端 Git 分支，支持保护分支、预览模式与跳过确认 |

## 🗂️ 工具架构

```text
tools/
├── 核心脚本(独立运行)
│   ├── fix_markdown.py              # Markdown 处理器入口
│   ├── check_links.py               # 链接检查工具
│   ├── check_frontmatter.py         # Frontmatter 验证
│   ├── update_git_timestamps.py     # Git 时间戳同步
│   ├── build_partitions_cn.py       # 分区索引生成
│   └── ...
│
├── 模块化组件
│   ├── processors/                  # 处理器模块
│   │   ├── markdown.py             # Markdown 处理规则
│   │   ├── links.py                # 链接处理逻辑
│   │   └── tags.py                 # 标签处理逻辑
│   ├── validators/                  # 验证器模块
│   ├── generators/                  # 生成器模块
│   └── core/                        # 核心工具库
│       ├── config.py               # 配置管理
│       ├── frontmatter.py          # Frontmatter 解析
│       ├── logger.py               # 日志输出
│       └── utils.py                # 通用工具函数
│
├── 专项工具集
│   ├── pdf_export/                  # PDF 导出工具包
│   └── cli/                         # 命令行接口(未来)
│
└── 废弃工具
    └── deprecated/                  # 已废弃的旧工具
```

## 🔄 迁移后的关键变更

- **词条目录**:从 `entries/` 迁移至 `docs/entries/`(保留根目录 `entries/` 作为同步备份)
- **文档文件**:统一放置在 `docs/` 目录(`README.md`, `CONTRIBUTING/`, `tags.md`, `Glossary.md` 等)
- **静态资源**:从 `assets/` 迁移至 `docs/assets/`
- **构建系统**:使用 `mkdocs build` 替代 Docsify
- **本地预览**:推荐使用 `mkdocs serve` 替代 `docsify serve` 或 `http.server`

## 📚 详细文档

- [**核心工具详解**](../dev/Tools-Core.md) - CI 集成工具的详细配置、规则说明和输出示例
- [**手动工具指南**](../dev/Tools-Manual.md) - SEO、搜索优化、版本管理等手动工具的完整用法
- [**废弃工具说明**](https://github.com/mps-team-cn/Multiple_personality_system_wiki/tree/main/tools/deprecated#readme) - 已废弃工具的迁移指南和保留原因

## 💡 Python 环境配置

推荐通过虚拟环境运行 Python 工具:

```bash
python3 -m venv venv
source venv/bin/activate           # Linux/macOS

# 或 venv\Scripts\activate.bat    # Windows

pip install -r requirements.txt
```

**常见问题**:

- `pip` 缺失 → 使用 `python3 -m pip`
- `externally-managed-environment` 错误 → 必须启用虚拟环境

## 🚨 重要约束

- **CI 双重检查机制**:
    - **PR 阶段**:自动检查链接规范和 Frontmatter 格式,发现问题会阻止合并
    - **合并后**:自动更新时间戳、修复格式、再次验证链接,确保质量
- **时间戳和格式**:推送后 CI 会自动更新,无需手动干预
- **词条 Frontmatter**:`updated` 字段由 CI 自动维护,编辑时无需手动更新

## 📖 相关文档

- [贡献流程与规范](../TEMPLATE_ENTRY.md)
- [技术约定](../contributing/technical-conventions.md)
- [MkDocs 配置说明](../dev/MkDocs-Configuration.md)
- [Cloudflare Pages 部署](../dev/CLOUDFLARE_PAGES.md)
- [SEO 自动化指南](../dev/SEO-Automation.md) ⭐ **新增**
- [性能优化指南](../dev/Performance-Optimization.md)
- [性能测试指南](../dev/Performance-Testing.md)
- [进一步优化建议](../dev/Further-Optimizations.md)
