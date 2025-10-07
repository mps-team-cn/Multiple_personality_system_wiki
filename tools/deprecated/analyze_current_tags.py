#!/usr/bin/env python3
"""分析当前词条的标签使用情况"""

from __future__ import annotations

import sys
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.pdf_export.pdf_export.frontmatter import load_entry_document

def main():
    entries_dir = REPO_ROOT / "entries"

    tag_counter = Counter()
    all_tags = set()

    for path in sorted(entries_dir.glob("*.md")):
        try:
            doc = load_entry_document(path)
            for tag in doc.tags:
                tag_counter[tag] += 1
                all_tags.add(tag)
        except Exception as e:
            print(f"警告: 解析 {path.name} 失败: {e}")
            continue

    print("=== 标签使用频率统计 ===")
    print(f"总标签数: {len(all_tags)}")
    print(f"总词条数: {sum(tag_counter.values())}")
    print()

    print("=== TOP 30 使用最多的标签 ===")
    for tag, count in tag_counter.most_common(30):
        print(f"  {tag}: {count}")

    print("\n=== 所有标签列表 (按字母顺序) ===")
    for tag in sorted(all_tags):
        print(f"  - {tag}")

if __name__ == "__main__":
    main()
