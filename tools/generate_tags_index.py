#!/usr/bin/env python3
"""根据词条 Frontmatter 自动生成标签索引页面。"""

from __future__ import annotations

from collections import defaultdict
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.pdf_export.pdf_export.frontmatter import FrontmatterError, load_entry_document


# MkDocs Material 迁移后，优先使用 docs/entries/，保留 entries/ 作为备份
DOCS_ENTRIES_DIR = REPO_ROOT / "docs" / "entries"
ENTRIES_DIR = REPO_ROOT / "entries"
DOCS_OUTPUT_PATH = REPO_ROOT / "docs" / "tags.md"
OUTPUT_PATH = REPO_ROOT / "tags.md"


def main() -> int:
    # 优先使用 docs/entries/，如果不存在则回退到 entries/
    if DOCS_ENTRIES_DIR.exists():
        entries_dir = DOCS_ENTRIES_DIR
        output_path = DOCS_OUTPUT_PATH
        print(f"✓ 使用 MkDocs 词条目录: {entries_dir}")
    elif ENTRIES_DIR.exists():
        entries_dir = ENTRIES_DIR
        output_path = OUTPUT_PATH
        print(f"⚠ 回退到旧版词条目录: {entries_dir}")
    else:
        print("未找到 entries/ 或 docs/entries/ 目录。", file=sys.stderr)
        return 1

    tag_map: dict[str, list] = defaultdict(list)

    for path in sorted(entries_dir.glob("*.md")):
        try:
            document = load_entry_document(path)
        except FrontmatterError as error:
            print(f"解析 {path} 失败：{error}", file=sys.stderr)
            return 1

        for tag in document.tags:
            tag_map[tag].append(document)

    if not tag_map:
        print("没有可用的标签。", file=sys.stderr)
        return 1

    lines: list[str] = ["# 标签索引", ""]

    for tag in sorted(tag_map):
        lines.append(f"## {tag}")
        lines.append("")

        seen_paths: set[Path] = set()
        for document in sorted(tag_map[tag], key=lambda item: (item.title, item.path.name)):
            if document.path in seen_paths:
                continue
            seen_paths.add(document.path)
            relative = document.path.relative_to(REPO_ROOT).as_posix()
            lines.append(f"- [{document.title}]({relative})")

        lines.append("")

    content = "\n".join(lines).rstrip() + "\n"
    output_path.write_text(content, encoding="utf-8")
    print(f"✓ 已生成 {output_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())







