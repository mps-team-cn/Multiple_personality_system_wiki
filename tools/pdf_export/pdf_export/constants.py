"""集中管理导出流程会用到的常量配置，便于统一维护。"""

from __future__ import annotations

DEFAULT_PDF_ENGINES = [
    "xelatex",
    "tectonic",
    "pdflatex",
]

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

DEFAULT_COVER_TITLE = "多重意识体系统知识库"
DEFAULT_COVER_SUBTITLE = "Plurality Wiki"
DEFAULT_COVER_FOOTER = "脸脸系统"
