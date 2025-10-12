#!/usr/bin/env python3
"""
从搜索索引中提取文本，供 AI 分析并生成优化的词典

使用方法:
    python3 tools/extract_terms_for_ai.py

输出:
    data/search_index_sample.txt - AI 分析用的文本样本
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

def extract_chinese_terms(text, min_len=2, max_len=6):
    """提取中文词组"""
    # 匹配连续的中文字符
    pattern = r'[\u4e00-\u9fff]+'
    terms = re.findall(pattern, text)
    # 过滤长度
    return [t for t in terms if min_len <= len(t) <= max_len]

def main():
    print("=== 搜索索引文本提取工具 ===\n")

    # 读取搜索索引
    index_path = Path('site/search/search_index.json')
    if not index_path.exists():
        print("❌ 错误: 找不到搜索索引文件")
        print("   请先运行: mkdocs build")
        sys.exit(1)

    print(f"📂 读取索引: {index_path}")
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    docs = index.get('docs', [])
    print(f"📊 文档总数: {len(docs)}")

    # 提取所有文本
    all_texts = []
    all_terms = []

    for i, doc in enumerate(docs):
        title = doc.get('title', '').strip()
        text = doc.get('text', '').strip()
        location = doc.get('location', '')

        # 提取中文词组
        terms = extract_chinese_terms(title + ' ' + text)
        all_terms.extend(terms)

        # 保存文档信息
        if title and text:
            all_texts.append({
                'id': i,
                'title': title,
                'text': text[:300],  # 只取前300字
                'location': location
            })

    print(f"📝 有效文档: {len(all_texts)}")
    print(f"🔤 提取词组: {len(all_terms)}")

    # 统计高频词
    term_freq = Counter(all_terms)
    print(f"📊 不同词组: {len(term_freq)}")

    # 生成分析报告
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)

    # 1. 完整文本样本（用于 AI 理解内容）
    sample_file = output_dir / 'search_index_sample.txt'
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("# 搜索索引文本样本（供 AI 分析）\n\n")
        f.write(f"文档总数: {len(docs)}\n")
        f.write(f"样本数量: {min(100, len(all_texts))}\n\n")
        f.write("="*60 + "\n\n")

        # 写入前100个文档
        for doc in all_texts[:100]:
            f.write(f"## {doc['title']}\n\n")
            f.write(f"位置: {doc['location']}\n\n")
            f.write(f"{doc['text']}\n\n")
            f.write("-"*60 + "\n\n")

    print(f"✅ 已保存样本: {sample_file}")

    # 2. 高频词统计（用于 AI 识别需要加入词典的词）
    freq_file = output_dir / 'term_frequency.txt'
    with open(freq_file, 'w', encoding='utf-8') as f:
        f.write("# 高频中文词组统计\n\n")
        f.write(f"总词组数: {len(all_terms)}\n")
        f.write(f"不同词组: {len(term_freq)}\n\n")
        f.write("词组       频次\n")
        f.write("="*30 + "\n")

        # 写入 Top 500
        for term, count in term_freq.most_common(500):
            if count >= 3:  # 只保留出现3次以上的
                f.write(f"{term:12s} {count:4d}\n")

    print(f"✅ 已保存词频: {freq_file}")

    # 3. 生成 AI 提示词
    prompt_file = output_dir / 'ai_prompt.md'
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write("# AI 词典生成提示词\n\n")
        f.write("## 任务说明\n\n")
        f.write("请分析以下文档内容和高频词组，生成一个优化的 Jieba 自定义词典。\n\n")
        f.write("## 要求\n\n")
        f.write("1. 识别专业术语（医学、心理学、系统相关）\n")
        f.write("2. 识别复合词需要拆分的基础词\n")
        f.write("3. 识别人名、系统名等专有名词\n")
        f.write("4. 输出格式：词语 999 词性\n")
        f.write("5. 按类别分组（临床术语、核心概念、理论框架等）\n\n")
        f.write("## 当前词典参考\n\n")
        f.write("```\n")

        # 读取当前词典
        dict_file = Path('data/user_dict.txt')
        if dict_file.exists():
            with open(dict_file, 'r', encoding='utf-8') as df:
                f.write(df.read()[:2000])  # 只显示前2000字

        f.write("\n```\n\n")
        f.write("## 高频词组（Top 100）\n\n")
        f.write("```\n")
        for term, count in term_freq.most_common(100):
            f.write(f"{term:12s} {count:4d}\n")
        f.write("```\n\n")
        f.write("## 文档样本\n\n")
        f.write(f"详见: {sample_file.name}\n")

    print(f"✅ 已生成提示词: {prompt_file}")

    # 4. 生成分析统计
    stats = {
        'total_docs': len(docs),
        'valid_docs': len(all_texts),
        'total_terms': len(all_terms),
        'unique_terms': len(term_freq),
        'high_freq_terms': len([t for t, c in term_freq.items() if c >= 5]),
        'sample_file': str(sample_file),
        'freq_file': str(freq_file),
        'prompt_file': str(prompt_file)
    }

    stats_file = output_dir / 'extraction_stats.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"✅ 已保存统计: {stats_file}")

    print("\n" + "="*60)
    print("✅ 提取完成！")
    print("\n📋 下一步：")
    print(f"1. 查看样本: cat {sample_file}")
    print(f"2. 查看词频: cat {freq_file}")
    print(f"3. 将 {prompt_file} 的内容和样本文件发送给 AI")
    print("4. AI 会生成优化的词典")
    print("5. 将生成的词典合并到 data/user_dict.txt")

if __name__ == '__main__':
    main()
