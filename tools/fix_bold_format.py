#!/usr/bin/env python3
"""
修复 Markdown 文件中的加粗格式问题
用于确保 MkDocs Material 正确渲染加粗文本和链接
"""

import re
from pathlib import Path
from typing import List, Tuple


def fix_bold_link_format(content: str) -> Tuple[str, int]:
    """
    修复 **[文本](链接)** 格式为 **文本（[链接](url)）**

    Returns:
        (修复后的内容, 修复次数)
    """
    count = 0

    # 匹配 **[文本](链接)** 格式
    pattern = r'\*\*\[([^\]]+)\]\(([^\)]+)\)\*\*'

    def replacer(match):
        nonlocal count
        text = match.group(1)
        url = match.group(2)

        # 提取中文和英文部分
        # 例如: "创伤(Trauma)" -> "创伤", "Trauma"
        chinese_english_pattern = r'^(.+?)[(\(]([^)\)]+)[)\)]$'
        m = re.match(chinese_english_pattern, text)

        if m:
            chinese = m.group(1)
            english = m.group(2)
            count += 1
            return f'**{chinese}（[{english}]({url})）**'
        else:
            # 如果没有括号，直接处理
            count += 1
            return f'**{text}**（[{text}]({url})）'

    return re.sub(pattern, replacer, content), count


def fix_list_bold_spacing(content: str) -> Tuple[str, int]:
    """
    修复列表项中加粗文本前缺少空格的问题
    例如: - 可以切**意识** -> - 可以切 **意识**

    Returns:
        (修复后的内容, 修复次数)
    """
    count = 0
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # 匹配列表项中间位置的加粗文本（前面没有空格）
        if line.startswith('- ') and '**' in line:
            # 查找 汉字** 或 字母** 的模式（加粗前缺少空格）
            pattern = r'([^\s\*])\*\*([^\*]+)\*\*'

            def replacer(match):
                nonlocal count
                before = match.group(1)
                bold_text = match.group(2)
                count += 1
                return f'{before} **{bold_text}**'

            fixed_line = re.sub(pattern, replacer, line)
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), count


def fix_parentheses_in_links(content: str) -> Tuple[str, int]:
    """
    修复链接文本中的半角括号为全角括号
    例如: [创伤(Trauma)](Trauma.md) -> [创伤（Trauma）](Trauma.md)

    Returns:
        (修复后的内容, 修复次数)
    """
    count = 0

    # 匹配链接文本中的半角括号
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

    def replacer(match):
        nonlocal count
        text = match.group(1)
        url = match.group(2)

        # 替换文本中的半角括号为全角括号
        if '(' in text or ')' in text:
            new_text = text.replace('(', '（').replace(')', '）')
            count += 1
            return f'[{new_text}]({url})'
        return match.group(0)

    return re.sub(pattern, replacer, content), count


def fix_colon_before_links(content: str) -> Tuple[str, int]:
    """
    修复"参阅:"等冒号为全角冒号

    Returns:
        (修复后的内容, 修复次数)
    """
    count = 0

    # 匹配"参阅:"、"参考:"等
    patterns = [
        (r'参阅:', '参阅：'),
        (r'参考:', '参考：'),
        (r'延伸阅读:', '延伸阅读：'),
        (r'详细了解请参阅:', '详细了解请参阅：'),
    ]

    result = content
    for pattern, replacement in patterns:
        if pattern in result:
            result = result.replace(pattern, replacement)
            count += result.count(replacement) - content.count(replacement)

    return result, count


def process_file(file_path: Path) -> dict:
    """
    处理单个文件

    Returns:
        修复统计信息
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        stats = {
            'file': str(file_path),
            'bold_link': 0,
            'list_spacing': 0,
            'parentheses': 0,
            'colon': 0,
            'total': 0,
        }

        # 应用所有修复
        content, count1 = fix_bold_link_format(content)
        stats['bold_link'] = count1

        content, count2 = fix_list_bold_spacing(content)
        stats['list_spacing'] = count2

        content, count3 = fix_parentheses_in_links(content)
        stats['parentheses'] = count3

        content, count4 = fix_colon_before_links(content)
        stats['colon'] = count4

        stats['total'] = count1 + count2 + count3 + count4

        # 只有在有修改时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return stats
    except Exception as e:
        return {'file': str(file_path), 'error': str(e)}


def main():
    """主函数"""
    import sys
    import io

    # 修复 Windows 控制台编码问题
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    docs_entries = Path('docs/entries')

    if not docs_entries.exists():
        print(f"错误：目录不存在 {docs_entries}")
        return

    # 收集所有 Markdown 文件
    md_files = list(docs_entries.glob('*.md'))

    print(f"找到 {len(md_files)} 个词条文件")
    print("开始处理...\n")

    all_stats = []
    total_fixes = 0

    for md_file in sorted(md_files):
        stats = process_file(md_file)

        if 'error' in stats:
            print(f"❌ {stats['file']}: {stats['error']}")
        elif stats['total'] > 0:
            all_stats.append(stats)
            total_fixes += stats['total']
            print(f"✓ {md_file.name}: "
                  f"加粗链接={stats['bold_link']}, "
                  f"列表空格={stats['list_spacing']}, "
                  f"括号={stats['parentheses']}, "
                  f"冒号={stats['colon']}")

    print(f"\n处理完成！")
    print(f"共修复 {len(all_stats)} 个文件，{total_fixes} 处问题")

    if all_stats:
        print("\n修复统计：")
        print(f"- 加粗链接格式: {sum(s['bold_link'] for s in all_stats)}")
        print(f"- 列表空格: {sum(s['list_spacing'] for s in all_stats)}")
        print(f"- 括号格式: {sum(s['parentheses'] for s in all_stats)}")
        print(f"- 冒号格式: {sum(s['colon'] for s in all_stats)}")


if __name__ == '__main__':
    main()
