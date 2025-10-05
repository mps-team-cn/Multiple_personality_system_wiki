# 自动化维护工具清单

> 本目录用于集中维护仓库中各类自动化脚本的说明与使用示例，便于在 README 与 docs 之间保持一致。

**重要更新**：本项目已从 Docsify 迁移至 MkDocs Material，部分工具的文件路径和使用方式有所调整。

## 🔄 迁移后的关键变更

- **词条目录**：从 `entries/` 迁移至 `docs/entries/`（保留根目录 `entries/` 作为同步备份）
- **文档文件**：统一放置在 `docs/` 目录（`README.md`, `CONTRIBUTING.md`, `tags.md`, `Glossary.md` 等）
- **静态资源**：从 `assets/` 迁移至 `docs/assets/`
- **构建系统**：使用 `mkdocs build` 替代 Docsify
- **本地预览**：推荐使用 `mkdocs serve` 替代 `docsify serve` 或 `http.server`

## 工具概览

### 核心处理器模块(重构后)

| 模块 | 功能摘要 | 常用用法 |
| --- | --- | --- |
| `tools/processors/markdown.py` | 统一的 Markdown 处理器,支持可配置的修复规则(MD009/MD012/MD022/MD028/MD034/MD040/MD047) | `python -m tools.processors.markdown` (开发中) |
| `tools/processors/links.py` | 链接检查器,验证内部链接完整性和格式规范 | `python -m tools.processors.links` (开发中) |
| `tools/processors/tags.py` | 标签处理器,提供智能标签提取、归一化和索引生成 | `python -m tools.processors.tags` (开发中) |

### 传统脚本(保留兼容)

| 脚本/模块 | 功能摘要 | 常用用法 |
| --- | --- | --- |
| `tools/fix_md.py` | 批量修复 Markdown 常见 Lint 问题，涵盖行尾空格、标题前后空行、围栏语言补全等 | `python tools/fix_md.py` 或 `python tools/fix_md.py --dry-run` |
| `tools/check_links.py` | 扫描 Markdown 文档中疑似内部链接写法，禁止 `./`、`../` 等相对路径 | `python tools/check_links.py --root .`，必要时配合 `--whitelist` |
| `tools/docs_preview.py` | 本地预览辅助：默认启动 `python -m http.server`，可选 `--docsify` 启用 docsify-cli | `python tools/docs_preview.py --port 4173`（启用 docsify 时追加 `--docsify`） |
| `tools/gen_changelog_by_tags.py` | 按 Git 标签时间顺序生成 `changelog.md` 并按提交类型分组 | `python tools/gen_changelog_by_tags.py --output changelog.md`，可加 `--latest-only`/`--latest-to-head` |
| `tools/pdf_export/` | Pandoc 驱动的整站 PDF 导出工具，支持封面、忽略列表与中文字体 | `python tools/pdf_export/export_to_pdf.py` 或 `python -m pdf_export` |
| `tools/gen-validation-report.py` | 校验词条结构并生成 `docs/VALIDATION_REPORT.md` | `python tools/gen-validation-report.py` |
| `tools/retag_and_related.py` | 批量重建 Frontmatter 标签并生成"相关词条"区块 | `python tools/retag_and_related.py` 或 `python tools/retag_and_related.py --dry-run --limit 5` |
| `tools/run_local_updates.sh` / `tools/run_local_updates.bat` | 串联常用维护脚本，一键完成日常更新任务（已增强：支持参数跳过、进度显示、错误提示） | `bash tools/run_local_updates.sh` 或 `tools\run_local_updates.bat`（均支持 `--skip-*` 选项和 `--help`） |
| `tools/build_search_index.py` | 解析词条 Frontmatter，同步生成带同义词与拼音归一化的 Docsify 搜索索引 JSON | `python tools/build_search_index.py` 或 `python tools/build_search_index.py --output assets/search-index.json` |
| `generate_tags_index.py` | 扫描 Frontmatter 标签并生成 `tags.md` 索引 | `python tools/generate_tags_index.py` |

如需新增脚本，请保持功能说明与示例用法同步更新本章节，方便贡献者快速定位维护工具。

### `retag_and_related.py` 标签过滤策略

- 自 2025 年起，脚本会自动忽略以“与”“在”“用于”等功能性词汇开头的段落标题，避免将“与治疗协作”“在多意识体语境中的使用”这类结构性语句当作标签；
- 对仅包含数字或纯中文空格组合的候选标签进行过滤，减少“1957”“与性别 年龄表达”等无效标签；
- 仍保留既有 Frontmatter 标签的权重优势，运行脚本不会意外删除手动维护的核心标签。
- 遍历范围限定为 `entries/*.md`，避免将草稿或二级目录误当作正式词条；
- 会读取根目录的 `index.md`，将词条所在分区视为优先级较高的候选标签（若分区为“未分类”则自动跳过）；
- “相关条目”区块在得分相同时会按词条英文标题排序，输出顺序更加稳定。

## 新处理器模块详解

### 📦 Markdown 处理器 (`processors/markdown.py`)

**功能特性:**

- 支持 7 种 Markdown Lint 规则修复
- 可配置的规则启用/禁用
- 批量处理能力
- 预览模式(dry-run)
- 详细的处理结果报告

**支持的修复规则:**

- **MD009**: 移除行尾空白字符(包括全角空格)
- **MD012**: 压缩连续空行为单行
- **MD022**: 确保标题前后空行
- **MD028**: 修复引用块中的空行
- **MD034**: 转换裸链接为标准格式
- **MD040**: 为代码围栏添加语言标注
- **MD047**: 确保文件以单个换行结束

**编程接口:**

```python
from tools.processors.markdown import MarkdownProcessor, fix_markdown_file

# 使用处理器类

processor = MarkdownProcessor()
result = processor.process_file(Path("entries/example.md"))

# 使用便捷函数

result = fix_markdown_file("entries/example.md", dry_run=True)
```

### 🔗 链接处理器 (`processors/links.py`)

**功能特性:**

- 内部链接完整性验证
- 相对路径检测
- 白名单管理
- 详细的违规报告
- 批量检查能力

**检查规则:**

- 禁止使用 `./` 或 `../` 相对路径
- 要求 entries 目录下的链接使用 `entries/*.md` 完整路径
- 支持根目录白名单文件(如 `index.md`, `CONTRIBUTING.md`)
- 支持 `docs/` 前缀的文档链接
- 自动跳过外部链接、锚点和图片

**编程接口:**

```python
from tools.processors.links import LinkProcessor, check_links_in_file

# 使用处理器类

processor = LinkProcessor(extra_whitelist={"custom.md"})
result = processor.check_file(Path("entries/example.md"), repo_root=Path("."))

# 使用便捷函数

result = check_links_in_file("entries/example.md", repo_root=".")
```

### 🏷️ 标签处理器 (`processors/tags.py`)

**功能特性:**

- 智能标签提取(从 Frontmatter、标题、内容)
- 同义词归一化
- 停用词过滤
- 标签索引生成
- 可配置的权重系统

**核心功能:**

- **标签归一化**: 统一格式、应用同义词映射、大小写处理
- **智能提取**: 从多个来源提取并按权重排序
- **有效性验证**: 过滤无效标签(过长、纯数字、停用词等)
- **索引生成**: 生成按标签分类的词条索引

**编程接口:**

```python
from tools.processors.tags import TagProcessor, generate_tags, generate_tags_index

# 使用处理器类

processor = TagProcessor()
result = processor.generate_tags_for_file(Path("entries/example.md"))

# 使用便捷函数

result = generate_tags("entries/example.md", dry_run=True)

# 生成标签索引

index_content = generate_tags_index("entries/", output_path="tags.md")
```

## 使用建议

### 🏃 一键执行日常维护

```bash

# macOS / Linux 默认执行全部步骤

bash tools/run_local_updates.sh

# macOS / Linux 查看帮助信息

bash tools/run_local_updates.sh --help

# macOS / Linux 跳过特定步骤

bash tools/run_local_updates.sh --skip-pdf --skip-markdownlint

# Windows 等效执行方式

tools\run_local_updates.bat

# Windows 查看帮助

tools\run_local_updates.bat --help

# Windows 同样可叠加跳过参数

tools\run_local_updates.bat --skip-pdf --skip-markdownlint
```

**功能特性:**

- 自动切换到仓库根目录
- 按顺序执行 8 个维护步骤
- 支持单独跳过任意步骤
- 显示执行进度和错误提示
- 完整的帮助信息
- UTF-8 编码支持(`.bat` 文件在 Windows CMD/PowerShell 中可正确显示中文)

**注意事项:**

- Windows 用户建议在 CMD 或 PowerShell 中运行 `.bat` 文件以获得最佳显示效果
- Git Bash 用户可以使用 `.sh` 版本获得更好的兼容性
- 所有步骤失败时会显示警告但不会中断后续步骤

**执行步骤:**

1. 生成变更日志 (`gen_changelog_by_tags.py`)
2. 刷新标签与相关词条 (`retag_and_related.py`)
3. 生成最后更新时间索引 (`gen-last-updated.mjs`)
4. 导出 PDF (`pdf_export/export_to_pdf.py`)
5. 生成标签索引 (`generate_tags_index.py`)
6. 生成搜索索引 (`build_search_index.py`)
7. 自动修复 Markdown (`fix_md.py`)
8. 运行 markdownlint 校验

**可用的跳过选项:**

- `--skip-changelog` - 跳过变更日志生成
- `--skip-retag` - 跳过标签与关联词条重建
- `--skip-last-updated` - 跳过最后更新时间索引生成
- `--skip-pdf` - 跳过 PDF 导出
- `--skip-tag-index` - 跳过标签索引生成
- `--skip-search-index` - 跳过搜索索引生成
- `--skip-fix-md` - 跳过 Markdown 自动修复
- `--skip-markdownlint` - 跳过 markdownlint 校验

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
- GitHub Actions 工作流 `.github/workflows/last-updated.yml` 在推送 `main` 分支或手动触发时自动运行上述脚本并提交最新索引；
- 前端在 `index.html` 内置 Docsify 插件，会在每篇词条标题下渲染形如 `🕒 最后更新：2025/10/02 12:34:56（abc1234）` 的提示；
- `tools/pdf_export/` 的导出流程同样会读取该索引，并在离线 PDF 中展示相同的最后更新时间提示；
- 如需强制刷新缓存，可重新触发工作流或在部署平台清除静态资源缓存。

### 标签索引维护

- `python tools/generate_tags_index.py` 会解析词条 Frontmatter 中的 `tags`，按标签分组生成 `tags.md`；
- 更新或新增词条后务必重新运行该脚本，确保索引与仓库内容一致；
- CI 会在 PR 中执行脚本并检查 `tags.md` 是否最新。

### 搜索索引维护

- `python tools/build_search_index.py` 会读取 `entries/` 下的 Frontmatter，将 `title`、`synonyms` 与自动生成的拼音写入 `assets/search-index.json`；
- 运行脚本后即可在本地预览中体验大小写不敏感、拼音与别名匹配的搜索结果；
- 如需输出到其他位置，可使用 `--output` 参数覆盖默认生成路径。

### PDF 导出目录生成逻辑

- `tools/pdf_export/` 在导出 PDF 时会优先读取仓库根目录的 `index.md`，目录页与章节书签都会遵循该文件的分组与顺序；
- 若 `index.md` 缺失或未收录全部词条，未出现在目录中的文档会自动归入“未索引词条”章节，确保不会遗漏内容；
- 目录中的词条链接会自动重写为 PDF 内部锚点，确保离线文档中的跳转行为与线上一致。
- `index.md` 中通过 `<!-- trigger-warning:start -->…<!-- trigger-warning:end -->` 包裹的触发警告区块，会在导出时转换为 `> ⚠️ …` 的 Markdown 形式，确保目录页在 PDF 中保留警示文本。
- 词条 Frontmatter 的 `updated` 字段支持 `YYYY-MM-DD` 字符串或 YAML 日期字面量，若留空、写成 `null`、布尔值或列表，导出脚本会终止并提示修正。

## 相关文档

- [导出 PDF 使用指南](../pdf_export/README_pdf_output.md)
- [贡献流程与规范](../TEMPLATE_ENTRY.md)
- [维护者手册](../ADMIN_GUIDE.md)
