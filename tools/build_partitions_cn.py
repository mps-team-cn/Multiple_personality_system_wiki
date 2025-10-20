#!/usr/bin/env python3
"""
生成主题分区索引页
根据词条的 topic frontmatter 字段，自动生成各主题分区的索引页
"""

from pathlib import Path
import frontmatter
from collections import defaultdict
from datetime import datetime
from pypinyin import lazy_pinyin

DOCS = Path("docs")
ENTRIES = DOCS / "entries"

# 七个主题分区及其英文文件名映射
TOPICS = {
    "诊断与临床": "Clinical-Diagnosis-index.md",
    "系统运作": "System-Operations-index.md",
    "实践指南": "Practice-index.md",
    "创伤与疗愈": "Trauma-Healing-index.md",
    "角色与身份": "Roles-Identity-index.md",
    "理论与分类": "Theory-Classification-index.md",
    "文化与表现": "Cultural-Media-index.md",
}

def get_first_letter(title):
    """
    获取标题的首字母,用于分组
    - 中文转拼音后取首字母
    - 英文直接取首字母
    - 数字和符号归类到 "#"
    """
    if not title:
        return "#"

    first_char = title[0]

    # 如果是英文字母
    if first_char.isalpha():
        return first_char.upper()

    # 如果是中文,转拼音
    if '\u4e00' <= first_char <= '\u9fff':
        pinyin = lazy_pinyin(first_char)[0]
        if pinyin and pinyin[0].isalpha():
            return pinyin[0].upper()

    # 其他情况(数字、符号等)
    return "#"


def generate_summary(buckets, use_letter_grouping=True):
    """
    生成 SUMMARY.md 文件

    Args:
        buckets: 主题词条字典
        use_letter_grouping: 是否使用字母分组(默认 True)
    """
    summary_file = DOCS / "SUMMARY.md"

    lines = []
    lines.append("* [Wiki首页](index.md)")
    lines.append("* 快速开始")
    lines.append("    * [快速开始](QuickStart.md)")
    lines.append("    * [最近更新](updates.md)")
    lines.append("    * [标签索引](tags.md)")
    lines.append("    * [术语词典](Glossary.md)")
    lines.append("    * [核心概念](entries/Core-Concepts-Guide.md)")
    lines.append("    * [健康导览](entries/Mental-Health-Guide.md)")

    lines.append("* 主题导览")
    lines.append("    * [诊断与临床导览](entries/Clinical-Diagnosis-Guide.md)")
    lines.append("    * [系统运作导览](entries/System-Operations-Guide.md)")
    lines.append("    * [实践指南导览](entries/Practice-Guide.md)")
    lines.append("    * [创伤与疗愈导览](entries/Trauma-Healing-Guide.md)")
    lines.append("    * [角色与身份导览](entries/Roles-Identity-Guide.md)")
    lines.append("    * [理论与分类导览](entries/Theory-Classification-Guide.md)")
    lines.append("    * [文化与表现导览](entries/Cultural-Media-Guide.md)")

    # 主题分区
    lines.append("* 主题分区")

    for topic, index_filename in TOPICS.items():
        items = buckets.get(topic, [])

        # 添加主题索引页
        lines.append(f"    * [{topic}](entries/{index_filename})")

        if not items:
            continue

        if use_letter_grouping:
            # 按字母分组
            letter_groups = defaultdict(list)
            for item in items:
                letter = get_first_letter(item['title'])
                letter_groups[letter].append(item)

            # 按字母排序
            sorted_letters = sorted(letter_groups.keys())
            for idx, letter in enumerate(sorted_letters):
                group_items = letter_groups[letter]
                # 组内按标题排序
                group_items.sort(key=lambda x: x['title'])

                # 添加该组的词条
                for item in group_items:
                    lines.append(f"        * [{item['title']}](entries/{item['filename']})")
        else:
            # 不分组,直接按标题排序
            items.sort(key=lambda x: x['title'])
            for item in items:
                lines.append(f"        * [{item['title']}](entries/{item['filename']})")

    lines.append("* 参与项目")
    lines.append("    * [参与贡献](contributing/index.md)")
    lines.append("    * [学术引用规范](contributing/academic-citation.md)")
    lines.append("    * [标注块示例](contributing/admonitions-demo.md)")
    lines.append("    * [临床内容指南](contributing/clinical-guidelines.md)")
    lines.append("    * [贡献者墙](contributing/contributors.md)")
    lines.append("    * [PR 工作流程](contributing/pr-workflow.md)")
    lines.append("    * [标签规范2.0](contributing/tagging-standard.md)")
    lines.append("    * [技术规范](contributing/technical-conventions.md)")
    lines.append("    * [写作指南](contributing/writing-guidelines.md)")
    lines.append("* [回到主站 →](https://mpsteam.cn/)")
    lines.append("")

    summary_file.write_text("\n".join(lines), encoding="utf-8")

    total_entries = sum(len(items) for items in buckets.values())
    if use_letter_grouping:
        print(f"[gen] 已生成 SUMMARY.md（7 个主题，按字母分组，共 {total_entries} 个词条）。")
    else:
        print(f"[gen] 已生成 SUMMARY.md（7 个主题，共 {total_entries} 个词条）。")

def main():
    # 收集词条
    buckets = defaultdict(list)

    for md in sorted(ENTRIES.glob("*.md")):
        # 跳过索引页和导览页
        if md.name.endswith("-index.md") or md.name.endswith("-Guide.md"):
            continue

        try:
            post = frontmatter.load(md)
            meta = post.metadata or {}
            topic = meta.get("topic")

            if not topic or topic not in TOPICS.keys():
                continue

            updated = meta.get("updated")
            try:
                dt = datetime.fromisoformat(str(updated)) if updated else None
            except Exception:
                dt = None

            buckets[topic].append({
                "title": meta.get("title") or md.stem,
                "filename": md.name,  # 只保存文件名，用于生成相对链接
                "updated": updated,
                "dt": dt or datetime.min,
            })
        except Exception as e:
            print(f"[警告] 跳过文件 {md.name}: {e}")
            continue

    # 生成每个分区索引
    for topic, filename in TOPICS.items():
        items = buckets.get(topic, [])

        # 按更新时间降序排列
        items.sort(key=lambda x: x["dt"], reverse=True)

        out_file = ENTRIES / filename

        lines = []
        lines.append("---")
        lines.append(f"title: {topic}索引")
        lines.append(f"topic: {topic}")
        lines.append("tags:")
        lines.append("  - meta:索引")
        lines.append("  - meta:导览")
        # lines.append(f"updated: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("comments: true")
        lines.append("search:")
        lines.append("  exclude: true")
        lines.append("hide:")
        lines.append("  - toc")
        lines.append("  - tags")
        lines.append("---")
        lines.append("")
        lines.append(f"# {topic}索引")
        lines.append("")
        lines.append(f"> 本页汇总所有主题为「{topic}」的词条，原文档仍在 `entries/` 目录中。")
        lines.append("")

        if items:
            lines.append("## 词条一览")
            lines.append("")
            for it in items:
                suffix = f" — *{it['updated']}*" if it["updated"] else ""
                # 使用相对路径链接到同目录下的词条文件
                lines.append(f"- [{it['title']}]({it['filename']}){suffix}")
        else:
            lines.append("*暂无词条*")

        lines.append("")

        out_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"[gen] 已生成 {len(TOPICS)} 个中文分区索引页。")

    # 生成 SUMMARY.md 文件
    generate_summary(buckets)

if __name__ == "__main__":
    main()
