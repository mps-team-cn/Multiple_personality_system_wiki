"""Dataclasses and type aliases used by the exporter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


CategoryStructure = Sequence[tuple[str, Sequence[Path]]]


@dataclass(frozen=True)
class IgnoreRules:
    """A minimal set of ignore rules similar to ``.gitignore``."""

    files: frozenset[Path]
    directories: frozenset[Path]

    def matches(self, path: Path) -> bool:
        """Return ``True`` if ``path`` should be skipped when exporting."""

        resolved = path.resolve()
        if resolved in self.files:
            return True

        return any(
            resolved == directory or resolved.is_relative_to(directory)
            for directory in self.directories
        )


@dataclass
class PandocExportError(RuntimeError):
    """Raised when Pandoc fails to render the combined markdown."""

    command: Sequence[str]
    stderr: str
