#!/usr/bin/env python3
"""Export the wiki contents into a single PDF with a generated table of contents."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ENTRIES_DIR = PROJECT_ROOT / "entries"

# The category directories are ordered to match the README index.
CATEGORY_ORDER = [
    "诊断与临床",
    "系统角色与类型",
    "系统体验与机制",
    "实践与支持",
]


def check_requirements(pandoc_cmd: str) -> None:
    """Ensure that the external tools required by the script are available."""

    if shutil.which(pandoc_cmd) is None:
        raise SystemExit(
            f"未找到 `{pandoc_cmd}` 可执行文件。请先安装 Pandoc 后再运行此脚本。"
        )


def collect_markdown_paths(include_readme: bool) -> list[Path]:
    """Collect markdown files in the desired export order."""

    markdown_paths: list[Path] = []

    if include_readme:
        readme_path = PROJECT_ROOT / "README.md"
        if readme_path.exists():
            markdown_paths.append(readme_path)

    for category in CATEGORY_ORDER:
        category_dir = ENTRIES_DIR / category
        if not category_dir.exists():
            continue

        markdown_paths.extend(sorted(category_dir.glob("*.md")))

    # Include any additional markdown files that are not in the predefined order.
    remaining = sorted(
        path
        for path in ENTRIES_DIR.glob("**/*.md")
        if path not in markdown_paths
    )
    markdown_paths.extend(remaining)

    return markdown_paths


def build_combined_markdown(markdown_paths: list[Path]) -> str:
    """Combine all markdown files into a single string."""

    parts: list[str] = []
    for path in markdown_paths:
        title = path.stem
        relative = path.relative_to(PROJECT_ROOT)
        parts.append(f"\n\n# {title}\n\n")
        parts.append(path.read_text(encoding="utf-8"))
        parts.append(f"\n\n<!-- 来源: {relative.as_posix()} -->\n")

    return "".join(parts).strip() + "\n"


def export_pdf(
    markdown_content: str,
    output_path: Path,
    pandoc_cmd: str,
    toc_depth: int,
    pdf_engine: str | None,
) -> None:
    """Run pandoc to generate a PDF file from the combined markdown."""

    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as temp_file:
        temp_file.write(markdown_content)
        temp_path = Path(temp_file.name)

    command = [pandoc_cmd, str(temp_path), "--toc", f"--toc-depth={toc_depth}", "-o", str(output_path)]
    if pdf_engine:
        command.extend(["--pdf-engine", pdf_engine])

    try:
        subprocess.run(command, check=True)
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
        "--toc-depth",
        type=int,
        default=3,
        help="目录深度 (默认: 3)",
    )
    parser.add_argument(
        "--no-readme",
        action="store_true",
        help="导出时不包含 README.md",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    check_requirements(args.pandoc)

    markdown_paths = collect_markdown_paths(include_readme=not args.no_readme)
    if not markdown_paths:
        raise SystemExit("没有找到可以导出的 Markdown 文件。")

    combined_markdown = build_combined_markdown(markdown_paths)

    try:
        export_pdf(
            markdown_content=combined_markdown,
            output_path=args.output,
            pandoc_cmd=args.pandoc,
            toc_depth=args.toc_depth,
            pdf_engine=args.pdf_engine,
        )
    except subprocess.CalledProcessError as error:
        raise SystemExit(
            "Pandoc 转换失败，请检查 Pandoc 是否安装完整并确认 PDF 引擎可用。"
        ) from error


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        raise
