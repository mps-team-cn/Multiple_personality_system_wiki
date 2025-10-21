"""整理仓库内的 Markdown 文件并生成导出顺序。"""

from __future__ import annotations

import re
import sys
from collections import OrderedDict, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

from .frontmatter import FrontmatterError, load_entry_document
from .markdown import infer_entry_title
from .models import CategoryStructure, EntryDocument, IgnoreRules
from .paths import ENTRIES_DIR, PROJECT_ROOT, PREFACE_PATH, INDEX_PATH, DOCS_DIR


# "其他"分类的标题
OTHER_CATEGORY_TITLE = "其他"


def _load_preface_document(ignore: IgnoreRules) -> EntryDocument | None:
    """若存在《前言》，加载为独立文档(不作为章节)。"""

    if not PREFACE_PATH.exists() or ignore.matches(PREFACE_PATH):
        return None
    preface_path = PREFACE_PATH

    try:
        raw_content = preface_path.read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - 仅在 I/O 出错时触发
        print(f"警告: 无法读取 {preface_path}: {error}", file=sys.stderr)
        return None

    # 移除 frontmatter（如果存在）
    lines = raw_content.splitlines()
    body_start = 0

    if lines and lines[0].strip() == "---":
        # 找到第二个 ---
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break

    # 提取正文（去除 frontmatter）
    body_lines = lines[body_start:]
    body = "\n".join(body_lines).lstrip("\n")

    return EntryDocument(
        path=preface_path.resolve(),
        title=infer_entry_title(preface_path),
        tags=(),
        topic="",
        body=body,
    )


def _load_single_entry(path: Path) -> EntryDocument | tuple[Path, Exception]:
    """加载单个词条文件，返回 EntryDocument 或错误信息。"""
    try:
        return load_entry_document(path)
    except FrontmatterError as error:
        return (path, error)
    except OSError as error:
        return (path, error)


def _load_single_guide(path: Path) -> EntryDocument | None:
    """加载单个导览页面，返回 EntryDocument 或 None（失败时）。"""
    try:
        return load_entry_document(path)
    except FrontmatterError:
        # 导览页面可能没有 frontmatter，使用简化处理
        try:
            content = path.read_text(encoding="utf-8")
            return EntryDocument(
                path=path.resolve(),
                title=infer_entry_title(path),
                tags=(),
                topic="",
                body=content,
            )
        except OSError as error:
            print(f"警告: 无法读取 {path}: {error}", file=sys.stderr)
            return None


def _load_entry_documents(ignore: IgnoreRules) -> OrderedDict[Path, EntryDocument]:
    """读取 entries 目录中的词条和 docs 目录中的导览页面，并保留原始文件名顺序。

    使用并行 I/O 加速大量文件的读取过程。
    """

    documents: OrderedDict[Path, EntryDocument] = OrderedDict()

    # 加载词条目录中的文件（并行化）
    if ENTRIES_DIR.exists():
        entry_paths = [
            path for path in sorted(ENTRIES_DIR.glob("*.md"))
            if not ignore.matches(path)
        ]

        # 使用线程池并行读取文件（I/O 密集型任务适合多线程）
        # 最多使用 8 个线程，避免过多线程导致资源竞争
        max_workers = min(8, len(entry_paths)) if entry_paths else 1

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务并保持路径顺序
            future_to_path = {
                executor.submit(_load_single_entry, path): path
                for path in entry_paths
            }

            # 按提交顺序收集结果
            for path in entry_paths:
                future = next(f for f, p in future_to_path.items() if p == path)
                result = future.result()

                if isinstance(result, EntryDocument):
                    documents[result.path] = result
                elif isinstance(result, tuple):
                    # 错误情况
                    error_path, error = result
                    raise SystemExit(f"解析 {error_path} 的 frontmatter 失败：{error}") from error

    # 加载 docs 目录中的导览页面（排除 index.md 和 Preface.md）
    if DOCS_DIR.exists():
        guide_patterns = [
            "*-Guide.md",  # 所有以 -Guide.md 结尾的文件
            "*-Operations-Guide.md",  # System-Operations-Guide.md 等
            "DSM-ICD-*.md",  # DSM-ICD-Diagnosis-Index.md 等
            "Glossary.md",  # 术语表
        ]

        guide_paths = []
        for pattern in guide_patterns:
            for path in sorted(DOCS_DIR.glob(pattern)):
                if ignore.matches(path):
                    continue
                if path.name in ("index.md", "Preface.md"):
                    continue
                guide_paths.append(path)

        # 并行加载导览页面
        if guide_paths:
            max_workers = min(8, len(guide_paths))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_path = {
                    executor.submit(_load_single_guide, path): path
                    for path in guide_paths
                }

                for path in guide_paths:
                    future = next(f for f, p in future_to_path.items() if p == path)
                    document = future.result()
                    if document is not None:
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

    if not INDEX_PATH.exists():
        return ([], set())
    index_path = INDEX_PATH

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


def _build_sections_by_topic(
    documents: Iterable[EntryDocument],
) -> list[tuple[str, tuple[EntryDocument, ...]]]:
    """根据词条的 topic 字段分组生成章节。

    每个词条按其 topic 字段归入对应章节。
    topic 为空的词条会被归入"其他"分类。
    章节顺序按 topic 名称排序。
    """

    # 收集所有的 topic 并分组
    topic_to_documents: dict[str, list[EntryDocument]] = defaultdict(list)

    for document in documents:
        # 如果 topic 为空或不存在，归入"其他"
        if not document.topic or not document.topic.strip():
            topic_to_documents[OTHER_CATEGORY_TITLE].append(document)
        else:
            topic_to_documents[document.topic].append(document)

    sections: list[tuple[str, tuple[EntryDocument, ...]]] = []

    # 按 topic 名称排序（中文按拼音排序）
    for topic in sorted(topic_to_documents.keys()):
        # 跳过"其他"，最后添加
        if topic == OTHER_CATEGORY_TITLE:
            continue

        # 按标题排序
        sorted_docs = sorted(
            topic_to_documents[topic],
            key=lambda doc: (doc.title, doc.path.name)
        )
        sections.append((topic, tuple(sorted_docs)))

    # 最后添加"其他"分类（如果有）
    if OTHER_CATEGORY_TITLE in topic_to_documents:
        sorted_docs = sorted(
            topic_to_documents[OTHER_CATEGORY_TITLE],
            key=lambda doc: (doc.title, doc.path.name)
        )
        sections.append((OTHER_CATEGORY_TITLE, tuple(sorted_docs)))

    return sections


def _build_untagged_section(
    documents: Iterable[EntryDocument],
) -> tuple[str, tuple[EntryDocument, ...]] | None:
    """将没有 tags 的词条组成兜底章节。"""

    untagged = [doc for doc in documents if not doc.tags]

    if not untagged:
        return None

    ordered = sorted(untagged, key=lambda item: (item.title, item.path.name))
    return ("未分类词条", tuple(ordered))


def collect_markdown_structure(ignore: IgnoreRules) -> tuple[EntryDocument | None, CategoryStructure]:
    """依据词条的 topic 字段构建 PDF 导出结构。

    根据每个词条的 topic 字段自动分组，
    topic 为空的词条归入"其他"分类。

    返回值:
        tuple[EntryDocument | None, CategoryStructure]: (前言文档, 分类结构)
        前言文档独立于分类结构，会在封面和目录之后单独插入
    """

    documents = _load_entry_documents(ignore)
    categories: list[tuple[str, tuple[EntryDocument, ...]]] = []

    # 加载前言文档（独立于章节结构）
    preface_doc = _load_preface_document(ignore)

    # 按 topic 构建章节（包含"其他"分类）
    topic_sections = _build_sections_by_topic(documents.values())
    categories.extend(topic_sections)

    return (preface_doc, tuple(categories))
