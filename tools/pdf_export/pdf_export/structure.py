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


def _load_entry_list(entry_list_path: Path | None) -> tuple[list[str], bool] | None:
    """加载词条白名单文件，返回有序词条列表。

    白名单文件格式支持两种模式：

    1. 简单模式（仅列出词条，保持顺序）：
       ```
       Alter.md
       DID.md
       Switch.md
       Front-Fronting.md
       ```
       词条按文件顺序排列，导出时仍按 topic 分组，但组内保持白名单顺序

    2. 自定义分组模式（使用 ## 分隔不同的 topic 组）：
       ```
       ## 解离性障碍
       Alter.md
       DID.md
       OSDD.md

       ## 系统运作
       Switch.md
       Front-Fronting.md
       Co-Fronting.md
       ```
       每个 ## 标题对应一个 topic 分组，词条按组内顺序排列

    每行可以是:
    - topic 分组标记（以 `##` 开头，用于自定义分组）
    - 词条文件名（如 'Alter.md'）
    - 词条标题（如 '人格（Alter）'）
    - 注释（以 `#` 开头，但不是 `##`）
    - 空行（忽略）

    返回值:
        tuple[list[str], bool] | None:
        - 第一个元素：有序词条列表（文件名或标题）
        - 第二个元素：是否使用了自定义分组模式（True=有 ##，False=简单模式）
        如果文件不存在则返回 None
    """
    if entry_list_path is None or not entry_list_path.exists():
        return None

    try:
        content = entry_list_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"警告: 无法读取词条列表文件 {entry_list_path}: {error}", file=sys.stderr)
        return None

    entries: list[str] = []
    has_custom_groups = False

    for line in content.splitlines():
        stripped = line.strip()

        # 跳过空行
        if not stripped:
            continue

        # 检查是否为分组标记（## 开头）
        if stripped.startswith('##'):
            has_custom_groups = True
            # 分组标记本身也作为特殊标记加入列表
            entries.append(stripped)
            continue

        # 跳过注释（# 开头但不是 ##）
        if stripped.startswith('#'):
            continue

        # 添加词条
        entries.append(stripped)

    if not entries:
        return None

    return (entries, has_custom_groups)


def _filter_documents(
    documents: OrderedDict[Path, EntryDocument],
    include_tags: set[str] | None = None,
    exclude_tags: set[str] | None = None,
    entry_list: set[str] | None = None,
) -> OrderedDict[Path, EntryDocument]:
    """根据标签和白名单过滤文档。

    过滤规则:
    1. 如果提供了 entry_list，只保留在白名单中的词条（按文件名或标题匹配）
    2. 如果提供了 include_tags，只保留至少包含一个指定标签的词条
    3. 如果提供了 exclude_tags，排除包含任何排除标签的词条

    注意：此函数仅负责过滤，不负责排序。
    排序由 _build_sections_from_whitelist 或 _build_sections_by_topic 处理。
    """
    filtered: OrderedDict[Path, EntryDocument] = OrderedDict()

    for path, doc in documents.items():
        # 白名单过滤
        if entry_list is not None:
            # 检查文件名或标题是否在白名单中
            if doc.path.name not in entry_list and doc.title not in entry_list:
                continue

        # 标签过滤
        doc_tags = set(doc.tags)

        # 排除标签过滤（优先级高）
        if exclude_tags and doc_tags & exclude_tags:
            continue

        # 包含标签过滤
        if include_tags and not (doc_tags & include_tags):
            continue

        filtered[path] = doc

    return filtered


def _build_sections_from_whitelist(
    documents: OrderedDict[Path, EntryDocument],
    whitelist_entries: list[str],
    has_custom_groups: bool,
) -> list[tuple[str, tuple[EntryDocument, ...]]]:
    """根据白名单顺序构建章节。

    参数:
        documents: 已过滤的文档字典
        whitelist_entries: 白名单词条列表（保持顺序，可能包含 ## 分组标记）
        has_custom_groups: 是否使用了自定义分组模式

    返回值:
        章节列表，每个章节是 (章节标题, 词条元组) 元组
    """
    # 构建文件名和标题到文档的映射
    name_to_doc: dict[str, EntryDocument] = {}
    title_to_doc: dict[str, EntryDocument] = {}

    for doc in documents.values():
        name_to_doc[doc.path.name] = doc
        title_to_doc[doc.title] = doc

    if has_custom_groups:
        # 自定义分组模式：按 ## 标记分组
        sections: list[tuple[str, list[EntryDocument]]] = []
        current_group_title: str | None = None
        current_group_docs: list[EntryDocument] = []

        for entry in whitelist_entries:
            if entry.startswith('##'):
                # 保存之前的分组
                if current_group_docs:
                    sections.append((current_group_title or OTHER_CATEGORY_TITLE, current_group_docs))
                    current_group_docs = []
                # 开始新分组
                current_group_title = entry[2:].strip()
                continue

            # 查找词条
            doc = name_to_doc.get(entry) or title_to_doc.get(entry)
            if doc is not None:
                current_group_docs.append(doc)
            else:
                print(f"警告: 白名单中的词条 '{entry}' 未找到或已被过滤", file=sys.stderr)

        # 添加最后一个分组
        if current_group_docs:
            sections.append((current_group_title or OTHER_CATEGORY_TITLE, current_group_docs))

        return [(title, tuple(docs)) for title, docs in sections if docs]

    else:
        # 简单模式：按 topic 分组，但保持白名单顺序
        # 先按白名单顺序收集所有文档
        ordered_docs: list[EntryDocument] = []
        for entry in whitelist_entries:
            doc = name_to_doc.get(entry) or title_to_doc.get(entry)
            if doc is not None:
                ordered_docs.append(doc)
            else:
                print(f"警告: 白名单中的词条 '{entry}' 未找到或已被过滤", file=sys.stderr)

        # 按 topic 分组，但每个组内保持白名单顺序
        topic_to_docs: dict[str, list[EntryDocument]] = defaultdict(list)
        for doc in ordered_docs:
            topic = doc.topic if doc.topic and doc.topic.strip() else OTHER_CATEGORY_TITLE
            topic_to_docs[topic].append(doc)

        # 构建章节（保持 topic 在白名单中第一次出现的顺序）
        seen_topics: set[str] = set()
        sections: list[tuple[str, tuple[EntryDocument, ...]]] = []

        for doc in ordered_docs:
            topic = doc.topic if doc.topic and doc.topic.strip() else OTHER_CATEGORY_TITLE
            if topic not in seen_topics:
                seen_topics.add(topic)
                sections.append((topic, tuple(topic_to_docs[topic])))

        return sections


def collect_markdown_structure(
    ignore: IgnoreRules,
    include_tags: set[str] | None = None,
    exclude_tags: set[str] | None = None,
    entry_list_path: Path | None = None,
) -> tuple[EntryDocument | None, CategoryStructure]:
    """依据词条的 topic 字段或白名单顺序构建 PDF 导出结构。

    支持两种模式：
    1. 标签过滤模式：根据 topic 字段自动分组
    2. 白名单模式：按白名单文件顺序排列，支持自定义分组

    参数:
        ignore: 忽略规则
        include_tags: 只包含具有这些标签的词条（至少匹配一个）
        exclude_tags: 排除具有这些标签的词条（匹配任一标签则排除）
        entry_list_path: 词条白名单文件路径

    返回值:
        tuple[EntryDocument | None, CategoryStructure]: (前言文档, 分类结构)
        前言文档独立于分类结构，会在封面和目录之后单独插入
    """

    documents = _load_entry_documents(ignore)

    # 加载词条白名单
    whitelist_result = _load_entry_list(entry_list_path)

    # 提取白名单词条集合（用于过滤）
    entry_list_set: set[str] | None = None
    whitelist_entries: list[str] | None = None
    has_custom_groups = False

    if whitelist_result is not None:
        whitelist_entries, has_custom_groups = whitelist_result
        entry_list_set = set(whitelist_entries) - {e for e in whitelist_entries if e.startswith('##')}

    # 应用过滤规则
    if include_tags is not None or exclude_tags is not None or entry_list_set is not None:
        documents = _filter_documents(documents, include_tags, exclude_tags, entry_list_set)

        if sys.stdout.isatty():
            filter_info = []
            if entry_list_set:
                filter_info.append(f"白名单: {len(entry_list_set)} 个词条")
            if include_tags:
                filter_info.append(f"包含标签: {', '.join(sorted(include_tags))}")
            if exclude_tags:
                filter_info.append(f"排除标签: {', '.join(sorted(exclude_tags))}")
            print(f"   应用过滤规则: {' | '.join(filter_info)}")
            print(f"   过滤后剩余: {len(documents)} 个词条")

    categories: list[tuple[str, tuple[EntryDocument, ...]]] = []

    # 加载前言文档（独立于章节结构）
    preface_doc = _load_preface_document(ignore)

    # 根据是否使用白名单选择构建方式
    if whitelist_entries is not None:
        # 白名单模式：按白名单顺序构建
        if sys.stdout.isatty():
            mode = "自定义分组" if has_custom_groups else "保持顺序并按 topic 分组"
            print(f"   使用白名单模式: {mode}")
        categories = _build_sections_from_whitelist(documents, whitelist_entries, has_custom_groups)
    else:
        # 标签过滤模式：按 topic 构建章节（包含"其他"分类）
        topic_sections = _build_sections_by_topic(documents.values())
        categories.extend(topic_sections)

    return (preface_doc, tuple(categories))
