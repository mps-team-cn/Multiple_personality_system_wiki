"""
统一的 Frontmatter 解析模块
提供 YAML frontmatter 的解析和验证功能
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml

from .logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class EntryFrontmatter:
    """表示词条 Markdown 文件头部声明的元数据。"""

    title: str
    tags: Tuple[str, ...]
    updated: str
    synonyms: Optional[Tuple[str, ...]] = None
    draft: Optional[bool] = False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式。"""
        result = {
            'title': self.title,
            'tags': list(self.tags),
            'updated': self.updated
        }
        if self.synonyms:
            result['synonyms'] = list(self.synonyms)
        if self.draft:
            result['draft'] = self.draft
        return result


class FrontmatterError(ValueError):
    """当词条缺少或错误声明 Frontmatter 时抛出的异常。"""
    pass


class FrontmatterParser:
    """Frontmatter 解析器。"""

    def __init__(self, strict: bool = True):
        """
        初始化解析器。

        Args:
            strict: 是否使用严格模式验证
        """
        self.strict = strict
        self.logger = get_logger(self.__class__.__name__)

    def parse_file(self, file_path: Union[str, Path]) -> Tuple[EntryFrontmatter, str]:
        """
        解析 Markdown 文件的 frontmatter。

        Args:
            file_path: 文件路径

        Returns:
            (frontmatter, 正文内容)

        Raises:
            FrontmatterError: 解析失败时抛出
        """
        path = Path(file_path)
        if not path.exists():
            raise FrontmatterError(f"文件不存在: {path}")

        try:
            content = path.read_text(encoding='utf-8')
            return self.parse_content(content)
        except OSError as e:
            raise FrontmatterError(f"无法读取文件 {path}: {e}") from e

    def parse_content(self, content: str) -> Tuple[EntryFrontmatter, str]:
        """
        解析 Markdown 内容的 frontmatter。

        Args:
            content: Markdown 内容

        Returns:
            (frontmatter, 正文内容)

        Raises:
            FrontmatterError: 解析失败时抛出
        """
        front_lines, body = self._split_frontmatter(content)
        frontmatter = self._parse_frontmatter(front_lines)

        return frontmatter, body

    def _split_frontmatter(self, content: str) -> Tuple[List[str], str]:
        """拆分原始 Markdown 文本，返回 frontmatter 行与正文。"""
        lines = content.splitlines()

        if not lines or lines[0].strip() != "---":
            if self.strict:
                raise FrontmatterError("词条缺少 YAML frontmatter，无法提取元数据。")
            else:
                self.logger.warning("文件缺少 frontmatter，使用默认值")
                return [], content

        front_lines: List[str] = []
        index = 1

        while index < len(lines):
            current = lines[index]
            if current.strip() == "---":
                body = "\n".join(lines[index + 1 :])
                return front_lines, body.lstrip("\n")
            front_lines.append(current)
            index += 1

        raise FrontmatterError("未找到 frontmatter 结束标记 '---'。")

    def _parse_frontmatter(self, lines: List[str]) -> EntryFrontmatter:
        """将 frontmatter 行转换为 EntryFrontmatter。"""
        raw_frontmatter = "\n".join(lines)

        try:
            loaded = yaml.safe_load(raw_frontmatter) if raw_frontmatter.strip() else {}
        except yaml.YAMLError as e:
            raise FrontmatterError(f"无法解析 frontmatter：{e}") from e

        if not isinstance(loaded, dict):
            raise FrontmatterError("frontmatter 必须以键值对形式声明。")

        # 验证必要字段
        required_fields = ["title", "tags", "updated"]
        missing = [field for field in required_fields if field not in loaded]

        if missing:
            if self.strict:
                raise FrontmatterError(f"frontmatter 缺少必要字段：{', '.join(missing)}")
            else:
                self.logger.warning(f"frontmatter 缺少字段: {', '.join(missing)}")
                # 提供默认值
                for field in missing:
                    if field == "title":
                        loaded[field] = "未命名词条"
                    elif field == "tags":
                        loaded[field] = ["未分类"]
                    elif field == "updated":
                        loaded[field] = datetime.now().strftime("%Y-%m-%d")

        # 解析并验证各个字段
        title = self._parse_title(loaded.get("title"))
        tags = self._parse_tags(loaded.get("tags"))
        updated = self._parse_updated(loaded.get("updated"))
        synonyms = self._parse_synonyms(loaded.get("synonyms"))
        draft = self._parse_draft(loaded.get("draft", False))

        return EntryFrontmatter(
            title=title,
            tags=tags,
            updated=updated,
            synonyms=synonyms,
            draft=draft
        )

    def _parse_title(self, value: Any) -> str:
        """解析 title 字段。"""
        if not isinstance(value, str) or not value.strip():
            if self.strict:
                raise FrontmatterError("title 字段必须为非空字符串。")
            else:
                self.logger.warning("title 字段无效，使用默认值")
                return "未命名词条"
        return value.strip()

    def _parse_tags(self, value: Any) -> Tuple[str, ...]:
        """解析 tags 字段。"""
        if isinstance(value, str):
            # 兼容以逗号分隔的字符串写法
            tags = [item.strip() for item in value.split(",") if item.strip()]
        elif isinstance(value, (list, tuple)):
            tags = [str(item).strip() for item in value if str(item).strip()]
        else:
            if self.strict:
                raise FrontmatterError("tags 字段必须为字符串或字符串列表。")
            else:
                self.logger.warning("tags 字段格式无效，使用默认值")
                return ("未分类",)

        if not tags:
            if self.strict:
                raise FrontmatterError("tags 字段至少包含一个标签。")
            else:
                self.logger.warning("tags 字段为空，使用默认值")
                return ("未分类",)

        return tuple(tags)

    def _parse_updated(self, value: Any) -> str:
        """解析 updated 字段。"""
        if isinstance(value, (date, datetime)):
            return value.isoformat()

        if isinstance(value, str):
            return value.strip()

        if value is None:
            if self.strict:
                raise FrontmatterError("updated 字段必须为日期或字符串。")
            else:
                self.logger.warning("updated 字段为空，使用当前日期")
                return datetime.now().strftime("%Y-%m-%d")

        if isinstance(value, bool):
            raise FrontmatterError("updated 字段必须为日期或字符串，不能使用布尔值。")

        if isinstance(value, (list, tuple, set, dict)):
            raise FrontmatterError("updated 字段必须为日期或字符串，不支持复合类型。")

        return str(value).strip()

    def _parse_synonyms(self, value: Any) -> Optional[Tuple[str, ...]]:
        """解析 synonyms 字段（可选）。"""
        if value is None:
            return None

        if isinstance(value, str):
            synonyms = [item.strip() for item in value.split(",") if item.strip()]
        elif isinstance(value, (list, tuple)):
            synonyms = [str(item).strip() for item in value if str(item).strip()]
        else:
            self.logger.warning("synonyms 字段格式无效，忽略")
            return None

        return tuple(synonyms) if synonyms else None

    def _parse_draft(self, value: Any) -> bool:
        """解析 draft 字段（可选）。"""
        return bool(value)


# 全局默认解析器实例
default_parser = FrontmatterParser()


def parse_frontmatter(file_path: Union[str, Path]) -> Tuple[EntryFrontmatter, str]:
    """
    使用默认解析器解析 frontmatter。

    Args:
        file_path: 文件路径

    Returns:
        (frontmatter, 正文内容)
    """
    return default_parser.parse_file(file_path)


def parse_frontmatter_content(content: str) -> Tuple[EntryFrontmatter, str]:
    """
    使用默认解析器解析 frontmatter 内容。

    Args:
        content: Markdown 内容

    Returns:
        (frontmatter, 正文内容)
    """
    return default_parser.parse_content(content)