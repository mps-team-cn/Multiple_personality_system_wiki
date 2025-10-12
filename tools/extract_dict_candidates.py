#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从搜索索引提取词典候选词

用法:
    python3 tools/extract_dict_candidates.py \\
        --input site/search/search_index.json \\
        --output data/candidates.txt \\
        --min-freq 3 \\
        --min-length 2 \\
        --max-length 8
"""

import json
import re
import argparse
from collections import Counter
from pathlib import Path
import sys


def load_search_index(filepath):
    """加载搜索索引文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"错误: 无法加载索引文件 {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def extract_text_from_index(index_data):
    """从索引中提取所有文本内容"""
    texts = []

    if isinstance(index_data, dict):
        if 'docs' in index_data:
            for doc in index_data['docs']:
                if 'title' in doc:
                    texts.append(doc['title'])
                if 'text' in doc:
                    texts.append(doc['text'])

    return texts


def segment_chinese_text(text):
    """提取连续的中文字符序列"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    segments = chinese_pattern.findall(text)
    return segments


def extract_ngrams(text, min_len=2, max_len=8):
    """提取 n-gram 词组"""
    ngrams = []
    segments = segment_chinese_text(text)

    for segment in segments:
        if len(segment) < min_len:
            continue

        # 提取所有可能的 n-gram
        for n in range(min_len, min(len(segment) + 1, max_len + 1)):
            for i in range(len(segment) - n + 1):
                ngram = segment[i:i+n]
                ngrams.append(ngram)

    return ngrams


def is_valid_candidate(word):
    """判断是否为有效候选词"""
    # 必须包含中文
    if not re.search(r'[\u4e00-\u9fff]', word):
        return False

    # 排除纯标点
    if re.fullmatch(r'[，。！？；：、""''（）【】《》\s]+', word):
        return False

    # 排除纯数字
    if re.fullmatch(r'\d+', word):
        return False

    # 排除单字词
    if len(word) == 1:
        return False

    return True


def extract_candidates(index_data, min_freq=3, min_len=2, max_len=8):
    """提取候选词"""
    print("开始提取候选词...")

    # 提取文本
    texts = extract_text_from_index(index_data)
    print(f"提取到 {len(texts)} 个文本片段")

    # 提取所有 n-gram
    print("提取 n-gram 词组...")
    all_ngrams = []

    for text in texts:
        if not text:
            continue
        ngrams = extract_ngrams(text, min_len, max_len)
        all_ngrams.extend(ngrams)

    print(f"提取到 {len(all_ngrams)} 个 n-gram")

    # 统计频率
    ngram_counter = Counter(all_ngrams)

    # 筛选候选词
    print(f"筛选候选词（最小频率: {min_freq}）...")
    candidates = {}

    for ngram, freq in ngram_counter.items():
        if freq < min_freq:
            continue

        if not is_valid_candidate(ngram):
            continue

        if len(ngram) < min_len or len(ngram) > max_len:
            continue

        candidates[ngram] = freq

    print(f"筛选出 {len(candidates)} 个候选词")
    return candidates


def save_candidates(candidates, output_path):
    """保存候选词到文件"""
    # 按频率排序
    sorted_candidates = sorted(
        candidates.items(),
        key=lambda x: (-x[1], x[0])  # 频率降序，词典序升序
    )

    # 保存到文件
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for word, freq in sorted_candidates:
            f.write(f"{word} {freq}\n")

    print(f"\n候选词已保存到: {output_path}")
    print(f"总计 {len(sorted_candidates)} 个候选词")


def print_preview(candidates, top_n=30):
    """打印预览"""
    print("\n" + "="*60)
    print(f"候选词预览 (Top {top_n})")
    print("="*60)

    sorted_candidates = sorted(
        candidates.items(),
        key=lambda x: (-x[1], x[0])
    )[:top_n]

    for i, (word, freq) in enumerate(sorted_candidates, 1):
        print(f"{i:3d}. {word:15s} {freq:6,}")

    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='从搜索索引提取词典候选词'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='搜索索引文件路径 (search_index.json)'
    )
    parser.add_argument(
        '--output',
        default='data/candidates.txt',
        help='输出候选词文件路径'
    )
    parser.add_argument(
        '--min-freq',
        type=int,
        default=3,
        help='最小词频 (默认: 3)'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=2,
        help='最小词长 (默认: 2)'
    )
    parser.add_argument(
        '--max-length',
        type=int,
        default=8,
        help='最大词长 (默认: 8)'
    )
    parser.add_argument(
        '--preview',
        type=int,
        default=30,
        help='预览显示的词数 (默认: 30)'
    )

    args = parser.parse_args()

    # 加载索引
    index_data = load_search_index(args.input)

    # 提取候选词
    candidates = extract_candidates(
        index_data,
        min_freq=args.min_freq,
        min_len=args.min_length,
        max_len=args.max_length
    )

    # 保存候选词
    output_path = Path(args.output)
    save_candidates(candidates, output_path)

    # 显示预览
    if args.preview > 0:
        print_preview(candidates, args.preview)

    print("\n完成！")


if __name__ == '__main__':
    main()
