#!/usr/bin/env python3
"""根据词条 Frontmatter 自动生成标签索引页面。"""

from __future__ import annotations

from collections import defaultdict
import sys
from pathlib import Path

from tools.pdf_export.pdf_export.frontmatter import FrontmatterError, load_entry_document


REPO_ROOT = Path(__file__).resolve().parent
ENTRIES_DIR = REPO_ROOT / "entries"
OUTPUT_PATH = REPO_ROOT / "tags.md"


def main() -> int:
    if not ENTRIES_DIR.exists():
        print("未找到 entries/ 目录。", file=sys.stderr)
        return 1

    tag_map: dict[str, list] = defaultdict(list)

    for path in sorted(ENTRIES_DIR.glob("*.md")):
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
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"已生成 {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

