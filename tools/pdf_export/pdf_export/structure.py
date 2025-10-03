"""整理仓库内的 Markdown 文件并生成导出顺序。"""

from __future__ import annotations

import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Iterable

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


def _load_entry_documents(ignore: IgnoreRules) -> OrderedDict[Path, EntryDocument]:
    """读取 entries 目录中的词条并保留原始文件名顺序。"""

    documents: OrderedDict[Path, EntryDocument] = OrderedDict()
    if not ENTRIES_DIR.exists():
        return documents

    for path in sorted(ENTRIES_DIR.glob("*.md")):
        if ignore.matches(path):
            continue
        try:
            document = load_entry_document(path)
        except FrontmatterError as error:
            raise SystemExit(f"解析 {path} 的 frontmatter 失败：{error}") from error
        documents[document.path] = document

    return documents


_INDEX_SECTION_PATTERN = re.compile(r"^##\s+(?P<title>.+?)\s*$")
_INDEX_ENTRY_PATTERN = re.compile(r"^-\s*\[[^\]]+\]\((?P<target>[^)]+)\)")


def _normalize_index_target(raw_target: str) -> Path | None:
    """将 ``index.md`` 中的链接目标转换为项目内的绝对路径。"""

    stripped = raw_target.strip()
    if not stripped:
        return None
    if stripped.startswith("<") and stripped.endswith(">"):
        stripped = stripped[1:-1].strip()
    if not stripped:
        return None

    # 忽略锚点，仅关注 Markdown 文件路径。
    if "#" in stripped:
        stripped = stripped.split("#", 1)[0].strip()
    if not stripped:
        return None

    candidate = PROJECT_ROOT / stripped
    try:
        return candidate.resolve(strict=False)
    except OSError:
        return None


def _build_sections_from_index(
    documents: OrderedDict[Path, EntryDocument],
) -> tuple[list[tuple[str, tuple[EntryDocument, ...]]], set[Path]]:
    """解析 ``index.md``，生成章节顺序并返回已使用的词条路径集合。"""

    index_path = PROJECT_ROOT / "index.md"
    if not index_path.exists():
        return ([], set())

    try:
        lines = index_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:  # pragma: no cover - 仅在 I/O 出错时触发
        print(f"警告: 无法读取 {index_path}: {error}", file=sys.stderr)
        return ([], set())

    sections: list[tuple[str, list[EntryDocument]]] = []
    used_paths: set[Path] = set()

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            continue

        section_match = _INDEX_SECTION_PATTERN.match(stripped)
        if section_match:
            title = section_match.group("title").strip()
            sections.append((title, []))
            continue

        entry_match = _INDEX_ENTRY_PATTERN.match(stripped)
        if not entry_match or not sections:
            continue

        target_path = _normalize_index_target(entry_match.group("target"))
        if target_path is None:
            continue

        document = documents.get(target_path)
        if document is None:
            continue

        if document.path in used_paths:
            continue

        sections[-1][1].append(document)
        used_paths.add(document.path)

    finalized = [
        (title, tuple(items))
        for title, items in sections
        if items
    ]
    return (finalized, used_paths)


def _build_fallback_section(
    documents: Iterable[EntryDocument],
    used_paths: set[Path],
) -> tuple[str, tuple[EntryDocument, ...]] | None:
    """将未在 ``index.md`` 中出现的词条组成兜底章节。"""

    remaining = [
        document
        for document in documents
        if document.path not in used_paths
    ]

    if not remaining:
        return None

    ordered = sorted(remaining, key=lambda item: (item.title, item.path.name))
    return ("未索引词条", tuple(ordered))


def collect_markdown_structure(ignore: IgnoreRules) -> CategoryStructure:
    """依据 ``index.md`` 的顺序构建导出结构。"""

    documents = _load_entry_documents(ignore)
    categories: list[tuple[str, tuple[EntryDocument, ...]]] = []

    preface_section = _build_preface_section(ignore)
    if preface_section is not None:
        categories.append(preface_section)

    index_sections, used_paths = _build_sections_from_index(documents)
    categories.extend(index_sections)

    fallback_section = _build_fallback_section(documents.values(), used_paths)
    if fallback_section is not None:
        categories.append(fallback_section)

    return tuple(categories)
