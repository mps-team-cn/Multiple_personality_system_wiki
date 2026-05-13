#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查 docs/entries/ 目录下所有 Markdown 文件的 Frontmatter 状态

检查项：
1. 是否包含 YAML Frontmatter（以 --- 开头和结尾）
2. 必需字段是否完整：title, tags, topic, description, updated

输出报告：
- 完全缺失 Frontmatter 的文件列表
- Frontmatter 不完整的文件列表（缺少哪些字段）
- 统计信息（总数、完整数、需要修复数）

用法：
    python3 tools/check_frontmatter.py
    python3 tools/check_frontmatter.py --verbose  # 显示详细信息
    python3 tools/check_frontmatter.py --path docs/entries/  # 指定目录
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

import yaml

# 必需的 Frontmatter 字段
REQUIRED_FIELDS = {"title", "tags", "topic", "updated"}

# 可选字段（仅供参考，不影响检查结果）
OPTIONAL_FIELDS = {"synonyms", "comments", "description"}

# 排除的文件（模板、索引、导览等）
EXCLUDE_FILES = {
    "TEMPLATE_ENTRY.md",
    "index.md",
    "SUMMARY.md",
}

# 排除的文件模式（如 *-index.md, *-Guide.md）
EXCLUDE_PATTERNS = [
    r".*-index\.md$",
    r".*-Guide\.md$",
]


def is_excluded(file_path: Path) -> bool:
    """检查文件是否应该被排除"""
    filename = file_path.name

    # 检查排除文件列表
    if filename in EXCLUDE_FILES:
        return True

    # 检查排除模式
    for pattern in EXCLUDE_PATTERNS:
        if re.match(pattern, filename):
            return True

    return False


def extract_frontmatter(content: str) -> Optional[Dict]:
    """
    从 Markdown 内容中提取 Frontmatter

    Args:
        content: Markdown 文件内容

    Returns:
        解析后的 YAML 字典，如果没有 Frontmatter 返回 None
    """
    # 匹配 YAML Frontmatter：以 --- 开头和结尾
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None

    yaml_content = match.group(1)

    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        # YAML 解析错误
        return {"_parse_error": str(e)}


def check_frontmatter(frontmatter: Optional[Dict]) -> Tuple[bool, Set[str]]:
    """
    检查 Frontmatter 是否完整

    Args:
        frontmatter: 解析后的 Frontmatter 字典

    Returns:
        (is_complete, missing_fields)
    """
    if frontmatter is None:
        return False, REQUIRED_FIELDS

    if "_parse_error" in frontmatter:
        return False, {"_parse_error"}

    existing_fields = set(frontmatter.keys())
    missing_fields = REQUIRED_FIELDS - existing_fields

    return len(missing_fields) == 0, missing_fields


def check_file(file_path: Path) -> Tuple[str, bool, Set[str], Optional[str]]:
    """
    检查单个 Markdown 文件的 Frontmatter

    Args:
        file_path: 文件路径

    Returns:
        (status, is_complete, missing_fields, error_message)
        status: "complete", "incomplete", "missing", "error"
    """
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return "error", False, set(), f"读取文件失败：{e}"

    frontmatter = extract_frontmatter(content)

    if frontmatter is None:
        return "missing", False, REQUIRED_FIELDS, None

    if "_parse_error" in frontmatter:
        return "error", False, {"_parse_error"}, f"YAML 解析错误：{frontmatter['_parse_error']}"

    is_complete, missing_fields = check_frontmatter(frontmatter)

    if is_complete:
        return "complete", True, set(), None
    else:
        return "incomplete", False, missing_fields, None


def format_field_list(fields: Set[str]) -> str:
    """格式化字段列表"""
    if not fields:
        return ""
    return ", ".join(sorted(fields))


def main():
    parser = argparse.ArgumentParser(
        description="检查 docs/entries/ 目录下所有 Markdown 文件的 Frontmatter 状态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
必需字段：
  - title: 词条标题
  - tags: 分类标签（YAML 列表）
  - topic: 主题分类
  - updated: 最后更新时间（YYYY-MM-DD）

可选字段：
  - description: SEO 描述（120-155 字符）
  - synonyms: 同义词列表
  - comments: 是否启用评论区

用法示例：
  python3 tools/check_frontmatter.py                    # 检查默认目录
  python3 tools/check_frontmatter.py --verbose          # 显示详细信息
  python3 tools/check_frontmatter.py --path docs/entries/  # 指定目录
        """
    )
    parser.add_argument(
        "--path",
        default="docs/entries",
        help="要检查的目录路径（默认：docs/entries）"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息（包括完整的文件）"
    )

    args = parser.parse_args()

    # 确定目录路径
    entries_dir = Path(args.path)
    if not entries_dir.exists():
        print(f"错误：目录不存在：{entries_dir}")
        sys.exit(1)

    if not entries_dir.is_dir():
        print(f"错误：不是目录：{entries_dir}")
        sys.exit(1)

    # 查找所有 Markdown 文件
    md_files = sorted([f for f in entries_dir.glob("*.md") if not is_excluded(f)])

    if not md_files:
        print(f"警告：在 {entries_dir} 中没有找到 Markdown 文件")
        sys.exit(0)

    print("=" * 70)
    print("Frontmatter 完整性检查")
    print("=" * 70)
    print(f"检查目录：{entries_dir.resolve()}")
    print(f"找到 {len(md_files)} 个词条文件")
    print()

    # 分类统计
    complete_files = []
    incomplete_files = []
    missing_files = []
    error_files = []

    # 检查所有文件
    for md_file in md_files:
        status, is_complete, missing_fields, error_msg = check_file(md_file)

        if status == "complete":
            complete_files.append(md_file)
        elif status == "incomplete":
            incomplete_files.append((md_file, missing_fields))
        elif status == "missing":
            missing_files.append(md_file)
        elif status == "error":
            error_files.append((md_file, error_msg))

    # 输出报告
    total = len(md_files)
    complete_count = len(complete_files)
    incomplete_count = len(incomplete_files)
    missing_count = len(missing_files)
    error_count = len(error_files)
    needs_fix = incomplete_count + missing_count + error_count

    # 1. 完全缺失 Frontmatter 的文件
    if missing_files:
        print(f"📋 完全缺失 Frontmatter 的文件（{missing_count} 个）：")
        print("-" * 70)
        for file_path in missing_files:
            print(f"  ❌ {file_path.name}")
        print()

    # 2. Frontmatter 不完整的文件
    if incomplete_files:
        print(f"📋 Frontmatter 不完整的文件（{incomplete_count} 个）：")
        print("-" * 70)
        for file_path, missing_fields in incomplete_files:
            print(f"  ⚠️  {file_path.name}")
            print(f"      缺少字段：{format_field_list(missing_fields)}")
        print()

    # 3. 解析错误的文件
    if error_files:
        print(f"📋 解析错误的文件（{error_count} 个）：")
        print("-" * 70)
        for file_path, error_msg in error_files:
            print(f"  ❌ {file_path.name}")
            print(f"      {error_msg}")
        print()

    # 4. 完整的文件（仅在 verbose 模式下显示）
    if args.verbose and complete_files:
        print(f"📋 Frontmatter 完整的文件（{complete_count} 个）：")
        print("-" * 70)
        for file_path in complete_files:
            print(f"  ✅ {file_path.name}")
        print()

    # 5. 统计信息
    print("=" * 70)
    print("📊 统计信息")
    print("=" * 70)
    print(f"总文件数：        {total}")
    print(f"完整：            {complete_count} ({complete_count/total*100:.1f}%)")
    print(f"不完整：          {incomplete_count} ({incomplete_count/total*100:.1f}%)")
    print(f"缺失 Frontmatter：{missing_count} ({missing_count/total*100:.1f}%)")
    print(f"解析错误：        {error_count} ({error_count/total*100:.1f}%)")
    print("-" * 70)
    print(f"需要修复：        {needs_fix} ({needs_fix/total*100:.1f}%)")
    print()

    # 6. 结论
    if needs_fix == 0:
        print("✅ 所有文件的 Frontmatter 均完整！")
        sys.exit(0)
    else:
        print(f"⚠️  发现 {needs_fix} 个文件需要修复")
        print()
        print("💡 修复建议：")
        print("   1. 参考 docs/TEMPLATE_ENTRY.md 中的 Frontmatter 模板")
        print("   2. 确保包含所有必需字段：title, tags, topic, description, updated")
        print("   3. tags 应使用 YAML 列表格式")
        print("   4. description 长度应为 120-155 字符")
        print("   5. updated 格式应为 YYYY-MM-DD")
        sys.exit(1)


if __name__ == "__main__":
    main()
