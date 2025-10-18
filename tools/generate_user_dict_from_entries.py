#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从词条 Frontmatter 提取标题和 boost 权重,生成 jieba user_dict.txt

用法:
    python3 tools/generate_user_dict_from_entries.py \\
        --entries-dir docs/entries \\
        --output data/user_dict.txt \\
        --base-freq 1000
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import yaml
import sys


def extract_frontmatter(file_path: Path) -> Dict:
    """从 Markdown 文件中提取 Frontmatter"""
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception as e:
        print(f"警告: 无法解析 {file_path} 的 Frontmatter: {e}", file=sys.stderr)
        return {}


def extract_title_from_content(content: str) -> str | None:
    """从 Markdown 内容中提取一级标题"""
    # 跳过 Frontmatter
    content_without_fm = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # 查找第一个一级标题
    match = re.search(r'^#\s+(.+)$', content_without_fm, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # 提取中文部分 (格式: 中文名(English/缩写))
        cn_match = re.match(r'^([^(（]+)', title)
        if cn_match:
            return cn_match.group(1).strip()
    return None


def calculate_frequency(boost: float, base_freq: int = 1000) -> int:
    """根据 boost 权重计算词频

    Args:
        boost: 权重值 (0.1-3.0)
        base_freq: 基础频率

    Returns:
        计算后的词频
    """
    # boost 转换为词频的映射:
    # boost=2.0 → 9999 (最高优先级)
    # boost=1.8 → 8000
    # boost=1.5 → 7000
    # boost=1.2 → 5000
    # boost=1.0 → 3000
    # boost<1.0 → 基于 base_freq 计算

    if boost >= 2.0:
        return 9999
    elif boost >= 1.8:
        return 8000
    elif boost >= 1.5:
        return 7000
    elif boost >= 1.3:
        return 6000
    elif boost >= 1.2:
        return 5000
    elif boost >= 1.0:
        return 3000
    else:
        return int(base_freq * boost)


def extract_entries_with_boost(entries_dir: Path, base_freq: int = 1000) -> List[Tuple[str, int]]:
    """从词条目录提取所有词条标题和权重

    Returns:
        List of (词条, 词频) tuples
    """
    entries = []

    for md_file in entries_dir.glob('*.md'):
        # 跳过索引和导览文件
        if md_file.stem.endswith('-index') or md_file.stem.endswith('-Guide'):
            continue

        frontmatter = extract_frontmatter(md_file)

        # 获取标题
        title = frontmatter.get('title')
        if not title:
            # 从内容中提取标题
            content = md_file.read_text(encoding='utf-8')
            title = extract_title_from_content(content)

        if not title:
            print(f"警告: {md_file.name} 没有找到标题", file=sys.stderr)
            continue

        # 获取 boost 权重 (可能在 search.boost 或直接在 frontmatter.boost)
        boost = None
        search_config = frontmatter.get('search', {})
        if isinstance(search_config, dict):
            boost = search_config.get('boost')
        if boost is None:
            boost = frontmatter.get('boost')

        if boost is not None:
            try:
                boost_value = float(boost)
                freq = calculate_frequency(boost_value, base_freq)
            except (ValueError, TypeError):
                print(f"警告: {md_file.name} 的 boost 值无效: {boost}", file=sys.stderr)
                freq = base_freq
        else:
            # 没有 boost 的词条使用基础频率
            freq = base_freq

        entries.append((title, freq))

        # 同时提取 synonyms 作为额外词条
        synonyms = frontmatter.get('synonyms', [])
        if isinstance(synonyms, str):
            synonyms = [s.strip() for s in synonyms.split(',') if s.strip()]

        for syn in synonyms:
            if syn and syn != title:
                # 同义词使用相同的频率
                entries.append((syn, freq))

    return entries


def extract_common_terms(entries: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """从词条中提取常见术语和复合词

    提取规则:
    - 包含"障碍"、"症"、"理论"等后缀的词
    - 常见的专业术语
    """
    terms = set()

    for title, freq in entries:
        # 提取包含特定后缀的子词
        # 例如: "解离性身份障碍" → "身份障碍"
        if '障碍' in title and len(title) > 2:
            # 提取 XX障碍
            match = re.search(r'(.{1,4}障碍)', title)
            if match:
                term = match.group(1)
                if len(term) >= 2:
                    terms.add((term, max(2000, freq // 2)))

        # 其他类似模式可以在这里添加

    return list(terms)


def generate_user_dict(entries: List[Tuple[str, int]], output_path: Path, include_terms: bool = True):
    """生成 jieba user_dict.txt

    Args:
        entries: List of (词条, 词频) tuples
        output_path: 输出文件路径
        include_terms: 是否包含提取的通用术语
    """
    # 去重并按频率排序
    entry_dict = {}
    for word, freq in entries:
        if word in entry_dict:
            # 保留更高的频率
            entry_dict[word] = max(entry_dict[word], freq)
        else:
            entry_dict[word] = freq

    # 如果需要,添加提取的通用术语
    if include_terms:
        terms = extract_common_terms(entries)
        for term, freq in terms:
            if term not in entry_dict:
                entry_dict[term] = freq

    # 按频率降序排序
    sorted_entries = sorted(entry_dict.items(), key=lambda x: (-x[1], x[0]))

    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Generated jieba userdict for MPS + medical domain\n")
        f.write("# 格式: 词语 词频 词性\n")

        for word, freq in sorted_entries:
            # jieba 格式: 词语 词频 词性
            # 词性设为 n (名词)
            f.write(f"{word} {freq} n\n")

    print(f"\n✅ 生成完成: {output_path}")
    print(f"   总词条数: {len(sorted_entries)}")
    print(f"   最高频率: {sorted_entries[0][1]}")
    print(f"   最低频率: {sorted_entries[-1][1]}")


def print_preview(entries: List[Tuple[str, int]], top_n: int = 30):
    """打印预览"""
    print("\n" + "="*70)
    print(f"词条预览 (Top {top_n})")
    print("="*70)

    # 去重
    entry_dict = {}
    for word, freq in entries:
        if word in entry_dict:
            entry_dict[word] = max(entry_dict[word], freq)
        else:
            entry_dict[word] = freq

    sorted_entries = sorted(entry_dict.items(), key=lambda x: (-x[1], x[0]))[:top_n]

    for i, (word, freq) in enumerate(sorted_entries, 1):
        print(f"{i:3d}. {word:20s} {freq:6,}")

    print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='从词条 Frontmatter 提取标题和 boost 权重,生成 jieba user_dict.txt'
    )
    parser.add_argument(
        '--entries-dir',
        default='docs/entries',
        help='词条目录路径 (默认: docs/entries)'
    )
    parser.add_argument(
        '--output',
        default='data/user_dict.txt',
        help='输出词典文件路径 (默认: data/user_dict.txt)'
    )
    parser.add_argument(
        '--base-freq',
        type=int,
        default=1000,
        help='基础词频 (默认: 1000)'
    )
    parser.add_argument(
        '--no-terms',
        action='store_true',
        help='不包含自动提取的通用术语'
    )
    parser.add_argument(
        '--preview',
        type=int,
        default=30,
        help='预览显示的词数 (默认: 30)'
    )

    args = parser.parse_args()

    entries_dir = Path(args.entries_dir)
    if not entries_dir.exists():
        print(f"错误: 词条目录不存在: {entries_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"📖 正在扫描词条目录: {entries_dir}")

    # 提取词条
    entries = extract_entries_with_boost(entries_dir, args.base_freq)

    print(f"✅ 提取了 {len(entries)} 个词条(含同义词)")

    # 显示预览
    if args.preview > 0:
        print_preview(entries, args.preview)

    # 生成词典
    output_path = Path(args.output)
    generate_user_dict(entries, output_path, include_terms=not args.no_terms)

    print("\n✅ 完成!")


if __name__ == '__main__':
    main()
