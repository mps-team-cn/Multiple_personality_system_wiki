"""从 ``ignore.md`` 读取忽略规则的辅助函数。"""

from __future__ import annotations

from pathlib import Path

from .models import IgnoreRules
from .paths import PROJECT_ROOT


def load_ignore_rules(path: Path) -> IgnoreRules:
    """解析 ``ignore.md`` 并返回与 .gitignore 类似的忽略配置。"""

    if not path.exists():
        return IgnoreRules(files=frozenset(), directories=frozenset())

    files: set[Path] = set()
    directories: set[Path] = set()
    patterns: set[str] = set()

    root = PROJECT_ROOT.resolve()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        normalized = line.replace("\\", "/")
        if any(symbol in normalized for symbol in "*?[]"):
            trimmed = normalized.lstrip("./")
            if trimmed:
                patterns.add(trimmed)
                patterns.add(f"{root.as_posix().rstrip('/')}/{trimmed}")
            continue

        candidate = Path(normalized)
        if not candidate.is_absolute():
            candidate = (PROJECT_ROOT / candidate).resolve()
        else:
            candidate = candidate.resolve()

        if line.endswith("/") or candidate.is_dir():
            directories.add(candidate)
        else:
            files.add(candidate)

    return IgnoreRules(
        files=frozenset(files),
        directories=frozenset(directories),
        patterns=tuple(sorted(patterns)),
        root=root,
    )
