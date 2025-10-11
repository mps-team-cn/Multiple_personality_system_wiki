#!/usr/bin/env python3
"""
批量为词条添加评论功能
为 docs/entries/ 目录下的所有 Markdown 文件添加 comments: true 到 frontmatter
"""

import os
import re
from pathlib import Path
from typing import Tuple


def parse_frontmatter(content: str) -> Tuple[dict, str, str]:
    """
    解析 Markdown 文件的 frontmatter

    Returns:
        (frontmatter_dict, frontmatter_text, body)
    """
    # 匹配 YAML frontmatter
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        # 没有 frontmatter
        return {}, '', content

    frontmatter_text = match.group(1)
    body = match.group(2)

    # 简单解析 frontmatter (只需要检查是否有 comments 字段)
    frontmatter_dict = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key = line.split(':', 1)[0].strip()
            frontmatter_dict[key] = line.split(':', 1)[1].strip()

    return frontmatter_dict, frontmatter_text, body


def add_comments_to_file(file_path: Path) -> bool:
    """
    为单个文件添加 comments: true

    Returns:
        True if modified, False if already has comments or no frontmatter
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter_dict, frontmatter_text, body = parse_frontmatter(content)

    # 如果没有 frontmatter，跳过
    if not frontmatter_text:
        print(f"⚠️  跳过 {file_path.name}: 没有 frontmatter")
        return False

    # 如果已经有 comments 字段，跳过
    if 'comments' in frontmatter_dict:
        print(f"⏭️  跳过 {file_path.name}: 已有 comments 字段")
        return False

    # 添加 comments: true
    # 在 frontmatter 末尾添加
    new_frontmatter = frontmatter_text.rstrip() + '\ncomments: true'
    new_content = f'---\n{new_frontmatter}\n---\n{body}'

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ 已添加 {file_path.name}")
    return True


def main():
    """批量处理所有词条"""
    entries_dir = Path(__file__).parent.parent / 'docs' / 'entries'

    if not entries_dir.exists():
        print(f"❌ 错误: {entries_dir} 不存在")
        return

    # 获取所有 .md 文件
    md_files = sorted(entries_dir.glob('*.md'))

    if not md_files:
        print(f"❌ 错误: {entries_dir} 中没有找到 .md 文件")
        return

    print(f"📊 找到 {len(md_files)} 个词条文件")
    print("=" * 60)

    modified_count = 0
    skipped_count = 0

    for md_file in md_files:
        if add_comments_to_file(md_file):
            modified_count += 1
        else:
            skipped_count += 1

    print("=" * 60)
    print(f"✨ 完成!")
    print(f"   - 已修改: {modified_count} 个文件")
    print(f"   - 已跳过: {skipped_count} 个文件")
    print(f"   - 总计: {len(md_files)} 个文件")


if __name__ == '__main__':
    main()
