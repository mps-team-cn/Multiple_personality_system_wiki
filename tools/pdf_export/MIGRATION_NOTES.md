# PDF 导出功能迁移说明

## 更新日期

2025-10-06

## 背景

项目从 Docsify 迁移到 MkDocs Material 后，词条文件和文档结构发生了以下变化：

1. **词条目录**：从 `entries/` 迁移到 `docs/entries/`
2. **文档文件**：`Preface.md`、`index.md` 等移至 `docs/` 目录
3. **链接格式**：从 `/entries/xxx.md` 改为相对路径 `xxx.md`

## 修复内容

### 1. 链接格式支持（markdown.py）

**更新的正则表达式**：
- 旧格式：`entries/xxx.md`、`./entries/xxx.md`、`../entries/xxx.md`
- 新格式：`xxx.md`（相对路径，假定在 docs/entries/ 目录下）

**更新的函数**：
- `ENTRY_INLINE_LINK_PATTERN`：支持行内链接 `[text](xxx.md)`
- `ENTRY_REFERENCE_LINK_PATTERN`：支持引用式链接 `[ref]: xxx.md`
- `ENTRY_ANGLE_LINK_PATTERN`：支持角括号链接 `<xxx.md>`
- `_resolve_entry_target()`：支持两种格式的路径解析

### 2. 路径自动检测（paths.py）

**智能路径选择**：
```python

# 词条目录：优先使用 docs/entries/（新结构），回退到 entries/（旧结构）

DOCS_ENTRIES_DIR = PROJECT_ROOT / "docs" / "entries"
ENTRIES_DIR = DOCS_ENTRIES_DIR if DOCS_ENTRIES_DIR.exists() else PROJECT_ROOT / "entries"

# 文档文件：优先使用 docs/ 目录

PREFACE_PATH = DOCS_DIR / "Preface.md" if (DOCS_DIR / "Preface.md").exists() else PROJECT_ROOT / "Preface.md"
INDEX_PATH = DOCS_DIR / "index.md" if (DOCS_DIR / "index.md").exists() else PROJECT_ROOT / "index.md"
LAST_UPDATED_JSON_PATH = DOCS_DIR / "assets" / "last-updated.json" if ...
```

### 3. 结构收集（structure.py）

**更新的函数**：
- `_build_preface_section()`：使用 `PREFACE_PATH` 常量
- `_build_sections_from_index()`：使用 `INDEX_PATH` 常量

## 兼容性

- ✅ 完全兼容新的 MkDocs 结构（docs/entries/, docs/Preface.md 等）
- ✅ 向后兼容旧的 Docsify 结构（entries/, Preface.md 等）
- ✅ 支持新格式链接（xxx.md）
- ✅ 支持旧格式链接（entries/xxx.md）

## 测试结果

成功测试：
- 正则表达式匹配：`[DID](DID.md)` ✓
- 路径解析：`DID.md` → `#entry-2d0c56bfbf` ✓
- 结构收集：143 个文档（1 个前言 + 142 个词条）✓
- Markdown 合并：307,852 字符 ✓

## 使用方法

保持不变，仍使用相同的命令：

```bash
python tools/pdf_export/export_to_pdf.py
```

工具会自动检测并使用正确的目录结构和链接格式。
