"""PDF 导出工具的命令行入口，负责解析参数并触发导出流程。"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path
from typing import Sequence

from .constants import (
    DEFAULT_COVER_FOOTER,
    DEFAULT_COVER_ONLINE_LINK_LABEL,
    DEFAULT_COVER_ONLINE_LINK_URL,
    DEFAULT_COVER_SUBTITLE,
    DEFAULT_COVER_TITLE,
)
from .exporter import export_pdf
from .ignore_loader import load_ignore_rules
from .markdown import build_combined_markdown
from .models import PandocExportError
from .paths import IGNORE_FILE_PATH, PROJECT_ROOT, README_PATH
from .requirements import check_requirements, detect_cjk_font, detect_pdf_engine
from .structure import collect_markdown_structure


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """解析命令行参数并返回 ``argparse.Namespace`` 结果。"""

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
        "--include-readme",
        action="store_true",
        help="导出时包含 README.md (默认根据 ignore.md 忽略)",
    )
    parser.add_argument(
        "--ignore-file",
        type=Path,
        default=IGNORE_FILE_PATH,
        help="自定义忽略列表文件路径 (默认: 项目根目录下的 ignore.md)",
    )
    parser.add_argument(
        "--no-cover",
        action="store_true",
        help="不生成默认封面页",
    )
    parser.add_argument(
        "--cover-title",
        default=DEFAULT_COVER_TITLE,
        help=f"封面标题 (默认: {DEFAULT_COVER_TITLE})",
    )
    parser.add_argument(
        "--cover-subtitle",
        default=DEFAULT_COVER_SUBTITLE,
        help=f"封面副标题 (默认: {DEFAULT_COVER_SUBTITLE})",
    )
    parser.add_argument(
        "--cover-date",
        default=None,
        help="封面日期文字 (默认: 使用当天日期)",
    )
    parser.add_argument(
        "--cover-footer",
        default=DEFAULT_COVER_FOOTER,
        help=f"封面底部文字 (默认: {DEFAULT_COVER_FOOTER})。传入空字符串可移除。",
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """统一的命令行入口，供封装脚本与 ``python -m`` 复用。"""

    args = parse_arguments(argv)
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

    ignore_rules = load_ignore_rules(args.ignore_file)
    structure = collect_markdown_structure(ignore_rules)
    if not structure:
        raise SystemExit("没有找到可以导出的 Markdown 文件。")

    cover_date = args.cover_date.strip() if args.cover_date else datetime.date.today().isoformat()
    cover_subtitle = args.cover_subtitle.strip() if args.cover_subtitle else None
    cover_footer = args.cover_footer
    if cover_footer is not None:
        cover_footer = cover_footer.strip()
        if not cover_footer:
            cover_footer = None

    combined_markdown = build_combined_markdown(
        structure=structure,
        include_readme=args.include_readme or not ignore_rules.matches(README_PATH),
        include_cover=not args.no_cover,
        cover_title=args.cover_title,
        cover_subtitle=cover_subtitle,
        cover_date=cover_date,
        cover_footer=cover_footer,
        cover_online_link_label=DEFAULT_COVER_ONLINE_LINK_LABEL,
        cover_online_link_url=DEFAULT_COVER_ONLINE_LINK_URL,
    )

    try:
        export_path = args.output
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_pdf(
            markdown_content=combined_markdown,
            output_path=export_path,
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
    except OSError as exc:
        raise SystemExit(f"无法写入输出文件: {exc}") from exc

    if sys.stdout.isatty():
        print(f"已成功导出 PDF 到 {args.output}")
