"""MkDocs 构建钩子：清理搜索索引中的零宽空格，避免中文搜索失效。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

ZERO_WIDTH_SPACE = "\u200b"


def _strip_zero_width(value: str) -> str:
    """移除文本中的零宽空格，保持其余字符不变。"""
    return value.replace(ZERO_WIDTH_SPACE, "")


def on_post_build(config: Dict[str, Any]) -> None:
    """在构建完成后清理搜索索引文本。"""
    site_dir = Path(config.get("site_dir", ""))
    search_index = site_dir / "search" / "search_index.json"

    if not search_index.exists():
        return

    data = json.loads(search_index.read_text(encoding="utf-8"))
    changed = False

    for doc in data.get("docs", []):
        for key in ("title", "text"):
            value = doc.get(key)
            if not value:
                continue

            cleaned = _strip_zero_width(value)
            if cleaned != value:
                doc[key] = cleaned
                changed = True

    if changed:
        search_index.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
