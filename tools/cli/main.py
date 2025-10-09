"""
统一的 CLI 接口
提供所有工具的统一命令行入口
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from ..core.config import load_config
from ..core.logger import configure_logging, get_logger
from ..core.frontmatter import parse_frontmatter

logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="wiki-tools",
        description="Multiple Personality System Wiki 自动化工具集"
    )

    # 全局选项
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="配置文件路径"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式"
    )

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # fix_md 命令
    fix_md_parser = subparsers.add_parser("fix-md", help="修复 Markdown 格式")
    fix_md_parser.add_argument(
        "paths",
        nargs="*",
        default=["entries"],
        help="要修复的文件或目录"
    )
    fix_md_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅显示将要进行的修改，不实际修改文件"
    )

    # check_links 命令
    check_links_parser = subparsers.add_parser("check-links", help="检查链接")
    check_links_parser.add_argument(
        "--root",
        default=".",
        help="根目录路径"
    )
    check_links_parser.add_argument(
        "--whitelist",
        help="白名单文件路径"
    )

    # generate_search_index 命令
    search_parser = subparsers.add_parser("search-index", help="生成搜索索引")
    search_parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    search_parser.add_argument(
        "--entries-dir",
        default="entries",
        help="词条目录路径"
    )

    # generate_tags_index 命令
    tags_parser = subparsers.add_parser("tags-index", help="生成标签索引")
    tags_parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )

    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="校验词条")
    validate_parser.add_argument(
        "--output", "-o",
        help="校验报告输出路径"
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式"
    )

    # preview 命令
    preview_parser = subparsers.add_parser("preview", help="启动预览服务器")
    preview_parser.add_argument(
        "--port", "-p",
        type=int,
        default=4173,
        help="端口号"
    )
    preview_parser.add_argument(
        "--docsify",
        action="store_true",
        help="使用 docsify 预览"
    )

    return parser


def handle_fix_md(args) -> int:
    """处理 fix-md 命令。"""
    logger.info("开始修复 Markdown 格式")

    try:
        # TODO: 实现具体的修复逻辑
        logger.info(f"目标路径: {args.paths}")
        logger.info(f"预览模式: {args.dry_run}")

        # 临时实现
        from ..processors.markdown import MarkdownProcessor
        processor = MarkdownProcessor(dry_run=args.dry_run)

        for path_str in args.paths:
            path = Path(path_str)
            if path.is_file():
                processor.process_file(path)
            elif path.is_dir():
                processor.process_directory(path)

        logger.info("Markdown 格式修复完成")
        return 0
    except Exception as e:
        logger.error(f"修复失败: {e}")
        return 1


def handle_check_links(args) -> int:
    """处理 check-links 命令。"""
    logger.info("开始检查链接")

    try:
        # TODO: 实现具体的链接检查逻辑
        logger.info(f"根目录: {args.root}")

        from ..processors.links import LinkProcessor
        processor = LinkProcessor()

        root_path = Path(args.root)
        issues = processor.check_links(root_path)

        if issues:
            logger.warning(f"发现 {len(issues)} 个链接问题")
            for issue in issues:
                logger.warning(f"  {issue}")
            return 1
        else:
            logger.info("未发现链接问题")
            return 0
    except Exception as e:
        logger.error(f"链接检查失败: {e}")
        return 1


def handle_search_index(args) -> int:
    """处理 search-index 命令。"""
    logger.info("开始生成搜索索引")

    try:
        from ..generators.search_index import SearchIndexGenerator

        generator = SearchIndexGenerator()
        entries_dir = Path(args.entries_dir)
        output_path = args.output or generator.get_default_output_path()

        generator.generate(entries_dir, output_path)
        logger.info(f"搜索索引已生成: {output_path}")
        return 0
    except Exception as e:
        logger.error(f"搜索索引生成失败: {e}")
        return 1


def handle_tags_index(args) -> int:
    """处理 tags-index 命令。"""
    logger.info("开始生成标签索引")

    try:
        from ..generators.tags_index import TagsIndexGenerator

        generator = TagsIndexGenerator()
        output_path = args.output or generator.get_default_output_path()

        generator.generate(output_path)
        logger.info(f"标签索引已生成: {output_path}")
        return 0
    except Exception as e:
        logger.error(f"标签索引生成失败: {e}")
        return 1


def handle_validate(args) -> int:
    """处理 validate 命令。"""
    logger.info("开始校验词条")

    try:
        from ..validators.content import ContentValidator

        validator = ContentValidator(strict=args.strict)
        report = validator.validate()

        output_path = args.output or "docs/VALIDATION_REPORT.md"
        validator.save_report(report, output_path)

        if report.errors:
            logger.error(f"校验失败，发现 {len(report.errors)} 个错误")
            return 1
        else:
            logger.info("校验通过")
            return 0
    except Exception as e:
        logger.error(f"校验失败: {e}")
        return 1


def handle_preview(args) -> int:
    """处理 preview 命令。"""
    logger.info("启动预览服务器")

    try:
        # TODO: 实现具体的预览逻辑
        logger.info(f"端口: {args.port}")
        logger.info(f"使用 docsify: {args.docsify}")

        import http.server
        import socketserver
        import threading
        import webbrowser

        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", args.port), Handler) as httpd:
            logger.info(f"服务器启动在 http://localhost:{args.port}")

            # 在新线程中打开浏览器
            def open_browser():
                import time
                time.sleep(1)
                webbrowser.open(f"http://localhost:{args.port}")

            threading.Thread(target=open_browser, daemon=True).start()

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                logger.info("服务器已停止")

        return 0
    except Exception as e:
        logger.error(f"预览服务器启动失败: {e}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    主入口函数。

    Args:
        argv: 命令行参数列表

    Returns:
        退出码
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # 加载配置
    try:
        config = load_config()
        configure_logging(config.logging)
    except Exception as e:
        print(f"配置加载失败: {e}", file=sys.stderr)
        return 1

    # 调整日志级别
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        import logging
        logging.getLogger().setLevel(logging.ERROR)

    # 处理命令
    if args.command == "fix-md":
        return handle_fix_md(args)
    elif args.command == "check-links":
        return handle_check_links(args)
    elif args.command == "search-index":
        return handle_search_index(args)
    elif args.command == "tags-index":
        return handle_tags_index(args)
    elif args.command == "validate":
        return handle_validate(args)
    elif args.command == "preview":
        return handle_preview(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())