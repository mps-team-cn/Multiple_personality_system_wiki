#!/usr/bin/env python3
"""PDF 导出工具入口脚本，作为 ``pdf_export`` 包命令行的简单封装。"""

from __future__ import annotations

import sys

from pdf_export.cli import main


if __name__ == "__main__":
    # 调用核心 CLI 入口，补充注释说明为何捕获 SystemExit：
    # - Pandoc 或依赖缺失时，子模块会通过 SystemExit 返回错误信息。
    # - 这里捕获后打印到标准错误输出，再重新抛出保持原始退出码。
    try:
        main()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        raise
