"""Helpers for reading ignore rules from ``ignore.md``."""

from __future__ import annotations

from pathlib import Path

from .models import IgnoreRules
from .paths import PROJECT_ROOT


def load_ignore_rules(path: Path) -> IgnoreRules:
    """Load ignore rules from ``ignore.md`` similar to a subset of .gitignore."""

    if not path.exists():
        return IgnoreRules(files=frozenset(), directories=frozenset())

    files: set[Path] = set()
    directories: set[Path] = set()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        candidate = Path(line)
        if not candidate.is_absolute():
            candidate = (PROJECT_ROOT / candidate).resolve()
        else:
            candidate = candidate.resolve()

        if line.endswith("/") or candidate.is_dir():
            directories.add(candidate)
        else:
            files.add(candidate)

    return IgnoreRules(files=frozenset(files), directories=frozenset(directories))
