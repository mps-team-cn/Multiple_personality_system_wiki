# 自动化维护工具清单

> 本目录用于集中维护仓库中各类自动化脚本的说明与使用示例，便于在 README 与 docs 之间保持一致。

**重要更新** ：本项目已从 Docsify 迁移至 MkDocs Material，部分工具的文件路径和使用方式有所调整。

## 🔄 迁移后的关键变更

- **词条目录** ：从 `entries/` 迁移至 `docs/entries/`（保留根目录 `entries/` 作为同步备份）
- **文档文件** ：统一放置在 `docs/` 目录（`README.md`, `CONTRIBUTING/`, `tags.md`, `Glossary.md` 等）
- **静态资源** ：从 `assets/` 迁移至 `docs/assets/`
- **构建系统** ：使用 `mkdocs build` 替代 Docsify
- **本地预览** ：推荐使用 `mkdocs serve` 替代 `docsify serve` 或 `http.server`

## 工具概览

### 核心处理器模块(重构后)

| 模块                          | 功能摘要                                                                                                     | 常用用法                                         |
| --------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `tools/fix_markdown.py`     | 统一的 Markdown 处理器,整合了 fix_md、fix_bold_format、fix_list_bold_colon 的所有功能,支持 13 条 Markdownlint 规则和 6 条中文排版规则 | `python tools/fix_markdown.py docs/entries/` |
| `tools/processors/links.py` | 链接检查器,验证内部链接完整性和格式规范                                                                                     | `python -m tools.processors.links` (开发中)     |
| `tools/processors/tags.py`  | 标签处理器,提供智能标签提取、归一化和索引生成                                                                                  | `python -m tools.processors.tags` (开发中)      |

### 传统脚本(保留兼容)

| 脚本/模块                                                        | 功能摘要                                                              | 常用用法                                                                                                |
| ------------------------------------------------------------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `tools/check_links.py`                                       | 扫描 Markdown 文档中疑似内部链接写法，禁止 `./`、`../` 等相对路径                       | `python tools/check_links.py --root .`，必要时配合 `--whitelist`                                          |
| `tools/docs_preview.py`                                      | 本地预览辅助：默认启动 `python -m http.server`，可选 `--docsify` 启用 docsify-cli | `python tools/docs_preview.py --port 4173`（启用 docsify 时追加 `--docsify`）                              |
| `tools/gen_changelog_by_tags.py`                             | 按 Git 标签时间顺序生成 `changelog.md` 并按提交类型分组                            | `python tools/gen_changelog_by_tags.py --output changelog.md`，可加 `--latest-only`/`--latest-to-head` |
| `tools/pdf_export/`                                          | Pandoc 驱动的整站 PDF 导出工具，支持封面、忽略列表、中文字体与带页码的 topic 目录                | `python tools/pdf_export/export_to_pdf.py` 或 `python -m pdf_export`                                 |
| `tools/gen-validation-report.py`                             | 校验词条结构并生成 `docs/VALIDATION_REPORT.md`                             | `python tools/gen-validation-report.py`                                                             |
| `tools/retag_and_related.py`                                 | 批量重建 Frontmatter 标签并生成"相关词条"区块                                    | `python tools/retag_and_related.py` 或 `python tools/retag_and_related.py --dry-run --limit 5`       |
| `tools/run_local_updates.sh` / `tools/run_local_updates.bat` | 串联常用维护脚本，一键完成日常更新任务（已增强：支持参数跳过、进度显示、错误提示）                         | `bash tools/run_local_updates.sh` 或 `tools\run_local_updates.bat`（均支持 `--skip-*` 选项和 `--help`）      |

如需新增脚本，请保持功能说明与示例用法同步更新本章节，方便贡献者快速定位维护工具。

### 部署运维工具

| 脚本/模块                                | 功能摘要                                                                                       | 常用用法                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `tools/update_git_timestamps.py`     | 根据 Git 历史记录自动更新词条的 `updated` 字段，确保时间戳与实际修改记录一致                                              | `python tools/update_git_timestamps.py` 或 `python tools/update_git_timestamps.py --dry-run` |
| `tools/delete-cf-pages-project.js` | Cloudflare Pages 项目批量删除工具，支持分页获取、并发删除、保留最新 production 部署、强制删除别名部署                      | `CF_API_TOKEN="..." CF_ACCOUNT_ID="..." CF_PAGES_PROJECT="..." node tools/delete-cf-pages-project.js` |

### `retag_and_related.py` 标签过滤策略

- 自 2025 年起，脚本会自动忽略以“与”“在”“用于”等功能性词汇开头的段落标题，避免将“与治疗协作”“在多意识体语境中的使用”这类结构性语句当作标签；
- 对仅包含数字或纯中文空格组合的候选标签进行过滤，减少“1957”“与性别 年龄表达”等无效标签；
- 仍保留既有 Frontmatter 标签的权重优势，运行脚本不会意外删除手动维护的核心标签。
- 遍历范围限定为 `entries/*.md`，避免将草稿或二级目录误当作正式词条；
- 会读取根目录的 `index.md`，将词条所在分区视为优先级较高的候选标签（若分区为“未分类”则自动跳过）；
- “相关条目”区块在得分相同时会按词条英文标题排序，输出顺序更加稳定。

## 新处理器模块详解

### 📦 Markdown 处理器 (`tools/fix_markdown.py`)

**功能特性:**

- 整合了 3 个独立工具的所有功能 (fix_markdown.py, fix_bold_format.py, fix_list_bold_colon.py)
- 支持 13 条 Markdownlint 规则 + 6 条中文排版规则
- 批量处理能力
- 预览模式 (--dry-run)
- 详细的处理结果报告

**支持的修复规则:**

**Markdownlint 标准规则:**

- **MD009**: 移除行尾空白字符 (包括全角空格)
- **MD012**: 压缩连续空行为单行
- **MD022**: 确保标题前后空行
- **MD028**: 修复引用块中的空行
- **MD031**: 确保代码块前后空行
- **MD032**: 确保列表前后空行
- **MD034**: 转换裸链接为标准格式
- **MD037**: 修复强调标记内空格 (增强版，支持中文标点)
- **MD040**: 为代码围栏添加语言标注
- **MD047**: 确保文件以单个换行结束

**中文排版规则:**

- **CUSTOM001**: 列表标记空格 (`-item` → `- item`)
- **CUSTOM002**: 加粗中文空格 (`中文 **加粗** 后面` → `中文 **加粗** 后面`)
- **CUSTOM003**: 列表加粗冒号 (`-**text**: ` → `- **text** : `)
- **CUSTOM004**: 链接括号转换 (中文括号 → 英文括号，加粗链接格式)
- **CUSTOM005**: 链接前冒号 (`参考：[链接]` → `参考：[链接]`)
- **CUSTOM006**: 嵌套列表缩进 (2空格 → 4空格，MkDocs 要求)

**命令行用法:**

```bash

# 处理单个文件

python tools/fix_markdown.py docs/entries/Tulpa.md

# 处理整个目录

python tools/fix_markdown.py docs/entries/

# 预览模式（不实际修改）

python tools/fix_markdown.py docs/entries/ --dry-run

# 详细输出

python tools/fix_markdown.py docs/entries/ --verbose
```

**编程接口:**

```python
from tools.processors.markdown import MarkdownProcessor, fix_markdown_file

# 使用处理器类

processor = MarkdownProcessor()
result = processor.process_file(Path("docs/entries/example.md"))

# 使用便捷函数

result = fix_markdown_file("docs/entries/example.md", dry_run=True)

# 处理文本字符串

text = "**加粗**后面"
fixed = processor.process(text)  # "**加粗** 后面"
```

### 🔗 链接处理器 (`processors/links.py`)

**功能特性:**

- 内部链接完整性验证
- 相对路径检测
- 白名单管理
- 详细的违规报告
- 批量检查能力

**检查规则:**

- 词条之间的链接：直接使用文件名（如 `DID.md`），无需 `entries/` 前缀
- 词条链接到根目录文档：使用 `../` 相对路径（如 `../CONTRIBUTING/index.md`）
- 根目录文档链接到词条：使用 `entries/` 前缀（如 `entries/DID.md`）
- 禁止使用 `./` 等模糊路径
- 支持根目录白名单文件验证
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

- **标签归一化** : 统一格式、应用同义词映射、大小写处理
- **智能提取** : 从多个来源提取并按权重排序
- **有效性验证** : 过滤无效标签(过长、纯数字、停用词等)
- **索引生成** : 生成按标签分类的词条索引

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
5. ~~生成标签索引 (`generate_tags_index.py`)~~ **[已废弃]** MkDocs 自动处理
6. ~~生成搜索索引 (`build_search_index.py`)~~ **[已废弃]** MkDocs 内置搜索
7. 自动修复 Markdown (`fix_markdown.py`)
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

# 使用新的统一工具（推荐）

python tools/fix_markdown.py docs/entries/

# 预览模式

python tools/fix_markdown.py docs/entries/ --dry-run

# 详细输出

python tools/fix_markdown.py docs/entries/ --verbose

# 校验（需安装 markdownlint-cli）

markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
```

> Windows 可用 `py tools/fix_markdown.py`，运行环境需 Python 3.10 及以上。

**统一工具优势:**

- ✅ 整合了 3 个独立工具的所有功能
- ✅ 支持 13 条 Markdownlint 规则 + 6 条中文排版规则
- ✅ 一次运行完成所有修复
- ✅ 智能处理中文标点，避免误加空格
- ✅ 完整的预览和详细输出模式

**常见修复示例:**

```markdown

# 列表标记空格

-item → - item

# 加粗中文空格

中文**加粗**后面 → 中文 **加粗** 后面

# 列表加粗冒号

- **text** : → - **text** :

# 链接前冒号

参考：[链接] → 参考：[链接]

# 加粗标点不加空格（正确保持）

**定义**：内容 → **定义**：内容

# 嵌套列表缩进（MkDocs 要求 4 空格）

- 主列表项
  - 子列表项  →  - 主列表项
                      - 子列表项

```

### 词条最后更新时间索引

- `scripts/gen-last-updated.mjs` 会遍历 `entries/` 下的所有 Markdown 词条，读取 Git 最后提交时间与提交哈希，并生成 `assets/last-updated.json` 索引文件；
- GitHub Actions 工作流 `.github/workflows/last-updated.yml` 在推送 `main` 分支或手动触发时自动运行上述脚本并提交最新索引；
- 前端在 `index.html` 内置 Docsify 插件，会在每篇词条标题下渲染形如 `🕒 最后更新：2025/10/02 12:34:56（abc1234）` 的提示；
- `tools/pdf_export/` 的导出流程同样会读取该索引，并在离线 PDF 中展示相同的最后更新时间提示；
- 如需强制刷新缓存，可重新触发工作流或在部署平台清除静态资源缓存。

### 标签索引维护 **[已自动化]**

> ⚠️ **迁移后变更** ：MkDocs Material 的 `tags` 插件会自动处理标签索引，无需手动运行脚本。

- MkDocs 会自动从词条 Frontmatter 读取 `tags` 字段
- 构建时自动生成 `tags.md` 标签索引页面
- 配置位置：`mkdocs.yml` 中的 `plugins.tags.tags_file`
- 只需在词条中正确填写 `tags`，构建时自动更新索引

**传统方式（已废弃）：**

- ~~`python tools/generate_tags_index.py`~~ - 不再需要手动运行
- ~~CI 检查 `tags.md` 是否最新~~ - MkDocs 自动处理

### 搜索索引维护 **[已自动化]**

> ⚠️ **迁移后变更** ：MkDocs Material 使用内置搜索插件，支持中文分词和智能建议。

- MkDocs 构建时自动生成搜索索引
- 支持中文、英文分词和搜索建议
- 配置位置：`mkdocs.yml` 中的 `plugins.search`
- 无需手动维护搜索索引文件

**传统方式（已废弃）：**

- ~~`python tools/build_search_index.py`~~ - Docsify 专用，已不再使用
- ~~`assets/search-index.json`~~ - MkDocs 使用自己的索引格式

### 🔍 AI 辅助搜索词典生成工具

**背景**：MkDocs 搜索使用 jieba 分词，需要自定义词典（`data/user_dict.txt`）来优化专业术语的识别。搜索索引约 3MB，无法一次性交给 AI 处理，因此采用 **预处理 + AI 审核 + 自动优化** 的三阶段方案。

**核心工具链**：

| 工具脚本 | 功能说明 | 用法示例 |
|---------|---------|---------|
| `analyze_search_index.py` | 分析搜索索引，统计词频和 n-gram 分布 | `python3 tools/analyze_search_index.py --input site/search/search_index.json --stats` |
| `extract_dict_candidates.py` | 从索引提取候选词（可配置频率、长度阈值） | `python3 tools/extract_dict_candidates.py --input site/search/search_index.json --min-freq 3` |
| `split_candidates.py` | 将候选词分批，便于 AI 审核（每批 50-100KB） | `python3 tools/split_candidates.py --input data/candidates.txt --batch-size 150` |
| `auto_review_candidates.py` | 自动审核候选词并生成优化词典（基于规则） | `python3 tools/auto_review_candidates.py --input data/candidates.txt --stats` |
| `test_dict_segmentation.py` | 测试词典的分词效果（内置测试套件） | `python3 tools/test_dict_segmentation.py --dict data/user_dict.txt --test-suite` |

**快速上手**：

```bash

# 1. 构建搜索索引

mkdocs build

# 2. 分析索引并提取候选词

python3 tools/extract_dict_candidates.py \
  --input site/search/search_index.json \
  --output data/candidates.txt \
  --min-freq 3

# 3. 自动审核并生成优化词典

python3 tools/auto_review_candidates.py \
  --input data/candidates.txt \
  --output data/user_dict_reviewed.txt \
  --stats

# 4. 测试分词效果

python3 tools/test_dict_segmentation.py \
  --dict data/user_dict_reviewed.txt \
  --test-suite

# 5. 应用新词典

cp data/user_dict_reviewed.txt data/user_dict.txt
mkdocs build  # 重新构建
```

**审核规则**（`auto_review_candidates.py`）：

1. **保留**：
    - 专业术语（障碍、疗法、诊断、解离性、创伤后等）
    - 核心复合词（解离性身份障碍、多意识体系统、系统内沟通等）
    - 重要缩写（DID、OSDD、PTSD 等）

2. **优化**：
    - 核心术语提升至 5000-8000 权重
    - 专业复合词提升至 2000-3000 权重
    - 通用短词降权至 500-1000

3. **删除**：
    - 片段词（如 "离性"、"识体"）
    - 通用词（如 "可能"、"使用"、"其他"）
    - 单字词和过长词组

**分词效果示例**：

```text
输入: 解离性身份障碍是一种多意识体系统
输出: 解离性身份障碍 / 是 / 一种 / 多意识体系统

输入: 心理治疗和情绪调节技巧有助于管理症状
输出: 心理治疗 / 和 / 情绪调节 / 技巧 / 有助于 / 管理 / 症状
```

**详细文档**：

- 完整流程说明：[docs/dev/AI-Dictionary-Generation.md](../dev/AI-Dictionary-Generation.md)
- 包含三阶段详细步骤、AI 审核 Prompt 模板、质量控制策略

### PDF 导出目录生成逻辑

- `tools/pdf_export/` 会读取词条 Frontmatter 中的 `topic` 字段自动构建章节顺序，缺失 `topic` 的词条将归入“其他”分类，并按 topic 字典序排序；
- 默认忽略列表来自 `tools/pdf_export/ignore.md`，支持目录、单个文件与通配符匹配，可通过 `--ignore-file` 自定义路径；
- 目录页会基于上述章节生成带页码的“图书式”排版，条目与页码均可点击跳转至对应内容；
- 目录中的词条链接会自动重写为 PDF 内部锚点，确保离线文档中的跳转行为与线上一致。
- 词条 Frontmatter 的 `updated` 字段支持 `YYYY-MM-DD` 字符串或 YAML 日期字面量，若留空、写成 `null`、布尔值或列表，导出脚本会终止并提示修正。

### 🕒 Git 时间戳自动更新工具

**背景：** 词条的 `updated` 字段应反映真实的最后修改时间，手动维护容易遗漏或不准确。通过读取 Git 历史记录，可以自动同步时间戳。

**功能特性：**

- ✅ 自动读取文件在 Git 中的最后提交时间
- ✅ 批量更新 `docs/entries/` 下的所有词条
- ✅ 支持单文件或目录处理
- ✅ 预览模式 (`--dry-run`)，可在修改前查看变更
- ✅ 详细输出模式 (`--verbose`)，显示所有文件状态
- ✅ 智能跳过未修改和未提交的文件
- ✅ 自动添加或更新 Frontmatter 中的 `updated` 字段

**使用示例：**

```bash
# 更新所有词条（默认处理 docs/entries/）
python tools/update_git_timestamps.py

# 预览模式（不实际修改文件）
python tools/update_git_timestamps.py --dry-run

# 详细输出（显示所有文件状态，包括未修改的）
python tools/update_git_timestamps.py --verbose

# 更新指定文件
python tools/update_git_timestamps.py docs/entries/DID.md

# 更新指定目录
python tools/update_git_timestamps.py docs/entries/

# 组合使用
python tools/update_git_timestamps.py --dry-run --verbose
```

**输出示例：**

```text
📊 更新模式: 找到 125 个词条文件
================================================================================
Attachment-Theory.md                               ✅ 已更新: 2025-10-05 → 2025-10-11
DID.md                                             ✓ 已是最新: 2025-10-11
Dissociation.md                                    ✓ 已是最新: 2025-10-08
Tulpa.md                                           🔄 将更新: 2025-09-28 → 2025-10-10
OSDD.md                                            ⚠️  跳过: 无法获取 Git 时间戳 (可能未提交)
...
================================================================================
✨ 完成!
   - 已修改: 23 个文件
   - 已跳过: 102 个文件
   - 总计: 125 个文件
```

**工作原理：**

1. 使用 `git log -1 --format=%ai` 获取文件的最后提交时间
2. 解析 Markdown 文件的 Frontmatter
3. 比较现有的 `updated` 字段与 Git 时间戳
4. 如果不一致，更新 Frontmatter 中的 `updated` 字段
5. 保持文件的其他内容不变

**注意事项：**

- ⚠️ 只处理已提交到 Git 的文件，新创建未提交的文件会被跳过
- ⚠️ 需要在 Git 仓库中运行
- ⚠️ 如果 Frontmatter 中没有 `updated` 字段，会自动添加
- ⚠️ 时间格式为 `YYYY-MM-DD`（与项目标准一致）
- 💡 建议在大量修改前先使用 `--dry-run` 预览

**集成到工作流：**

可以在 `tools/run_local_updates.sh` 中添加此工具，确保每次维护时自动同步时间戳：

```bash
echo "📅 更新 Git 时间戳..."
python3 tools/update_git_timestamps.py
```

### 🚀 Cloudflare Pages 项目删除工具

**背景：** Cloudflare Pages 项目如果包含大量部署（通常 > 100），无法直接通过 Dashboard 或 API 删除，需要先批量删除部署。

**功能特性：**

- ✅ 自动分页获取所有部署（API 限制每页最多 25 条）
- ✅ 支持并发批量删除（默认每批 5 个）
- ✅ 可选保留最新 production 部署（默认保留）
- ✅ 强制删除别名部署（自动添加 `?force=true` 参数）
- ✅ 详细的进度显示和错误处理
- ✅ 删除完成后自动清理项目

**环境变量配置：**

```bash

# 必需的环境变量

export CF_API_TOKEN="your-cloudflare-api-token"      # Cloudflare API Token
export CF_ACCOUNT_ID="your-account-id"               # Cloudflare Account ID
export CF_PAGES_PROJECT="your-project-name"          # Pages 项目名称

# 可选配置

export KEEP_PRODUCTION="true"   # 是否保留最新 production 部署（默认 true）
```

**获取 API Token：**

1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. 点击 "Create Token" → "Edit Cloudflare Workers" 模板
3. 权限设置：Account - Cloudflare Pages - Edit
4. 复制生成的 Token

**使用示例：**

```bash

# 方式 1: 设置环境变量后运行

export CF_API_TOKEN="G1r-bNax-xxxXxxXxxXxxXxxXxxXxxXxx"
export CF_ACCOUNT_ID="873xxxxxxxxxxxxxxxxxxxxxxxc5"
export CF_PAGES_PROJECT="my-project"
node tools/delete-cf-pages-project.js

# 方式 2: 单行执行

CF_API_TOKEN="..." CF_ACCOUNT_ID="..." CF_PAGES_PROJECT="my-project" \
  node tools/delete-cf-pages-project.js

# 方式 3: 删除所有部署（不保留 production）

export KEEP_PRODUCTION="false"
CF_API_TOKEN="..." CF_ACCOUNT_ID="..." CF_PAGES_PROJECT="my-project" \
  node tools/delete-cf-pages-project.js
```

**执行流程：**

1. 📋 **获取部署列表** - 分页获取所有部署（每页 25 条）
2. 🔒 **保留最新部署** - 可选保留最新 production 部署
3. 🗑️ **批量删除** - 并发删除部署（显示实时进度）
4. 📊 **统计报告** - 显示成功/失败数量
5. ✅ **删除项目** - 清理空项目

**输出示例：**

```text
🚀 Cloudflare Pages 项目删除工具
==================================================
📌 配置信息:
   账户 ID: 87315bd1eb72810d6740708623fd10c5
   项目名称: plurality-wiki
   保留最新 production: 是
==================================================

📋 正在获取所有部署列表...
   第 1 页: 25 个部署
   第 2 页: 25 个部署
   ...
✅ 共找到 433 个部署

🔒 保留最新 production 部署: ca925a18-f484-4ec3-aa9a-5605a4c4ddcf

🗑️  开始删除 432 个部署...
   进度: 432/432 (100.0%) | 成功: 431 | 失败: 1

📊 删除统计:
   成功: 431
   失败: 1
   总计: 432

🗑️  正在删除项目 "plurality-wiki"...
✅ 项目删除成功！

🎉 所有操作完成！项目已彻底删除。
```

**常见问题：**

- **错误: Unauthorized** - 检查 API Token 是否正确，权限是否足够
- **错误: Invalid list options** - 已修复，确保使用最新版本脚本
- **错误: Cannot delete aliased deployment** - 已修复，脚本自动添加 `?force=true`
- **部分删除失败** - 通常是网络问题，脚本会继续执行并报告失败项

**注意事项：**

- ⚠️ 删除操作不可逆，请确认项目名称无误
- ⚠️ 建议先设置 `KEEP_PRODUCTION="true"` 保留最新部署
- ⚠️ 大量部署（> 500）可能需要几分钟执行时间
- ⚠️ API 有速率限制，脚本已通过并发控制避免触发

## 相关文档

- [贡献流程与规范](../TEMPLATE_ENTRY.md)
- [维护者手册](../ADMIN_GUIDE.md)
- [Cloudflare Pages 部署说明](../dev/CLOUDFLARE_PAGES.md)
