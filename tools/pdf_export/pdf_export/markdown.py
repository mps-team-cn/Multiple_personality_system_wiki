"""Helpers for building the combined markdown document."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .models import CategoryStructure
from .paths import PROJECT_ROOT, README_PATH


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
    """Escape LaTeX special characters in ``text``."""

    return "".join(LATEX_SPECIAL_CHARS.get(ch, ch) for ch in text)


def infer_entry_title(path: Path) -> str:
    """Best-effort guess of an entry's display title."""

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
    """Increase heading levels by ``offset`` while keeping Pandoc fences intact."""

    if offset == 0:
        return markdown

    pattern = re.compile(r"^(#{1,6})(\s+)(.*)$", re.MULTILINE)

    def _replace(match: re.Match[str]) -> str:
        hashes, spacing, title = match.groups()
        new_level = min(6, len(hashes) + offset)
        return f"{'#' * new_level}{spacing}{title}"

    return pattern.sub(_replace, markdown)


def build_entry_anchor(path: Path) -> str:
    """Return a stable anchor identifier for ``path`` within the combined PDF."""

    relative = path.relative_to(PROJECT_ROOT)
    digest = hashlib.sha1(relative.as_posix().encode("utf-8")).hexdigest()[:10]
    return f"entry-{digest}"


def strip_primary_heading(content: str, title: str) -> str:
    """Remove the first heading that matches ``title`` from ``content``."""

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
) -> str:
    """Return a standalone cover page using LaTeX's titlepage environment."""

    def _format_line(size_command: str, text: str) -> str:
        """Render ``text`` inside a LaTeX sizing command."""

        escaped = escape_latex(text.strip())
        return f"{{{size_command} {escaped}\\par}}"

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

    if date_text:
        lines.extend([
            "\\vfill",
            _format_line("\\large", date_text),
        ])

    if footer_text:
        lines.extend([
            "\\vfill",
            f"\\textit{{{escape_latex(footer_text)}}}",
        ])

    lines.extend([
        "\\vspace{1cm}",
        "\\end{titlepage}",
        "",
        "\\newpage",
        "",
    ])

    return "\n".join(lines)


def build_directory_page(structure: CategoryStructure) -> str:
    """Construct a table-of-contents page based on README categories."""

    lines: list[str] = ["# 目录", ""]

    for category_title, paths in structure:
        lines.append(f"## {category_title}")
        lines.append("")
        for path in paths:
            entry_title = infer_entry_title(path)
            anchor = build_entry_anchor(path)
            lines.append(f"- [{entry_title}](#{anchor})")
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
) -> str:
    """Combine all markdown files into a single string."""

    parts: list[str] = []

    if include_cover:
        parts.append(
            build_cover_page(
                title=cover_title,
                subtitle=cover_subtitle,
                date_text=cover_date,
                footer_text=cover_footer,
            )
        )

    if structure:
        parts.append(build_directory_page(structure))

    if include_readme and README_PATH.exists():
        parts.append(README_PATH.read_text(encoding="utf-8").strip())
        parts.append("\n\n\\newpage\n")

    first_category = True
    for category_title, paths in structure:
        if not paths:
            continue

        if not first_category:
            parts.append("\n\\newpage\n")
        first_category = False

        parts.append(f"# {category_title}\n\n")

        for index, path in enumerate(paths):
            if index > 0:
                parts.append("\n\\newpage\n")

            entry_title = infer_entry_title(path)
            anchor = build_entry_anchor(path)
            relative = path.relative_to(PROJECT_ROOT)
            content = path.read_text(encoding="utf-8")
            body = strip_primary_heading(content, entry_title)
            shifted = shift_heading_levels(body, offset=2).strip()

            parts.append(f"## {entry_title} {{#{anchor}}}\n\n")
            if shifted:
                parts.append(shifted)
                parts.append("\n\n")
            parts.append(f"<!-- 来源: {relative.as_posix()} -->\n\n")

    combined = "".join(parts).strip()
    if not combined.endswith("\n"):
        combined += "\n"
    return combined
