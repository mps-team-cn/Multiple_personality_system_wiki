#!/usr/bin/env python3
"""
标签标准化脚本
根据既定的标签规范对所有词条进行批量标准化处理

A类操作: 合并/下线冗余标签
B类操作: 重命名/标准化标签

使用方法:
    python3 tag_normalization.py
"""

import os
import re
from typing import Dict, List, Set
from pathlib import Path


# A类: 需要合并或下线的标签映射
TAG_MERGE_MAP: Dict[str, str] = {
    # Tulpa相关导览 -> community:Tulpa + guide:创造型系统
    "Tulpa 完全创造指南·基础篇": "",  # 删除,使用文件名识别
    "Tulpa 完全创造指南·实践篇": "",  # 删除
    "Tulpa 完全创造指南·提高篇": "",  # 删除

    # 导览类合并
    "实践指南导览": "guide:实践指南",
    "创伤与疗愈导览": "guide:导览",
    "健康导览": "guide:导览",

    # 系统运作类
    "系统(System)": "ops:系统运作",
    "系统运作": "ops:系统运作",

    # 核心概念 -> 删除(无检索价值)
    "核心概念": "",

    # 角色类
    "卡前台(Front Stuck / Frontstuck)": "ops:卡前台",
    "卡前台": "ops:卡前台",

    # 社群术语
    "T 语(Tulpish)": "community:Tulpish",
    "T语": "community:Tulpish",

    # 心理学流派
    "人本主义心理学": "theory:人本主义心理学",
    "精神分析心理学": "theory:精神分析心理学",
    "行为主义心理学": "theory:行为主义心理学",

    # DSM量表
    "DSM-5-TR 评估量表总览": "scale:DSM-5-TR 评估量表",
    "DSM-5-TR": "scale:DSM-5-TR 评估量表",
    "DSM-5": "scale:DSM-5-TR 评估量表",
}

# B类: 标准化重命名映射
TAG_RENAME_MAP: Dict[str, str] = {
    # 诊断类标准化(添加 dx: 前缀)
    "DID": "dx:DID",
    "OSDD": "dx:OSDD",
    "DPDR": "dx:DPDR",
    "PTSD": "dx:PTSD",
    "CPTSD": "dx:CPTSD",
    "FND": "dx:功能性神经症状障碍(FND)",
    "GD": "dx:性别不安(GD)",

    # 人格障碍类
    "人格障碍": "dx:人格障碍(PDs)",
    "A组人格障碍": "dx:A组人格障碍",
    "B组人格障碍": "dx:B组人格障碍",
    "C组人格障碍": "dx:C组人格障碍",

    # 情绪障碍标准化
    "焦虑": "dx:焦虑障碍",
    "焦虑障碍": "dx:焦虑障碍",
    "抑郁": "dx:抑郁障碍",
    "抑郁障碍": "dx:抑郁障碍",
    "情绪障碍": "dx:双相及相关障碍",
    "情感障碍": "dx:双相及相关障碍",
    "心境障碍": "dx:双相及相关障碍",

    # Tulpa/附体类
    "Tulpa": "community:Tulpa",
    "tulpa": "community:Tulpa",
    "附体": "ops:附体(Possession)",
    "Possession": "ops:附体(Possession)",

    # 系统运作类
    "并行": "ops:并行",
    "共前台": "ops:共前台",
    "混合": "ops:混合",
    "切换": "ops:切换",
    "权限": "ops:权限",
    "子系统": "ops:子系统",

    # 理论类
    "ANP-EP 模型": "theory:ANP-EP 模型",
    "ANP": "theory:ANP",
    "EP": "theory:EP",
    "结构性解离理论": "theory:结构性解离理论(TSDP)",

    # 治疗类(tx: = treatment)
    "IFS": "tx:IFS",
    "CBT": "tx:CBT",
    "DBT": "tx:DBT",
    "EMDR": "tx:EMDR",
    "PE": "tx:PE",
    "ACT": "tx:ACT",
    "SE": "tx:SE",

    # 生物治疗类
    "MECT": "bio:MECT",
    "脑刺激": "bio:脑刺激",

    # 量表类
    "DES-II": "scale:DES-II",
    "MID-60": "scale:MID-60",
    "MID": "scale:MID-60",
    "量表": "scale:评估量表",
    "评估工具": "scale:评估量表",

    # 历史术语类
    "癔症": "history:癔症",
    "MPD": "history:MPD",
    "历史术语": "history:历史术语",

    # 误用类
    "人格分裂": "misuse:人格分裂",

    # 导览类
    "危机与支援资源": "guide:支援资源",
    "自我照护工具箱": "guide:自我照护",
    "主题导览": "guide:导览",
    "索引": "guide:索引",

    # 文化表现类
    "文化与表现": "culture:文化表现",

    # 多意识体保持原样,但统一书写
    "多意识体": "多意识体",
    "解离": "解离",
    "创伤": "创伤",
    "诊断与临床": "诊断与临床",
    "角色与身份": "角色与身份",
    "理论与分类": "理论与分类",
    "创伤与疗愈": "创伤与疗愈",
}


def extract_frontmatter(content: str) -> tuple[str, str, str]:
    """
    提取frontmatter、tags部分和剩余内容
    返回: (frontmatter_before_tags, tags_content, content_after_tags)
    """
    # 匹配整个frontmatter
    fm_match = re.search(r'^---\n(.*?)^---', content, re.MULTILINE | re.DOTALL)
    if not fm_match:
        return "", "", content

    fm_content = fm_match.group(1)
    before_fm = content[:fm_match.start()]
    after_fm = content[fm_match.end():]

    # 提取tags部分
    tags_match = re.search(r'^tags:\s*\n((?:^\s*-\s*.+\n)+)', fm_content, re.MULTILINE)
    if not tags_match:
        return fm_content, "", after_fm

    fm_before_tags = fm_content[:tags_match.start()]
    tags_content = tags_match.group(1)
    fm_after_tags = fm_content[tags_match.end():]

    return (fm_before_tags, tags_content, fm_after_tags, before_fm, after_fm)


def parse_tags(tags_content: str) -> List[str]:
    """从tags内容中提取所有标签"""
    tags = re.findall(r'^\s*-\s*(.+?)\s*$', tags_content, re.MULTILINE)
    return [tag.strip() for tag in tags]


def normalize_tags(tags: List[str]) -> List[str]:
    """标准化标签列表"""
    normalized = set()

    for tag in tags:
        # 先检查是否需要合并/删除(A类)
        if tag in TAG_MERGE_MAP:
            new_tag = TAG_MERGE_MAP[tag]
            if new_tag:  # 如果映射不为空,添加新标签
                normalized.add(new_tag)
            # 如果为空,则删除该标签
        # 再检查是否需要重命名(B类)
        elif tag in TAG_RENAME_MAP:
            normalized.add(TAG_RENAME_MAP[tag])
        else:
            # 保持原样
            normalized.add(tag)

    # 排序并返回
    return sorted(normalized)


def format_tags(tags: List[str]) -> str:
    """格式化标签为YAML格式"""
    if not tags:
        return ""
    lines = ["tags:", ""]
    for tag in tags:
        lines.append(f"  - {tag}")
    lines.append("")
    return "\n".join(lines)


def process_file(filepath: Path, dry_run: bool = True) -> tuple[bool, str]:
    """
    处理单个文件的标签
    返回: (是否修改, 修改说明)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取frontmatter和tags
        parts = extract_frontmatter(content)
        if len(parts) != 5:
            return False, "无法解析frontmatter"

        fm_before, tags_content, fm_after, before_fm, after_fm = parts

        if not tags_content:
            return False, "未找到tags字段"

        # 解析并标准化标签
        old_tags = parse_tags(tags_content)
        new_tags = normalize_tags(old_tags)

        if set(old_tags) == set(new_tags):
            return False, "无需修改"

        # 构建新内容
        new_tags_str = format_tags(new_tags)
        new_fm = f"{fm_before}tags:\n\n" + "\n".join(f"  - {tag}" for tag in new_tags) + f"\n{fm_after}"
        new_content = f"{before_fm}---\n{new_fm}---{after_fm}"

        # 写入文件(如果不是dry run)
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

        removed = set(old_tags) - set(new_tags)
        added = set(new_tags) - set(old_tags)

        changes = []
        if removed:
            changes.append(f"删除: {', '.join(sorted(removed))}")
        if added:
            changes.append(f"添加: {', '.join(sorted(added))}")

        return True, " | ".join(changes)

    except Exception as e:
        return False, f"错误: {str(e)}"


def main():
    """主函数"""
    import sys

    entries_dir = Path("docs/entries")

    if not entries_dir.exists():
        print(f"错误: 目录不存在 {entries_dir}")
        return

    # 检查命令行参数
    execute = "--execute" in sys.argv or "-e" in sys.argv

    print("=" * 80)
    print("标签标准化脚本")
    print("=" * 80)
    print()

    # 先执行dry run
    if execute:
        print("【执行模式】开始修改文件...")
    else:
        print("【预览模式】检查需要修改的文件...")
        print("(使用 --execute 或 -e 参数执行实际修改)")
    print()

    modified_files = []

    for filepath in sorted(entries_dir.glob("*.md")):
        changed, msg = process_file(filepath, dry_run=not execute)
        if changed:
            modified_files.append((filepath, msg))
            if execute:
                print(f"✅ {filepath.name}")
            else:
                print(f"📝 {filepath.name}")
                print(f"   {msg}")
                print()

    if not modified_files:
        print("✅ 所有文件的标签已符合规范,无需修改")
        return

    print()
    print("=" * 80)
    if execute:
        print(f"完成! 成功修改 {len(modified_files)} 个文件")
    else:
        print(f"共发现 {len(modified_files)} 个文件需要修改")
        print("使用 'python3 tools/tag_normalization.py --execute' 执行实际修改")
    print("=" * 80)


if __name__ == "__main__":
    main()
