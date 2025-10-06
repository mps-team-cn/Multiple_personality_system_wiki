#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 Markdown 文件中的粗体格式问题
1. 将 -**xxxx**: 修改为 - **xxxx** :
2. 确保加粗文本与中文之间有空格
确保 Material for MkDocs 正确渲染
"""

import re
from pathlib import Path
from typing import Tuple


def fix_list_bold_colon(content: str) -> Tuple[str, list]:
    """
    修复列表项中粗体冒号格式
    -**text**: -> - **text** :
    -**text**： -> - **text** :

    支持半角冒号(:)和全角冒号(：)

    Returns:
        (修复后的内容, 修改记录列表)
    """
    lines = content.split('\n')
    fixed_lines = []
    changes = []

    # 匹配模式：行首可能有空格，然后是 -**内容**: 或 -**内容**：
    # 支持半角冒号和全角冒号
    pattern = re.compile(r'^(\s*)-\*\*([^*]+)\*\*[：:]\s*(.*)$')
    
    for i, line in enumerate(lines, 1):
        match = pattern.match(line)
        if match:
            indent = match.group(1)  # 前面的缩进
            bold_text = match.group(2)  # 加粗的文本
            rest = match.group(3)  # 冒号后面的内容
            
            # 构造新格式：缩进 + - + 空格 + ** + 文本 + ** + 空格 + : + 空格 + 其余内容
            new_line = f"{indent}- **{bold_text}** : {rest}"
            fixed_lines.append(new_line)
            
            changes.append({
                'line': i,
                'old': line,
                'new': new_line
            })
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines), changes


def fix_bold_spacing(content: str) -> Tuple[str, list]:
    """
    修复加粗文本与中文之间的空格问题
    **中文**中文 -> **中文** 中文
    中文**中文** -> 中文 **中文**

    注意：
    - 行首和行尾的加粗文本不处理
    - 加粗文本与标点符号之间不加空格

    Returns:
        (修复后的内容, 修改记录列表)
    """
    lines = content.split('\n')
    fixed_lines = []
    changes = []

    # 中文字符范围（包括常用汉字和标点）
    chinese_pattern = r'[\u4e00-\u9fff\u3400-\u4dbf]'
    # 中文标点（不需要空格的情况）
    chinese_punct = r'[，。！？；：、''""（）《》【】…—]'

    for i, line in enumerate(lines, 1):
        original_line = line
        modified = False

        # 处理 **文本**后面紧跟中文字符（非标点）的情况
        # 负向前瞻确保后面不是标点
        pattern1 = re.compile(rf'(\*\*[^*]+\*\*)(?![\s{chinese_punct[1:-1]}])({chinese_pattern})')
        line = pattern1.sub(r'\1 \2', line)

        # 处理中文字符后面紧跟**文本**的情况
        # 负向后顾确保前面不是标点或空格
        pattern2 = re.compile(rf'(?<![\s{chinese_punct[1:-1]}])({chinese_pattern})(\*\*[^*]+\*\*)')
        line = pattern2.sub(r'\1 \2', line)

        if line != original_line:
            fixed_lines.append(line)
            changes.append({
                'line': i,
                'old': original_line,
                'new': line
            })
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), changes


def process_file(file_path: Path, dry_run: bool = False) -> dict:
    """
    处理单个文件

    Args:
        file_path: 文件路径
        dry_run: 如果为True，只预览不实际修改

    Returns:
        处理统计信息
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 应用所有修复规则
        all_changes = []

        # 1. 修复列表项的粗体冒号格式
        content, changes1 = fix_list_bold_colon(content)
        all_changes.extend(changes1)

        # 2. 修复加粗文本与中文之间的空格
        content, changes2 = fix_bold_spacing(content)
        all_changes.extend(changes2)

        result = {
            'file': str(file_path),
            'changes': len(all_changes),
            'details': all_changes
        }

        if all_changes and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            result['modified'] = True
        else:
            result['modified'] = False

        return result

    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e)
        }


def main():
    """主函数"""
    import sys
    
    # 解析命令行参数
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    if dry_run:
        print("=" * 60)
        print("预览模式 (Dry Run)")
        print("只显示会修改什么，不会实际修改文件")
        print("=" * 60)
        print()
    
    # 查找所有 Markdown 文件
    docs_path = Path('docs')
    if not docs_path.exists():
        docs_path = Path('.')
    
    md_files = list(docs_path.rglob('*.md'))
    
    # 排除某些目录
    excluded = ['.git', 'node_modules', 'venv', '.venv']
    md_files = [f for f in md_files if not any(ex in str(f) for ex in excluded)]
    
    print(f"找到 {len(md_files)} 个 Markdown 文件\n")
    
    total_files_changed = 0
    total_changes = 0
    all_results = []
    
    for md_file in sorted(md_files):
        result = process_file(md_file, dry_run)
        
        if 'error' in result:
            print(f"[ERROR] {result['file']}")
            print(f"   {result['error']}\n")
        elif result['changes'] > 0:
            all_results.append(result)
            total_files_changed += 1
            total_changes += result['changes']

            status = '[预览]' if dry_run else '[修改]'
            print(f"{status} {md_file.name}")
            print(f"   发现 {result['changes']} 处需要修改")

            # 显示前3个修改示例，避免字符截断问题
            for change in result['details'][:3]:
                old_line = change['old']
                new_line = change['new']
                # 安全截断，避免破坏UTF-8字符
                if len(old_line.encode('utf-8')) > 100:
                    old_line = old_line[:30] + "..."
                if len(new_line.encode('utf-8')) > 100:
                    new_line = new_line[:30] + "..."

                try:
                    print(f"   行 {change['line']}:")
                    print(f"     旧: {old_line}")
                    print(f"     新: {new_line}")
                except UnicodeEncodeError:
                    print(f"   行 {change['line']}: (包含特殊字符)")

            if len(result['details']) > 3:
                print(f"   ... 还有 {len(result['details']) - 3} 处修改")
            print()
    
    # 打印总结
    print("=" * 60)
    print("处理完成")
    print("=" * 60)
    print(f"修改文件数: {total_files_changed}")
    print(f"修改总数: {total_changes}")
    
    if dry_run:
        print()
        print("这是预览模式，未实际修改任何文件")
        print("要实际修改，请运行: python tools/fix_list_bold_colon.py")
    else:
        print()
        print("所有文件已成功修改！")
    print("=" * 60)


if __name__ == '__main__':
    main()
