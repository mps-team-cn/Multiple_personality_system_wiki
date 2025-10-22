---
title: 编写规范
description: MPS Wiki 词条编写规范与格式要求,包含语言风格、Frontmatter 规范、标题层级、段落格式、列表引用等。确保内容质量与一致性的完整指南
---

# 编写规范

本文档定义 Multiple Personality System Wiki 的通用编写约定与格式要求。

---

## 1. 语言规范

### 1.1 统一使用简体中文

- 所有条目、说明文档、提交信息统一使用简体中文
- 英文术语首次出现时必须标注中文翻译

### 1.2 标题格式

- **一级标题** ：`中文名（English/缩写）`
- 示例：
    - `解离性身份障碍（Dissociative Identity Disorder, DID）`
    - `图帕（Tulpa）`
    - `多意识体系统（MPS）`

### 1.3 术语使用

- 首次出现时必须标注 **英文原名与缩写**
- 社群用语需与临床术语明确区分

---

## 2. 文件结构规范

!!! warning "重要"
    本项目已从 Docsify 迁移至 MkDocs Material。

### 2.1 词条模板

创建新词条时，请使用项目提供的标准模板：

- **模板文件** ：`docs/TEMPLATE_ENTRY.md`
- **使用方法** ：复制模板并重命名，然后填写内容

```bash

# 复制模板创建新词条

cp docs/TEMPLATE_ENTRY.md docs/entries/新词条名.md
```

### 2.2 词条存放位置

- **所有词条** ：统一存放在 `docs/entries/` 目录
- **禁止** ：在 `docs/entries/` 下创建二级子目录
- **备份同步** ：`entries/` 根目录保留词条副本（工具兼容）

### 2.3 Frontmatter 要求

每篇词条必须以 YAML Frontmatter 开头：

```yaml
---
title: 词条标题
tags:

  - 标签1
  - 标签2

topic: 主题分类
updated: 2025-10-07
---
```

**必需字段** ：

- `title`：词条标题
- `tags`：相关标签（数组格式）
- `updated`：最后更新日期（YYYY-MM-DD）
- `topic`：主题分类（如"系统运作"、"心理健康"等）

---

## 3. Markdown 规范

### 3.1 标题层级

- **一级标题** （`#`）：词条名
- **二级标题** （`##`）：主要章节
- **三级及以下** ：依层级递增

### 3.2 触发警告

涉及以下内容时，必须在文首添加触发警告：

- 创伤
- 暴力
- 自伤
- 性侵
- 其他敏感内容

**示例** ：

```markdown
!!! warning "触发警告"
    本文涉及创伤、暴力等敏感内容，请谨慎阅读。
!!! info "免责声明"
    本文内容仅供参考，不构成医疗建议。如需诊断或治疗，请咨询专业医疗机构。
```

### 3.3 列表规范（强制）

!!! danger "必须使用连字符（-）作为无序列表符号"

为确保 MkDocs Material 渲染一致，所有 Markdown 无序列表必须使用 `-` 作为项目符号。

✅ **正确示例：**

```markdown
- 条目一
- 条目二
    - 子条目
```

❌ **错误示例：**

```markdown
* 条目一
+ 条目二
```

说明：

- `-` 可保证在 MkDocs Material 中的缩进、符号样式统一
- `*` 与 `+` 可能在插件解析或渲染中出现不兼容情况
- 有序列表使用阿拉伯数字加英文句点（如 `1.`、`2.`）
- 列表项与上一段之间须 **空一行**，以避免渲染粘连

---

## 4. 格式规范（MkDocs Material 兼容性）

为确保在 MkDocs Material 中正确渲染，请遵循以下格式规范：

### 4.1 加粗链接格式

❌ **错误** ：

```markdown
[**文本**](链接)
```

✅ **正确** ：

```markdown
**文本([链接](url))**
```

**说明** ：MkDocs Material 无法正确渲染加粗标记包裹链接的格式。

### 4.2 列表中的加粗文本

❌ **错误** ：

```markdown

- 可以切**意识**

```

✅ **正确** ：

```markdown

- 可以切 **意识**

```

**说明** ：加粗标记前需要空格以确保正确渲染。

### 4.3 链接文本中的括号

❌ **错误** ：

```markdown
[创伤（Trauma）](Trauma.md)
```

✅ **正确** ：

```markdown
[创伤（Trauma）](Trauma.md)
```

**说明** ：统一使用全角括号（）而非半角括号 ()。

### 4.4 冒号格式

❌ **错误** ：

```markdown
参阅：
```

✅ **正确** ：

```markdown
参阅：
```

**说明** ：在中文语境中使用全角冒号。

---

## 5. 自动修复工具

!!! tip "自动修复"
    运行 `python tools/fix_markdown.py` 可自动修复以上格式问题。

### 5.1 使用方法

```bash

# 修复所有文件

python tools/fix_markdown.py

# 修复特定文件

python tools/fix_markdown.py docs/entries/某词条.md
```

### 5.2 修复范围

- 加粗链接格式
- 列表加粗文本空格
- 链接括号格式
- 冒号格式

---

## 6. 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 6.1 提交类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat:` | 新增条目/新增章节 | `feat: 添加 OSDD 词条` |
| `fix:` | 错误修复（链接/引用/格式） | `fix: 修复 DID 词条引用链接` |
| `docs:` | 文档与索引更新（不影响语义） | `docs: 更新贡献指南` |
| `refactor:` | 结构与命名重构（不改变内容含义） | `refactor: 重组创伤相关词条` |
| `chore:` | 工具、CI、脚本维护项 | `chore: 更新构建脚本` |
| `style:` | 空格/缩进/行尾等非语义变更 | `style: 统一 Markdown 格式` |

### 6.2 提交信息格式

```text
<type>: <subject>

[optional body]

[optional footer]
```

**示例** ：

```text
feat: 添加解离性遗忘症词条

- 添加 ICD-11 诊断标准
- 补充 DSM-5-TR 对照
- 包含临床案例与治疗方法

参考：WHO ICD-11 Browser (MMS 2025-01)
```

---

## 7. 翻译与术语规范

### 7.1 术语格式

采用 **中文名（English, 缩写）** 格式：

- 解离性身份障碍（Dissociative Identity Disorder, DID）
- 图帕（Tulpa）
- 多意识体系统（MPS）

### 7.2 社群用语处理

社群用语必须与临床术语分开，列入"同义词/社群用法"小节。

**示例** ：

```markdown

## 同义词与社群用法

- **临床术语**：解离性身份障碍（DID）
- **社群用语**：多重人格、系统

```

### 7.3 多译名处理

若存在多译名，需标明使用场景与来源：

```markdown

## 术语说明

- **临床**：解离性身份障碍
- **社群**：多重人格
- **媒体**：人格分裂（不推荐）

```

---

## 相关文档

- [学术引用规范](academic-citation.md)
- [诊断临床规范](clinical-guidelines.md)
- [技术约定](technical-conventions.md)
- [PR 流程](pr-workflow.md)
