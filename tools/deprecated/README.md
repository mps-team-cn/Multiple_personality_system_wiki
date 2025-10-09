# 废弃工具 (Deprecated Tools)

本目录包含已废弃的工具脚本。这些工具的功能已被整合到更新的系统中，不再推荐使用。

## 迁移到 MkDocs Material (2025-10-07)

以下工具因 MkDocs Material 插件提供了更好的替代方案而废弃：

- `docs_preview.py` - 被 `mkdocs serve` 替代
- `generate_tags_index.py` - 被 MkDocs Material tags 插件替代
- `add_top_level_tags.py` - 标签管理现由 Frontmatter 直接处理
- `add_topic_tags.py` - 标签管理现由 Frontmatter 直接处理
- `analyze_current_tags.py` - 不再需要独立的标签分析
- `analyze_tags.py` - 不再需要独立的标签分析
- `optimize_tags.py` - 标签优化现由编辑器直接处理
- `update_entry_tags.py` - 标签更新现由编辑器直接处理
- `retag_and_related.py` - 标签和相关文章管理已整合

详见：`docs/dev/CLEANUP_RECOMMENDATIONS.md`

## Markdown 处理工具整合 (2025-10-07)

以下 Markdown 处理工具已整合到统一的 `tools/processors/markdown.py`：

### fix_markdown.py

**功能**：修复 Markdown 格式问题（MD009, MD012, MD022, MD028, MD031, MD032, MD034, MD037, MD040, MD047）

**替代方案**：使用 `MarkdownProcessor` 类

```python
from tools.processors.markdown import MarkdownProcessor
processor = MarkdownProcessor()
processor.process_file(Path("file.md"))
```

或使用便捷函数：

```python
from tools.processors.markdown import fix_markdown_file
fix_markdown_file("file.md")
```

### fix_bold_format.py

**功能**：修复加粗文本格式和中文空格

**替代方案**：已整合到 `MarkdownProcessor` 的以下规则中：

- `fix_bold_spacing()` - 确保中文和加粗文本之间有空格
- `fix_parentheses_in_links()` - 修复链接中的括号和加粗链接格式

### fix_list_bold_colon.py

**功能**：修复列表项中的粗体冒号格式

**替代方案**：已整合到 `MarkdownProcessor` 的 `fix_list_bold_colon()` 规则中

## 使用新的统一接口

### 命令行使用（推荐）

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

### 在代码中使用

```python
from tools.processors.markdown import MarkdownProcessor

# 创建处理器实例

processor = MarkdownProcessor()

# 处理文本字符串

text = "**bold**text"
fixed = processor.process(text)

# 处理文件

from pathlib import Path
result = processor.process_file(Path("file.md"))
print(f"Changed: {result.changed}, Rules applied: {result.applied_rules}")

# 批量处理目录

results = processor.process_directory(Path("docs/entries/"))
for result in results:
    if result.changed:
        print(f"Fixed: {result.file_path}")
```

## 保留原因

这些工具被保留在此目录中是为了：

1. **历史参考** - 保留原始实现作为参考
2. **回退支持** - 如果新系统出现问题，可以临时回退
3. **迁移验证** - 验证新系统实现了所有原有功能

## 注意事项

⚠️ **不建议在生产环境中使用这些废弃工具**

- 这些工具不再维护
- 可能与当前项目结构不兼容
- 功能可能不完整或有 bug

如果需要使用这些工具的功能，请使用上述的新接口。

## 清理计划

这些废弃工具将在以下条件满足后被删除：

1. 新系统稳定运行 3 个月以上
2. 所有用户和 CI/CD 流程已迁移到新系统
3. 团队一致同意删除

预计清理时间：2026-01-01 之后

---

**最后更新**：2025-10-07
**维护者**：Multiple Personality System Wiki Team
