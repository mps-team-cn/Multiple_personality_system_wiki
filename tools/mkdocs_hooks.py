"""MkDocs 构建钩子：清理搜索索引中的零宽空格，避免中文搜索失效；将 Frontmatter 中的 synonyms 注入搜索索引；生成基于 Frontmatter updated 字段的最近更新列表。"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml

ZERO_WIDTH_SPACE = "\u200b"
RECENTLY_UPDATED_PLACEHOLDER = "<!-- RECENTLY_UPDATED_DOCS -->"


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


def _extract_frontmatter(file_path: Path) -> Dict[str, Any]:
    """从 Markdown 文件中提取完整的 Frontmatter。"""
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}

    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def _generate_recently_updated_html(docs_dir: Path, limit: int = 100) -> str:
    """生成基于 Frontmatter updated 字段的最近更新列表 HTML。"""
    entries = []

    # 遍历所有 Markdown 文件
    for md_file in docs_dir.rglob("*.md"):
        frontmatter = _extract_frontmatter(md_file)
        updated = frontmatter.get("updated")
        title = frontmatter.get("title")

        if not updated or not title:
            continue

        # 解析日期 - 支持 str, datetime.date, datetime.datetime
        try:
            if isinstance(updated, str):
                # 验证字符串格式并解析
                updated_date = datetime.strptime(updated, "%Y-%m-%d")
            elif isinstance(updated, datetime):
                # 直接使用 datetime 对象
                updated_date = updated
            else:
                # 尝试将 date 对象转换为 datetime
                from datetime import date
                if isinstance(updated, date):
                    updated_date = datetime.combine(updated, datetime.min.time())
                else:
                    # 类型不匹配，跳过此词条
                    continue
        except (ValueError, TypeError):
            # 日期格式错误或类型转换失败，跳过此词条
            continue

        # 计算相对路径和 URL（使用绝对路径，从根目录开始）
        rel_path = md_file.relative_to(docs_dir)
        url = str(rel_path.with_suffix("")).replace("\\", "/")
        if url.endswith("/index"):
            url = url[:-6]  # 移除 /index
        elif url == "index":
            url = ""  # 首页特殊处理
        # 使用站点根路径（以 / 开头），确保所有页面的链接都正确
        url = "/" + url.rstrip("/")
        if url != "/":
            url += "/"

        entries.append((updated_date, title, url))

    # 按日期排序并取前 N 条
    entries.sort(reverse=True, key=lambda x: x[0])
    entries = entries[:limit]

    # 生成 HTML（样式已提取到 docs/assets/extra-material.css）
    html_parts = ['<div class="recently-updated">']

    for updated_date, title, url in entries:
        date_str = updated_date.strftime("%Y-%m-%d")
        html_parts.append(f'    <div class="recently-updated-item">')
        html_parts.append(f'        <span>{date_str}</span>')
        html_parts.append(f'        <a href="{url}">{title}</a>')
        html_parts.append(f'    </div>')

    html_parts.append('</div>')

    return '\n'.join(html_parts)


def on_page_markdown(markdown: str, page: Any, config: Dict[str, Any], files: Any) -> str:
    """在页面 Markdown 处理前替换最近更新占位符。"""
    if RECENTLY_UPDATED_PLACEHOLDER in markdown:
        docs_dir = Path(config.get("docs_dir", "docs"))
        recently_updated_html = _generate_recently_updated_html(docs_dir, limit=100)
        markdown = markdown.replace(RECENTLY_UPDATED_PLACEHOLDER, recently_updated_html)
    return markdown


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
