#!/usr/bin/env python3
"""优化词条标签"""

from pathlib import Path
import sys
import re

# 添加路径
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.pdf_export.pdf_export.frontmatter import load_entry_document

# 标签映射规则
TAG_MAPPING = {
    '&': None,  # 删除
    '3.0': None,  # 删除
    '解离性身份障碍_DID': 'DID',
    '创伤后应激障碍_PTSD': 'PTSD',
    '其他特定解离性障碍_OSDD': 'OSDD',
    '注意力缺陷多动障碍_ADHD': 'ADHD',
    '管理员': None,  # 删除，因为已有"多重意识体"标签
}

def update_tags_in_file(file_path: Path) -> bool:
    """更新文件中的标签"""
    content = file_path.read_text(encoding='utf-8')

    # 匹配 frontmatter
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f'警告: {file_path.name} 没有找到 frontmatter')
        return False

    frontmatter = match.group(1)

    # 提取tags部分
    tags_pattern = r'tags:\n((?:- .+\n)*)'
    tags_match = re.search(tags_pattern, frontmatter)

    if not tags_match:
        return False

    tags_section = tags_match.group(0)
    original_tags_section = tags_section

    # 替换标签
    modified = False
    for old_tag, new_tag in TAG_MAPPING.items():
        old_line = f"- '{old_tag}'\n"
        old_line_no_quote = f"- {old_tag}\n"

        if new_tag is None:
            # 删除标签
            if old_line in tags_section:
                tags_section = tags_section.replace(old_line, '')
                modified = True
                print(f'  删除标签: {old_tag}')
            elif old_line_no_quote in tags_section:
                tags_section = tags_section.replace(old_line_no_quote, '')
                modified = True
                print(f'  删除标签: {old_tag}')
        else:
            # 替换标签
            new_line = f"- {new_tag}\n"
            if old_line in tags_section:
                tags_section = tags_section.replace(old_line, new_line)
                modified = True
                print(f'  替换标签: {old_tag} → {new_tag}')
            elif old_line_no_quote in tags_section:
                tags_section = tags_section.replace(old_line_no_quote, new_line)
                modified = True
                print(f'  替换标签: {old_tag} → {new_tag}')

    if not modified:
        return False

    # 更新文件内容
    new_content = content.replace(original_tags_section, tags_section)
    file_path.write_text(new_content, encoding='utf-8')
    return True

def main():
    # 同时更新两个目录
    entries_dirs = [
        REPO_ROOT / 'entries',
        REPO_ROOT / 'docs' / 'entries'
    ]

    for entries_dir in entries_dirs:
        if not entries_dir.exists():
            print(f'跳过不存在的目录: {entries_dir}')
            continue

        print(f'开始优化标签: {entries_dir}')
        print('=' * 80)

        updated_count = 0
        for path in sorted(entries_dir.glob('*.md')):
            try:
                if update_tags_in_file(path):
                    print(f'[OK] 更新: {path.name}')
                    updated_count += 1
            except Exception as e:
                print(f'[ERROR] 错误 {path.name}: {e}')

        print('=' * 80)
        print(f'{entries_dir.name} 目录完成! 共更新 {updated_count} 个文件')
        print()

if __name__ == '__main__':
    main()
