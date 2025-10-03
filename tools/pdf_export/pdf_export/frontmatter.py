"""解析词条前置元数据（frontmatter）的辅助函数。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .models import EntryDocument


@dataclass(frozen=True)
class EntryFrontmatter:
    """表示词条 Markdown 文件头部声明的元数据。"""

    title: str
    tags: tuple[str, ...]
    updated: str


class FrontmatterError(ValueError):
    """当词条缺少或错误声明 Frontmatter 时抛出的异常。"""


def _split_frontmatter(raw: str) -> tuple[list[str], str]:
    """拆分原始 Markdown 文本，返回 frontmatter 行与正文。"""

    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("词条缺少 YAML frontmatter，无法提取元数据。")

    front_lines: list[str] = []
    index = 1
    while index < len(lines):
        current = lines[index]
        if current.strip() == "---":
            body = "\n".join(lines[index + 1 :])
            return front_lines, body.lstrip("\n")
        front_lines.append(current)
        index += 1

    raise FrontmatterError("未找到 frontmatter 结束标记 '---'。")


def _parse_frontmatter(lines: list[str]) -> EntryFrontmatter:
    """将 frontmatter 行转换为 ``EntryFrontmatter``。"""

    raw_frontmatter = "\n".join(lines)
    try:
        loaded = yaml.safe_load(raw_frontmatter) if raw_frontmatter.strip() else {}
    except yaml.YAMLError as error:  # pragma: no cover - 仅在 YAML 无法解析时触发
        raise FrontmatterError(f"无法解析 frontmatter：{error}") from error

    if not isinstance(loaded, dict):
        raise FrontmatterError("frontmatter 必须以键值对形式声明。")

    missing = [field for field in ("title", "tags", "updated") if field not in loaded]
    if missing:
        raise FrontmatterError(f"frontmatter 缺少必要字段：{', '.join(missing)}")

    title = loaded["title"]
    if not isinstance(title, str) or not title.strip():
        raise FrontmatterError("title 字段必须为非空字符串。")

    tags_value = loaded["tags"]
    if isinstance(tags_value, str):
        # 兼容以逗号分隔的字符串写法
        tags = [item.strip() for item in tags_value.split(",") if item.strip()]
    elif isinstance(tags_value, (list, tuple)):
        tags = [str(item).strip() for item in tags_value if str(item).strip()]
    else:
        raise FrontmatterError("tags 字段必须为字符串或字符串列表。")

    if not tags:
        raise FrontmatterError("tags 字段至少包含一个标签。")

    updated = loaded["updated"]
    if not isinstance(updated, str) or not updated.strip():
        raise FrontmatterError("updated 字段必须为非空字符串。")

    return EntryFrontmatter(title=title.strip(), tags=tuple(tags), updated=updated.strip())


def load_entry_document(path: Path) -> EntryDocument:
    """读取词条 Markdown，返回 ``EntryDocument``。"""

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - 仅在 I/O 出错时触发
        raise FrontmatterError(f"无法读取词条 {path}: {error}") from error

    front_lines, body = _split_frontmatter(raw)
    meta = _parse_frontmatter(front_lines)

    return EntryDocument(
        path=path.resolve(),
        title=meta.title,
        tags=meta.tags,
        body=body,
    )

