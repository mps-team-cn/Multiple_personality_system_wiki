#!/usr/bin/env python3
"""
检查词条 Frontmatter 的标签是否符合《MPS Wiki Tagging Standard v2.0》

校验维度：
  1) 至少一个带合法前缀的标签
  2) 标签总数 ≤ 5
  3) 前缀必须在允许分面集合内
  4) 不使用别名（通过 data/tags_alias.yaml 管理）
  5) 标签“名称部分”不得与页面 title 完全相同
  6) 每个标签匹配正则：^[a-z]+:[^\s()]+$ （无空格与英文半角括号）

用法：
  python3 tools/check_tags.py docs/entries/
  python3 tools/check_tags.py docs/entries/DID.md
  python3 tools/check_tags.py --verbose docs/entries/
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import yaml
import frontmatter


ALLOWED_PREFIXES = {
    "dx", "sx", "tx", "scale", "theory", "ops", "role",
    "community", "guide", "history", "misuse", "bio", "sleep",
    "dev", "culture", "meta",
}

TAG_PATTERN = re.compile(r"^[a-z]+:[^\s()]+$")


@dataclass
class TagIssue:
    file: Path
    message: str


def load_alias_map(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            return {}
        # 只接受 str->str 的简单映射
        return {str(k): str(v) for k, v in data.items()}
    except Exception:
        return {}


def iter_markdown_targets(paths: List[Path]) -> List[Path]:
    targets: List[Path] = []
    for p in paths:
        if p.is_dir():
            targets.extend(sorted(p.glob("*.md")))
        elif p.is_file() and p.suffix.lower() == ".md":
            targets.append(p)
    return targets


def validate_tags(md_path: Path, alias_map: Dict[str, str], verbose: bool = False) -> List[TagIssue]:
    issues: List[TagIssue] = []

    try:
        post = frontmatter.load(md_path)
    except Exception as e:
        issues.append(TagIssue(md_path, f"无法解析 Frontmatter：{e}"))
        return issues

    meta = post.metadata or {}
    title = str(meta.get("title", "")).strip()
    tags = meta.get("tags")

    if not isinstance(tags, list) or not tags:
        issues.append(TagIssue(md_path, "缺少 tags 或 tags 为空（至少 1 个）"))
        return issues

    # 数量限制
    if len(tags) > 5:
        issues.append(TagIssue(md_path, f"标签数量 {len(tags)} 超出上限（≤ 5）"))

    has_allowed_prefix = False

    for raw in tags:
        if not isinstance(raw, str):
            issues.append(TagIssue(md_path, f"存在非字符串标签：{raw!r}"))
            continue

        tag = raw.strip()
        if not TAG_PATTERN.match(tag):
            issues.append(TagIssue(md_path, f"格式不合法：{tag!r}（需匹配 ^[a-z]+:[^\\s()]+$）"))
            # 无法继续解析前缀/名称，跳过后续检查
            continue

        # 前缀校验
        prefix, name = tag.split(":", 1)
        if prefix not in ALLOWED_PREFIXES:
            issues.append(TagIssue(md_path, f"未定义前缀：{prefix}:（不在允许分面中）"))
        else:
            has_allowed_prefix = True

        # 别名校验（禁止使用映射键作为标签）
        if tag in alias_map:
            issues.append(TagIssue(md_path, f"使用了别名：{tag!r} → 请改用规范名 {alias_map[tag]!r}"))

        # 与标题重复（名称部分与 title 完全一致）
        if title and name == title:
            issues.append(TagIssue(md_path, f"标签名称与页面标题重复：{tag!r}（请精炼为分面分类）"))

    if not has_allowed_prefix:
        issues.append(TagIssue(md_path, "未发现带合法前缀的标签（需至少 1 个）"))

    if verbose and not issues:
        print(f"✅ {md_path}")

    return issues


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "检查 Markdown 词条的标签是否符合 Tagging Standard v2.0。"
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("docs/entries/")],
        help="要检查的目录或文件（默认：docs/entries/）",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示通过文件",
    )

    args = parser.parse_args(argv)

    alias_map = load_alias_map(Path("data/tags_alias.yaml"))
    targets = [p for p in iter_markdown_targets(args.paths) if p.exists()]

    if not targets:
        print("⚠️ 未找到要检查的 Markdown 文件。")
        return 0

    all_issues: List[TagIssue] = []
    base_entries = Path("docs/entries").resolve()
    for md in targets:
        # 仅对 docs/entries/ 下的词条强制校验（若传入单文件也允许）
        in_entries = False
        try:
            md.resolve().relative_to(base_entries)
            in_entries = True
        except Exception:
            in_entries = False

        if in_entries or len(args.paths) == 1:
            all_issues.extend(validate_tags(md, alias_map, verbose=args.verbose))

    if not all_issues:
        print("✅ 标签规范检查通过")
        return 0

    # 输出报告
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("❌ 标签规范检查失败！\n")

    by_file: Dict[Path, List[str]] = {}
    for issue in all_issues:
        by_file.setdefault(issue.file, []).append(f"- {issue.message}")

    for file, messages in by_file.items():
        print(f"文件：{file}")
        for msg in messages:
            print(f"  {msg}")
        print()

    print("📋 规范摘要：")
    print("  - 至少 1 个合法前缀；总数 ≤ 5")
    print("  - 允许前缀：dx/sx/tx/scale/theory/ops/role/community/guide/history/misuse/bio/sleep/dev/culture/meta")
    print("  - 禁止别名；禁止空格、句号、英文半角括号；正则 ^[a-z]+:[^\\s()]+$")
    print("  - 名称部分不得与页面 title 完全相同")
    print()
    print("📖 参考文档：docs/contributing/tagging-standard.md")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
