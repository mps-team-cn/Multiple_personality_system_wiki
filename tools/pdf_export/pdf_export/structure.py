"""Gather markdown files and ordering information from the repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .models import CategoryStructure, IgnoreRules
from .paths import ENTRIES_DIR, PROJECT_ROOT, README_PATH


def parse_readme_index(readme_path: Path, ignore: IgnoreRules) -> CategoryStructure:
    """Parse README.md to determine the desired export order."""

    if not readme_path.exists():
        return []

    heading_pattern = re.compile(r"^###\s+(?P<title>.+?)\s*$")
    link_pattern = re.compile(r"^\s*-\s*\[(?P<label>[^\]]+)\]\((?P<path>[^)]+)\)")

    categories: list[tuple[str, list[Path]]] = []
    current_category: tuple[str, list[Path]] | None = None

    for raw_line in readme_path.read_text(encoding="utf-8").splitlines():
        if match := heading_pattern.match(raw_line):
            title = match.group("title").strip()
            current_category = (title, [])
            categories.append(current_category)
            continue

        if current_category is None:
            continue

        if link_match := link_pattern.match(raw_line):
            rel_path = link_match.group("path").strip()
            candidate = (PROJECT_ROOT / rel_path).resolve()
            if ignore.matches(candidate):
                continue
            if candidate.exists() and candidate.suffix.lower() == ".md":
                current_category[1].append(candidate)
            else:
                print(
                    f"警告: README 中的条目 {rel_path} 未找到，已忽略。",
                    file=sys.stderr,
                )

    return [(title, tuple(paths)) for title, paths in categories if paths]


def collect_markdown_structure(ignore: IgnoreRules) -> CategoryStructure:
    """Collect markdown files following the README index order."""

    categories = list(parse_readme_index(README_PATH, ignore))
    listed_paths = {path for _, paths in categories for path in paths}

    # 项目根目录下的《前言》应在 PDF 中最先展示。
    preface_path = PROJECT_ROOT / "前言.md"
    if (
        preface_path.exists()
        and not ignore.matches(preface_path)
        and preface_path not in listed_paths
    ):
        categories.insert(0, ("前言", (preface_path,)))

    if categories:
        return tuple(categories)

    fallback_categories: list[tuple[str, list[Path]]] = []

    if ENTRIES_DIR.exists():
        ungrouped = [
            path
            for path in sorted(ENTRIES_DIR.glob("*.md"))
            if not ignore.matches(path)
        ]
        if ungrouped:
            fallback_categories.append(("未分组条目", ungrouped))

        for directory in sorted(ENTRIES_DIR.iterdir()):
            if not directory.is_dir():
                continue
            if ignore.matches(directory):
                continue

            files = [
                path
                for path in sorted(directory.rglob("*.md"))
                if not ignore.matches(path)
            ]
            if files:
                fallback_categories.append((directory.name, files))

    return tuple(fallback_categories)
