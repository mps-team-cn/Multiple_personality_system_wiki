"""加载词条最后更新时间索引并提供格式化工具。"""

from __future__ import annotations

import datetime as _dt
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LastUpdatedInfo:
    """表示单个词条的最后更新时间与提交哈希。"""

    updated: str
    commit: str | None = None


def _normalize_iso_timestamp(raw: str) -> str:
    """将 ISO-8601 字符串格式化为 ``YYYY/MM/DD HH:MM:SS``。"""

    try:
        normalized = raw.replace("Z", "+00:00")
        dt = _dt.datetime.fromisoformat(normalized)
        if dt.tzinfo is not None:
            dt = dt.astimezone()
        return dt.strftime("%Y/%m/%d %H:%M:%S")
    except (ValueError, TypeError):
        return raw


def load_last_updated_map(json_path: Path) -> dict[str, LastUpdatedInfo]:
    """从 ``json_path`` 加载最后更新时间映射。文件缺失或格式异常时返回空映射。"""

    if not json_path.exists():
        return {}

    try:
        raw = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    result: dict[str, LastUpdatedInfo] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, Mapping):
            continue

        updated = value.get("updated")
        commit = value.get("commit")
        if isinstance(updated, str):
            info = LastUpdatedInfo(updated=updated, commit=commit if isinstance(commit, str) else None)
            result[key] = info

    return result


def render_last_updated_text(repo_path: str, mapping: Mapping[str, LastUpdatedInfo]) -> str | None:
    """根据仓库内路径返回格式化后的“最后更新时间”文案。"""

    info = mapping.get(repo_path)
    if info is None:
        return None

    formatted = _normalize_iso_timestamp(info.updated)
    if info.commit:
        short_hash = info.commit[:7]
        if short_hash:
            return f"最后更新：{formatted}（{short_hash}）"

    return f"最后更新：{formatted}"
