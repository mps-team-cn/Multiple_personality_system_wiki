"""MkDocs 构建钩子：清理搜索索引中的零宽空格，避免中文搜索失效；将 Frontmatter 中的 synonyms 注入搜索索引。"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

import yaml

ZERO_WIDTH_SPACE = "\u200b"


def _strip_zero_width(value: str) -> str:
    """移除文本中的零宽空格，保持其余字符不变。"""
    return value.replace(ZERO_WIDTH_SPACE, "")


def _extract_frontmatter_synonyms(file_path: Path) -> list[str]:
    """从 Markdown 文件的 Frontmatter 中提取 synonyms 字段。"""
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8")

    # 匹配 Frontmatter (以 --- 包裹的 YAML)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return []

    try:
        frontmatter = yaml.safe_load(match.group(1))
        synonyms = frontmatter.get("synonyms", [])
        if isinstance(synonyms, list):
            return [str(s).strip() for s in synonyms if s]
        return []
    except Exception:
        return []


def on_post_build(config: Dict[str, Any]) -> None:
    """在构建完成后清理搜索索引文本，并将 Frontmatter 中的 synonyms 注入搜索索引。"""
    site_dir = Path(config.get("site_dir", ""))
    docs_dir = Path(config.get("docs_dir", "docs"))
    search_index = site_dir / "search" / "search_index.json"

    if not search_index.exists():
        return

    data = json.loads(search_index.read_text(encoding="utf-8"))
    changed = False

    for doc in data.get("docs", []):
        # 1. 清理零宽空格
        for key in ("title", "text"):
            value = doc.get(key)
            if not value:
                continue

            cleaned = _strip_zero_width(value)
            if cleaned != value:
                doc[key] = cleaned
                changed = True

        # 2. 将 Frontmatter 中的 synonyms 注入搜索文本
        location = doc.get("location", "")
        if location:
            # 从 location 推断原始文件路径
            # location 格式如: "entries/Adjustment-Disorders/"
            file_path = docs_dir / location.rstrip("/")
            if file_path.is_dir():
                file_path = file_path / "index.md"
            elif not file_path.suffix:
                file_path = file_path.with_suffix(".md")

            # 提取 synonyms
            synonyms = _extract_frontmatter_synonyms(file_path)
            if synonyms:
                # 将 synonyms 添加到搜索文本末尾(作为隐藏关键词)
                current_text = doc.get("text", "")
                synonyms_text = " ".join(synonyms)
                doc["text"] = f"{current_text}\n{synonyms_text}"
                changed = True

    if changed:
        search_index.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
