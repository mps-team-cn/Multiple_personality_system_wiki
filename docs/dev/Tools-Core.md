# 核心自动化工具详解

> 本文档详细介绍已集成到 CI/CD 流程的核心自动化工具的配置、规则和输出示例。

## 📦 Markdown 处理器

**文件**:[tools/fix_markdown.py](../../tools/fix_markdown.py)

### 功能特性

- 整合了 3 个独立工具的所有功能(fix_markdown.py, fix_bold_format.py, fix_list_bold_colon.py)
- 支持 13 条 Markdownlint 规则 + 6 条中文排版规则
- 批量处理能力
- 预览模式(`--dry-run`)
- 详细的处理结果报告

### 支持的修复规则

#### Markdownlint 标准规则

- **MD009**:移除行尾空白字符(包括全角空格)
- **MD012**:压缩连续空行为单行
- **MD022**:确保标题前后空行
- **MD028**:修复引用块中的空行
- **MD031**:确保代码块前后空行
- **MD032**:确保列表前后空行
- **MD034**:转换裸链接为标准格式
- **MD037**:修复强调标记内空格(增强版,支持中文标点)
- **MD040**:为代码围栏添加语言标注
- **MD047**:确保文件以单个换行结束

#### 中文排版规则

- **CUSTOM001**:列表标记空格(`-item` → `- item`)
- **CUSTOM002**:加粗中文空格(`中文 **加粗** 后面` → `中文 **加粗** 后面`)
- **CUSTOM003**:列表加粗冒号(`-**text**: ` → `- **text** : `)
- **CUSTOM004**:链接括号转换(中文括号 → 英文括号,加粗链接格式)
- **CUSTOM005**:链接前冒号(`参考：linktext` → `参考：linktext`)
- **CUSTOM006**:嵌套列表缩进(2空格 → 4空格,MkDocs 要求)

### 命令行用法

```bash

# 处理单个文件

python tools/fix_markdown.py docs/entries/Tulpa.md

# 处理整个目录

python tools/fix_markdown.py docs/entries/

# 预览模式(不实际修改)

python tools/fix_markdown.py docs/entries/ --dry-run

# 详细输出

python tools/fix_markdown.py docs/entries/ --verbose
```

### 编程接口

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

## 🔗 链接检查工具

**文件**:[tools/check_links.py](../../tools/check_links.py)

### 功能特性

- ✅ 内部链接完整性验证(检查目标文件是否存在)
- ✅ 链接格式规范检查(相对路径、绝对路径等)
- ✅ 支持检查整个项目、指定目录或单个文件
- ✅ 详细的违规报告(显示行号、目标、错误原因)
- ✅ 批量检查能力
- ✅ 自动跳过外部链接、锚点和图片

### 检查规则

根据文件所在位置的不同,链接格式规范也不同:

1. **词条间链接**(`docs/entries/` 内):直接使用文件名
    - ✅ 正确:`[DID](../entries/DID.md)`(其他目录→词条)
    - ❌ 错误:`[DID](DID.md)`(仅限词条目录内)

2. **词条→其他目录**:使用 `../` 相对路径
    - ✅ 正确:`[贡献指南](../contributing/index.md)`
    - ❌ 错误:`[贡献指南](contributing/index.md)`

3. **其他目录→词条**:使用 `../entries/` 路径
    - ✅ 正确:`[DID](../entries/DID.md)`
    - ❌ 错误:`[DID](DID.md)`(省略路径)

4. **禁止事项**:
    - ❌ 绝对路径:`/docs/entries/DID.md`
    - ❌ 链接到不存在的文件

### 命令行用法

```bash

# 检查词条目录(推荐,CI 使用)

python3 tools/check_links.py docs/entries/

# 检查整个项目

python3 tools/check_links.py

# 检查单个文件

python3 tools/check_links.py docs/entries/DID.md

# 显示详细信息(包含通过的文件)

python3 tools/check_links.py --verbose docs/entries/

# 指定仓库根目录(当不在项目根目录时)

python3 tools/check_links.py --root /path/to/repo docs/entries/
```

### 输出示例

```text
======================================================================
Markdown 链接规范检查
======================================================================
仓库根目录:/path/to/repo
扫描路径:/path/to/repo/docs/entries

找到 205 个 Markdown 文件

[违规] docs/entries/Example.md
  行 42: ../../../invalid/path.md
    禁止使用绝对路径,请使用相对路径(如 `../entries/xxx.md`)

  行 58: NonExistent.md
    文件不存在:NonExistent.md

======================================================================
[FAIL] 发现 2 处违规链接(1 个文件)

提示:

  - 词条间链接使用文件名:DID.md
  - 词条到其他目录使用:../contributing/index.md
  - 其他目录到词条使用:../entries/DID.md
  - 详见:docs/contributing/技术约定.md

```

### 排除列表配置

脚本默认排除以下类型的文件(可能包含示例链接或待完善内容):

1. **模板和示例文件**:`TEMPLATE_ENTRY.md`、`404.md`
2. **Contributing 指南**:`contributing/` 下的所有规范文档
3. **开发文档**:`dev/INDEX_GUIDE.md`、`dev/MIGRATION_REPORT.md` 等
4. **工具文档**:`tools/REFACTORING_PLAN.md`、`pdf_export/` 相关文档
5. **README 文件**:各目录下的 `README.md`

如需添加新的排除文件,请编辑 [tools/check_links.py:294-327](../../tools/check_links.py#L294-L327) 中的 `exclude_files` 集合。

### CI 集成

此工具已集成到 GitHub Actions 工作流(`.github/workflows/auto-fix-entries.yml`):

- ✅ 在格式修复后自动检查链接规范
- ✅ 如果检查不通过,CI 会失败并阻止提交
- ✅ 显示详细的错误信息和修复提示

## 📋 Frontmatter 检查工具

**文件**:[tools/check_frontmatter.py](../../tools/check_frontmatter.py)

### 功能特性

- ✅ 检查词条是否包含 YAML Frontmatter
- ✅ 验证必需字段完整性(title, tags, topic, description, updated)
- ✅ 生成详细的检查报告
- ✅ 支持批量检查整个目录
- ✅ 自动排除模板、索引和导览文件
- ✅ 提供统计信息和修复建议

### 检查规则

根据 `docs/TEMPLATE_ENTRY.md` 规范,每个词条必须包含以下 Frontmatter 字段:

1. **title**:词条标题(一级标题文字)
2. **tags**:分类标签(YAML 列表格式)
3. **topic**:主题分类(七大主题之一)
4. **description**:SEO 描述(120-155 字符)
5. **updated**:最后更新时间(YYYY-MM-DD 格式)

可选字段:

- **synonyms**:同义词/别名列表
- **comments**:是否启用评论区(true/false)

### 命令行用法

```bash

# 检查默认目录(docs/entries/)

python3 tools/check_frontmatter.py

# 检查指定目录

python3 tools/check_frontmatter.py --path docs/entries/

# 显示详细信息(包括完整的文件)

python3 tools/check_frontmatter.py --verbose
```

### 输出示例

```text
======================================================================
Frontmatter 完整性检查
======================================================================
检查目录:/path/to/repo/docs/entries
找到 212 个词条文件

📋 Frontmatter 不完整的文件(163 个):
----------------------------------------------------------------------
  ⚠️  Acute-Stress-Disorder-ASD.md
      缺少字段:description
  ⚠️  Adaptive.md
      缺少字段:description
  ...

======================================================================
📊 统计信息
======================================================================
总文件数:        212
完整:            49 (23.1%)
不完整:          163 (76.9%)
缺失 Frontmatter:0 (0.0%)
解析错误:        0 (0.0%)
----------------------------------------------------------------------
需要修复:        163 (76.9%)

💡 修复建议:

   1. 参考 docs/TEMPLATE_ENTRY.md 中的 Frontmatter 模板
   2. 确保包含所有必需字段:title, tags, topic, description, updated
   3. tags 应使用 YAML 列表格式
   4. description 长度应为 120-155 字符
   5. updated 格式应为 YYYY-MM-DD

```

## 🕒 Git 时间戳更新工具

**文件**:[tools/update_git_timestamps.py](../../tools/update_git_timestamps.py)

### 功能特性

- ✅ 自动读取文件在 Git 中的最后提交时间
- ✅ 批量更新 `docs/entries/` 下的所有词条
- ✅ 支持单文件或目录处理
- ✅ 预览模式(`--dry-run`),可在修改前查看变更
- ✅ 详细输出模式(`--verbose`),显示所有文件状态
- ✅ 智能跳过未修改和未提交的文件
- ✅ 自动添加或更新 Frontmatter 中的 `updated` 字段

### 使用示例

```bash

# 更新所有词条(默认处理 docs/entries/)

python tools/update_git_timestamps.py

# 预览模式(不实际修改文件)

python tools/update_git_timestamps.py --dry-run

# 详细输出(显示所有文件状态,包括未修改的)

python tools/update_git_timestamps.py --verbose

# 更新指定文件

python tools/update_git_timestamps.py docs/entries/DID.md

# 更新指定目录

python tools/update_git_timestamps.py docs/entries/

# 组合使用

python tools/update_git_timestamps.py --dry-run --verbose
```

### 输出示例

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

### 工作原理

1. 使用 `git log -1 --format=%ai` 获取文件的最后提交时间
2. 解析 Markdown 文件的 Frontmatter
3. 比较现有的 `updated` 字段与 Git 时间戳
4. 如果不一致,更新 Frontmatter 中的 `updated` 字段
5. 保持文件的其他内容不变

### 注意事项

- ⚠️ 只处理已提交到 Git 的文件,新创建未提交的文件会被跳过
- ⚠️ 需要在 Git 仓库中运行
- ⚠️ 如果 Frontmatter 中没有 `updated` 字段,会自动添加
- ⚠️ 时间格式为 `YYYY-MM-DD`(与项目标准一致)
- 💡 建议在大量修改前先使用 `--dry-run` 预览

## 📂 主题分区索引生成

**文件**:[tools/build_partitions_cn.py](../../tools/build_partitions_cn.py)

### 功能概述

自动根据词条 Frontmatter 中的 `topic` 字段生成七个主题分区的聚合索引页,提供按主题浏览词条的便捷方式。

### 七大主题分区

1. **诊断与临床** - DID、OSDD、PTSD 等诊断相关词条
2. **系统运作** - 切换、共识、内世界等系统机制
3. **实践指南** - Tulpa 创造、接地技巧等实用指南
4. **创伤与疗愈** - 创伤处理、疗愈方法、心理治疗
5. **角色与身份** - 人格、主人格、守门人等角色定义
6. **理论与分类** - 结构性解离理论、分类体系等
7. **文化与表现** - 文学、影视作品中的多重人格表现

### 工作原理

1. 扫描 `docs/entries/` 下的所有词条文件
2. 读取每个词条的 `topic` 字段
3. 按主题分类聚合词条信息(标题、路径、更新时间)
4. 为每个主题生成独立的索引页(如 `诊断与临床-index.md`)
5. 按更新时间降序排列词条列表

### 自动化集成

- ✅ 通过 `mkdocs-gen-files` 插件在构建时自动运行
- ✅ 每次 `mkdocs build` 或 `mkdocs serve` 时自动更新
- ✅ 无需手动维护索引页面
- ✅ CI/CD 流程中自动生成

### 手动运行

```bash

# 直接运行脚本生成索引页

python3 tools/build_partitions_cn.py

# 输出示例

[gen] 已生成 7 个中文分区索引页。
```

### 生成的索引页格式

```markdown
---
title: 诊断与临床
comments: true
---

# 诊断与临床

> 本页汇总所有主题为「诊断与临床」的词条,原文档仍在 `entries/` 目录中。

## 词条一览

- [解离性身份障碍（DID）](DID.md) — *2025-10-14*
- [其他特定解离性障碍（OSDD）](OSDD.md) — *2025-10-14*
- [创伤后应激障碍（PTSD）](PTSD.md) — *2025-10-14*

...
```

### 配置要求

1. **requirements.txt** - 已添加 `mkdocs-gen-files>=0.5.0`
2. **mkdocs.yml** - 已配置 gen-files 插件:

```yaml
plugins:

  - gen-files:

      scripts:

        - tools/build_partitions_cn.py

```

### 词条要求

每个词条的 Frontmatter 需包含 `topic` 字段:

```yaml
---
title: 解离性身份障碍(DID)
topic: 诊断与临床
tags:

  - DID
  - 解离

updated: 2025-10-14
---
```

### 生成文件清单

- `guides/Clinical-Diagnosis-index.md` - 诊断与临床索引
- `guides/System-Operations-index.md` - 系统运作索引
- `guides/Practice-index.md` - 实践指南索引
- `guides/Trauma-Healing-index.md` - 创伤与疗愈索引
- `guides/Roles-Identity-index.md` - 角色与身份索引
- `guides/Theory-Classification-index.md` - 理论与分类索引
- `guides/Cultural-Media-index.md` - 文化与表现索引
- `SUMMARY.md` - 侧边栏导航配置(自动生成)

### 导航集成

脚本自动生成 `docs/SUMMARY.md` 文件,控制 MkDocs Material 的侧边栏导航。导航结构包括:

1. **主题索引页** - 每个主题的汇总页面
2. **所有词条** - 按标题首字母排序,方便查找
3. **字母分组** - 中文词条按拼音首字母,英文词条按字母排序

这确保了点进任何词条后,左侧侧边栏都能显示同主题的其他词条,便于用户浏览和导航。

## 📖 相关文档

- [工具索引](Tools-Index.md)
- [手动工具指南](Tools-Manual.md)
- [技术约定](../contributing/technical-conventions.md)
