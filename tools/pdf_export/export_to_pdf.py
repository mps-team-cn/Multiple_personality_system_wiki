#!/usr/bin/env python3
"""Export the wiki contents into a single PDF with cover page and README-based order."""

from __future__ import annotations

import argparse
import datetime
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple


# ``export_to_pdf.py`` lives under ``tools/pdf_export`` while the markdown
# sources we want to bundle are located in the repository root.  Move two
# levels up so ``PROJECT_ROOT`` points to the project directory instead of the
# ``tools`` folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENTRIES_DIR = PROJECT_ROOT / "entries"
README_PATH = PROJECT_ROOT / "README.md"

DEFAULT_PDF_ENGINES = [
    "xelatex",
    "tectonic",
    "pdflatex",
]

# Common CJK font families that ship with major operating systems or are easy to
# install from open-source distributions. The first available font in this list
# will be used when generating the PDF so that Chinese characters render
# correctly without extra configuration.
CJK_FONT_CANDIDATES = [
    "Noto Serif CJK SC",
    "Noto Sans CJK SC",
    "Source Han Serif SC",
    "Source Han Sans SC",
    "思源宋体",
    "思源黑体",
    "SimSun",
    "SimHei",
    "Microsoft YaHei",
    "PingFang SC",
    "Songti SC",
]


@dataclass
class PandocExportError(RuntimeError):
    command: Sequence[str]
    stderr: str


CategoryStructure = Sequence[Tuple[str, Sequence[Path]]]


def check_requirements(pandoc_cmd: str) -> None:
    """Ensure that the external tools required by the script are available."""

    if shutil.which(pandoc_cmd) is None:
        raise SystemExit(
            f"未找到 `{pandoc_cmd}` 可执行文件。请先安装 Pandoc 后再运行此脚本。"
        )


def detect_pdf_engine(preferred: str | None) -> str | None:
    """Find an available PDF engine for Pandoc, if any."""

    if preferred:
        if shutil.which(preferred) is None:
            raise SystemExit(
                f"未找到指定的 PDF 引擎 `{preferred}`。请确认其已安装或改用其他引擎。"
            )
        return preferred

    for candidate in DEFAULT_PDF_ENGINES:
        if shutil.which(candidate):
            return candidate

    return None


def detect_cjk_font() -> str | None:
    """Return the first available Chinese font family, if any."""

    if shutil.which("fc-list") is None:
        return None

    for candidate in CJK_FONT_CANDIDATES:
        try:
            result = subprocess.run(
                ["fc-list", candidate],
                check=False,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )
        except OSError:
            return None

        if result.stdout.strip():
            return candidate

    return None


def parse_readme_index(readme_path: Path) -> CategoryStructure:
    """Parse README.md to determine the desired export order."""

    if not readme_path.exists():
        return []

    heading_pattern = re.compile(r"^###\s+(?P<title>.+?)\s*$")
    link_pattern = re.compile(
        r"^\s*-\s*\[(?P<label>[^\]]+)\]\((?P<path>[^)]+)\)"
    )

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
            if candidate.exists() and candidate.suffix.lower() == ".md":
                current_category[1].append(candidate)
            else:
                print(
                    f"警告: README 中的条目 {rel_path} 未找到，已忽略。",
                    file=sys.stderr,
                )

    # Filter out empty categories to avoid generating blank sections.
    return [(title, tuple(paths)) for title, paths in categories if paths]


def collect_markdown_structure() -> CategoryStructure:
    """Collect markdown files following the README index order."""

    categories = list(parse_readme_index(README_PATH))
    return tuple(categories)


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


def build_cover_page(title: str, subtitle: str | None, date_text: str | None) -> str:
    """Return a standalone cover page using LaTeX's titlepage environment."""

    lines = [
        "\\begin{titlepage}",
        "\\centering",
        "\\vspace*{3cm}",
        f"{{\\Huge {title.strip()} \\}}",
    ]

    if subtitle:
        lines.extend([
            "\\vspace{1.5cm}",
            f"{{\\Large {subtitle.strip()} \\}}",
        ])

    if date_text:
        lines.extend([
            "\\vfill",
            f"{{\\large {date_text.strip()} \\}}",
        ])

    lines.extend([
        "\\vfill",
        "\\textit{plurality\\_wiki 项目}",
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
            lines.append(f"- {entry_title}")
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
) -> str:
    """Combine all markdown files into a single string."""

    parts: list[str] = []

    if include_cover:
        parts.append(build_cover_page(cover_title, cover_subtitle, cover_date))

    if structure:
        parts.append(build_directory_page(structure))

    if include_readme and README_PATH.exists():
        parts.append(README_PATH.read_text(encoding="utf-8").strip())
        parts.append("\n\n\\newpage\n")

    for index, (category_title, paths) in enumerate(structure):
        if index > 0:
            parts.append("\\newpage\n")

        parts.append(f"# {category_title}\n")
        for path in paths:
            relative = path.relative_to(PROJECT_ROOT)
            content = path.read_text(encoding="utf-8")
            shifted = shift_heading_levels(content, offset=1)
            parts.append(shifted.strip())
            parts.append(f"\n\n<!-- 来源: {relative.as_posix()} -->\n\n")

    combined = "".join(parts).strip()
    if not combined.endswith("\n"):
        combined += "\n"
    return combined


def export_pdf(
    markdown_content: str,
    output_path: Path,
    pandoc_cmd: str,
    pdf_engine: str | None,
    cjk_font: str | None,
) -> None:
    """Run pandoc to generate a PDF file from the combined markdown."""

    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as temp_file:
        temp_file.write(markdown_content)
        temp_path = Path(temp_file.name)

    command: list[str] = [
        pandoc_cmd,
        str(temp_path),
        "-o",
        str(output_path),
    ]
    if pdf_engine:
        command.extend(["--pdf-engine", pdf_engine])

    if cjk_font and pdf_engine in {"xelatex", "lualatex", "tectonic"}:
        command.extend([
            "-V",
            f"mainfont={cjk_font}",
            "-V",
            f"CJKmainfont={cjk_font}",
            "-V",
            f"sansfont={cjk_font}",
        ])

    try:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if result.returncode != 0:
            raise PandocExportError(command=command, stderr=result.stderr.strip())
    finally:
        temp_path.unlink(missing_ok=True)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=PROJECT_ROOT / "plurality_wiki.pdf",
        help="输出 PDF 文件路径 (默认: plurality_wiki.pdf)",
    )
    parser.add_argument(
        "--pandoc",
        default="pandoc",
        help="Pandoc 命令名称 (默认: pandoc)",
    )
    parser.add_argument(
        "--pdf-engine",
        default=None,
        help="Pandoc 使用的 PDF 引擎 (例如 xelatex)。留空则使用 Pandoc 默认配置。",
    )
    parser.add_argument(
        "--cjk-font",
        default=None,
        help="优先用于中文内容的字体名称。例如 `Noto Serif CJK SC`。",
    )
    parser.add_argument(
        "--no-readme",
        action="store_true",
        help="导出时不包含 README.md",
    )
    parser.add_argument(
        "--no-cover",
        action="store_true",
        help="不生成默认封面页",
    )
    parser.add_argument(
        "--cover-title",
        default="plurality_wiki",
        help="封面标题 (默认: plurality_wiki)",
    )
    parser.add_argument(
        "--cover-subtitle",
        default="多重意识体系统知识库",
        help="封面副标题 (默认: 多重意识体系统知识库)",
    )
    parser.add_argument(
        "--cover-date",
        default=None,
        help="封面日期文字 (默认: 使用当天日期)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    check_requirements(args.pandoc)

    pdf_engine = detect_pdf_engine(args.pdf_engine)
    if pdf_engine is None:
        raise SystemExit(
            "未找到可用的 PDF 引擎。请安装以下任意工具后重试:\n"
            "- TeX Live、MiKTeX 等 TeX 发行版 (提供 xelatex 或 pdflatex)\n"
            "- [Tectonic](https://tectonic-typesetting.github.io/)\n"
            "安装完成后可通过 `python export_to_pdf.py --pdf-engine xelatex` 指定所需的引擎。"
        )
    cjk_font = args.cjk_font.strip() if args.cjk_font else detect_cjk_font()

    structure = collect_markdown_structure()
    if not structure:
        raise SystemExit("没有找到可以导出的 Markdown 文件。")

    cover_date = args.cover_date.strip() if args.cover_date else datetime.date.today().isoformat()
    combined_markdown = build_combined_markdown(
        structure=structure,
        include_readme=not args.no_readme,
        include_cover=not args.no_cover,
        cover_title=args.cover_title,
        cover_subtitle=args.cover_subtitle.strip() if args.cover_subtitle else None,
        cover_date=cover_date,
    )

    try:
        export_pdf(
            markdown_content=combined_markdown,
            output_path=args.output,
            pandoc_cmd=args.pandoc,
            pdf_engine=pdf_engine,
            cjk_font=cjk_font,
        )
    except PandocExportError as error:
        message = [
            "Pandoc 转换失败，请检查 Pandoc 是否安装完整并确认 PDF 引擎可用。",
        ]
        if error.stderr:
            message.append("Pandoc 输出:\n" + error.stderr)
        raise SystemExit("\n".join(message)) from None


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        raise
