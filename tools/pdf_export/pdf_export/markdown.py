"""组合 Markdown 内容、生成目录与封面等辅助函数集合。"""

from __future__ import annotations

import hashlib
import html
import re
import sys
from collections.abc import Mapping
from pathlib import Path

from .paths import PROJECT_ROOT, README_PATH

# Markdown 中指向词条的常见链接格式：
# - 行内链接 [描述](entries/词条.md)
# - 引用式链接 [ref]: entries/词条.md
# - 角括号自动链接 <entries/词条.md>
#
# PDF 导出时会将所有词条合并为单一文档，因此需要将这些链接
# 统一重写为指向合并文档内部锚点的形式。正则表达式仅捕获链接
# 的前缀/目标/后缀部分，便于在替换时保留原有排版细节。
ENTRY_INLINE_LINK_PATTERN = re.compile(
    r"(?P<prefix>\[[^\]]+\]\()(?P<target>(?:\./|\.\./|)entries/[^)#\s]+?\.md)"
    r"(?P<fragment>#[^)\s]*)?(?P<suffix>\))"
)

ENTRY_REFERENCE_LINK_PATTERN = re.compile(
    r"(?P<prefix>^\s*\[[^\]]+\]:\s*)(?P<target>(?:\./|\.\./|)entries/[^#\s]+?\.md)"
    r"(?P<fragment>#[^\s]*)?(?P<suffix>\s*$)",
    re.MULTILINE,
)

ENTRY_ANGLE_LINK_PATTERN = re.compile(
    r"(?P<prefix><)(?P<target>(?:\./|\.\./|)entries/[^>#\s]+?\.md)"
    r"(?P<fragment>#[^>\s]*)?(?P<suffix>>)",
)

_TRIGGER_WARNING_BLOCK_PATTERN = re.compile(
    r"<!--\s*trigger-warning:start\s*-->(?P<body>.*?)<!--\s*trigger-warning:end\s*-->",
    re.IGNORECASE | re.DOTALL,
)

from .last_updated import LastUpdatedInfo, render_last_updated_text
from .models import CategoryStructure, EntryDocument


LATEX_SPECIAL_CHARS = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "_": r"\_",
    "%": r"\%",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    """对 ``text`` 中的 LaTeX 特殊字符做转义。"""

    return "".join(LATEX_SPECIAL_CHARS.get(ch, ch) for ch in text)


def infer_entry_title(path: Path) -> str:
    """尽力从条目文件推断展示标题，失败时回退到文件名。"""

    heading_pattern = re.compile(r"^#{1,6}\s+(?P<title>.+?)\s*$")
    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            match = heading_pattern.match(raw_line.strip())
            if match:
                return match.group("title").strip()
    except OSError:
        pass

    return path.stem


def shift_heading_levels(markdown: str, offset: int) -> str:
    """将所有标题级别整体上移 ``offset``，同时保留 Pandoc 代码块。"""

    if offset == 0:
        return markdown

    pattern = re.compile(r"^(#{1,6})(\s+)(.*)$", re.MULTILINE)

    def _replace(match: re.Match[str]) -> str:
        hashes, spacing, title = match.groups()
        new_level = min(6, len(hashes) + offset)
        return f"{'#' * new_level}{spacing}{title}"

    return pattern.sub(_replace, markdown)


def build_entry_anchor(path: Path) -> str:
    """基于路径生成稳定锚点，确保合并文档中的引用可重复。"""

    relative = path.relative_to(PROJECT_ROOT)
    digest = hashlib.sha1(relative.as_posix().encode("utf-8")).hexdigest()[:10]
    return f"entry-{digest}"


def _build_anchor_lookup(structure: CategoryStructure) -> dict[Path, str]:
    """为所有导出条目生成“绝对路径 → 锚点”映射。"""

    lookup: dict[Path, str] = {}
    for _, documents in structure:
        for document in documents:
            lookup[document.path.resolve()] = build_entry_anchor(document.path)
    return lookup


def _resolve_entry_target(target: str, lookup: Mapping[Path, str]) -> str | None:
    """根据 ``target`` 查找对应的合并文档锚点。"""

    stripped = target.strip()
    if not stripped:
        return None
    index = stripped.find("entries/")
    if index == -1:
        return None

    candidate = Path(stripped[index:])
    if candidate.is_absolute():
        return None

    try:
        resolved = (PROJECT_ROOT / candidate).resolve()
    except OSError:
        return None

    anchor = lookup.get(resolved)
    if not anchor:
        return None

    return f"#{anchor}"


def rewrite_entry_links(markdown: str, lookup: Mapping[Path, str]) -> str:
    """将 Markdown 中的词条链接重写为 PDF 内部锚点。"""

    def _replace(match: re.Match[str]) -> str:
        target = match.group("target")
        resolved = _resolve_entry_target(target, lookup)
        if not resolved:
            return match.group(0)
        # PDF 合并后仅能跳转到词条起始位置，忽略原有局部锚点。
        return f"{match.group('prefix')}{resolved}{match.group('suffix')}"

    updated = ENTRY_INLINE_LINK_PATTERN.sub(_replace, markdown)
    updated = ENTRY_REFERENCE_LINK_PATTERN.sub(_replace, updated)
    updated = ENTRY_ANGLE_LINK_PATTERN.sub(_replace, updated)
    return updated


def _strip_html_tags(content: str) -> str:
    """移除 ``content`` 中的 HTML 标签并压缩空白字符。"""

    without_tags = re.sub(r"<[^>]+>", " ", content)
    condensed = re.sub(r"\s+", " ", without_tags)
    return html.unescape(condensed).strip()


def _normalize_index_content(content: str) -> str:
    """将 ``index.md`` 中的自定义 HTML 区块替换为通用 Markdown。"""

    def _replace_trigger_warning(match: re.Match[str]) -> str:
        plain_text = _strip_html_tags(match.group("body"))
        if not plain_text:
            return ""
        return f"> ⚠️ {plain_text}\n\n"

    return _TRIGGER_WARNING_BLOCK_PATTERN.sub(_replace_trigger_warning, content)


def strip_primary_heading(content: str, title: str) -> str:
    """移除与 ``title`` 相同的首个标题，避免重复标题干扰。"""

    heading_re = re.compile(rf"^#{{1,6}}\s+{re.escape(title)}\s*$")
    lines = content.splitlines()
    stripped: list[str] = []
    removed = False

    index = 0
    while index < len(lines):
        current = lines[index]
        if not removed and heading_re.match(current.strip()):
            removed = True
            index += 1
            if index < len(lines) and not lines[index].strip():
                index += 1
            continue
        stripped.append(current)
        index += 1

    return "\n".join(stripped)


def build_cover_page(
    title: str,
    subtitle: str | None,
    date_text: str | None,
    footer_text: str | None,
    online_link_label: str | None,
    online_link_url: str | None,
) -> str:
    """使用 LaTeX ``titlepage`` 环境构建封面页。"""

    def _format_line(size_command: str, text: str, *, italic: bool = False) -> str:
        """以指定字号指令渲染 ``text``，同时完成转义。"""

        escaped = escape_latex(text.strip())
        content = f"\\textit{{{escaped}}}" if italic else escaped
        return f"{{{size_command} {content}\\par}}"

    def _format_link_line(size_command: str, label: str, url: str) -> str:
        """构建带超链接的字号行。"""

        label_escaped = escape_latex(label.strip())
        url_escaped = escape_latex(url.strip())
        return f"{{{size_command} \\href{{{url_escaped}}}{{{label_escaped}}}\\par}}"

    lines = [
        "\\begin{titlepage}",
        "\\centering",
        "\\vspace*{3cm}",
        _format_line("\\Huge", title),
    ]

    if subtitle:
        lines.extend([
            "\\vspace{1.5cm}",
            _format_line("\\Large", subtitle),
        ])

    if online_link_label and online_link_url:
        lines.extend([
            "\\vspace{1.2cm}",
            _format_link_line("\\Large", online_link_label, online_link_url),
        ])

    bottom_inserted = False

    if date_text:
        lines.extend([
            "\\vfill",
            _format_line("\\large", date_text),
        ])
        bottom_inserted = True

    if footer_text:
        if bottom_inserted:
            lines.append("\\vspace{0.8cm}")
        else:
            lines.append("\\vfill")
        lines.append(_format_line("\\Large", footer_text, italic=True))

    lines.extend([
        "\\vspace{1cm}",
        "\\end{titlepage}",
        "",
        "\\newpage",
        "",
    ])

    return "\n".join(lines)


def _build_directory_from_index(anchor_lookup: Mapping[Path, str]) -> str | None:
    """尝试以仓库根目录的 ``index.md`` 作为目录页内容。"""

    index_path = PROJECT_ROOT / "index.md"
    if not index_path.exists():
        return None

    try:
        raw_content = index_path.read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - 仅在 I/O 出错时触发
        print(f"警告: 无法读取 {index_path}: {error}", file=sys.stderr)
        return None

    normalized = _normalize_index_content(raw_content)
    stripped = normalized.strip()
    if not stripped:
        return None

    lines = stripped.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines[index] = "# 目录"
            break
    else:
        lines.insert(0, "# 目录")
        lines.insert(1, "")

    directory_markdown = "\n".join(lines)
    rewritten = rewrite_entry_links(directory_markdown, anchor_lookup).strip()
    if not rewritten:
        return None

    return f"{rewritten}\n\n\\newpage\n"


def build_directory_page(
    structure: CategoryStructure, anchor_lookup: Mapping[Path, str]
) -> str:
    """根据 ``index.md`` 或标签结构生成目录页内容。"""

    index_based = _build_directory_from_index(anchor_lookup)
    if index_based is not None:
        return index_based

    lines: list[str] = ["# 目录", ""]

    for category_title, documents in structure:
        if not documents:
            continue
        lines.append(f"## {category_title}")
        lines.append("")
        for document in documents:
            anchor = anchor_lookup.get(
                document.path.resolve(),
                build_entry_anchor(document.path),
            )
            lines.append(f"- [{document.title}](#{anchor})")
        lines.append("")

    lines.extend(["\\newpage", ""])
    return "\n".join(lines)


def build_combined_markdown(
    structure: CategoryStructure,
    include_readme: bool,
    include_cover: bool,
    cover_title: str,
    cover_subtitle: str | None,
    cover_date: str | None,
    cover_footer: str | None,
    cover_online_link_label: str | None,
    cover_online_link_url: str | None,
    last_updated_map: Mapping[str, LastUpdatedInfo] | None = None,
) -> str:
    """将所有 Markdown 文件拼接为单一字符串供 Pandoc 使用。"""

    parts: list[str] = []
    anchor_lookup = _build_anchor_lookup(structure)

    if include_cover:
        parts.append(
            build_cover_page(
                title=cover_title,
                subtitle=cover_subtitle,
                date_text=cover_date,
                footer_text=cover_footer,
                online_link_label=cover_online_link_label,
                online_link_url=cover_online_link_url,
            )
        )

    if structure:
        parts.append(build_directory_page(structure, anchor_lookup))

    if include_readme and README_PATH.exists():
        parts.append(README_PATH.read_text(encoding="utf-8").strip())
        parts.append("\n\n\\newpage\n")

    first_category = True
    for category_title, documents in structure:
        if not documents:
            continue

        if not first_category:
            parts.append("\n\\newpage\n")
        first_category = False

        parts.append(f"# {category_title}\n\n")

        for index, document in enumerate(documents):
            if index > 0:
                parts.append("\n\\newpage\n")

            entry_title = document.title
            anchor = anchor_lookup.get(
                document.path.resolve(),
                build_entry_anchor(document.path),
            )
            relative = document.path.relative_to(PROJECT_ROOT)
            rewritten = rewrite_entry_links(document.body, anchor_lookup)
            body = strip_primary_heading(rewritten, entry_title)
            shifted = shift_heading_levels(body, offset=2).strip()

            parts.append(f"## {entry_title} {{#{anchor}}}\n\n")
            if last_updated_map:
                repo_path = relative.as_posix()
                last_updated_text = render_last_updated_text(repo_path, last_updated_map)
                if last_updated_text:
                    parts.append(f"{last_updated_text}\n\n")
            if shifted:
                parts.append(shifted)
                parts.append("\n\n")
            parts.append(f"<!-- 来源: {relative.as_posix()} -->\n\n")

    combined = "".join(parts).strip()
    if not combined.endswith("\n"):
        combined += "\n"
    return combined
