#!/usr/bin/env python3
"""
标签标准化脚本 - 基于 MPS Wiki Tagging Standard v2.0

将旧格式标签批量转换为新的分面前缀格式,通过 data/tags_alias.yaml 进行映射。

核心功能:
  1. 读取词条 Frontmatter 中的标签
  2. 应用别名映射表(tags_alias.yaml)将旧标签转换为新格式
  3. 验证转换后的标签符合 v2.0 规范
  4. 生成转换报告和预览

使用方法:
  # 预览模式(不修改文件)
  python3 tools/tag_normalization.py

  # 执行模式(实际修改文件)
  python3 tools/tag_normalization.py --execute

  # 检查单个文件
  python3 tools/tag_normalization.py --file docs/entries/DID.md

  # 详细模式(显示所有文件,包括无需修改的)
  python3 tools/tag_normalization.py --verbose
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

import frontmatter
import yaml


# 允许的标签前缀(分面体系)
ALLOWED_PREFIXES = {
    "dx", "sx", "tx", "scale", "theory", "ops", "role",
    "community", "guide", "history", "misuse", "bio", "sleep",
    "dev", "culture", "meta",
}

# 标签格式正则
TAG_PATTERN = re.compile(r"^[a-z]+:[^\s()]+$")


@dataclass
class TagChange:
    """标签变更记录"""
    file: Path
    old_tags: List[str]
    new_tags: List[str]
    removed: Set[str]
    added: Set[str]
    mapped: Dict[str, str]  # 旧标签 -> 新标签的映射


def load_alias_map(path: Path) -> Dict[str, str]:
    """
    加载标签别名映射表

    返回: {旧标签/别名 -> 规范标签} 的映射字典
    """
    if not path.exists():
        print(f"⚠️ 警告: 别名文件不存在 {path}")
        return {}

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            print(f"⚠️ 警告: 别名文件格式不正确 {path}")
            return {}

        # 转换为 str -> str 映射
        alias_map = {str(k).strip(): str(v).strip() for k, v in data.items()}
        return alias_map
    except Exception as e:
        print(f"⚠️ 警告: 读取别名文件失败 {path}: {e}")
        return {}


def normalize_tag(tag: str, alias_map: Dict[str, str]) -> str | None:
    """
    标准化单个标签

    Args:
        tag: 原始标签
        alias_map: 别名映射表

    Returns:
        标准化后的标签,如果需要删除则返回 None
    """
    tag = tag.strip()

    # 如果已经是规范格式,直接返回
    if TAG_PATTERN.match(tag):
        prefix = tag.split(":", 1)[0]
        if prefix in ALLOWED_PREFIXES:
            return tag

    # 尝试从别名映射表中查找
    if tag in alias_map:
        normalized = alias_map[tag]
        # 验证映射后的标签是否合法
        if TAG_PATTERN.match(normalized):
            prefix = normalized.split(":", 1)[0]
            if prefix in ALLOWED_PREFIXES:
                return normalized
        else:
            print(f"⚠️ 警告: 别名映射的目标标签格式不正确: {tag} -> {normalized}")
            return None

    # 无法映射的标签返回 None(将被删除)
    return None


def normalize_tags(tags: List[str], alias_map: Dict[str, str]) -> tuple[List[str], Dict[str, str]]:
    """
    标准化标签列表

    Returns:
        (标准化后的标签列表, 映射记录字典)
    """
    normalized = []
    mapping = {}

    for tag in tags:
        new_tag = normalize_tag(tag, alias_map)
        if new_tag:
            normalized.append(new_tag)
            if new_tag != tag:
                mapping[tag] = new_tag
        else:
            # 记录被删除的标签
            mapping[tag] = "[删除]"

    # 去重并保持顺序
    seen = set()
    unique_tags = []
    for tag in normalized:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    # 限制标签数量 ≤ 5
    if len(unique_tags) > 5:
        unique_tags = unique_tags[:5]

    return unique_tags, mapping


def process_file(
    filepath: Path,
    alias_map: Dict[str, str],
    dry_run: bool = True
) -> TagChange | None:
    """
    处理单个文件的标签标准化

    Args:
        filepath: 词条文件路径
        alias_map: 别名映射表
        dry_run: 是否为预览模式(不实际修改文件)

    Returns:
        TagChange 对象,如果无需修改则返回 None
    """
    try:
        post = frontmatter.load(filepath)
    except Exception as e:
        print(f"❌ 无法解析 {filepath}: {e}")
        return None

    meta = post.metadata or {}
    old_tags = meta.get("tags")

    # 检查是否有 tags 字段
    if not isinstance(old_tags, list) or not old_tags:
        return None

    # 标准化标签
    new_tags, mapping = normalize_tags(old_tags, alias_map)

    # 检查是否有变更
    if old_tags == new_tags:
        return None

    # 计算变更
    old_set = set(old_tags)
    new_set = set(new_tags)
    removed = old_set - new_set
    added = new_set - old_set

    # 如果不是 dry run,则写入文件
    if not dry_run:
        meta["tags"] = new_tags
        post.metadata = meta

        # 写回文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

    return TagChange(
        file=filepath,
        old_tags=old_tags,
        new_tags=new_tags,
        removed=removed,
        added=added,
        mapped=mapping,
    )


def print_change_summary(change: TagChange, verbose: bool = False):
    """打印单个文件的变更摘要"""
    print(f"\n📝 {change.file.name}")

    if verbose:
        print(f"   旧标签: {', '.join(change.old_tags)}")
        print(f"   新标签: {', '.join(change.new_tags)}")

    if change.mapped:
        print("   映射:")
        for old, new in change.mapped.items():
            if new == "[删除]":
                print(f"     ❌ {old} → [删除]")
            else:
                print(f"     ✓ {old} → {new}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="标签标准化工具 - 基于 MPS Wiki Tagging Standard v2.0"
    )
    parser.add_argument(
        "--execute", "-e",
        action="store_true",
        help="执行实际修改(默认为预览模式)"
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="处理单个文件"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息(包括所有标签)"
    )

    args = parser.parse_args()

    # 加载别名映射表
    alias_file = Path("data/tags_alias.yaml")
    alias_map = load_alias_map(alias_file)

    if not alias_map:
        print("❌ 错误: 无法加载别名映射表,退出")
        return 1

    print("=" * 80)
    print("MPS Wiki 标签标准化工具 v2.0")
    print("=" * 80)
    print()
    print(f"📋 别名映射表: {alias_file} ({len(alias_map)} 条规则)")
    print()

    # 确定要处理的文件
    if args.file:
        if not args.file.exists():
            print(f"❌ 错误: 文件不存在 {args.file}")
            return 1
        files = [args.file]
    else:
        entries_dir = Path("docs/entries")
        if not entries_dir.exists():
            print(f"❌ 错误: 目录不存在 {entries_dir}")
            return 1
        files = sorted(entries_dir.glob("*.md"))

    # 处理文件
    if args.execute:
        print("【执行模式】开始修改文件...")
    else:
        print("【预览模式】检查需要修改的文件...")
        print("(使用 --execute 或 -e 参数执行实际修改)")
    print()

    changes: List[TagChange] = []

    for filepath in files:
        change = process_file(filepath, alias_map, dry_run=not args.execute)
        if change:
            changes.append(change)
            if args.execute:
                print(f"✅ {filepath.name}")
            else:
                print_change_summary(change, verbose=args.verbose)

    # 输出总结
    print()
    print("=" * 80)

    if not changes:
        print("✅ 所有文件的标签已符合规范,无需修改")
    else:
        if args.execute:
            print(f"✅ 成功修改 {len(changes)} 个文件")
            print()
            print("💡 提示: 运行以下命令验证标签规范:")
            print("   python3 tools/check_tags.py docs/entries/")
        else:
            print(f"📊 共发现 {len(changes)} 个文件需要修改")
            print()
            print("💡 执行修改命令:")
            print("   python3 tools/tag_normalization.py --execute")

    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
