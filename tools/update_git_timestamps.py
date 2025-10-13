#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据 Git 历史记录更新词条的 updated 字段

用法:
  python tools/update_git_timestamps.py                    # 更新所有词条
  python tools/update_git_timestamps.py --dry-run          # 预览模式(不实际修改文件)
  python tools/update_git_timestamps.py --verbose          # 显示详细信息
  python tools/update_git_timestamps.py docs/entries/DID.md  # 更新指定文件
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def get_git_last_modified_date(file_path: Path) -> Optional[str]:
    """
    获取文件在 Git 中的最后修改日期

    Args:
        file_path: 文件路径

    Returns:
        YYYY-MM-DD 格式的日期字符串,如果获取失败则返回 None
    """
    try:
        # 使用 git log 获取文件的最后提交时间
        # 注意：使用仓库根目录作为工作目录，而不是文件所在目录
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ai', '--', str(file_path)],
            capture_output=True,
            text=True,
            check=True
        )

        if not result.stdout.strip():
            # 文件可能是新添加但未提交的
            return None

        # 解析时间戳 (格式: 2025-10-11 13:02:30 +0800)
        timestamp_str = result.stdout.strip().split()[0]
        return timestamp_str

    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  获取 {file_path.name} 的 Git 时间戳失败: {e}", file=sys.stderr)
        return None


def parse_frontmatter(content: str) -> Tuple[str, str, str]:
    """
    解析 Markdown 文件的 frontmatter

    Returns:
        (frontmatter_text, body, updated_value)
        updated_value 为 None 表示没有 updated 字段
    """
    # 匹配 YAML frontmatter
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return '', content, None

    frontmatter_text = match.group(1)
    body = match.group(2)

    # 查找 updated 字段
    updated_pattern = r'^updated:\s*(.+)$'
    updated_match = re.search(updated_pattern, frontmatter_text, re.MULTILINE)
    updated_value = updated_match.group(1).strip() if updated_match else None

    return frontmatter_text, body, updated_value


def update_frontmatter_date(frontmatter_text: str, new_date: str) -> str:
    """
    更新 frontmatter 中的 updated 字段

    Args:
        frontmatter_text: frontmatter 文本
        new_date: 新的日期 (YYYY-MM-DD)

    Returns:
        更新后的 frontmatter 文本
    """
    updated_pattern = r'^updated:\s*.+$'

    # 检查是否已有 updated 字段
    if re.search(updated_pattern, frontmatter_text, re.MULTILINE):
        # 替换现有的 updated 字段
        new_frontmatter = re.sub(
            updated_pattern,
            f'updated: {new_date}',
            frontmatter_text,
            flags=re.MULTILINE
        )
    else:
        # 添加 updated 字段 (在 frontmatter 末尾)
        new_frontmatter = frontmatter_text.rstrip() + f'\nupdated: {new_date}'

    return new_frontmatter


def update_file_timestamp(
    file_path: Path,
    dry_run: bool = False,
    verbose: bool = False
) -> Tuple[bool, str]:
    """
    更新单个文件的时间戳

    Args:
        file_path: 文件路径
        dry_run: 是否为预览模式
        verbose: 是否显示详细信息

    Returns:
        (是否修改, 状态消息)
    """
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"❌ 读取失败: {e}"

    # 解析 frontmatter
    frontmatter_text, body, current_updated = parse_frontmatter(content)

    if not frontmatter_text:
        return False, "⏭️  跳过: 没有 frontmatter"

    # 获取 Git 时间戳
    git_date = get_git_last_modified_date(file_path)

    if not git_date:
        return False, "⚠️  跳过: 无法获取 Git 时间戳 (可能未提交)"

    # 比较日期
    if current_updated == git_date:
        if verbose:
            return False, f"✓ 已是最新: {git_date}"
        return False, "✓"

    # 更新 frontmatter
    new_frontmatter = update_frontmatter_date(frontmatter_text, git_date)
    new_content = f'---\n{new_frontmatter}\n---\n{body}'

    # 预览模式或实际写入
    if dry_run:
        old_display = current_updated or "(无)"
        return True, f"🔄 将更新: {old_display} → {git_date}"
    else:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            old_display = current_updated or "(无)"
            return True, f"✅ 已更新: {old_display} → {git_date}"
        except Exception as e:
            return False, f"❌ 写入失败: {e}"


def process_files(
    files: list[Path],
    dry_run: bool = False,
    verbose: bool = False
) -> Tuple[int, int, int]:
    """
    批量处理文件

    Returns:
        (修改数量, 跳过数量, 总数量)
    """
    modified_count = 0
    skipped_count = 0

    for file_path in files:
        modified, message = update_file_timestamp(file_path, dry_run, verbose)

        if modified or verbose or dry_run:
            print(f"{file_path.name:50s} {message}")

        if modified:
            modified_count += 1
        else:
            skipped_count += 1

    return modified_count, skipped_count, len(files)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='根据 Git 历史记录更新词条的 updated 字段',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                           # 更新所有词条
  %(prog)s --dry-run                 # 预览模式
  %(prog)s --verbose                 # 显示详细信息
  %(prog)s docs/entries/DID.md       # 更新指定文件
        """
    )

    parser.add_argument(
        'paths',
        nargs='*',
        help='要处理的文件或目录路径 (默认: docs/entries/)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式,不实际修改文件'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细信息 (包括未修改的文件)'
    )

    args = parser.parse_args()

    # 确定要处理的文件
    if args.paths:
        files = []
        for path_str in args.paths:
            path = Path(path_str)
            if path.is_file() and path.suffix == '.md':
                files.append(path)
            elif path.is_dir():
                files.extend(sorted(path.glob('*.md')))
            else:
                print(f"⚠️  跳过无效路径: {path_str}", file=sys.stderr)
    else:
        # 默认处理 docs/entries/
        entries_dir = Path(__file__).parent.parent / 'docs' / 'entries'
        if not entries_dir.exists():
            print(f"❌ 错误: {entries_dir} 不存在", file=sys.stderr)
            return 1
        files = sorted(entries_dir.glob('*.md'))

    if not files:
        print("❌ 错误: 没有找到要处理的 .md 文件", file=sys.stderr)
        return 1

    # 显示处理信息
    mode_text = "预览模式" if args.dry_run else "更新模式"
    print(f"📊 {mode_text}: 找到 {len(files)} 个词条文件")
    print("=" * 80)

    # 处理文件
    modified_count, skipped_count, total_count = process_files(
        files,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    # 显示统计
    print("=" * 80)
    print(f"✨ 完成!")
    if args.dry_run:
        print(f"   - 将修改: {modified_count} 个文件")
    else:
        print(f"   - 已修改: {modified_count} 个文件")
    print(f"   - 已跳过: {skipped_count} 个文件")
    print(f"   - 总计: {total_count} 个文件")

    if args.dry_run and modified_count > 0:
        print()
        print("💡 提示: 移除 --dry-run 参数以实际更新文件")

    return 0


if __name__ == '__main__':
    sys.exit(main())
