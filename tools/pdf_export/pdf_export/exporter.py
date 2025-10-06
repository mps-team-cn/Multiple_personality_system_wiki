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
        "markdown+east_asian_line_breaks+raw_tex",
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
