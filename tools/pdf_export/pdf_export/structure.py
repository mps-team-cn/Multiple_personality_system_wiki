"""整理仓库内的 Markdown 文件并生成导出顺序。"""

from __future__ import annotations

from collections import defaultdict
import sys

from .frontmatter import FrontmatterError, load_entry_document
from .markdown import infer_entry_title
from .models import CategoryStructure, EntryDocument, IgnoreRules
from .paths import ENTRIES_DIR, PROJECT_ROOT


def _build_preface_section(ignore: IgnoreRules) -> tuple[str, tuple[EntryDocument, ...]] | None:
    """若存在《前言》，构建对应的章节分组。"""

    preface_path = PROJECT_ROOT / "Preface.md"
    if not preface_path.exists() or ignore.matches(preface_path):
        return None

    try:
        content = preface_path.read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - 仅在 I/O 出错时触发
        print(f"警告: 无法读取 {preface_path}: {error}", file=sys.stderr)
        return None

    document = EntryDocument(
        path=preface_path.resolve(),
        title=infer_entry_title(preface_path),
        tags=(),
        body=content,
    )
    return ("前言", (document,))


def collect_markdown_structure(ignore: IgnoreRules) -> CategoryStructure:
    """依据词条标签构建导出结构。"""

    if not ENTRIES_DIR.exists():
        return ()

    tag_map: dict[str, list[EntryDocument]] = defaultdict(list)

    for path in sorted(ENTRIES_DIR.glob("*.md")):
        if ignore.matches(path):
            continue
        try:
            document = load_entry_document(path)
        except FrontmatterError as error:
            raise SystemExit(f"解析 {path} 的 frontmatter 失败：{error}") from error

        for tag in document.tags:
            tag_map[tag].append(document)

    categories: list[tuple[str, tuple[EntryDocument, ...]]] = []

    preface_section = _build_preface_section(ignore)
    if preface_section is not None:
        categories.append(preface_section)

    for tag in sorted(tag_map):
        seen = set()
        ordered: list[EntryDocument] = []
        for document in sorted(tag_map[tag], key=lambda item: (item.title, item.path.name)):
            resolved = document.path
            if resolved in seen:
                continue
            seen.add(resolved)
            ordered.append(document)
        if ordered:
            categories.append((tag, tuple(ordered)))

    return tuple(categories)
