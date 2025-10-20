#!/usr/bin/env python3
"""
新标签建议工具
通过关键词匹配,建议哪些词条可能需要添加新的分面标签或概念标签

使用方法:
    python3 tools/suggest_new_tags.py
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


# C类: 需要新增的标签及其识别关键词
NEW_TAG_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    # 症状类标签(sx:)
    "sx:解离性恍惚": {
        "title_keywords": ["恍惚", "Daze", "trance"],
        "content_keywords": ["恍惚状态", "意识模糊", "出神", "神游"],
    },
    "sx:时间丢失": {
        "title_keywords": ["失时", "lost time", "time loss", "时间丢失"],
        "content_keywords": ["失时", "时间丢失", "记不起", "断片", "时间空白"],
    },
    "sx:身份混淆": {
        "title_keywords": ["身份混淆", "identity confusion"],
        "content_keywords": ["身份混淆", "不确定自己是谁", "身份困惑", "自我混乱"],
    },
    "sx:内在语音": {
        "title_keywords": ["内在语音", "internal voice", "inner voice"],
        "content_keywords": ["内在语音", "内在声音", "听到声音", "脑内对话"],
    },

    # 系统运作类标签(ops:)
    "ops:接管": {
        "title_keywords": ["接管", "takeover"],
        "content_keywords": ["接管身体", "被接管", "外控", "控制冲突"],
    },
    "ops:内部会议": {
        "title_keywords": ["内部会议", "internal meeting"],
        "content_keywords": ["内部会议", "系统会议", "内部讨论", "集体决策"],
    },
    "ops:契约": {
        "title_keywords": ["契约", "agreement", "contract"],
        "content_keywords": ["内部契约", "系统规则", "约定", "协议"],
    },

    # 治疗类标签(tx:)
    "tx:创伤阶段化治疗": {
        "title_keywords": ["阶段化", "phase", "三阶段"],
        "content_keywords": ["阶段化治疗", "三阶段", "稳定化阶段", "整合阶段", "Phase-Oriented"],
    },

    # 导览类标签(guide:)
    "guide:就医与转介": {
        "title_keywords": ["就医", "转介", "寻求帮助"],
        "content_keywords": ["就医指南", "如何寻求帮助", "转介", "专业支持", "寻求治疗"],
    },
    "guide:伦理与边界": {
        "title_keywords": ["伦理", "边界", "ethics", "boundary"],
        "content_keywords": ["伦理边界", "专业边界", "治疗边界", "知情同意"],
    },
}


def extract_frontmatter_and_content(filepath: Path) -> tuple[str, List[str], str]:
    """
    提取文件的标题、现有标签和内容
    返回: (title, current_tags, content)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取frontmatter
    fm_match = re.search(r'^---\n(.*?)^---', content, re.MULTILINE | re.DOTALL)
    if not fm_match:
        return "", [], content

    fm_content = fm_match.group(1)

    # 提取title
    title_match = re.search(r'^title:\s*(.+?)\s*$', fm_content, re.MULTILINE)
    title = title_match.group(1) if title_match else ""

    # 提取现有标签
    tags_match = re.search(r'^tags:\s*\n((?:^\s*-\s*.+\n)+)', fm_content, re.MULTILINE)
    current_tags = []
    if tags_match:
        tags_section = tags_match.group(1)
        current_tags = re.findall(r'^\s*-\s*(.+?)\s*$', tags_section, re.MULTILINE)

    # 提取正文内容(去除frontmatter)
    body_content = content[fm_match.end():]

    return title, current_tags, body_content


def suggest_tags_for_file(filepath: Path) -> Dict[str, List[str]]:
    """
    为单个文件建议新标签
    返回: {tag: [匹配原因列表]}
    """
    title, current_tags, content = extract_frontmatter_and_content(filepath)

    suggestions = defaultdict(list)

    for tag, patterns in NEW_TAG_PATTERNS.items():
        # 跳过已有标签
        if tag in current_tags:
            continue

        # 检查标题关键词
        for keyword in patterns.get("title_keywords", []):
            if keyword.lower() in title.lower():
                suggestions[tag].append(f"标题包含: {keyword}")
                break

        # 检查内容关键词
        for keyword in patterns.get("content_keywords", []):
            if keyword in content:
                # 计算出现次数
                count = content.count(keyword)
                if count > 0:
                    suggestions[tag].append(f"内容包含'{keyword}' {count}次")
                    break

    return dict(suggestions)


def main():
    """主函数"""
    entries_dir = Path("docs/entries")

    if not entries_dir.exists():
        print(f"错误: 目录不存在 {entries_dir}")
        return

    print("=" * 80)
    print("新标签建议工具")
    print("=" * 80)
    print()
    print("正在分析词条...")
    print()

    all_suggestions = defaultdict(list)

    for filepath in sorted(entries_dir.glob("*.md")):
        suggestions = suggest_tags_for_file(filepath)
        if suggestions:
            for tag, reasons in suggestions.items():
                all_suggestions[tag].append({
                    "file": filepath.name,
                    "reasons": reasons
                })

    if not all_suggestions:
        print("✅ 未发现需要添加新标签的词条")
        return

    # 按标签分组输出
    print("建议添加的标签及对应词条:")
    print()

    for tag in sorted(all_suggestions.keys()):
        files = all_suggestions[tag]
        print(f"## {tag}")
        print(f"   建议添加到 {len(files)} 个词条:")
        print()

        for item in files:
            print(f"   📝 {item['file']}")
            for reason in item['reasons']:
                print(f"      - {reason}")
            print()

        print()

    # 生成统计摘要
    print("=" * 80)
    print("统计摘要")
    print("=" * 80)
    print()

    for tag, files in sorted(all_suggestions.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {tag:30s} → {len(files):3d} 个词条")

    print()
    print("=" * 80)
    print("注意:")
    print("  1. 这些建议基于关键词匹配,需要人工审核")
    print("  2. facet:* 标签仅用于顶层分类,暂不建议自动添加")
    print("  3. 建议逐个审查词条内容后手动添加标签")
    print("=" * 80)


if __name__ == "__main__":
    main()
