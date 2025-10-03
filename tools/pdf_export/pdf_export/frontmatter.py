"""解析词条前置元数据（frontmatter）的辅助函数。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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


def _parse_tags(value: str) -> tuple[str, ...]:
    """解析形如 ``[标签1, 标签2]`` 的标签声明。"""

    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        raise FrontmatterError("tags 字段必须使用 [tag1, tag2] 格式声明。")

    inner = stripped[1:-1].strip()
    if not inner:
        return ()

    tags = tuple(tag.strip() for tag in inner.split(",") if tag.strip())
    if not tags:
        raise FrontmatterError("tags 字段不能为空。")
    return tags


def _parse_frontmatter(lines: list[str]) -> EntryFrontmatter:
    """将 frontmatter 行转换为 ``EntryFrontmatter``。"""

    data: dict[str, str] = {}
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in raw_line:
            raise FrontmatterError(f"无法解析 frontmatter 行：{raw_line}")
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip()

    missing = [field for field in ("title", "tags", "updated") if field not in data]
    if missing:
        raise FrontmatterError(f"frontmatter 缺少必要字段：{', '.join(missing)}")

    title = data["title"].strip()
    if not title:
        raise FrontmatterError("title 字段不能为空。")

    tags = _parse_tags(data["tags"])
    if not tags:
        raise FrontmatterError("tags 字段至少包含一个标签。")

    updated = data["updated"].strip()
    if not updated:
        raise FrontmatterError("updated 字段不能为空。")

    return EntryFrontmatter(title=title, tags=tags, updated=updated)


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

