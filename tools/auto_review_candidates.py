#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动审核候选词并生成优化的词典

用法:
    python3 tools/auto_review_candidates.py \\
        --input data/candidates.txt \\
        --output data/user_dict_reviewed.txt \\
        --existing-dict data/user_dict.txt
"""

import argparse
import re
from pathlib import Path
from collections import Counter
import sys


# 专业术语模式（高优先级保留）
PROFESSIONAL_PATTERNS = [
    # 核心诊断术语
    r'.*障碍$',
    r'.*症状$',
    r'.*疾病$',
    r'.*综合征$',
    r'解离.*',
    r'创伤.*',
    r'多.*意识.*',
    r'.*人格.*',
    r'.*身份.*',

    # 治疗相关
    r'.*疗法$',
    r'.*治疗$',
    r'.*技巧$',
    r'.*策略$',

    # 系统相关
    r'系统.*',
    r'.*成员$',
    r'前台.*',
    r'后台.*',
    r'.*意识体.*',

    # 临床术语
    r'临床.*',
    r'.*诊断$',
    r'.*评估$',
]

# 需要提升权重的复合词
IMPORTANT_COMPOUNDS = [
    '解离性身份障碍',
    '多意识体系统',
    '意识体系统',
    '系统成员',
    '前台人格',
    '后台人格',
    '人格切换',
    '触发因素',
    '应激反应',
    '情绪调节',
    '接地技巧',
    '共病障碍',
    '创伤后应激',
    '创伤后应激障碍',
    '身份认同',
    '系统内沟通',
    '整合疗法',
    '心理治疗',
    '药物治疗',
    '临床诊断',
    '风险评估',
    '日常生活',
    '解离性障碍',
    '人格障碍',
]

# 常见缩写和别名
ABBREVIATIONS = {
    'DID': 8000,
    'OSDD': 5000,
    'PTSD': 4000,
    'MPD': 3000,
}

# 应该删除的通用词（过于宽泛）
COMMON_WORDS_TO_REMOVE = {
    '可能', '使用', '其他', '更新', '需要', '参考',
    '相关', '不同', '出现', '存在', '通过', '说明',
    '内容', '常见', '时间', '专业', '显著', '帮助',
    '信息', '过度', '描述', '差异', '问题', '发展',
}

# 片段词（应该被删除，因为是其他词的一部分）
FRAGMENT_PATTERNS = [
    r'^离性$',  # 解离性
    r'^识体$',  # 意识体
    r'^格障$',  # 人格障碍
    r'^份障$',  # 身份障碍
    r'^性身$',  # 解离性身份
    r'^多意$',  # 多意识
]


def load_existing_dict(filepath):
    """加载现有词典"""
    existing = {}
    if not Path(filepath).exists():
        return existing

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()
            if len(parts) >= 2:
                word = parts[0]
                try:
                    freq = int(parts[1])
                    existing[word] = freq
                except:
                    pass

    return existing


def is_professional_term(word):
    """判断是否为专业术语"""
    for pattern in PROFESSIONAL_PATTERNS:
        if re.match(pattern, word):
            return True
    return False


def is_fragment(word):
    """判断是否为片段词"""
    for pattern in FRAGMENT_PATTERNS:
        if re.match(pattern, word):
            return True
    return False


def should_remove(word, freq):
    """判断是否应该删除"""
    # 删除片段词
    if is_fragment(word):
        return True

    # 删除通用词（除非频率很高）
    if word in COMMON_WORDS_TO_REMOVE and freq < 300:
        return True

    # 删除单字词
    if len(word) == 1:
        return True

    # 删除过长的词（可能是提取错误）
    if len(word) > 10:
        return True

    # 删除低频短词
    if len(word) == 2 and freq < 50:
        return True

    return False


def calculate_optimized_freq(word, original_freq, is_existing=False):
    """计算优化后的词频"""
    # 如果是现有词典中的词，保持原频率
    if is_existing:
        return original_freq

    # 重要复合词 - 高权重
    if word in IMPORTANT_COMPOUNDS:
        return max(5000, original_freq * 2)

    # 专业术语 - 提升权重
    if is_professional_term(word):
        if len(word) >= 4:
            return max(2000, int(original_freq * 1.5))
        else:
            return max(1000, int(original_freq * 1.2))

    # 较长的复合词 - 适当提升
    if len(word) >= 4:
        return max(1500, original_freq)

    # 中等长度词 - 保持或略微提升
    if len(word) == 3:
        return max(800, original_freq)

    # 短词 - 降权
    if len(word) == 2:
        return min(500, original_freq)

    return original_freq


def review_candidates(candidates, existing_dict):
    """审核并优化候选词"""
    reviewed = {}

    print(f"\n开始审核 {len(candidates)} 个候选词...")

    removed_count = 0
    kept_count = 0
    optimized_count = 0

    for word, freq in candidates.items():
        # 检查是否应该删除
        if should_remove(word, freq):
            removed_count += 1
            continue

        # 检查是否在现有词典中
        is_existing = word in existing_dict

        # 计算优化后的频率
        optimized_freq = calculate_optimized_freq(word, freq, is_existing)

        reviewed[word] = optimized_freq
        kept_count += 1

        if optimized_freq != freq:
            optimized_count += 1

    # 添加缩写
    for abbr, freq in ABBREVIATIONS.items():
        if abbr not in reviewed:
            reviewed[abbr] = freq
            kept_count += 1

    print(f"保留: {kept_count} 词")
    print(f"删除: {removed_count} 词")
    print(f"优化频率: {optimized_count} 词")

    return reviewed


def save_reviewed_dict(reviewed, output_path, add_header=True):
    """保存审核后的词典"""
    # 按频率和字典序排序
    sorted_words = sorted(
        reviewed.items(),
        key=lambda x: (-x[1], x[0])
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        if add_header:
            f.write("# 多重人格系统 Wiki - 搜索词典\n")
            f.write("# 自动生成并优化\n")
            f.write("#\n")
            f.write("# 格式: 词条 词频 [词性]\n")
            f.write("#" + "="*58 + "\n\n")

        for word, freq in sorted_words:
            f.write(f"{word} {freq}\n")

    print(f"\n审核后的词典已保存到: {output_path}")
    print(f"总计 {len(sorted_words)} 个词条")


def print_statistics(reviewed):
    """打印统计信息"""
    print("\n" + "="*60)
    print("词典统计")
    print("="*60)

    # 按长度统计
    length_dist = Counter(len(w) for w in reviewed.keys())
    print("\n长度分布:")
    for length in sorted(length_dist.keys()):
        count = length_dist[length]
        print(f"  {length} 字: {count:4d} 词")

    # 高频词
    print("\n高频词 (Top 30):")
    sorted_words = sorted(
        reviewed.items(),
        key=lambda x: (-x[1], x[0])
    )[:30]

    for i, (word, freq) in enumerate(sorted_words, 1):
        print(f"  {i:2d}. {word:20s} {freq:6,}")

    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='自动审核候选词并生成优化的词典'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='候选词文件路径'
    )
    parser.add_argument(
        '--output',
        default='data/user_dict_reviewed.txt',
        help='输出词典文件路径'
    )
    parser.add_argument(
        '--existing-dict',
        help='现有词典文件路径（用于保持一致性）'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='显示详细统计信息'
    )

    args = parser.parse_args()

    # 加载候选词
    print(f"加载候选词: {args.input}")
    candidates = {}

    with open(args.input, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()
            if len(parts) >= 2:
                word = parts[0]
                try:
                    freq = int(parts[1])
                    candidates[word] = freq
                except:
                    continue

    print(f"加载了 {len(candidates)} 个候选词")

    # 加载现有词典
    existing_dict = {}
    if args.existing_dict:
        print(f"加载现有词典: {args.existing_dict}")
        existing_dict = load_existing_dict(args.existing_dict)
        print(f"加载了 {len(existing_dict)} 个现有词条")

    # 审核候选词
    reviewed = review_candidates(candidates, existing_dict)

    # 保存审核后的词典
    output_path = Path(args.output)
    save_reviewed_dict(reviewed, output_path)

    # 显示统计信息
    if args.stats:
        print_statistics(reviewed)

    print("\n完成！")
    print(f"\n下一步：")
    print(f"  1. 检查输出文件: {output_path}")
    print(f"  2. 测试分词效果")
    print(f"  3. 如果满意，替换现有词典: cp {output_path} data/user_dict.txt")


if __name__ == '__main__':
    main()
