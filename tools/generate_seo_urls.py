#!/usr/bin/env python3
"""
生成高权重 URL 列表用于 SEO 提交
基于搜索词频权重和页面重要性生成优先级 URL
"""

import re
from pathlib import Path
from typing import List, Tuple

# 网站基础 URL
BASE_URL = "https://wiki.mpsteam.cn"

# 根据 user_dict.txt 中的权重定义的核心诊断/概念词条
# 权重 >= 8000 的核心术语
HIGH_PRIORITY_TERMS = {
    "DID": "DID",
    "解离性身份障碍": "DID",
    "OSDD": "OSDD",
    "其他特定解离性障碍": "OSDD",
    "PTSD": "PTSD",
    "创伤后应激障碍": "PTSD",
    "CPTSD": "CPTSD",
    "复杂性创伤后应激障碍": "CPTSD",
    "焦虑障碍": "Anxiety-Disorders",
    "抑郁障碍": "Depressive-Disorders",
    "惊恐障碍": "Panic-Disorder",
    "精神分裂症": "Schizophrenia-SZ",
    "边缘性人格障碍": "Borderline-Personality-Disorder-BPD",
    "自恋型人格障碍": "Narcissistic-Personality-Disorder-NPD",
    "广泛性焦虑障碍": "Generalized-Anxiety-Disorder-GAD",
    "社交焦虑障碍": "Social-Anxiety-Disorder",
    "强迫症": "OCD",
}

# 核心导览页面(按重要性排序)
CORE_GUIDES = [
    ("", "Wiki 首页"),
    ("QuickStart", "快速开始"),
    ("guides/Core-Concepts-Guide", "核心概念导览"),
    ("guides/Mental-Health-Guide", "心理健康导览"),
    ("guides/Clinical-Diagnosis-Guide", "诊断与临床导览"),
    ("guides/System-Operations-Guide", "系统运作导览"),
    ("guides/Practice-Guide", "实践指南导览"),
    ("guides/Trauma-Healing-Guide", "创伤与疗愈导览"),
    ("guides/Roles-Identity-Guide", "角色与身份导览"),
    ("guides/Theory-Classification-Guide", "理论与分类导览"),
    ("guides/Cultural-Media-Guide", "文化与表现导览"),
]

# 主题分区索引页面
PARTITION_PAGES = [
    ("guides/Clinical-Diagnosis-index", "诊断与临床主题分区"),
    ("guides/System-Operations-index", "系统运作主题分区"),
    ("guides/Practice-index", "实践指南主题分区"),
    ("guides/Trauma-Healing-index", "创伤与疗愈主题分区"),
    ("guides/Roles-Identity-index", "角色与身份主题分区"),
    ("guides/Theory-Classification-index", "理论与分类主题分区"),
    ("guides/Cultural-Media-index", "文化与表现主题分区"),
]

# 关键工具页面
TOOL_PAGES = [
    ("tags", "标签索引"),
    ("Glossary", "术语词典"),
    ("updates", "最近更新"),
    ("changelog", "更新日志"),
]

# 高优先级词条(基于核心概念和高频诊断)
PRIORITY_ENTRIES = [
    # 核心诊断
    "DID", "OSDD", "PTSD", "CPTSD",
    "Dissociative-Disorders",
    "Anxiety-Disorders", "Depressive-Disorders",
    "Borderline-Personality-Disorder-BPD",
    "Generalized-Anxiety-Disorder-GAD",
    "Social-Anxiety-Disorder",
    "Panic-Disorder",
    "OCD",
    "Schizophrenia-SZ",

    # 核心概念
    "Multiple_Personality_System",
    "Dissociation",
    "Trauma",
    "System",
    "Alter",
    "Switch",
    "Co-Consciousness",
    "Tulpa",

    # 核心操作
    "Front-Fronting",
    "Co-Fronting",
    "Internal-Communication",
    "Headspace-Inner-World",
    "Grounding",
    "Integration",

    # 核心角色
    "Host",
    "Protector",
    "Gatekeeper",
    "Fragment",
    "Child-Alter",

    # 核心疗法
    "Cognitive-Behavioral-Therapy-CBT",
    "Dialectical-Behavior-Therapy-DBT",
    "Eye-Movement-Desensitization-Reprocessing-EMDR",
    "Internal-Family-Systems-IFS",

    # 记忆相关核心概念
    "Dissociative-Amnesia-DA",
    "Memory-Shielding",
]


def generate_url_list() -> List[Tuple[int, str, str]]:
    """
    生成带优先级的 URL 列表
    返回: [(优先级, URL, 描述)]
    优先级: 1=最高, 5=最低
    """
    urls = []

    # 1. 首页和核心导览 (优先级 1)
    for path, desc in CORE_GUIDES:
        url = f"{BASE_URL}/{path}" if path else BASE_URL
        urls.append((1, url, desc))

    # 2. 关键工具页面 (优先级 1)
    for path, desc in TOOL_PAGES:
        urls.append((1, f"{BASE_URL}/{path}", desc))

    # 3. 主题分区索引 (优先级 2)
    for path, desc in PARTITION_PAGES:
        urls.append((2, f"{BASE_URL}/{path}", desc))

    # 4. 高优先级词条 (优先级 2)
    for entry in PRIORITY_ENTRIES:
        urls.append((2, f"{BASE_URL}/entries/{entry}", f"词条: {entry}"))

    return urls


def format_url_list(urls: List[Tuple[int, str, str]]) -> str:
    """格式化 URL 列表为可读文本"""
    # 按优先级排序
    urls.sort(key=lambda x: (x[0], x[1]))

    output = []
    output.append("=" * 80)
    output.append("Multiple Personality System Wiki - SEO 高权重 URL 清单")
    output.append(f"网站地址: {BASE_URL}")
    output.append("=" * 80)
    output.append("")

    current_priority = None
    for priority, url, desc in urls:
        if priority != current_priority:
            current_priority = priority
            priority_label = {
                1: "最高优先级 - 核心页面与工具",
                2: "高优先级 - 主题分区与核心词条",
                3: "中等优先级 - 重要词条",
                4: "普通优先级 - 一般词条",
                5: "低优先级 - 补充内容"
            }
            output.append("")
            output.append(f"{'─' * 80}")
            output.append(f"【优先级 {priority}】{priority_label.get(priority, '其他')}")
            output.append(f"{'─' * 80}")
            output.append("")

        output.append(url)

    output.append("")
    output.append("=" * 80)
    output.append(f"总计: {len(urls)} 个 URL")
    output.append("")
    output.append("使用建议:")
    output.append("1. 优先提交「优先级 1」的 URL 到搜索引擎")
    output.append("2. 定期更新「优先级 2」的词条内容")
    output.append("3. 建议使用 Google Search Console / Bing Webmaster Tools 批量提交")
    output.append("4. 配合 sitemap.xml 自动提交(已由 MkDocs 生成)")
    output.append("=" * 80)

    return "\n".join(output)


def main():
    """主函数"""
    urls = generate_url_list()
    output = format_url_list(urls)

    # 输出到文件
    output_file = Path(__file__).parent.parent / "seo_priority_urls.txt"
    output_file.write_text(output, encoding="utf-8")

    print(output)
    print()
    print(f"✓ URL 清单已保存到: {output_file}")


if __name__ == "__main__":
    main()
