#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 MkDocs 搜索索引，统计词频和文本特征

用法:
    python3 tools/analyze_search_index.py \\
        --input site/search/search_index.json \\
        --output data/analysis_report.json \\
        --stats
"""

import json
import re
import argparse
from collections import Counter, defaultdict
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

    # 处理不同格式的索引结构
    if isinstance(index_data, dict):
        if 'docs' in index_data:
            # MkDocs search 插件格式
            for doc in index_data['docs']:
                if 'title' in doc:
                    texts.append(doc['title'])
                if 'text' in doc:
                    texts.append(doc['text'])
                if 'location' in doc:
                    texts.append(doc['location'])
        elif 'config' in index_data and 'docs' in index_data:
            # lunr.js 格式
            for doc in index_data['docs']:
                texts.append(doc.get('title', ''))
                texts.append(doc.get('text', ''))

    return texts


def segment_chinese_text(text):
    """简单的中文文本分段（提取中文词组）"""
    # 提取连续的中文字符序列
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


def analyze_index(index_data, min_len=2, max_len=8):
    """分析索引内容"""
    print("开始分析索引...")

    # 提取文本
    texts = extract_text_from_index(index_data)
    print(f"提取到 {len(texts)} 个文本片段")

    # 统计信息
    stats = {
        'total_texts': len(texts),
        'total_chars': sum(len(t) for t in texts),
        'total_chinese_chars': 0,
        'total_documents': 0
    }

    # 统计文档数量
    if isinstance(index_data, dict) and 'docs' in index_data:
        stats['total_documents'] = len(index_data['docs'])

    # 提取所有 n-gram 并统计频率
    print("提取 n-gram 词组...")
    all_ngrams = []

    for text in texts:
        if not text:
            continue
        ngrams = extract_ngrams(text, min_len, max_len)
        all_ngrams.extend(ngrams)
        stats['total_chinese_chars'] += len(segment_chinese_text(text))

    print(f"提取到 {len(all_ngrams)} 个 n-gram")

    # 统计频率
    ngram_counter = Counter(all_ngrams)

    # 按长度分组统计
    length_distribution = defaultdict(int)
    for ngram in all_ngrams:
        length_distribution[len(ngram)] += 1

    stats['length_distribution'] = dict(length_distribution)
    stats['unique_ngrams'] = len(ngram_counter)
    stats['total_ngrams'] = len(all_ngrams)

    return ngram_counter, stats


def filter_candidates(ngram_counter, min_freq=3, min_len=2, max_len=8):
    """筛选候选词"""
    print(f"筛选候选词（最小频率: {min_freq}, 长度范围: {min_len}-{max_len}）...")

    candidates = {}

    for ngram, freq in ngram_counter.items():
        # 频率过滤
        if freq < min_freq:
            continue

        # 长度过滤
        if len(ngram) < min_len or len(ngram) > max_len:
            continue

        # 过滤单字词
        if len(ngram) == 1:
            continue

        # 过滤纯标点和数字
        if not re.search(r'[\u4e00-\u9fff]', ngram):
            continue

        candidates[ngram] = freq

    print(f"筛选出 {len(candidates)} 个候选词")
    return candidates


def generate_report(stats, candidates, output_path):
    """生成分析报告"""
    report = {
        'statistics': stats,
        'top_candidates': sorted(
            candidates.items(),
            key=lambda x: x[1],
            reverse=True
        )[:100],  # 只保存前 100 个高频词
        'total_candidates': len(candidates)
    }

    # 保存报告
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n分析报告已保存到: {output_path}")


def print_stats(stats, candidates):
    """打印统计信息"""
    print("\n" + "="*60)
    print("索引分析报告")
    print("="*60)
    print(f"文档数量: {stats['total_documents']}")
    print(f"文本片段数: {stats['total_texts']}")
    print(f"总字符数: {stats['total_chars']:,}")
    print(f"中文字符数: {stats['total_chinese_chars']:,}")
    print(f"唯一 n-gram 数: {stats['unique_ngrams']:,}")
    print(f"总 n-gram 数: {stats['total_ngrams']:,}")
    print(f"候选词数量: {len(candidates):,}")

    print("\n长度分布:")
    for length in sorted(stats['length_distribution'].keys()):
        count = stats['length_distribution'][length]
        print(f"  {length} 字: {count:,}")

    print("\n高频候选词 (Top 20):")
    top_candidates = sorted(
        candidates.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]

    for i, (word, freq) in enumerate(top_candidates, 1):
        print(f"  {i:2d}. {word:10s} {freq:6,}")

    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='分析 MkDocs 搜索索引，统计词频和文本特征'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='搜索索引文件路径 (search_index.json)'
    )
    parser.add_argument(
        '--output',
        default='data/analysis_report.json',
        help='输出报告文件路径'
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
        '--stats',
        action='store_true',
        help='显示详细统计信息'
    )

    args = parser.parse_args()

    # 加载索引
    index_data = load_search_index(args.input)

    # 分析索引
    ngram_counter, stats = analyze_index(
        index_data,
        min_len=args.min_length,
        max_len=args.max_length
    )

    # 筛选候选词
    candidates = filter_candidates(
        ngram_counter,
        min_freq=args.min_freq,
        min_len=args.min_length,
        max_len=args.max_length
    )

    # 生成报告
    output_path = Path(args.output)
    generate_report(stats, candidates, output_path)

    # 显示统计信息
    if args.stats:
        print_stats(stats, candidates)

    print("\n完成！")


if __name__ == '__main__':
    main()
