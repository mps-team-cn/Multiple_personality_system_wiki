"""与 Pandoc 交互的封装函数，负责实际的 PDF 渲染。"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .models import PandocExportError


def export_pdf(
    markdown_content: str,
    output_path: Path,
    pandoc_cmd: str,
    pdf_engine: str | None,
    cjk_font: str | None,
    main_font: str | None,
    sans_font: str | None,
    mono_font: str | None,
) -> None:
    """调用 Pandoc 将 ``markdown_content`` 渲染为 ``output_path`` 指定的文件。"""

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        handle.write(markdown_content)
        temp_path = Path(handle.name)

    command = [
        pandoc_cmd,
        "--from",
        "markdown+east_asian_line_breaks+raw_tex+fancy_lists+startnum+task_lists",
        "--to",
        "pdf",
        "--output",
        str(output_path),
        str(temp_path),
    ]

    if pdf_engine:
        command.extend(["--pdf-engine", pdf_engine])

    font_variables: list[tuple[str, str]] = []
    if main_font:
        font_variables.append(("mainfont", main_font))
    if sans_font:
        font_variables.append(("sansfont", sans_font))
    if mono_font:
        font_variables.append(("monofont", mono_font))
    if cjk_font:
        font_variables.append(("CJKmainfont", cjk_font))

    for key, value in font_variables:
        command.extend(["--variable", f"{key}={value}"])

    # 添加 LaTeX 头部来优化列表渲染
    # 使用 enumitem 包来改善多级列表的缩进和符号
    latex_header = r"""
\usepackage{enumitem}
\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=\textendash}
\setlist[itemize,3]{label=\textasteriskcentered}
\setlist[itemize,4]{label=\textperiodcentered}
\setlist{itemsep=0.2em,parsep=0em,topsep=0.5em,partopsep=0em}
\setlist[itemize]{leftmargin=1.5em}
\setlist[enumerate]{leftmargin=2em}
"""
    # 创建临时 LaTeX 头部文件
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tex", delete=False) as header_handle:
        header_handle.write(latex_header.strip())
        header_path = Path(header_handle.name)

    command.extend(["--include-in-header", str(header_path)])

    try:
        # 执行 Pandoc 命令，设置更长的超时时间（10分钟）
        result = subprocess.run(
            command,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=600,  # 10分钟超时
        )
        if result.returncode != 0:
            raise PandocExportError(command=command, stderr=result.stderr.strip())
    except subprocess.TimeoutExpired as timeout_error:
        raise PandocExportError(
            command=command,
            stderr=f"PDF 生成超时（超过 10 分钟）。可能是文档过大或 TeX 编译遇到问题。\n原始错误: {timeout_error}"
        ) from timeout_error
    finally:
        temp_path.unlink(missing_ok=True)
        header_path.unlink(missing_ok=True)
