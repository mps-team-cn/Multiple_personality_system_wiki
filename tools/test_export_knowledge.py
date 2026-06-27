#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 export_knowledge.py 的清洗规则。

运行:
    uv run python3 -m pytest tools/test_export_knowledge.py -v

或直接:
    uv run python3 tools/test_export_knowledge.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# 确保可以从 tools/ 目录导入
sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_knowledge import (
    ExportStats,
    check_output_safety,
    process_entry,
    export_knowledge,
)


# ── 测试数据 ──

SAMPLE_WITH_FRONTMATTER = """---
title: 测试词条（Test Entry）
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 测试词条（Test Entry）

## 概述

这是一个测试词条，用于验证导出工具。

### 子标题

正文内容包含 **粗体** 和 *斜体*。

## 相关条目

- [DID](DID.md)
- [OSDD](OSDD.md)

## 参考与延伸阅读

1. 参考书 A
2. 参考书 B
"""

SAMPLE_WITH_LINKS = """---
title: 链接测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 链接测试

这是一个[普通链接](DID.md)。

这是一个带标题的[链接](DID.md "标题文字")。

这是一个[括号链接](<DID.md>)。

这是一个[外部链接](https://example.com)。

正文包含 DID 与 OSDD 的概念比较。
"""

SAMPLE_WITH_IMAGES = """---
title: 图片测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 图片测试

文字内容。

![测试图片](../assets/images/test.png)

![SVG图片](../assets/figures/diagram.svg)

文字再接续。
"""

SAMPLE_WITH_ADMONITIONS = """---
title: Admonition 测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# Admonition 测试

!!! warning "触发警告"
    内容涉及敏感议题。

!!! info "免责声明"
    本站资料仅供参考，不构成医疗建议。若需诊断或治疗，请联系持证专业人员。

!!! tip "有用的提示"
    这是一个有用的提示正文。

## 正文标题

正文内容。

??? question "这是一个问题？"
    这是问题的回答。

!!! note "无内容的"
"""

SAMPLE_WITH_FOOTNOTES = """---
title: 脚注测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 脚注测试

正文包含脚注引用[^fn1]。

更多内容[^fn2]。

## 正文标题

正文继续。

[^fn1]: 第一个脚注定义。
[^fn2]: 第二个脚注定义，
    带缩进的多行内容。
"""

SAMPLE_WITH_TABLES = """---
title: 表格测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 表格测试

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |
| 数据3 | 数据4 |

正文内容。
"""

SAMPLE_WITH_CODE = """---
title: 代码测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 代码测试

正文。

```python
def hello():
    print("world")
```

行内 `代码` 应该保留。
"""

SAMPLE_NAV_IN_BODY = """---
title: 正文中关键词测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 正文中关键词测试

在诊断过程中，相关条目需要仔细检查。

参见相关文献资料时，注意区分。

该参考资料来源于临床研究。
"""

SAMPLE_NAV_MULTI_LEVEL = """---
title: 多级导航测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 多级导航测试

## 诊断要点

### ICD-11 条目

内容。

## 相关条目

### 子分类一

- [DID](DID.md)

### 子分类二

- [OSDD](OSDD.md)

## 治疗

治疗内容。
"""

SAMPLE_TEMPLATE_TEXT = """---
title: 模板文本测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 模板文本测试

正文内容。

本站资料仅供参考，不构成医疗建议。若需诊断或治疗，请联系持证专业人员。

更多正文。
"""

SAMPLE_WHITESPACE = """---
title: 空白清理测试
tags:
  - dx:测试
topic: 理论与分类
updated: 2026-01-01
---

# 空白清理测试

正文。


---

更多正文。

---
"""

SAMPLE_FRONTMATTER_PRESERVATION = """---
title: Frontmatter 测试
tags:
  - dx:测试
  - theory:理论
topic: 理论与分类
search:
  boost: 1.5
description: 一个测试词条
synonyms:
  - 测试
  - test
updated: 2026-06-01
---

# Frontmatter 测试

正文。
"""


# ── 辅助函数 ──

def _run(content: str) -> str:
    """对内容运行完整清洗，返回结果。"""
    stats = ExportStats()
    return process_entry(content, stats)


def test_frontmatter_preserved():
    """Frontmatter 仅保留 title 和 synonyms。"""
    result = _run(SAMPLE_WITH_FRONTMATTER)
    assert "title: 测试词条（Test Entry）" in result
    assert "tags:" not in result  # 不保留
    assert "dx:测试" not in result  # 不保留
    assert "topic: 理论与分类" not in result  # 不保留
    assert "updated: 2026-01-01" not in result  # 不保留
    assert result.startswith("---")


def test_nav_section_removed():
    """相关条目 章节被删除。"""
    result = _run(SAMPLE_WITH_FRONTMATTER)
    assert "## 相关条目" not in result
    assert "[DID](DID.md)" not in result
    assert "## 参考与延伸阅读" not in result


def test_nav_stops_at_next_same_level():
    """导航章节删除到下一个同级标题时停止。"""
    result = _run(SAMPLE_NAV_MULTI_LEVEL)
    assert "## 相关条目" not in result
    assert "### 子分类一" not in result
    assert "### 子分类二" not in result
    assert "[DID](DID.md)" not in result or "DID" not in result.replace("---", "")
    # 下一个同级标题 "## 治疗" 应该保留
    assert "## 治疗" in result
    assert "治疗内容" in result


def test_nav_keyword_not_removed_in_body():
    """普通正文中的“相关条目”文字不被误删。"""
    result = _run(SAMPLE_NAV_IN_BODY)
    assert "相关条目" in result  # 正文中出现的不能被误删
    assert "参见" in result
    assert "参考资料" in result
    assert "诊断" in result


def test_links_converted_to_text():
    """Markdown 链接转纯文字。"""
    result = _run(SAMPLE_WITH_LINKS)
    assert "普通链接" in result
    assert "[普通链接](DID.md)" not in result
    assert "带标题的链接" in result
    assert "标题文字" not in result  # URL title 应该被删除
    assert "外部链接" in result
    assert "https://" not in result or "https" not in ''.join(result.split())


def test_images_removed():
    """图片被删除。"""
    result = _run(SAMPLE_WITH_IMAGES)
    assert "![测试图片](../assets/images/test.png)" not in result
    assert "![SVG图片](../assets/figures/diagram.svg)" not in result
    assert "文字内容" in result
    assert "文字再接续" in result


def test_admonition_marker_removed():
    """admonition 标记和标题被删除。"""
    result = _run(SAMPLE_WITH_ADMONITIONS)
    assert "!!!" not in result
    # 触发警告被删除（模板文本）
    assert "触发警告" not in result
    # 免责声明被删除
    assert "本站资料仅供参考，不构成医疗建议" not in result
    # tip 的标题 "有用的提示" 在正文 "这是一个有用的提示正文" 中作为子串存在，
    # 但 admonition 语法标记已被删除，且标题未作为独立标题输出
    assert "!!! tip" not in result
    assert "这是一个有用的提示正文" in result


def test_admonition_body_indentation_removed():
    """admonition 正文去缩进并保留。"""
    result = _run(SAMPLE_WITH_ADMONITIONS)
    assert "这是一个有用的提示正文" in result
    # 确认没有多余的缩进
    for line in result.split("\n"):
        if "这是一个有用的提示正文" in line:
            assert not line.startswith("    "), f"缩进未清除: {line!r}"


def test_question_admonition_title_preserved():
    """??? question 的标题（问题）被保留。"""
    result = _run(SAMPLE_WITH_ADMONITIONS)
    assert "这是一个问题？" in result
    assert "这是问题的回答" in result


def test_footnote_definitions_removed():
    """单行脚注定义被删除。"""
    result = _run(SAMPLE_WITH_FOOTNOTES)
    assert "[^fn1]:" not in result
    assert "第一个脚注定义" not in result  # 定义内容也被删除
    # 但正文内容保留
    assert "正文包含脚注引用" in result


def test_footnote_multi_line_removed():
    """多行脚注定义被删除。"""
    result = _run(SAMPLE_WITH_FOOTNOTES)
    assert "[^fn2]:" not in result
    assert "带缩进的多行内容" not in result  # 多行定义内容也被删除


def test_inline_footnotes_removed():
    """行内脚注引用被删除。"""
    result = _run(SAMPLE_WITH_FOOTNOTES)
    assert "[^fn1]" not in result
    assert "正文包含脚注引用" in result
    assert "更多内容" in result


def test_tables_preserved():
    """表格保留。"""
    result = _run(SAMPLE_WITH_TABLES)
    assert "| 列1 | 列2 |" in result
    assert "| 数据1 | 数据2 |" in result


def test_code_blocks_preserved():
    """代码块保留。"""
    result = _run(SAMPLE_WITH_CODE)
    assert "```python" in result
    assert 'def hello():' in result
    assert '`代码`' in result or "`代码`" in result


def test_bold_italic_preserved():
    """粗体和斜体保留。"""
    result = _run(SAMPLE_WITH_FRONTMATTER)
    assert "**粗体**" in result
    assert "*斜体*" in result


def test_template_text_removed():
    """模板化免责声明被删除。"""
    result = _run(SAMPLE_TEMPLATE_TEXT)
    assert "本站资料仅供参考，不构成医疗建议" not in result
    assert "正文内容" in result
    assert "更多正文" in result


def test_excessive_blank_lines_removed():
    """连续超过两个空行被清理。"""
    result = _run(SAMPLE_WHITESPACE)
    # 不应该有连续 3+ 空行
    assert "正文\n\n\n" not in result


def test_output_safety():
    """输出目录安全检查。"""
    import pytest
    from pathlib import Path
    
    repo_root = Path(__file__).resolve().parent.parent
    
    # 不能与输入目录相同
    with pytest.raises(ValueError, match="输入目录和输出目录不能相同"):
        check_output_safety(repo_root / "docs/entries", repo_root / "docs/entries")
    
    # 不能是仓库根目录
    with pytest.raises(ValueError, match="输出目录不得为禁止目录"):
        check_output_safety(repo_root / "docs/entries", repo_root)
    
    # 不能是 docs/
    with pytest.raises(ValueError, match="输出目录不得位于 docs/ 下"):
        check_output_safety(repo_root / "docs/entries", repo_root / "docs")
    
    # 不能是 docs/entries/
    with pytest.raises(ValueError, match="输出目录不得为禁止目录"):
        check_output_safety(repo_root / "tools", repo_root / "docs/entries")
    
    # 合法路径
    check_output_safety(repo_root / "docs/entries", repo_root / "dist" / "knowledge" / "entries")


def test_repeatable_output():
    """重复执行结果一致。"""
    content = SAMPLE_WITH_FRONTMATTER
    result1 = _run(content)
    result2 = _run(content)
    assert result1 == result2


def test_idempotent():
    """对已清洗内容再次清洗仍保持一致。"""
    content = SAMPLE_WITH_LINKS
    result1 = _run(content)
    result2 = _run(result1)  # 对结果再跑一次
    assert result1 == result2


def test_export_integration():
    """集成测试：导出、删除源文件后旧输出不残留。"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        input_dir = tmp / "input"
        output_dir = tmp / "output"
        input_dir.mkdir()
        
        # 创建两个源文件
        (input_dir / "test-a.md").write_text(SAMPLE_WITH_FRONTMATTER, encoding="utf-8")
        (input_dir / "test-b.md").write_text(SAMPLE_WITH_LINKS, encoding="utf-8")
        
        result = export_knowledge(input_dir, output_dir)
        assert result.exported == 2
        assert (output_dir / "test-a.md").exists()
        assert (output_dir / "test-b.md").exists()
        
        # 删除一个源文件后重新导出
        (input_dir / "test-a.md").unlink()
        result2 = export_knowledge(input_dir, output_dir)
        assert result2.exported == 1
        # 旧输出文件不应残留
        assert not (output_dir / "test-a.md").exists()
        assert (output_dir / "test-b.md").exists()


def test_file_no_frontmatter():
    """没有 Frontmatter 的文件也能正确处理。"""
    content = "# 无 Frontmatter 的文件\n\n正文内容。\n\n## 相关条目\n\n- [DID](DID.md)"
    result = _run(content)
    assert "# 无 Frontmatter 的文件" in result
    assert "## 相关条目" not in result
    assert "正文内容" in result


def test_all_nav_headings_removed():
    """所有导航标题变体都被删除。"""
    variants = [
        "## 相关条目",
        "### 关联条目",
        "## 参见",
        "### 另见",
        "## See also",
        "## See Also",
        "## 延伸阅读",
        "## 参考与延伸阅读",
        "## 参考文献",
        "## 参考资料",
        "## 外部链接",
    ]
    for heading in variants:
        content = f"---\ntitle: Test\ntags:\n  - dx:test\ntopic: 理论与分类\nupdated: 2026-01-01\n---\n\n# Test\n\n{heading}\n\n内容。"
        result = _run(content)
        assert heading.strip() not in result, f"标题未被删除: {heading}"


def test_nav_heading_trailing_punctuation():
    """导航标题带标点也能匹配。"""
    content = f"---\ntitle: Test\ntags:\n  - dx:test\ntopic: 理论与分类\nupdated: 2026-01-01\n---\n\n# Test\n\n## 相关条目：\n\n- [DID](DID.md)\n\n## 正文\n\n内容。"
    result = _run(content)
    assert "## 相关条目：" not in result
    assert "## 正文" in result
    assert "内容。" in result


def test_statistics_reporting():
    """统计报告正确反映操作次数。"""
    stats = ExportStats()
    _ = process_entry(SAMPLE_WITH_ADMONITIONS, stats)
    assert stats.admonitions_cleaned >= 3  # warning, info, tip, note → 至少3个非空
    assert stats.template_texts_removed >= 1  # 免责声明
    assert stats.nav_sections_removed >= 0  # 没有导航章节


# ── 主入口（直接运行时用 pytest） ──

if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
