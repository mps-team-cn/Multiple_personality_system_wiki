"""提供 PDF 导出脚本使用的路径常量，保证目录定位一致。"""

from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
TOOLS_EXPORT_DIR = PACKAGE_DIR.parent
TOOLS_DIR = TOOLS_EXPORT_DIR.parent
PROJECT_ROOT = TOOLS_DIR.parent

ENTRIES_DIR = PROJECT_ROOT / "entries"
README_PATH = PROJECT_ROOT / "README.md"
IGNORE_FILE_PATH = PROJECT_ROOT / "ignore.md"
LAST_UPDATED_JSON_PATH = PROJECT_ROOT / "assets" / "last-updated.json"
