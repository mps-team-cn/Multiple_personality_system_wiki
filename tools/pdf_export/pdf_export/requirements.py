"""校验运行时依赖并提供外部工具探测函数。"""

from __future__ import annotations

import shutil
import subprocess
from typing import Iterable

from .constants import CJK_FONT_CANDIDATES, DEFAULT_PDF_ENGINES


def check_requirements(pandoc_cmd: str) -> None:
    """确认导出脚本所需的 Pandoc 命令是否可用。"""

    if shutil.which(pandoc_cmd) is None:
        raise SystemExit(
            f"未找到 `{pandoc_cmd}` 可执行文件。请先安装 Pandoc 后再运行此脚本。"
        )


def _first_available(executables: Iterable[str]) -> str | None:
    for candidate in executables:
        if shutil.which(candidate):
            return candidate
    return None


def detect_pdf_engine(preferred: str | None) -> str | None:
    """查找可供 Pandoc 使用的 PDF 引擎并返回名称。"""

    if preferred:
        if shutil.which(preferred) is None:
            raise SystemExit(
                f"未找到指定的 PDF 引擎 `{preferred}`。请确认其已安装或改用其他引擎。"
            )
        return preferred

    return _first_available(DEFAULT_PDF_ENGINES)


def detect_cjk_font() -> str | None:
    """检测系统已安装的中文字体并返回首个匹配项。"""

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
