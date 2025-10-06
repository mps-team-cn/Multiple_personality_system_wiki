"""构建 Docsify 标题搜索的增强索引。"""

from __future__ import annotations
from pypinyin import lazy_pinyin, Style  # type: ignore

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from unidecode import unidecode  # type: ignore

try:
    import frontmatter  # type: ignore
except ImportError as exc:  # pragma: no cover - 环境缺少依赖时给出清晰提示
    raise SystemExit("需要安装 python-frontmatter 才能构建搜索索引") from exc


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ENTRIES_DIR = ROOT_DIR / "entries"
DEFAULT_OUTPUT = ROOT_DIR / "assets" / "search-index.json"

CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")
PAREN_PATTERN = re.compile(r"[（(]([^()（）]+)[)）]")
SPLIT_PATTERN = re.compile(r"[、，,；;｜|/]+")


@dataclass(frozen=True)
class Token:
    """描述可用于匹配的关键字。"""

    normalized: str
    display: str
    kind: str


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="为前端搜索生成 JSON 索引")
    parser.add_argument(
        "--entries-dir",
        type=Path,
        default=DEFAULT_ENTRIES_DIR,
        help="词条 Markdown 所在目录，默认为仓库 entries/",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="索引输出路径，默认为 assets/search-index.json",
    )
    return parser.parse_args()


def load_synonym_list(raw: object) -> List[str]:
    """将 Frontmatter 中的 synonyms 字段规范化为字符串列表。"""

    if raw is None:
        return []
    if isinstance(raw, str):
        items: Sequence[str] = [raw]
    elif isinstance(raw, Sequence):  # type: ignore[redundant-expr]
        items = [str(item) for item in raw if isinstance(item, (str, int, float))]
    else:
        return []

    results: List[str] = []
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        if SPLIT_PATTERN.search(text):
            results.extend(
                candidate.strip()
                for candidate in SPLIT_PATTERN.split(text)
                if candidate.strip()
            )
            continue
        results.append(text)
    return results


def iter_title_variants(title: str) -> Iterable[str]:
    """从标题中提取原文、去括号文本与括号内的别名。"""

    clean = title.strip()
    if not clean:
        return []

    variants: List[str] = []
    seen: set[str] = set()

    def extend(text: str) -> None:
        """加入去重后的候选文本，并拆分顿号/斜杠等分隔的别名。"""

        normalized = re.sub(r"\s+", " ", text.strip())
        if not normalized:
            return

        candidates = [normalized]
        if SPLIT_PATTERN.search(normalized):
            candidates.extend(
                candidate.strip()
                for candidate in SPLIT_PATTERN.split(normalized)
                if candidate.strip()
            )

        for candidate in candidates:
            if candidate and candidate not in seen:
                seen.add(candidate)
                variants.append(candidate)

    extend(clean)

    base_without_paren = PAREN_PATTERN.sub(" ", clean)
    extend(base_without_paren)

    for part in PAREN_PATTERN.findall(clean):
        extend(part)

    return variants


def has_chinese(text: str) -> bool:
    """判断字符串中是否包含中文字符。"""

    return bool(CHINESE_PATTERN.search(text))


def expand_variants(value: str) -> List[str]:
    """为同一个词条生成大小写、去空格与 ASCII 形式。"""

    base = value.strip().lower()
    if not base:
        return []

    variants = {base}
    ascii_form = unidecode(base).lower()
    variants.add(ascii_form)

    def compress(text: str) -> str:
        return re.sub(r"[\s\-_/]+", "", text)

    variants.add(compress(base))
    variants.add(compress(ascii_form))

    return [variant for variant in variants if variant]


def add_token(
    token_map: Dict[str, Token], value: str, kind: str, display: str | None = None
) -> None:
    """将词条写入 token_map，保证同一 key 只保留第一条来源。"""

    display_text = display or value
    for variant in expand_variants(value):
        if variant not in token_map:
            token_map[variant] = Token(variant, display_text, kind)


def add_pinyin(token_map: Dict[str, Token], text: str) -> None:
    """使用 pypinyin 生成中文全拼与首字母，避免 unidecode 的误判。"""
    # 仅保留中文部分参与拼音计算，避免英文/括号干扰
    han = "".join(re.findall(r"[\u4e00-\u9fff]", text))
    if not han:
        return

    # 多音字用常用读音；需要更精细可用 heteronym=True 再做词典消歧
    full_list = lazy_pinyin(han, style=Style.NORMAL, errors="ignore")
    abbr_list = lazy_pinyin(han, style=Style.FIRST_LETTER, errors="ignore")

    full = "".join(full_list).lower()
    abbr = "".join(abbr_list).lower()

    if full:
        add_token(token_map, full, "pinyin_full", full)
    if abbr:
        add_token(token_map, abbr, "pinyin_abbr", abbr)



def build_entry_index(markdown_path: Path) -> Dict[str, object] | None:
    """从 Markdown 文件中抽取用于搜索的索引信息。"""

    post = frontmatter.load(markdown_path)
    title = str(post.metadata.get("title", "")).strip()
    if not title:
        return None

    synonyms = load_synonym_list(post.metadata.get("synonyms"))

    terms = []
    for variant in iter_title_variants(title):
        terms.append((variant, "title" if variant == title else "alias"))
    for synonym in synonyms:
        terms.append((synonym, "synonym"))

    token_map: Dict[str, Token] = {}

    for value, kind in terms:
        add_token(token_map, value, kind, value)
        add_pinyin(token_map, value)

    aliases = sorted({value for value, _ in terms})

    tokens = [
        {
            "normalized": token.normalized,
            "display": token.display,
            "kind": token.kind,
        }
        for token in sorted(token_map.values(), key=lambda item: (item.kind, item.normalized))
    ]

    return {
        "path": str(markdown_path.relative_to(ROOT_DIR)).replace("\\", "/"),
        "title": title,
        "aliases": aliases,
        "tokens": tokens,
    }


def build_index(entries_dir: Path) -> List[Dict[str, object]]:
    """遍历词条目录，构建索引列表。"""

    records: List[Dict[str, object]] = []
    for markdown_path in sorted(entries_dir.glob("*.md")):
        record = build_entry_index(markdown_path)
        if record is None:
            continue
        records.append(record)
    return records


def main() -> None:
    """脚本入口。"""

    args = parse_args()
    entries_dir = args.entries_dir.resolve()
    output_path = args.output.resolve()

    if not entries_dir.exists():
        raise SystemExit(f"词条目录不存在：{entries_dir}")

    records = build_index(entries_dir)

    data = {
        "version": 1,
        "entries": records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
