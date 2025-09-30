"""Path helpers for the PDF exporter."""

from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
TOOLS_EXPORT_DIR = PACKAGE_DIR.parent
TOOLS_DIR = TOOLS_EXPORT_DIR.parent
PROJECT_ROOT = TOOLS_DIR.parent

ENTRIES_DIR = PROJECT_ROOT / "entries"
README_PATH = PROJECT_ROOT / "README.md"
IGNORE_FILE_PATH = PROJECT_ROOT / "ignore.md"
