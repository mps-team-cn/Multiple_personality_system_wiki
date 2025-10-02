#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
按 Git 标签逐段生成 CHANGELOG.md（Windows/Linux/Mac 通用）
- 以标签创建时间排序，依次生成每个版本段落（PREV..CUR）
- 每个版本内按 Conventional Commits 类型分组
- 末尾追加“其他”分组（未匹配类型）
- 自动解析 GitHub 仓库 slug 用于生成提交链接；失败则降级为纯哈希

用法：
    python tools/gen_changelog_by_tags.py
    python tools/gen_changelog_by_tags.py --output CHANGELOG.md
    python tools/gen_changelog_by_tags.py --latest-only   # 只生成“上一个标签..最新标签（或 HEAD）”一段
"""

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# Conventional Commits 分组与中文标题
GROUPS = [
    ("feat",     "✨ 新增"),
    ("fix",      "🐛 修复"),
    ("docs",     "📝 文档"),
    ("refactor", "🔧 重构"),
    ("chore",    "📦 杂务"),
    ("style",    "🎨 风格"),
    ("perf",     "⚡ 性能"),
    ("test",     "✅ 测试"),
    ("ci",       "🤖 CI"),
    ("build",    "🏗️ 构建"),
    ("revert",   "⏪ 回滚"),
]

ENCODING = "utf-8"

def sh(cmd: str) -> str:
    """Run shell command and return stdout (stripped)."""
    # 在 Windows 下使用 shell=True 以执行 git 命令
    return subprocess.check_output(cmd, shell=True, text=True, encoding=ENCODING).strip()

def try_sh(cmd: str) -> Optional[str]:
    try:
        return sh(cmd)
    except subprocess.CalledProcessError:
        return None

def get_repo_root() -> Path:
    out = sh("git rev-parse --show-toplevel")
    return Path(out)

def get_repo_slug() -> Optional[str]:
    """
    解析 remote.origin.url，尝试提取 GitHub slug: owner/repo
    支持：
      - https://github.com/owner/repo.git
      - git@github.com:owner/repo.git
      - https://github.com/owner/repo
    """
    url = try_sh("git config --get remote.origin.url")
    if not url:
        return None
    url = url.strip()

    # 常见两种
    m = re.search(r"github\.com[:/](?P<owner>[^/\s]+)/(?P<repo>[^/\s\.]+)(?:\.git)?$", url)
    if m:
        owner = m.group("owner")
        repo = m.group("repo")
        return f"{owner}/{repo}"
    return None

def get_all_tags_sorted() -> List[str]:
    out = try_sh("git tag --sort=creatordate")
    if not out:
        return []
    tags = [t for t in out.splitlines() if t.strip()]
    return tags

def get_tag_date(tag: str) -> str:
    """
    返回标签对应提交的日期（YYYY-MM-DD）
    """
    out = sh(f'git log -1 --format=%ad --date=format:%Y-%m-%d {tag}')
    return out or datetime.now().strftime("%Y-%m-%d")

def get_commits_in_range(rng: str) -> List[Tuple[str, str]]:
    """
    返回 (hash, subject) 列表
    rng 例子：  v1.2.0..v1.2.3  或  v1.2.3
    """
    out = try_sh(f'git log {rng} --pretty=format:"%H|%s"')
    if not out:
        return []
    commits = []
    for line in out.splitlines():
        if "|" not in line:
            continue
        h, s = line.split("|", 1)
        commits.append((h, s.strip()))
    return commits

def group_commits(commits: List[Tuple[str, str]]) -> Tuple[Dict[str, List[Tuple[str, str]]], List[Tuple[str, str]]]:
    grouped: Dict[str, List[Tuple[str, str]]] = {k: [] for k, _ in GROUPS}
    others: List[Tuple[str, str]] = []
    for h, s in commits:
        lowered = s.lower()
        matched = False
        for k, _ in GROUPS:
            if lowered.startswith(k + ":"):
                grouped[k].append((h, s))
                matched = True
                break
        if not matched:
            others.append((h, s))
    return grouped, others

def format_commit_line(hash_full: str, subject: str, repo_slug: Optional[str]) -> str:
    h7 = hash_full[:7]
    if repo_slug:
        return f"- {subject} ([{h7}](https://github.com/{repo_slug}/commit/{hash_full}))"
    else:
        return f"- {subject} [{h7}]"

def build_changelog(latest_only: bool = False) -> str:
    repo_slug = get_repo_slug()
    tags = get_all_tags_sorted()

    lines: List[str] = []
    header_written = False

    def ensure_header():
        nonlocal header_written
        if not header_written:
            lines.append("# 更新日志")
            header_written = True

    if not tags:
        # 没有任何 tag，生成一个“Unreleased”区间（从初始到 HEAD）
        ensure_header()
        today = datetime.now().strftime("%Y-%m-%d")
        lines.append(f"\n## Unreleased ({today})")
        commits = get_commits_in_range("HEAD")
        grouped, others = group_commits(commits)
        for k, label in GROUPS:
            items = grouped[k]
            if not items:
                continue
            lines.append(f"\n### {label}")
            for h, s in items:
                lines.append(format_commit_line(h, s, repo_slug))
        if others:
            lines.append("\n### 其他")
            for h, s in others:
                lines.append(format_commit_line(h, s, repo_slug))
        lines.append("\n— 由 Git 提交记录自动生成")
        return "\n".join(lines).strip() + "\n"

    if latest_only and len(tags) >= 1:
        # 仅生成“上一个标签..最新标签（或 HEAD）”
        prev = tags[-2] if len(tags) >= 2 else ""
        cur = tags[-1]
        rng = f"{prev}..{cur}" if prev else cur
        date_str = get_tag_date(cur)
        ensure_header()
        lines.append(f"\n## {cur} ({date_str})")
        commits = get_commits_in_range(rng)
        grouped, others = group_commits(commits)
        for k, label in GROUPS:
            items = grouped[k]
            if not items:
                continue
            lines.append(f"\n### {label}")
            for h, s in items:
                lines.append(format_commit_line(h, s, repo_slug))
        if others:
            lines.append("\n### 其他")
            for h, s in others:
                lines.append(format_commit_line(h, s, repo_slug))
        lines.append("\n— 由 Git 提交记录自动生成")
        return "\n".join(lines).strip() + "\n"

    # 全量：从最早 tag 到最新 tag，逐段生成 PREV..CUR
    ensure_header()
    for i, cur in enumerate(tags):
        prev = tags[i - 1] if i - 1 >= 0 else ""
        rng = f"{prev}..{cur}" if prev else cur
        date_str = get_tag_date(cur)
        lines.append(f"\n## {cur} ({date_str})")

        commits = get_commits_in_range(rng)
        grouped, others = group_commits(commits)

        for k, label in GROUPS:
            items = grouped[k]
            if not items:
                continue
            lines.append(f"\n### {label}")
            for h, s in items:
                lines.append(format_commit_line(h, s, repo_slug))

        if others:
            lines.append("\n### 其他")
            for h, s in others:
                lines.append(format_commit_line(h, s, repo_slug))

    lines.append("\n— 由 Git 提交记录自动生成")
    return "\n".join(lines).strip() + "\n"

def main():
    parser = argparse.ArgumentParser(description="按标签逐段生成 CHANGELOG.md")
    parser.add_argument("--output", default="CHANGELOG.md", help="输出文件路径（默认：仓库根目录 CHANGELOG.md）")
    parser.add_argument("--latest-only", action="store_true", help="只生成从上一个标签到最新标签的一段")
    args = parser.parse_args()

    repo_root = get_repo_root()
    out_path = (repo_root / args.output).resolve()

    md = build_changelog(latest_only=args.latest_only)

    # 写入文件（覆盖）
    out_path.write_text(md, encoding=ENCODING)
    print(f"[OK] 已生成：{out_path}")

if __name__ == "__main__":
    main()
