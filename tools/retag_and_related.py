"""
retag_and_related.py

批量维护词条标签与“相关条目”区块。

功能：
1. 解析 entries/**/*.md Frontmatter 与正文。
2. 基于标题、定义、同义词等信息重新生成归一化标签。
3. 根据标签重叠与语义相似度计算相关条目，更新“## 相关条目”区块。
4. 提供 --dry-run / --limit / --only / --since 参数控制执行范围。

依赖：pyyaml、python-frontmatter、jieba、nltk、unidecode。
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, MutableMapping, Sequence, Tuple

try:
    import frontmatter  # type: ignore
except ImportError:  # pragma: no cover - 依赖缺失时启用简易解析
    frontmatter = None

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - 依赖缺失
    yaml = None

try:
    import jieba  # type: ignore
    import jieba.analyse  # type: ignore
except ImportError:  # pragma: no cover
    jieba = None
    jieba_analyse = None
else:  # pragma: no cover - 依赖存在
    jieba_analyse = jieba.analyse

try:
    from nltk.stem import PorterStemmer  # type: ignore
except ImportError:  # pragma: no cover
    class PorterStemmer:  # type: ignore
        def stem(self, word: str) -> str:
            return word

try:
    from unidecode import unidecode  # type: ignore
except ImportError:  # pragma: no cover
    def unidecode(text: str) -> str:  # type: ignore
        return text

ROOT = Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "entries"

SYN_MAP = {
    "多重人格": "多重意识体",
    "多重人格障碍": "多重意识体",
    "多重系统": "多重意识体",
    "多重意识体系统": "多重意识体",
    "分离性身份障碍": "解离性身份障碍",
    "分离性身份辨识障碍": "解离性身份障碍",
    "解离症状": "解离",
    "解离状态": "解离",
    "解离体验": "解离",
    "心理创伤": "创伤",
    "创伤事件": "创伤",
    "复杂创伤": "创伤",
    "创伤后压力症候群": "创伤后应激障碍 PTSD",
    "创伤后应激症候群": "创伤后应激障碍 PTSD",
    "创伤后应激障碍": "创伤后应激障碍 PTSD",
    "创伤后应激障碍 (PTSD)": "创伤后应激障碍 PTSD",
    "PTSD": "创伤后应激障碍 PTSD",
    "ptsd": "创伤后应激障碍 PTSD",
    "DID": "解离性身份障碍 DID",
    "did": "解离性身份障碍 DID",
    "osdd": "其他特定解离性障碍 OSDD",
    "OSDD": "其他特定解离性障碍 OSDD",
    "admin": "管理者",
    "Admin": "管理者",
    "adaptive": "适应型",
    "Adaptive": "适应型",
    "内在世界": "系统内空间",
    "内在空间": "系统内空间",
    "守门者": "守门人",
    "守门员": "守门人",
    "保护者": "防御者",
    "守护者": "防御者",
    "融合": "整合",
    "治疗": "治疗支持",
    "支持网络": "社会支持",
    "安全计划": "安全策略",
    "地面化": "地面化练习",
    "冥想": "冥想练习",
    "冥想练习": "冥想",
    "正念冥想": "正念",
    "正念训练": "正念",
    "述情障碍": "述情障碍",
    "述情困难": "述情障碍",
    "alexithymia": "述情障碍",
    "dissociation": "解离",
    "anxiety": "焦虑",
    "alcohol-induced": "醉酒解离",
    "alcohol induced": "醉酒解离",
    "another": "解离性身份障碍 DID",
    "adhd": "注意力缺陷多动障碍 ADHD",
    "ADHD": "注意力缺陷多动障碍 ADHD",
    "注意缺陷多动障碍": "注意力缺陷多动障碍 ADHD",
    "注意缺陷多动症": "注意力缺陷多动障碍 ADHD",
    "形成背景": "创伤",
    "创伤经历": "创伤",
    "常见体验": "系统体验与机制",
    "支持与自我照顾建议": "自我照护",
    "风险提示": "风险应对",
    "风险应对": "风险应对",
    "跨语境沟通": "沟通协作",
    "知识与访问优势": "记忆管理",
    "社群用法": "社区文化",
    "沟通工具": "沟通协作",
    "统称概念": "身份认同",
    "特殊认同": "身份认同",
    "认同范围": "身份认同",
    "自我照护": "自我照护",
    "社会文化因素": "社会文化",
    "表现": "媒体呈现",
    "悬疑结构": "叙事结构",
    "身份认同": "身份认同",
    "外部介入": "治疗支持",
    "双重人格 类作品的": "媒体呈现",
    "概述": "基础概念",
    "模型": "理论模型",
    "模型概述": "理论模型",
    "鉴别": "诊断与临床",
    "结构性解离的层级": "结构性解离",
    "社群与系统语境下的讨论": "社区文化",
    "是否存在摄入": "物质影响",
    "感知离散化": "感知体验",
    "运动与语言迟缓": "躯体化",
    "角色间的交叠": "内部角色互动",
    "沟通目的": "沟通协作",
    "防御与角色分化": "防御机制",
    "躯体症状及慢性疾病": "躯体化",
    "教育与家庭支持": "教育支持",
    "多动 冲动": "行为特征",
    "功能受损": "功能评估",
    "领导者 系统组织者": "系统角色与类型",
    "维持运作": "系统管理",
    "社区语境": "社区文化",
    "解离性诊断关联": "诊断与临床",
    "与临床术语的区分": "诊断与临床",
    "沟通协调": "沟通协作",
    "处理方式不同": "应对策略",
    "多来源解释": "身份认同",
    "与性别 性倾向的区别": "身份认同",
    "常见叙事模式": "叙事结构",
    "评估重点": "诊断与临床",
    "流动性": "系统体验与机制",
    "功能分工": "系统角色与类型",
    "意识特征": "系统体验与机制",
    "语言敏感性": "沟通协作",
    "外部披露": "沟通协作",
    "同意与界限": "内部界限",
    "临床描述": "诊断与临床",
    "与其他标签的关系": "分类与对比",
    "核心要点": "基础概念",
    "多意识体视角": "媒体呈现",
    "关联词条": "媒体呈现",
}

STOP_TAGS = {
    "简介",
    "定义",
    "参考",
    "参考资料",
    "参考文献",
    "相关条目",
    "模板",
    "条目",
    "外部链接",
    "目录",
    "更新",
    "同义词",
    "延伸阅读",
    "注释",
}

HEADING_SKIP_PREFIXES = (
    "与",
    "在",
    "于",
    "用于",
    "用以",
    "作为",
    "针对",
    "围绕",
    "关于",
    "包含",
    "通过",
)

HEADING_SKIP_SUFFIXES = (
    "的比较",
    "的区别",
    "的区分",
    "的并列",
    "的交集",
    "的联系",
    "的关系",
)

MIN_TAGS = 3
MAX_TAGS = 8

ALLOWED_ASCII_TAGS = {
    "DID",
    "OSDD",
    "PTSD",
    "CPTSD",
    "DPDR",
    "ADHD",
    "BPD",
    "NPD",
    "SSD",
    "ANP",
    "EP",
}

CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
ASCII_RE = re.compile(r"[A-Za-z]")

PRIMARY_TAG_PRIORITY = {
    "多重意识体": 10,
    "解离": 9,
    "创伤": 9,
    "解离性身份障碍 DID": 8,
    "其他特定解离性障碍 OSDD": 8,
    "创伤后应激障碍 PTSD": 8,
    "系统体验": 7,
    "系统角色与类型": 7,
    "实践与支持": 6,
    "治疗支持": 6,
}

REF_SECTION_RE = re.compile(
    r"\n## (参考(资料|文献|来源)?|注释|外部链接)",
    re.IGNORECASE,
)

RELATED_BLOCK_RE = re.compile(r"^## 相关条目\b.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)

ps = PorterStemmer()


@dataclass
class SimplePost:
    metadata: MutableMapping[str, object]
    order: List[str]
    content: str


@dataclass
class PostRecord:
    path: Path
    title: str
    tags: List[str]
    tokens: Counter


def _format_frontmatter_line(key: str, value: object) -> str:
    if isinstance(value, list):
        joined = ", ".join(str(v) for v in value)
        return f"{key}: [{joined}]"
    return f"{key}: {value}"


def _simple_parse_frontmatter(text: str) -> Tuple[MutableMapping[str, object], List[str], str]:
    if not text.startswith("---"):
        return OrderedDict(), [], text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return OrderedDict(), [], text
    fm_text = match.group(1)
    body = text[match.end():]
    if yaml is not None:
        data = yaml.safe_load(fm_text) or {}
        if not isinstance(data, dict):
            data = {}
        order = list(data.keys())
        metadata = OrderedDict((k, data[k]) for k in order)
    else:
        metadata = OrderedDict()
        order: List[str] = []
        for raw_line in fm_text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                items = []
                if inner:
                    for part in inner.split(","):
                        item = part.strip().strip('"\'')
                        if item:
                            items.append(item)
                metadata[key] = items
            else:
                metadata[key] = value.strip('"\'')
            order.append(key)
    return metadata, order, body


def _simple_load(path: Path) -> SimplePost:
    raw = path.read_text(encoding="utf-8")
    metadata, order, body = _simple_parse_frontmatter(raw)
    return SimplePost(metadata=metadata, order=order, content=body)


def _simple_dump(post: SimplePost) -> str:
    lines = ["---"]
    seen = set()
    for key in post.order:
        value = post.metadata.get(key)
        if value is None:
            continue
        lines.append(_format_frontmatter_line(key, value))
        seen.add(key)
    for key, value in post.metadata.items():
        if key in seen or value is None:
            continue
        lines.append(_format_frontmatter_line(key, value))
    lines.append("---")
    body = post.content.lstrip("\n")
    return "\n".join(lines) + "\n\n" + body


def _ensure_order(post: object, key: str) -> None:
    if hasattr(post, "order"):
        order = getattr(post, "order")
        if isinstance(order, list) and key not in order:
            order.append(key)


def normalize_tag(tag: str) -> str:
    tag = tag.strip()
    if not tag:
        return ""
    tag = tag.replace("　", " ")
    tag = re.sub(r"[\u3000\u200b]+", " ", tag)
    tag = re.sub(r"[，,。；;：:！!？?（）()\[\]【】<>《》“”\"'·•…、/\\|]+", " ", tag)
    tag = re.sub(r"\s+", " ", tag).strip()
    ascii_candidate = unidecode(tag)
    if ascii_candidate and re.fullmatch(r"[A-Za-z0-9\- ]+", ascii_candidate):
        tag = ascii_candidate
    if not tag:
        return ""
    lower_tag = tag.lower()
    if lower_tag in SYN_MAP:
        tag = SYN_MAP[lower_tag]
    else:
        tag = SYN_MAP.get(tag, tag)
    if re.fullmatch(r"[A-Za-z0-9\- ]+", tag):
        upper = tag.upper()
        if len(upper.replace(" ", "")) <= 6:
            tag = upper
        else:
            tag = upper.title()
    return tag


def cut_chinese(text: str) -> Iterable[str]:
    if jieba is not None:
        yield from jieba.cut(text, cut_all=False)
    else:
        for match in re.finditer(r"[\u4e00-\u9fff]{2,}", text):
            yield match.group(0)


def extract_keyword_candidates(text: str, top_k: int = 15) -> Iterable[Tuple[str, float]]:
    if jieba_analyse is not None:
        yield from jieba_analyse.extract_tags(text, topK=top_k, withWeight=True)
        return
    freq: Counter[str] = Counter()
    for token in cut_chinese(text):
        if len(token) < 2:
            continue
        freq[token] += 1
    for match in re.finditer(r"[A-Za-z]{2,}", text):
        freq[match.group(0).lower()] += 1
    total = sum(freq.values()) or 1
    for word, count in freq.most_common(top_k):
        yield word, count / total


def is_valid_tag(tag: str) -> bool:
    if not tag:
        return False
    if tag in STOP_TAGS:
        return False
    if len(tag) > 18:
        return False
    if re.fullmatch(r"\d+(?:年|年代)?", tag):
        return False
    has_cn = bool(CHINESE_RE.search(tag))
    has_en = bool(ASCII_RE.search(tag))
    if has_cn and has_en:
        ascii_letters = "".join(ch for ch in tag if ch.isalpha())
        if ascii_letters and not ascii_letters.isupper():
            return False
    if has_cn and " " in tag:
        parts = [part for part in tag.split(" ") if part]
        if parts and all(CHINESE_RE.search(part) for part in parts):
            return False
    if not has_cn and has_en:
        condensed = tag.replace("-", "").replace(" ", "")
        if condensed in ALLOWED_ASCII_TAGS:
            return True
        return False
    return True


def should_skip_heading_tag(tag: str) -> bool:
    if re.fullmatch(r"\d+(?:年|年代)?", tag):
        return True
    for prefix in HEADING_SKIP_PREFIXES:
        if tag.startswith(prefix) and len(tag) > len(prefix):
            return True
    for suffix in HEADING_SKIP_SUFFIXES:
        if tag.endswith(suffix):
            return True
    return False


def tokenize_for_similarity(text: str) -> Counter:
    tokens: List[str] = []
    # 中文分词
    for word in cut_chinese(text):
        word = word.strip()
        if len(word) < 2:
            continue
        if re.fullmatch(r"[\d]+", word):
            continue
        normalized = normalize_tag(word)
        if not normalized or len(normalized) == 1:
            continue
        tokens.append(normalized)
    # 英文词干
    for match in re.finditer(r"[A-Za-z]+", text):
        w = match.group(0).lower()
        stem = ps.stem(w)
        if len(stem) < 2:
            continue
        tokens.append(stem)
    counter = Counter(tokens)
    return counter


def cosine_similarity(counter_a: Counter, counter_b: Counter) -> float:
    if not counter_a or not counter_b:
        return 0.0
    intersection = set(counter_a) & set(counter_b)
    numerator = sum(counter_a[t] * counter_b[t] for t in intersection)
    if numerator == 0:
        return 0.0
    norm_a = math.sqrt(sum(v * v for v in counter_a.values()))
    norm_b = math.sqrt(sum(v * v for v in counter_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return numerator / (norm_a * norm_b)


def extract_synonym_line(line: str) -> Iterable[str]:
    line = line.split("：", 1)[-1]
    for sep in ["，", "、", ",", "/", "|", "或", ";", "；"]:
        line = line.replace(sep, " ")
    for token in line.split():
        cleaned = normalize_tag(token)
        if cleaned:
            yield cleaned


def collect_candidates(post: frontmatter.Post) -> Dict[str, float]:
    candidates: Dict[str, float] = defaultdict(float)

    def add_candidate(raw: object, weight: float = 1.0, source: str = "generic") -> None:
        if raw is None:
            return
        if not isinstance(raw, str):
            raw = str(raw)
        raw = raw.strip()
        if not raw:
            return
        if "#" in raw:
            raw = raw.replace("#", "").strip()
            if not raw:
                return
        if CHINESE_RE.search(raw) and ASCII_RE.search(raw) and re.search(r"\s", raw):
            for part in re.split(r"[\s/、，,]+", raw):
                if part and part != raw:
                    add_candidate(part, weight * 0.6)
            return
        tag = normalize_tag(raw)
        if not is_valid_tag(tag):
            return
        if source in {"heading", "list_key"} and should_skip_heading_tag(tag):
            return
        candidates[tag] += weight

    tags_meta = post.metadata.get("tags", [])
    if isinstance(tags_meta, str):
        tags_meta = [tags_meta]
    for tag in tags_meta or []:
        add_candidate(tag, 2.5, source="metadata")

    title = str(post.metadata.get("title", ""))
    if title:
        if len(title) <= 12:
            add_candidate(title, 1.5, source="title")
        m = re.match(r"([^（(]+)", title)
        if m:
            add_candidate(m.group(1), 2.0, source="title")
        inner = re.findall(r"[（(]([^）)]+)[）)]", title)
        for part in inner:
            for token in re.split(r"[，、/,\s]+", part):
                add_candidate(token, 1.8, source="title_inner")

    content = post.content
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if re.search(r"同义词|别称|亦称", stripped):
            for tag in extract_synonym_line(stripped):
                add_candidate(tag, 2.2, source="synonym")
        if stripped.startswith("## "):
            heading = stripped[3:]
            add_candidate(heading, 0.8, source="heading")
        if stripped.startswith("- **") and "：" in stripped:
            key = stripped.split("：", 1)[0]
            key = re.sub(r"[-*\s]+", "", key)
            key = key.strip("*")
            add_candidate(key, 0.9, source="list_key")

    summary_segment = "\n".join(lines[:20])
    for word, weight in extract_keyword_candidates(summary_segment, top_k=15):
        add_candidate(word, weight, source="keyword")

    for tag, priority in PRIMARY_TAG_PRIORITY.items():
        if tag in candidates:
            candidates[tag] += priority

    return candidates


def pick_tags(post: frontmatter.Post) -> List[str]:
    candidates = collect_candidates(post)
    if not candidates:
        return []
    sorted_tags = sorted(
        candidates.items(), key=lambda item: (item[1], item[0]), reverse=True
    )
    tags: List[str] = []
    for tag, _score in sorted_tags:
        if tag in tags:
            continue
        tags.append(tag)
        if len(tags) >= MAX_TAGS:
            break
    if len(tags) < MIN_TAGS:
        for tag in PRIMARY_TAG_PRIORITY:
            if tag not in tags:
                tags.append(tag)
            if len(tags) >= MIN_TAGS:
                break
    return tags[:MAX_TAGS]


def compute_related(
    all_posts: Dict[Path, PostRecord],
    cur_path: Path,
    cur_tags: Sequence[str],
) -> List[Tuple[Path, float]]:
    cur_record = all_posts[cur_path]
    cur_tag_set = set(cur_tags)
    results: List[Tuple[Path, float]] = []

    for other_path, record in all_posts.items():
        if other_path == cur_path:
            continue
        other_tags = set(record.tags)
        intersection = len(cur_tag_set & other_tags)
        union = len(cur_tag_set | other_tags) or 1
        jaccard = intersection / union
        cos = cosine_similarity(cur_record.tokens, record.tokens)
        score = 0.55 * jaccard + 0.30 * cos
        if cur_path.parent == other_path.parent:
            score += 0.15
        if score <= 0:
            continue
        results.append((other_path, score))

    results.sort(key=lambda item: item[1], reverse=True)
    if len(results) < 2:
        # 放宽条件，保留得分最高的若干条
        all_sorted = sorted(
            ((p, 0.01) for p in all_posts if p != cur_path),
            key=lambda x: str(x[0]),
        )
        for item in all_sorted:
            if item[0] == cur_path:
                continue
            results.append(item)
            if len(results) >= 8:
                break
    return results[:8]


def render_related_block(rel_list: List[Tuple[Path, float]], lookup: Dict[Path, PostRecord]) -> str:
    lines = ["## 相关条目", ""]
    for rel_path, _score in rel_list:
        record = lookup[rel_path]
        title = record.title or rel_path.stem
        lines.append(f"- [{title}](/{rel_path.as_posix()})")
    lines.append("")
    return "\n".join(lines)


def upsert_related_block(markdown_text: str, block: str) -> str:
    if RELATED_BLOCK_RE.search(markdown_text):
        return RELATED_BLOCK_RE.sub(block, markdown_text, count=1)
    match = REF_SECTION_RE.search(markdown_text)
    if match:
        insert_pos = match.start()
        before = markdown_text[:insert_pos].rstrip()
        after = markdown_text[insert_pos:]
        return before + "\n\n" + block + "\n\n" + after.lstrip()
    return markdown_text.rstrip() + "\n\n" + block + "\n"


def load_markdown(path: Path):
    if frontmatter is not None:
        return frontmatter.load(path)
    return _simple_load(path)


def dump_post(post: object) -> str:
    if frontmatter is not None:
        return frontmatter.dumps(post)
    if isinstance(post, SimplePost):
        return _simple_dump(post)
    raise TypeError("Unsupported post type for dumping")


def select_files(args: argparse.Namespace) -> Tuple[List[Path], List[Path]]:
    all_files = sorted(ENTRIES_DIR.rglob("*.md"))
    if args.only:
        targets = [ROOT / Path(p) for p in args.only]
    else:
        targets = list(all_files)
        if args.since:
            git_cmd = [
                "git",
                "diff",
                "--name-only",
                f"{args.since}..HEAD",
                "--",
                "entries",
            ]
            result = subprocess.run(
                git_cmd, cwd=ROOT, capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                candidates = {
                    ROOT / Path(line.strip())
                    for line in result.stdout.splitlines()
                    if line.strip()
                }
                if candidates:
                    targets = [p for p in targets if p in candidates]
    if args.limit:
        targets = targets[: args.limit]
    return all_files, targets


def process(args: argparse.Namespace) -> None:
    all_files, target_files = select_files(args)
    if not target_files:
        print("未找到需要处理的词条。")
        return

    records: Dict[Path, PostRecord] = {}

    for path in all_files:
        post = load_markdown(path)
        tags = pick_tags(post)
        title = str(post.metadata.get("title", path.stem))
        tokens = tokenize_for_similarity(title + "\n" + post.content)
        rel_path = path.relative_to(ROOT)
        record = PostRecord(path=rel_path, title=title, tags=tags, tokens=tokens)
        records[rel_path] = record

    for path in target_files:
        rel_path = path.relative_to(ROOT)
        path = ROOT / rel_path
        post = load_markdown(path)
        tags = records[rel_path].tags
        post.metadata["tags"] = tags
        _ensure_order(post, "tags")

        related = compute_related(records, rel_path, tags)
        block = render_related_block(related, records)
        updated_content = upsert_related_block(post.content, block)
        post.content = updated_content

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "path": rel_path.as_posix(),
                        "tags": tags,
                        "related": [p.as_posix() for p, _ in related],
                    },
                    ensure_ascii=False,
                )
            )
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(dump_post(post))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="批量重建词条标签与相关条目")
    parser.add_argument("--dry-run", action="store_true", help="仅打印结果，不写回文件")
    parser.add_argument("--limit", type=int, default=0, help="限制处理的文件数量")
    parser.add_argument("--only", nargs="*", help="仅处理指定词条路径（entries/...）")
    parser.add_argument(
        "--since",
        help="仅处理自指定 Git 基准以来有变更的词条，可传入 commit、tag 或日期字符串",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    process(args)


if __name__ == "__main__":
    main()
