"""集中管理导出流程会用到的常量配置，便于统一维护。"""

from __future__ import annotations

DEFAULT_PDF_ENGINES = [
    "tectonic",  # 优先使用 Tectonic (性能比 XeLaTeX 快 2-3 倍)
    "xelatex",
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

DEFAULT_COVER_TITLE = "多意识体系统知识库"
DEFAULT_COVER_SUBTITLE = "Multiple Personality System Wiki"
DEFAULT_COVER_FOOTER = "脸脸系统&&逝水流年系统&&弦羽系统&&全体贡献者"
DEFAULT_COVER_ONLINE_LINK_LABEL = "https://wiki.mpsteam.cn/"
DEFAULT_COVER_ONLINE_LINK_URL = "https://wiki.mpsteam.cn/"
