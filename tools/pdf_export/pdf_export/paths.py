"""提供 PDF 导出脚本使用的路径常量，保证目录定位一致。"""

from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
TOOLS_EXPORT_DIR = PACKAGE_DIR.parent
TOOLS_DIR = TOOLS_EXPORT_DIR.parent
PROJECT_ROOT = TOOLS_DIR.parent

# 词条目录：优先使用 docs/entries/（新结构），回退到 entries/（旧结构）
DOCS_ENTRIES_DIR = PROJECT_ROOT / "docs" / "entries"
ENTRIES_DIR = DOCS_ENTRIES_DIR if DOCS_ENTRIES_DIR.exists() else PROJECT_ROOT / "entries"

# README、Preface 等文档：优先使用 docs/ 目录
DOCS_DIR = PROJECT_ROOT / "docs"
README_PATH = DOCS_DIR / "README.md" if (DOCS_DIR / "README.md").exists() else PROJECT_ROOT / "README.md"
PREFACE_PATH = DOCS_DIR / "Preface.md" if (DOCS_DIR / "Preface.md").exists() else PROJECT_ROOT / "Preface.md"
INDEX_PATH = DOCS_DIR / "index.md" if (DOCS_DIR / "index.md").exists() else PROJECT_ROOT / "index.md"

IGNORE_FILE_PATH = PROJECT_ROOT / "ignore.md"
LAST_UPDATED_JSON_PATH = DOCS_DIR / "assets" / "last-updated.json" if (DOCS_DIR / "assets" / "last-updated.json").exists() else PROJECT_ROOT / "assets" / "last-updated.json"
