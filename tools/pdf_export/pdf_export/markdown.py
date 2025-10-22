"""组合 Markdown 内容、生成目录与封面等辅助函数集合。"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from pathlib import Path

from .paths import PROJECT_ROOT, README_PATH

# Markdown 中指向词条的常见链接格式：
# - 行内链接 [描述](entries/词条.md) 或 [描述](词条.md)
# - 引用式链接 [ref]: entries/词条.md 或 [ref]: 词条.md
# - 角括号自动链接 <entries/词条.md> 或 <词条.md>
#
# PDF 导出时会将所有词条合并为单一文档，因此需要将这些链接
# 统一重写为指向合并文档内部锚点的形式。正则表达式仅捕获链接
# 的前缀/目标/后缀部分，便于在替换时保留原有排版细节。
#
# 支持两种格式：
# 1. 旧格式：entries/xxx.md 或 ./entries/xxx.md 或 ../entries/xxx.md
# 2. 新格式：xxx.md（相对路径，假定在 docs/entries/ 目录下）
ENTRY_INLINE_LINK_PATTERN = re.compile(
    r"(?P<prefix>\[[^\]]+\]\()(?P<target>(?:(?:\./|\.\./|)entries/)?[^)#\s/]+?\.md)"
    r"(?P<fragment>#[^)\s]*)?(?P<suffix>\))"
)

ENTRY_REFERENCE_LINK_PATTERN = re.compile(
    r"(?P<prefix>^\s*\[[^\]]+\]:\s*)(?P<target>(?:(?:\./|\.\./|)entries/)?[^#\s/]+?\.md)"
    r"(?P<fragment>#[^\s]*)?(?P<suffix>\s*$)",
    re.MULTILINE,
)

ENTRY_ANGLE_LINK_PATTERN = re.compile(
    r"(?P<prefix><)(?P<target>(?:(?:\./|\.\./|)entries/)?[^>#\s/]+?\.md)"
    r"(?P<fragment>#[^>\s]*)?(?P<suffix>>)",
)

from .last_updated import LastUpdatedInfo, render_last_updated_text
from .models import CategoryStructure, EntryDocument

# MkDocs Material Admonitions 匹配模式
# 格式: !!! type "title" 或 ??? type "title" 或 ???+ type "title"
#           content (缩进4空格)
# 支持：
#   - !!! = 不可折叠的 admonition
#   - ??? = 默认折叠的 admonition
#   - ???+ = 默认展开的可折叠 admonition
ADMONITION_PATTERN = re.compile(
    r'^(?P<marker>!!!|\?\?\?\+?) +(?P<type>\w+)(?: +"(?P<title>[^"]+)")?\s*$',
    re.MULTILINE
)

# Admonitions 类型到 LaTeX 样式的映射
ADMONITION_STYLES = {
    "note": ("备注", "gray"),
    "abstract": ("摘要", "gray"),
    "info": ("信息", "blue"),
    "tip": ("提示", "green"),
    "success": ("成功", "green"),
    "question": ("问题", "yellow"),
    "warning": ("警告", "orange"),
    "failure": ("失败", "red"),
    "danger": ("危险", "red"),
    "bug": ("错误", "red"),
    "example": ("示例", "purple"),
    "quote": ("引用", "gray"),
}


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
    """根据 ``target`` 查找对应的合并文档锚点。

    支持两种格式：
    1. 包含 entries/ 的路径：entries/xxx.md, ./entries/xxx.md, ../entries/xxx.md
    2. 相对路径：xxx.md（假定在 docs/entries/ 目录下）
    """

    stripped = target.strip()
    if not stripped:
        return None

    candidates: list[Path] = []

    # 检查是否包含 "entries/"
    index = stripped.find("entries/")
    if index != -1:
        # 旧格式：entries/xxx.md 或其相对写法
        relative_target = Path(stripped[index:])
        candidates.append(relative_target)
        # 兼容 MkDocs 新目录结构下的 docs/entries/ 位置
        if relative_target.parts and relative_target.parts[0] != "docs":
            candidates.append(Path("docs") / relative_target)
    else:
        # 新格式：纯文件名，假定位于 docs/entries/ 下
        if not stripped.endswith(".md"):
            return None
        # 避免匹配路径中包含 / 的情况（例如 foo/bar.md）
        if "/" in stripped or "\\" in stripped:
            return None
        candidates.append(Path("docs/entries") / stripped)
        # 为向后兼容保留 entries/xxx.md 形式
        candidates.append(Path("entries") / stripped)

    for candidate in candidates:
        if candidate.is_absolute():
            continue
        try:
            resolved = (PROJECT_ROOT / candidate).resolve()
        except OSError:
            continue

        anchor = lookup.get(resolved)
        if anchor:
            return f"#{anchor}"

    return None


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


def convert_html_br_tags(markdown: str) -> str:
    """将 HTML 换行标签 <br>, <br/>, <br /> 转换为 Markdown 双空格换行或 LaTeX \\\\。

    在表格中使用双反斜杠 \\\\，在其他地方使用双空格 + 换行，并保留原始行的缩进。
    这确保了缩进块（如 admonitions、列表项）中的 <br> 标签转换后不会破坏块结构。
    """
    # 匹配 <br>、<br/>、<br /> 等各种形式
    br_pattern = re.compile(r'<br\s*/?\s*>', re.IGNORECASE)

    # 在表格行中（以 | 开始的行），将 <br> 替换为 \\
    lines = markdown.splitlines()
    result = []

    for line in lines:
        # 检查是否是表格行（包含 | 字符）
        if '|' in line and not line.strip().startswith('#'):
            # 在表格中使用双反斜杠
            result.append(br_pattern.sub(r'\\\\', line))
        else:
            # 在其他地方使用双空格 + 换行，并保留原始缩进
            # 提取行首缩进
            leading_spaces = len(line) - len(line.lstrip())
            indent = line[:leading_spaces]

            # 检查是否是列表项（- , * , 或数字.）
            stripped = line.lstrip()
            list_match = re.match(r'^([*\-+]|\d+\.)\s+', stripped)
            if list_match:
                # 列表项：续行需要额外缩进以对齐列表内容
                # 计算列表标记的长度（例如 "- " 是 2，"1. " 是 3）
                list_marker_len = len(list_match.group(0))
                # 续行缩进 = 原始缩进 + 列表标记长度
                continuation_indent = indent + ' ' * list_marker_len
                converted = br_pattern.sub(f'  \n{continuation_indent}', line)
            else:
                # 普通行或已缩进的块：使用相同缩进
                converted = br_pattern.sub(f'  \n{indent}', line)

            result.append(converted)

    return '\n'.join(result)


def convert_admonitions_to_latex(markdown: str) -> str:
    """将 MkDocs Material admonitions 转换为 LaTeX 格式的框。

    MkDocs 格式:
        !!! warning "标题"
            内容行1
            内容行2

    转换为 Pandoc/LaTeX 兼容的块引用格式:
        > **⚠️ 警告: 标题**
        >
        > 内容行1
        > 内容行2

    支持嵌套在列表中的 admonition（带有额外缩进）。
    """
    lines = markdown.splitlines()
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        match = ADMONITION_PATTERN.match(line)

        if match:
            admon_type = match.group("type").lower()
            title = match.group("title") or ""

            # 检测 admonition 行的前导空格（用于处理嵌套）
            leading_spaces = len(line) - len(line.lstrip())

            # 获取类型对应的中文名称和图标
            type_name, _ = ADMONITION_STYLES.get(admon_type, (admon_type.capitalize(), "gray"))

            # 图标映射
            icon_map = {
                "warning": "⚠️",
                "danger": "🚫",
                "info": "ℹ️",
                "tip": "💡",
                "note": "📝",
                "success": "✅",
                "failure": "❌",
                "bug": "🐛",
                "example": "📋",
                "question": "❓",
                "quote": "💬",
                "abstract": "📄",
            }
            icon = icon_map.get(admon_type, "📌")

            # 构建标题行（保留原有缩进）
            indent = " " * leading_spaces
            if title:
                header = f"{indent}> **{icon} {type_name}: {title}**"
            else:
                header = f"{indent}> **{icon} {type_name}**"

            result.append(header)
            result.append(f"{indent}>")

            # 收集缩进内容（至少需要 leading_spaces + 4 个空格）
            min_indent = leading_spaces + 4
            i += 1
            while i < len(lines):
                content_line = lines[i]

                # 检查是否是 admonition 内容（缩进行）或空行
                if len(content_line) >= min_indent and content_line[:min_indent] == " " * min_indent:
                    # 移除基础缩进（leading_spaces + 4），保留额外缩进，添加引用标记
                    result.append(f"{indent}> {content_line[min_indent:]}")
                    i += 1
                elif not content_line.strip():
                    # 空行，可能是 admonition 内部的段落分隔
                    # 先检查下一行是否还是缩进内容
                    if i + 1 < len(lines) and len(lines[i + 1]) >= min_indent and lines[i + 1][:min_indent] == " " * min_indent:
                        result.append(f"{indent}>")
                        i += 1
                    else:
                        # admonition 结束
                        break
                else:
                    # 非缩进行，admonition 结束
                    break

            # 添加空行分隔
            result.append("")
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


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


def build_directory_page(
    structure: CategoryStructure, anchor_lookup: Mapping[Path, str]
) -> str:
    """根据 ``structure`` 生成带页码的目录页。"""

    lines: list[str] = ["# 目录", ""]
    lines.extend(
        [
            r"\begingroup",
            r"\setlength{\parindent}{0pt}",
            r"\setlength{\parskip}{0.4em}",
            "",
        ]
    )

    for category_title, documents in structure:
        if not documents:
            continue

        lines.append(rf"\textbf{{{escape_latex(category_title)}}}\par")
        lines.append(r"\vspace{0.2em}")

        for document in documents:
            anchor = anchor_lookup.get(
                document.path.resolve(),
                build_entry_anchor(document.path),
            )
            entry_title = escape_latex(document.title)
            lines.append(
                rf"\noindent\hspace{{1em}}\textbullet\hspace{{0.6em}}"
                rf"\hyperref[{anchor}]{{{entry_title}}}"
                rf"\nobreak\dotfill\pageref{{{anchor}}}\par"
            )

        lines.append(r"\medskip")

    lines.extend([r"\endgroup", "", r"\newpage", ""])
    return "\n".join(lines)


def build_combined_markdown(
    preface_doc: EntryDocument | None,
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
    """将所有 Markdown 文件拼接为单一字符串供 Pandoc 使用。

    顺序: 封面 -> 目录 -> 前言 -> README -> 内容章节
    """

    parts: list[str] = []
    anchor_lookup = _build_anchor_lookup(structure)

    # 1. 封面页 (LaTeX titlepage)
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

    # 2. 目录页
    if structure:
        parts.append(build_directory_page(structure, anchor_lookup))

    # 3. 前言（独立章节，不在目录中列出）
    if preface_doc:
        # 为前言生成锚点
        preface_anchor = build_entry_anchor(preface_doc.path)
        relative = preface_doc.path.relative_to(PROJECT_ROOT)
        rewritten = rewrite_entry_links(preface_doc.body, anchor_lookup)
        # 转换 HTML 换行标签
        br_converted = convert_html_br_tags(rewritten)
        # 转换 admonitions
        converted = convert_admonitions_to_latex(br_converted)
        body = strip_primary_heading(converted, preface_doc.title)
        shifted = shift_heading_levels(body, offset=1).strip()

        parts.append(f"# {preface_doc.title} {{#{preface_anchor}}}\n\n")
        if last_updated_map:
            repo_path = relative.as_posix()
            last_updated_text = render_last_updated_text(repo_path, last_updated_map)
            if last_updated_text:
                parts.append(f"{last_updated_text}\n\n")
        if shifted:
            parts.append(shifted)
            parts.append("\n\n")
        parts.append(f"<!-- 来源: {relative.as_posix()} -->\n\n")
        parts.append("\\newpage\n\n")

    # 4. README
    if include_readme and README_PATH.exists():
        readme_content = README_PATH.read_text(encoding="utf-8").strip()
        # 转换 HTML 换行标签
        readme_br_converted = convert_html_br_tags(readme_content)
        # 转换 admonitions
        readme_converted = convert_admonitions_to_latex(readme_br_converted)
        parts.append(readme_converted)
        parts.append("\n\n\\newpage\n")

    # 5. 内容章节
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
            # 转换 HTML 换行标签
            br_converted = convert_html_br_tags(rewritten)
            # 转换 admonitions
            converted = convert_admonitions_to_latex(br_converted)
            body = strip_primary_heading(converted, entry_title)
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
