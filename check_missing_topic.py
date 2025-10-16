#!/usr/bin/env python3
"""检查词条文件中缺少 topic 字段的文件"""

import os
import re
from pathlib import Path

def parse_frontmatter(content):
    """解析 Frontmatter"""
    pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter

def check_entries():
    """检查所有词条文件"""
    entries_dir = Path('docs/entries')
    missing_topic = []
    no_frontmatter = []

    for md_file in sorted(entries_dir.glob('*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = parse_frontmatter(content)

        if frontmatter is None:
            no_frontmatter.append(md_file.name)
        elif 'topic' not in frontmatter:
            missing_topic.append(md_file.name)

    print(f"总计词条文件: {len(list(entries_dir.glob('*.md')))} 个\n")

    if no_frontmatter:
        print(f"❌ 没有 Frontmatter 的文件 ({len(no_frontmatter)} 个):")
        for name in no_frontmatter:
            print(f"  - {name}")
        print()

    if missing_topic:
        print(f"⚠️  缺少 topic 字段的文件 ({len(missing_topic)} 个):")
        for name in missing_topic:
            print(f"  - {name}")
    else:
        print("✅ 所有词条都包含 topic 字段")

if __name__ == '__main__':
    check_entries()
