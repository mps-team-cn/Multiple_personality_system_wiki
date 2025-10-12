#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将候选词文件分批处理，便于 AI 审核

用法:
    python3 tools/split_candidates.py \\
        --input data/candidates.txt \\
        --batch-size 100 \\
        --output data/batches/
"""

import argparse
from pathlib import Path
import sys


def load_candidates(filepath):
    """加载候选词文件"""
    try:
        candidates = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) >= 2:
                    word = parts[0]
                    freq = int(parts[1])
                    candidates.append((word, freq))

        return candidates
    except Exception as e:
        print(f"错误: 无法加载候选词文件 {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def split_into_batches(candidates, batch_size=100, max_chars=50000):
    """
    将候选词分批

    参数:
        candidates: 候选词列表 [(word, freq), ...]
        batch_size: 每批最大词数
        max_chars: 每批最大字符数（估算，含格式）

    返回:
        批次列表
    """
    batches = []
    current_batch = []
    current_chars = 0

    for word, freq in candidates:
        # 估算该词条的字符数（词 + 空格 + 频率 + 换行）
        entry_chars = len(word) + len(str(freq)) + 10

        # 检查是否超出限制
        if (len(current_batch) >= batch_size or
            current_chars + entry_chars > max_chars):

            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_chars = 0

        current_batch.append((word, freq))
        current_chars += entry_chars

    # 添加最后一批
    if current_batch:
        batches.append(current_batch)

    return batches


def save_batches(batches, output_dir):
    """保存批次文件"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n保存 {len(batches)} 个批次到: {output_dir}")

    for i, batch in enumerate(batches, 1):
        batch_file = output_path / f"batch_{i:03d}.txt"

        with open(batch_file, 'w', encoding='utf-8') as f:
            # 写入批次头部信息
            f.write(f"# 批次 {i}/{len(batches)}\n")
            f.write(f"# 包含 {len(batch)} 个候选词\n")
            f.write("#" + "="*58 + "\n\n")

            # 写入候选词
            for word, freq in batch:
                f.write(f"{word} {freq}\n")

        # 计算文件大小
        file_size = batch_file.stat().st_size
        print(f"  批次 {i:3d}: {len(batch):4d} 词, {file_size:7,} 字节 -> {batch_file.name}")


def print_summary(candidates, batches):
    """打印汇总信息"""
    total_words = len(candidates)
    total_batches = len(batches)
    avg_words_per_batch = total_words / total_batches if total_batches > 0 else 0

    print("\n" + "="*60)
    print("分批汇总")
    print("="*60)
    print(f"总候选词数: {total_words:,}")
    print(f"批次数量: {total_batches}")
    print(f"平均每批: {avg_words_per_batch:.1f} 词")

    if batches:
        batch_sizes = [len(b) for b in batches]
        print(f"最小批次: {min(batch_sizes)} 词")
        print(f"最大批次: {max(batch_sizes)} 词")

    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='将候选词文件分批处理，便于 AI 审核'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='候选词文件路径'
    )
    parser.add_argument(
        '--output',
        default='data/batches/',
        help='输出目录路径'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='每批最大词数 (默认: 100)'
    )
    parser.add_argument(
        '--max-chars',
        type=int,
        default=50000,
        help='每批最大字符数 (默认: 50000)'
    )

    args = parser.parse_args()

    # 加载候选词
    print(f"加载候选词: {args.input}")
    candidates = load_candidates(args.input)
    print(f"加载了 {len(candidates)} 个候选词")

    # 分批
    print(f"\n开始分批（每批 ≤ {args.batch_size} 词，≤ {args.max_chars:,} 字符）...")
    batches = split_into_batches(
        candidates,
        batch_size=args.batch_size,
        max_chars=args.max_chars
    )

    # 保存批次
    save_batches(batches, args.output)

    # 显示汇总
    print_summary(candidates, batches)

    print("\n完成！")
    print(f"\n下一步：使用 AI 逐批审核 {args.output} 目录下的文件")


if __name__ == '__main__':
    main()
