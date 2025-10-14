#!/usr/bin/env python3
"""
检查词条的 description 字段覆盖情况
"""
import os
import re
from pathlib import Path

def extract_frontmatter(content):
    """提取 Frontmatter 内容"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def has_description(frontmatter):
    """检查是否包含 description 字段"""
    if not frontmatter:
        return False
    return bool(re.search(r'^\s*description\s*:', frontmatter, re.MULTILINE))

def extract_title(frontmatter):
    """提取 title"""
    if not frontmatter:
        return None
    match = re.search(r'^\s*title\s*:\s*(.+)$', frontmatter, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def main():
    entries_dir = Path('docs/entries')

    if not entries_dir.exists():
        print(f"错误: {entries_dir} 目录不存在")
        return

    all_entries = []
    with_description = []
    without_description = []

    for entry_file in sorted(entries_dir.glob('*.md')):
        try:
            content = entry_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)
            title = extract_title(frontmatter)

            entry_info = {
                'file': entry_file.name,
                'title': title or entry_file.stem,
                'has_description': has_description(frontmatter)
            }

            all_entries.append(entry_info)

            if entry_info['has_description']:
                with_description.append(entry_info)
            else:
                without_description.append(entry_info)

        except Exception as e:
            print(f"处理 {entry_file.name} 时出错: {e}")

    # 输出统计结果
    total = len(all_entries)
    with_desc_count = len(with_description)
    without_desc_count = len(without_description)
    coverage = (with_desc_count / total * 100) if total > 0 else 0

    print("=" * 70)
    print(f"词条 description 字段覆盖情况统计")
    print("=" * 70)
    print(f"总词条数: {total}")
    print(f"已有 description: {with_desc_count} ({coverage:.1f}%)")
    print(f"缺少 description: {without_desc_count} ({100-coverage:.1f}%)")
    print("=" * 70)

    if without_description:
        print(f"\n缺少 description 的词条列表 ({without_desc_count} 个):")
        print("-" * 70)
        for i, entry in enumerate(without_description, 1):
            print(f"{i:3d}. {entry['file']:50s} | {entry['title']}")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
