# 手动维护工具指南

> 本文档详细介绍需要手动运行的维护工具,包括 SEO 优化、搜索优化、版本管理和文档导出等。

## 🔍 SEO 优化工具

### check_descriptions.py - 描述字段覆盖率检查

**文件**:[tools/check_descriptions.py](../../tools/check_descriptions.py)

#### 功能说明

扫描所有词条,统计 `description` 字段的覆盖情况,列出缺失的词条清单。

#### 使用方法

```bash
# 检查当前覆盖情况
python3 tools/check_descriptions.py
```

#### 输出示例

```text
=== Description 字段覆盖情况 ===
总词条数: 212
已有 description: 49 (23.1%)
缺失 description: 163 (76.9%)

缺失 description 的词条:
- Acute-Stress-Disorder-ASD.md
- Adaptive.md
- Age-Regression.md
...
```

### add_descriptions.py - 批量添加 SEO 描述

**文件**:[tools/add_descriptions.py](../../tools/add_descriptions.py)

#### 功能说明

批量为优先级词条添加 SEO 友好的 `description` 字段(120-155 字符),包含:

- 32 个核心词条的精心撰写的描述
- DID、OSDD、Tulpa、CPTSD 等主要诊断词条
- 系统运作、创伤疗愈、成员角色等关键概念
- 符合 SEO 最佳实践的关键词密度

#### 使用方法

```bash
# 为核心词条添加 description
python3 tools/add_descriptions.py
```

#### 扩展方法

编辑 `tools/add_descriptions.py` 中的 `PRIORITY_DESCRIPTIONS` 字典:

```python
PRIORITY_DESCRIPTIONS = {
    "词条文件名.md": "简洁准确的描述文字(120-155 字符,包含核心关键词)",
    # ...
}
```

#### 使用流程

```bash
# 1. 检查当前覆盖情况
python3 tools/check_descriptions.py

# 2. 为核心词条添加 description
python3 tools/add_descriptions.py

# 3. 再次检查验证结果
python3 tools/check_descriptions.py
```

## 🔎 搜索优化工具(jieba 词典管理)

**背景**:MkDocs 搜索使用 jieba 分词,需要自定义词典(`data/user_dict.txt`)来优化专业术语的识别。采用 **预处理 + AI 审核 + 自动优化** 的三阶段方案。

### 工具链概览

| 工具脚本 | 功能说明 | 使用场景 |
|---------|---------|---------|
| **analyze_search_index.py** | 分析搜索索引,统计词频和 n-gram 分布 | 了解索引结构 |
| **extract_dict_candidates.py** | 从索引提取候选词(可配置频率、长度阈值) | 生成候选词表 |
| **split_candidates.py** | 将候选词分批,便于 AI 审核(每批 50-100KB) | AI 审核准备 |
| **auto_review_candidates.py** | 自动审核候选词并生成优化词典(基于规则) | 批量优化词典 |
| **test_dict_segmentation.py** | 测试词典的分词效果(内置测试套件) | 验证分词质量 |

### 快速上手

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

### analyze_search_index.py - 索引分析

#### 使用方法

```bash
# 分析索引并显示统计信息
python3 tools/analyze_search_index.py \
  --input site/search/search_index.json \
  --stats

# 输出高频词汇(Top 50)
python3 tools/analyze_search_index.py \
  --input site/search/search_index.json \
  --top 50
```

#### 输出示例

```text
=== 搜索索引分析 ===
总文档数: 212
总词汇数: 15432
唯一词汇数: 8765
平均文档长度: 72.8 词

=== 高频词汇 Top 20 ===
1. 解离 (542)
2. 系统 (487)
3. 人格 (423)
...
```

### extract_dict_candidates.py - 候选词提取

#### 使用方法

```bash
# 提取候选词(频率 >= 3,长度 2-6)
python3 tools/extract_dict_candidates.py \
  --input site/search/search_index.json \
  --output data/candidates.txt \
  --min-freq 3 \
  --min-length 2 \
  --max-length 6
```

#### 参数说明

- `--min-freq`:最小词频(默认 3)
- `--min-length`:最小词长(默认 2)
- `--max-length`:最大词长(默认 6)

### auto_review_candidates.py - 自动审核

#### 审核规则

1. **保留**:
    - 专业术语(障碍、疗法、诊断、解离性、创伤后等)
    - 核心复合词(解离性身份障碍、多意识体系统、系统内沟通等)
    - 重要缩写(DID、OSDD、PTSD 等)

2. **优化**:
    - 核心术语提升至 5000-8000 权重
    - 专业复合词提升至 2000-3000 权重
    - 通用短词降权至 500-1000

3. **删除**:
    - 片段词(如 "离性"、"识体")
    - 通用词(如 "可能"、"使用"、"其他")
    - 单字词和过长词组

#### 使用方法

```bash
# 自动审核并生成优化词典
python3 tools/auto_review_candidates.py \
  --input data/candidates.txt \
  --output data/user_dict_reviewed.txt \
  --stats

# 只显示统计信息,不生成文件
python3 tools/auto_review_candidates.py \
  --input data/candidates.txt \
  --stats
```

### test_dict_segmentation.py - 分词测试

#### 使用方法

```bash
# 使用内置测试套件
python3 tools/test_dict_segmentation.py \
  --dict data/user_dict.txt \
  --test-suite

# 测试自定义文本
python3 tools/test_dict_segmentation.py \
  --dict data/user_dict.txt \
  --text "解离性身份障碍是一种多意识体系统"

# 对比两个词典的效果
python3 tools/test_dict_segmentation.py \
  --dict data/user_dict.txt \
  --compare data/user_dict_reviewed.txt
```

#### 分词效果示例

```text
输入: 解离性身份障碍是一种多意识体系统
输出: 解离性身份障碍 / 是 / 一种 / 多意识体系统

输入: 心理治疗和情绪调节技巧有助于管理症状
输出: 心理治疗 / 和 / 情绪调节 / 技巧 / 有助于 / 管理 / 症状
```

### 详细文档

完整流程说明:[AI 辅助词典生成指南](AI-Dictionary-Generation.md)(包含三阶段详细步骤、AI 审核 Prompt 模板、质量控制策略)

## 📅 版本管理工具

### gen_changelog_by_tags.py - 变更日志生成

**文件**:[tools/gen_changelog_by_tags.py](../../tools/gen_changelog_by_tags.py)

#### 功能说明

按 Git 标签时间顺序生成 `changelog.md`,并按提交类型(feat, fix, docs, chore 等)分组。

#### 使用方法

```bash
# 生成完整变更日志
python tools/gen_changelog_by_tags.py --output changelog.md

# 只生成最新版本的变更
python tools/gen_changelog_by_tags.py --output changelog.md --latest-only

# 生成从最新标签到 HEAD 的变更(未发布)
python tools/gen_changelog_by_tags.py --output changelog.md --latest-to-head
```

#### 输出格式

```markdown
# Changelog

## [v3.12.1] - 2025-10-14

### ✨ Features
- feat: 新增 Tulpa 实践核心词条

### 🐛 Bug Fixes
- fix: 修复链接检查排除列表不生效的问题

### 📝 Documentation
- docs: 更新实践指南导览

### 🔧 Chore
- chore: 删除已废弃的脚本
```

#### 版本发布流程

```bash
# 1. 生成或更新 changelog
python tools/gen_changelog_by_tags.py --output changelog.md

# 2. 检查 changelog 内容
cat changelog.md

# 3. 创建 GitHub Release(使用 gh CLI)
gh release create v3.12.1 --notes-file changelog.md

# 或编辑现有 Release
gh release edit v3.12.1 --notes-file changelog.md
```

## 📄 文档导出工具

### pdf_export/ - PDF 整站导出

**文件**:[tools/pdf_export/](../../tools/pdf_export/)

#### 功能特性

- ✅ Pandoc 驱动的整站 PDF 导出
- ✅ 支持封面、忽略列表、中文字体
- ✅ 带页码的 topic 目录
- ✅ 自动读取词条 Frontmatter 的 `topic` 字段构建章节顺序
- ✅ 词条链接自动重写为 PDF 内部锚点
- ✅ 支持 `updated` 字段的多种格式

#### 使用方法

```bash
# 基本用法
python tools/pdf_export/export_to_pdf.py

# 或使用模块方式
python -m pdf_export

# 自定义输出路径
python tools/pdf_export/export_to_pdf.py --output custom_output.pdf

# 自定义忽略文件
python tools/pdf_export/export_to_pdf.py --ignore-file custom_ignore.md
```

#### 目录生成逻辑

- 读取词条 Frontmatter 中的 `topic` 字段自动构建章节顺序
- 缺失 `topic` 的词条归入"其他"分类
- 按 topic 字典序排序
- 目录页基于章节生成带页码的"图书式"排版
- 条目与页码均可点击跳转至对应内容

#### 忽略列表配置

默认忽略列表位于 [tools/pdf_export/ignore.md](../../tools/pdf_export/ignore.md),支持:

- 目录匹配(如 `node_modules/`)
- 单个文件(如 `README.md`)
- 通配符(如 `*.tmp`)

#### Frontmatter 要求

词条的 `updated` 字段支持以下格式:

- ✅ `YYYY-MM-DD` 字符串(推荐)
- ✅ YAML 日期字面量
- ❌ `null`、布尔值、列表(会终止导出并提示修正)

#### 详细文档

完整配置和用法:[PDF 导出工具文档](../../tools/pdf_export/README.md)

## 🧪 开发者工具

### gen-validation-report.py - 词条结构验证

**文件**:[tools/gen-validation-report.py](../../tools/gen-validation-report.py)

#### 功能说明

校验词条结构并生成 `docs/VALIDATION_REPORT.md`,检查:

- Frontmatter 完整性
- 链接有效性
- 格式规范性
- 内容质量

#### 使用方法

```bash
python tools/gen-validation-report.py
```

生成的报告位于 `docs/VALIDATION_REPORT.md`。

### delete-cf-pages-project.js - Cloudflare Pages 项目删除

**文件**:[tools/delete-cf-pages-project.js](../../tools/delete-cf-pages-project.js)

#### 功能说明

Cloudflare Pages 项目批量删除工具,支持:

- ✅ 自动分页获取所有部署(API 限制每页最多 25 条)
- ✅ 支持并发批量删除(默认每批 5 个)
- ✅ 可选保留最新 production 部署(默认保留)
- ✅ 强制删除别名部署(自动添加 `?force=true` 参数)
- ✅ 详细的进度显示和错误处理

#### 环境变量配置

```bash
# 必需的环境变量
export CF_API_TOKEN="your-cloudflare-api-token"      # Cloudflare API Token
export CF_ACCOUNT_ID="your-account-id"               # Cloudflare Account ID
export CF_PAGES_PROJECT="your-project-name"          # Pages 项目名称

# 可选配置
export KEEP_PRODUCTION="true"   # 是否保留最新 production 部署(默认 true)
```

#### 获取 API Token

1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. 点击 "Create Token" → "Edit Cloudflare Workers" 模板
3. 权限设置:Account - Cloudflare Pages - Edit
4. 复制生成的 Token

#### 使用示例

```bash
# 方式 1: 设置环境变量后运行
export CF_API_TOKEN="G1r-bNax-xxxXxxXxxXxxXxxXxxXxxXxx"
export CF_ACCOUNT_ID="873xxxxxxxxxxxxxxxxxxxxxxxc5"
export CF_PAGES_PROJECT="my-project"
node tools/delete-cf-pages-project.js

# 方式 2: 单行执行
CF_API_TOKEN="..." CF_ACCOUNT_ID="..." CF_PAGES_PROJECT="my-project" \
  node tools/delete-cf-pages-project.js

# 方式 3: 删除所有部署(不保留 production)
export KEEP_PRODUCTION="false"
CF_API_TOKEN="..." CF_ACCOUNT_ID="..." CF_PAGES_PROJECT="my-project" \
  node tools/delete-cf-pages-project.js
```

#### 执行流程

1. 📋 获取部署列表 - 分页获取所有部署(每页 25 条)
2. 🔒 保留最新部署 - 可选保留最新 production 部署
3. 🗑️ 批量删除 - 并发删除部署(显示实时进度)
4. 📊 统计报告 - 显示成功/失败数量
5. ✅ 删除项目 - 清理空项目

#### 注意事项

- ⚠️ 删除操作不可逆,请确认项目名称无误
- ⚠️ 建议先设置 `KEEP_PRODUCTION="true"` 保留最新部署
- ⚠️ 大量部署(> 500)可能需要几分钟执行时间
- ⚠️ API 有速率限制,脚本已通过并发控制避免触发

## 📖 相关文档

- [工具索引](Tools-Index.md)
- [核心工具详解](Tools-Core.md)
- [技术约定](../contributing/technical-conventions.md)
