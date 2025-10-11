#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试词典的分词效果

用法:
    python3 tools/test_dict_segmentation.py \\
        --dict data/user_dict_reviewed.txt \\
        --test-text "解离性身份障碍是一种多意识体系统"
"""

import argparse
import jieba
from pathlib import Path
import sys


# 测试用例
TEST_CASES = [
    "解离性身份障碍是一种多意识体系统",
    "多意识体系统中的成员可以通过系统内沟通进行协作",
    "前台人格负责日常生活，后台人格提供支持",
    "触发因素可能导致人格切换",
    "心理治疗和情绪调节技巧有助于管理症状",
    "创伤后应激障碍（PTSD）常与DID共病",
    "接地技巧可以帮助稳定意识体的状态",
    "临床诊断需要排除其他人格障碍",
    "系统成员之间的身份认同差异很大",
    "整合疗法是治疗解离性障碍的常用方法",
]


def load_dict(dict_path):
    """加载自定义词典"""
    if not Path(dict_path).exists():
        print(f"警告: 词典文件不存在: {dict_path}", file=sys.stderr)
        return 0

    try:
        jieba.load_userdict(str(dict_path))
        print(f"已加载词典: {dict_path}")

        # 统计词典大小
        with open(dict_path, 'r', encoding='utf-8') as f:
            word_count = sum(1 for line in f if line.strip() and not line.startswith('#'))
        print(f"词典包含 {word_count} 个词条\n")
        return word_count

    except Exception as e:
        print(f"错误: 加载词典失败: {e}", file=sys.stderr)
        return 0


def test_segmentation(text, show_detail=False):
    """测试分词效果"""
    words = jieba.lcut(text)

    if show_detail:
        print(f"原文: {text}")
        print(f"分词: {' / '.join(words)}")
        print()

    return words


def compare_dicts(text, dict1_path=None, dict2_path=None):
    """对比两个词典的分词效果"""
    print("="*60)
    print(f"测试文本: {text}")
    print("="*60)

    # 默认分词
    print("\n【默认分词（无自定义词典）】")
    jieba.initialize()  # 重新初始化
    words_default = jieba.lcut(text)
    print(' / '.join(words_default))

    # 词典1
    if dict1_path:
        print(f"\n【使用词典: {dict1_path}】")
        jieba.initialize()
        jieba.load_userdict(str(dict1_path))
        words_dict1 = jieba.lcut(text)
        print(' / '.join(words_dict1))

    # 词典2
    if dict2_path:
        print(f"\n【使用词典: {dict2_path}】")
        jieba.initialize()
        jieba.load_userdict(str(dict2_path))
        words_dict2 = jieba.lcut(text)
        print(' / '.join(words_dict2))

    print()


def run_test_suite(dict_path=None):
    """运行测试套件"""
    print("\n" + "="*60)
    print("分词效果测试套件")
    print("="*60)

    if dict_path:
        jieba.initialize()
        load_dict(dict_path)

    print("运行测试用例...\n")

    for i, text in enumerate(TEST_CASES, 1):
        print(f"测试 {i:2d}: {text}")
        words = jieba.lcut(text)
        print(f"       {' / '.join(words)}")
        print()


def analyze_coverage(dict_path, text):
    """分析词典覆盖率"""
    print("\n" + "="*60)
    print("词典覆盖率分析")
    print("="*60)

    # 加载词典中的词
    dict_words = set()
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if parts:
                dict_words.add(parts[0])

    # 分词
    jieba.initialize()
    jieba.load_userdict(str(dict_path))
    words = jieba.lcut(text)

    # 统计覆盖情况
    matched = []
    unmatched = []

    for word in words:
        if word in dict_words:
            matched.append(word)
        else:
            unmatched.append(word)

    print(f"\n测试文本: {text}")
    print(f"\n分词结果: {' / '.join(words)}")
    print(f"\n总词数: {len(words)}")
    print(f"匹配词典: {len(matched)} 词 ({len(matched)/len(words)*100:.1f}%)")
    print(f"未匹配: {len(unmatched)} 词 ({len(unmatched)/len(words)*100:.1f}%)")

    if matched:
        print(f"\n匹配的词: {', '.join(matched)}")

    if unmatched:
        print(f"\n未匹配的词: {', '.join(unmatched)}")


def main():
    parser = argparse.ArgumentParser(
        description='测试词典的分词效果'
    )
    parser.add_argument(
        '--dict',
        help='自定义词典文件路径'
    )
    parser.add_argument(
        '--compare-dict',
        help='用于对比的第二个词典文件路径'
    )
    parser.add_argument(
        '--test-text',
        help='测试文本'
    )
    parser.add_argument(
        '--test-suite',
        action='store_true',
        help='运行完整测试套件'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='分析词典覆盖率'
    )

    args = parser.parse_args()

    # 运行测试套件
    if args.test_suite:
        run_test_suite(args.dict)
        return

    # 对比两个词典
    if args.compare_dict:
        if not args.test_text:
            print("错误: 使用 --compare-dict 时必须指定 --test-text", file=sys.stderr)
            sys.exit(1)
        compare_dicts(args.test_text, args.dict, args.compare_dict)
        return

    # 覆盖率分析
    if args.coverage:
        if not args.dict:
            print("错误: 使用 --coverage 时必须指定 --dict", file=sys.stderr)
            sys.exit(1)
        if not args.test_text:
            print("错误: 使用 --coverage 时必须指定 --test-text", file=sys.stderr)
            sys.exit(1)
        analyze_coverage(args.dict, args.test_text)
        return

    # 单个文本测试
    if args.test_text:
        if args.dict:
            jieba.initialize()
            load_dict(args.dict)

        print("\n" + "="*60)
        print("分词测试")
        print("="*60)
        test_segmentation(args.test_text, show_detail=True)
    else:
        # 默认运行测试套件
        run_test_suite(args.dict)


if __name__ == '__main__':
    main()
