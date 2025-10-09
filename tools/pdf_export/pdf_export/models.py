"""导出流程中共享的数据结构与类型别名定义。"""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class EntryDocument:
    """表示参与导出的单篇词条内容。"""

    path: Path
    title: str
    tags: tuple[str, ...]
    topic: str
    body: str


CategoryStructure = Sequence[tuple[str, Sequence[EntryDocument]]]


@dataclass(frozen=True)
class IgnoreRules:
    """表示与 ``.gitignore`` 类似的忽略规则集合。"""

    files: frozenset[Path]
    directories: frozenset[Path]
    patterns: tuple[str, ...]
    root: Path

    def matches(self, path: Path) -> bool:
        """判断 ``path`` 是否应在导出时被跳过。"""

        resolved = path.resolve()
        if resolved in self.files:
            return True

        if any(
            resolved == directory or resolved.is_relative_to(directory)
            for directory in self.directories
        ):
            return True

        candidates: list[str] = [resolved.as_posix(), resolved.name]

        try:
            relative = resolved.relative_to(self.root)
        except ValueError:
            relative = None

        if relative is not None:
            relative_posix = relative.as_posix()
            candidates.append(relative_posix)
            candidates.append(relative.name)

        for candidate in candidates:
            for pattern in self.patterns:
                if fnmatch(candidate, pattern):
                    return True

        return False


@dataclass
class PandocExportError(RuntimeError):
    """当 Pandoc 渲染合并后的 Markdown 失败时抛出的异常。"""

    command: Sequence[str]
    stderr: str
