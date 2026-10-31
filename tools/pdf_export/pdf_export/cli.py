"""PDF 导出工具的命令行入口，负责解析参数并触发导出流程。"""

from __future__ import annotations

import argparse
import datetime
import sys
import os
from pathlib import Path
from typing import Sequence

# Windows 终端 UTF-8 支持
if sys.platform == 'win32':
    try:
        # 重新配置 stdout/stderr 为 UTF-8 编码
        import codecs
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from .constants import (
    DEFAULT_COVER_FOOTER,
    DEFAULT_COVER_ONLINE_LINK_LABEL,
    DEFAULT_COVER_ONLINE_LINK_URL,
    DEFAULT_COVER_SUBTITLE,
    DEFAULT_COVER_TITLE,
)
from .exporter import export_pdf
from .ignore_loader import load_ignore_rules
from .last_updated import load_last_updated_map
from .markdown import build_combined_markdown
from .models import PandocExportError
from .paths import COVER_FILE_PATH, IGNORE_FILE_PATH, LAST_UPDATED_JSON_PATH, PROJECT_ROOT, README_PATH
from .requirements import check_requirements, detect_cjk_font, detect_pdf_engine
from .structure import collect_markdown_structure


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """解析命令行参数并返回 ``argparse.Namespace`` 结果。"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=PROJECT_ROOT / "Multiple_Personality_System_wiki.pdf",
        help="输出 PDF 文件路径 (默认: Multiple_Personality_System_wiki.pdf)",
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
        "--main-font",
        default=None,
        help="正文使用的主字体名称。若未指定但提供了 --cjk-font，将默认与中文字体保持一致。",
    )
    parser.add_argument(
        "--sans-font",
        default=None,
        help="无衬线字体名称，用于 Pandoc 需要切换到无衬线文字的场景。",
    )
    parser.add_argument(
        "--mono-font",
        default=None,
        help="等宽字体名称，用于代码块或行内代码。",
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
        "--cover-image",
        type=Path,
        default=None,
        help="封面图片路径（PNG/JPG/PDF），会放在标题上方",
    )
    parser.add_argument(
        "--cover-file",
        type=Path,
        default=None,
        help="自定义封面文件（Markdown/LaTeX 原样插入），默认取 tools/pdf_export/cover.md（存在则生效）",
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
    parser.add_argument(
        "--paper",
        default=None,
        help="纸张大小，如 a4 / a5 / b5 / letter / legal (传 a4paper 也行)",
    )
    parser.add_argument(
        "--margin",
        default=None,
        help="页边距，geometry 语法：2.5cm 或 top=2cm,bottom=2cm,left=1.5cm",
    )
    parser.add_argument(
        "--binding-offset",
        default=None,
        help="装订线宽度（内侧额外留白，如 1cm），自动启用 twoside 奇偶页镜像",
    )
    parser.add_argument(
        "--exclude-topics",
        type=str,
        default=None,
        help="不导出的章节，按 frontmatter 的 topic 匹配，逗号分隔。例如: --exclude-topics '文化与表现'",
    )
    parser.add_argument(
        "--include-tags",
        type=str,
        default=None,
        help="只导出包含指定标签的词条，多个标签用逗号分隔。例如: --include-tags '基础概念,入门指南'",
    )
    parser.add_argument(
        "--exclude-tags",
        type=str,
        default=None,
        help="排除包含指定标签的词条，多个标签用逗号分隔。例如: --exclude-tags '进阶内容,实验性'",
    )
    parser.add_argument(
        "--entry-list",
        type=Path,
        default=None,
        help="指定词条白名单文件路径，每行一个词条文件名（如 'Alter.md'）或标题",
    )
    parser.add_argument(
        "--emit-markdown",
        type=Path,
        default=None,
        help="只写出合并后的 Markdown，不调 Pandoc（不需要 LaTeX，本地秒级校对章节与封面）",
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """统一的命令行入口，供封装脚本与 ``python -m`` 复用。"""

    args = parse_arguments(argv)

    emit_markdown = args.emit_markdown

    if emit_markdown is None:
        if sys.stdout.isatty():
            print("🔍 检查依赖项...")
        check_requirements(args.pandoc)

        if sys.stdout.isatty():
            print("🔧 检测 PDF 引擎...")
        pdf_engine = detect_pdf_engine(args.pdf_engine)
        if pdf_engine is None:
            raise SystemExit(
                "未找到可用的 PDF 引擎。请安装以下任意工具后重试:\n"
                "- TeX Live、MiKTeX 等 TeX 发行版 (提供 xelatex 或 pdflatex)\n"
                "- [Tectonic](https://tectonic-typesetting.github.io/)\n"
                "安装完成后可通过 `python export_to_pdf.py --pdf-engine xelatex` 指定所需的引擎。"
            )
    else:
        pdf_engine = None

    cjk_font = args.cjk_font.strip() if args.cjk_font else detect_cjk_font()
    main_font = args.main_font.strip() if args.main_font else None
    sans_font = args.sans_font.strip() if args.sans_font else None
    mono_font = args.mono_font.strip() if args.mono_font else None

    if main_font is None and cjk_font:
        # 当未指定主字体但明确了中文字体时，优先与中文字体保持一致，
        # 以避免 Roman Numeral 等特殊符号回退到不支持的默认字体。
        main_font = cjk_font

    if sys.stdout.isatty():
        print("📂 加载忽略规则...")
    ignore_rules = load_ignore_rules(args.ignore_file)

    if sys.stdout.isatty():
        print("📚 收集 Markdown 文件结构...")

    # 解析标签过滤参数
    include_tags = None
    if args.include_tags:
        include_tags = set(tag.strip() for tag in args.include_tags.split(',') if tag.strip())

    exclude_tags = None
    if args.exclude_tags:
        exclude_tags = set(tag.strip() for tag in args.exclude_tags.split(',') if tag.strip())

    exclude_topics = None
    if args.exclude_topics:
        exclude_topics = set(topic.strip() for topic in args.exclude_topics.split(',') if topic.strip())

    preface_doc, structure = collect_markdown_structure(
        ignore_rules,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        entry_list_path=args.entry_list,
        exclude_topics=exclude_topics,
    )
    if not structure:
        raise SystemExit("没有找到可以导出的 Markdown 文件。")

    # 统计文件数量
    total_entries = sum(len(entries) for _, entries in structure)
    if preface_doc:
        total_entries += 1  # 包含前言
    if sys.stdout.isatty():
        print(f"   找到 {len(structure)} 个分类，共 {total_entries} 个文档")

    cover_date = args.cover_date.strip() if args.cover_date else datetime.date.today().isoformat()
    cover_subtitle = args.cover_subtitle.strip() if args.cover_subtitle else None
    cover_footer = args.cover_footer
    if cover_footer is not None:
        cover_footer = cover_footer.strip()
        if not cover_footer:
            cover_footer = None

    cover_image = None
    if args.cover_image:
        # 合并后的 Markdown 写在临时目录，LaTeX 只认绝对路径。
        if not args.cover_image.is_file():
            raise SystemExit(f"封面图片不存在: {args.cover_image}")
        cover_image = str(args.cover_image.resolve())

    # 自定义封面文件优先于内置封面（内置的 --cover-* 参数随之失效）
    cover_source = None
    cover_path = args.cover_file or (COVER_FILE_PATH if COVER_FILE_PATH.is_file() else None)
    if cover_path:
        if not cover_path.is_file():
            raise SystemExit(f"封面文件不存在: {cover_path}")
        cover_source = cover_path.read_text(encoding="utf-8").strip()
        print(f"使用自定义封面: {cover_path}（--cover-* 参数已忽略）")

    if sys.stdout.isatty():
        print("📅 加载更新时间戳...")
    last_updated_map = load_last_updated_map(LAST_UPDATED_JSON_PATH)

    if sys.stdout.isatty():
        print("🔨 合并 Markdown 内容...")
    combined_markdown = build_combined_markdown(
        preface_doc=preface_doc,
        structure=structure,
        include_readme=args.include_readme or not ignore_rules.matches(README_PATH),
        include_cover=not args.no_cover,
        cover_source=cover_source,
        cover_title=args.cover_title,
        cover_subtitle=cover_subtitle,
        cover_date=cover_date,
        cover_footer=cover_footer,
        cover_online_link_label=DEFAULT_COVER_ONLINE_LINK_LABEL,
        cover_online_link_url=DEFAULT_COVER_ONLINE_LINK_URL,
        last_updated_map=last_updated_map,
        cover_image=cover_image,
    )

    if emit_markdown is not None:
        emit_markdown.parent.mkdir(parents=True, exist_ok=True)
        emit_markdown.write_text(combined_markdown, encoding="utf-8")
        print(f"已写出合并后的 Markdown: {emit_markdown}")
        print(f"章节 {len(structure)} 个 / 词条 {total_entries} 篇 / {len(combined_markdown)} 字符")
        return

    try:
        export_path = args.output
        export_path.parent.mkdir(parents=True, exist_ok=True)

        if sys.stdout.isatty():
            print(f"📄 调用 Pandoc 生成 PDF (使用引擎: {pdf_engine})...")
        export_pdf(
            markdown_content=combined_markdown,
            output_path=export_path,
            pandoc_cmd=args.pandoc,
            pdf_engine=pdf_engine,
            cjk_font=cjk_font,
            main_font=main_font,
            sans_font=sans_font,
            mono_font=mono_font,
            paper=args.paper,
            margin=args.margin,
            binding_offset=args.binding_offset,
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
        # 确保Windows终端正确显示中文
        try:
            print(f"已成功导出 PDF 到 {args.output}")
        except UnicodeEncodeError:
            # Windows终端编码回退处理
            print(f"已成功导出 PDF 到 {args.output}".encode('gbk', errors='ignore').decode('gbk'))
