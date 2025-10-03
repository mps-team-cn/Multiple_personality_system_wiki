"""词条标签重生成与相关条目维护脚本。

该脚本将遍历 `entries/` 目录下的所有 Markdown 词条，依据规范化的标签词表与内容相似度
自动生成 Front Matter 中的 `tags` 字段，并重写 `## 相关条目` 段落。运行后会在
`scripts/output/` 目录下生成汇总报告，便于人工复核。

主要能力：

* 依据标题、段落及正文中的关键词为词条打分，筛选规范化标签；
* 融合互链与文本相似度信息补充候选标签；
* 综合标签重叠、标题相似度、互链共现以及目录位置计算相关条目得分；
* 覆盖写回 Front Matter 与相关条目段落，保持正文其他内容不变；
* 输出 JSONL 与 Markdown 报告文件。

用法：

```bash
python scripts/retag_and_related/run.py
```

执行前建议在独立分支中操作，运行后请抽查部分词条确认结果合理。
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[2]
ENTRIES_DIR = ROOT / "entries"
OUTPUT_DIR = ROOT / "scripts" / "output"

TAG_SCORE_THRESHOLD = 1.2
TAG_LIMIT = 6
SIMILARITY_THRESHOLD = 0.82
RELATED_LIMIT = 5
RELATED_BASE_THRESHOLD = 0.35
RELATED_FALLBACK_THRESHOLD = 0.25
MAX_INHERITED_TAGS = 2

# 规范化标签词表。alias: 同义词；kw: 关键词命中。
CANONICAL_TAGS: Dict[str, Dict[str, Sequence[str]]] = {
    # 诊断与临床
    "DID": {
        "alias": ["解离性身份障碍", "多重人格", "Dissociative Identity Disorder"],
        "kw": ["DID", "解离性身份", "多重人格"],
    },
    "Partial-DID": {
        "alias": ["部分解离", "Partial DID"],
        "kw": ["Partial DID", "部分解离"],
    },
    "OSDD": {
        "alias": ["其他特定解离障碍", "OSDD-1", "OSDD1"],
        "kw": ["OSDD", "其他特定解离", "OSDD-1"],
    },
    "PTSD": {
        "alias": ["创伤后应激障碍"],
        "kw": ["PTSD", "创伤后应激"],
    },
    "CPTSD": {
        "alias": ["复杂性创伤后应激障碍", "复杂性PTSD"],
        "kw": ["CPTSD", "复杂性创伤"],
    },
    "DRD": {
        "alias": ["去人格/现实解体", "去人格", "现实解体", "DPDR", "去人格化"],
        "kw": ["DRD", "去人格", "现实解体", "DPDR"],
    },
    "BPD": {
        "alias": ["边缘型人格障碍"],
        "kw": ["BPD", "边缘型人格"],
    },
    "抑郁": {
        "alias": ["抑郁症", "抑郁障碍"],
        "kw": ["抑郁", "抑郁症"],
    },
    "双相": {
        "alias": ["双相情感障碍", "躁郁症"],
        "kw": ["双相", "躁郁"],
    },
    "评估": {
        "alias": ["评估量表", "assessment"],
        "kw": ["评估", "量表", "assessment"],
    },
    "鉴别诊断": {
        "alias": ["鉴别", "differential diagnosis"],
        "kw": ["鉴别诊断"],
    },
    "DSM-5-TR": {
        "alias": ["DSM5-TR", "DSM-5"],
        "kw": ["DSM", "DSM-5-TR"],
    },
    "ICD-11": {
        "alias": ["ICD11"],
        "kw": ["ICD-11"],
    },
    # 系统体验与机制
    "切换": {
        "alias": ["切换/转换", "转换"],
        "kw": ["切换", "转换", "switch"],
    },
    "共识": {
        "alias": ["共在", "co-consciousness", "co-conscious"],
        "kw": ["共识", "共在", "co-conscious"],
    },
    "旁观": {
        "alias": ["共驾", "陪驾"],
        "kw": ["旁观", "共驾"],
    },
    "触发": {
        "alias": ["trigger"],
        "kw": ["触发", "trigger"],
    },
    "内在空间": {
        "alias": ["内心空间", "内世界"],
        "kw": ["内在空间", "内部空间"],
    },
    "记忆共享": {
        "alias": ["记忆共享/失忆", "记忆传递"],
        "kw": ["记忆共享", "共享记忆"],
    },
    "失忆": {
        "alias": ["解离性失忆"],
        "kw": ["失忆", "断片"],
    },
    "共在": {
        "alias": ["共同在场"],
        "kw": ["共在"],
    },
    # 系统角色与类型
    "守门人": {
        "alias": ["gatekeeper"],
        "kw": ["守门人", "gatekeeper"],
    },
    "保护者": {
        "alias": ["保护者/防御者"],
        "kw": ["保护者"],
    },
    "迫害者": {"alias": [], "kw": ["迫害者"]},
    "照顾者": {"alias": ["照料者"], "kw": ["照顾者"]},
    "执行者": {"alias": ["执行角色"], "kw": ["执行者"]},
    "初始持有者": {
        "alias": ["主控", "原主", "host"],
        "kw": ["初始持有者", "主控", "host"],
    },
    "儿童人格": {
        "alias": ["儿童人格/青少年", "little"],
        "kw": ["儿童人格", "little"],
    },
    "偏重": {
        "alias": ["median"],
        "kw": ["偏重", "median"],
    },
    "tulpa": {
        "alias": ["图帕"],
        "kw": ["tulpa", "图帕"],
    },
    # 实践与支持
    "接地": {
        "alias": ["grounding"],
        "kw": ["接地", "grounding"],
    },
    "冥想": {
        "alias": ["meditation"],
        "kw": ["冥想", "meditation"],
    },
    "自助练习": {
        "alias": ["自我照顾"],
        "kw": ["自助练习", "自我照顾"],
    },
    "安全计划": {"alias": ["safety plan"], "kw": ["安全计划"]},
    "同伴支持": {
        "alias": ["peer support"],
        "kw": ["同伴支持", "peer support"],
    },
    "治疗关系": {
        "alias": ["治疗联盟", "治疗师关系"],
        "kw": ["治疗关系", "治疗联盟"],
    },
    "伦理": {
        "alias": ["伦理风险"],
        "kw": ["伦理", "风险"],
    },
    # 虚拟角色与文艺再现
    "文艺再现": {
        "alias": ["影视再现", "叙事与误读"],
        "kw": ["文艺", "影视", "叙事"],
    },
    # 方法与资源
    "术语表": {
        "alias": ["术语", "术语表/词汇"],
        "kw": ["术语表", "术语"],
    },
    "模板": {
        "alias": ["条目模板"],
        "kw": ["模板", "条目模板"],
    },
    "贡献规范": {
        "alias": ["贡献指南"],
        "kw": ["贡献规范", "贡献指南"],
    },
    "导出": {
        "alias": ["PDF"],
        "kw": ["导出", "PDF"],
    },
}

LOWER_REPLACEMENTS = {
    "partial did": "Partial-DID",
    "partial-did": "Partial-DID",
    "dpdr": "DRD",
    "dr/dp": "DRD",
    "drd": "DRD",
    "co-consciousness": "共识",
    "co consciousness": "共识",
    "co-conscious": "共识",
    "median": "偏重",
    "little": "儿童人格",
    "host": "初始持有者",
    "safety plan": "安全计划",
    "peer support": "同伴支持",
    "grounding": "接地",
    "trigger": "触发",
    "tulpa": "tulpa",
    "gatekeeper": "守门人",
}

NOISE_TAG_PATTERN = re.compile(r"^(misc|其它|other|test|todo|\w)$", re.I)
ENTRY_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((entries/[^)]+?\.md)\)")
FRONT_MATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
TITLE_PATTERN = re.compile(r"^#\s+(.+)$", re.M)
HEADING_PATTERN = re.compile(r"^##\s+(.+)$", re.M)
RELATED_SECTION_PATTERN = re.compile(r"\n##\s*相关条目[\s\S]*?(?=\n##\s|\Z)", re.M)
TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


@dataclass
class EntryInfo:
    path: Path
    title: str
    headings: List[str]
    body: str
    meta: Dict[str, object]
    old_tags: List[str]
    normalized_old_tags: List[str]
    tokens: Counter
    title_tokens: Counter
    outgoing_links: List[str]

    def normalized_path(self) -> str:
        return self.path.as_posix()


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def split_front_matter(text: str) -> Tuple[Optional[str], str]:
    match = FRONT_MATTER_PATTERN.match(text)
    if match:
        return match.group(1), match.group(2)
    return None, text


def load_front_matter(raw: Optional[str]) -> Dict[str, object]:
    if raw is None:
        return {}
    try:
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            return {}
        return data
    except yaml.YAMLError:
        return {}


def normalize_tag(tag: str) -> str:
    cleaned = re.sub(r"\s+", " ", tag.strip())
    lower = cleaned.lower()
    if lower in LOWER_REPLACEMENTS:
        return LOWER_REPLACEMENTS[lower]
    for canonical, info in CANONICAL_TAGS.items():
        if cleaned == canonical:
            return canonical
        aliases = info.get("alias", [])
        if cleaned in aliases:
            return canonical
        alias_lower = [a.lower() for a in aliases]
        if lower in alias_lower:
            return canonical
    return cleaned


def is_noise_tag(tag: str) -> bool:
    return bool(NOISE_TAG_PATTERN.match(tag))


def tokenize(text: str) -> Counter:
    tokens = Counter()
    for match in TOKEN_PATTERN.finditer(text.lower()):
        token = match.group(0)
        if len(token) == 1 and not token.isalpha() and not token.isdigit():
            continue
        tokens[token] += 1
    return tokens


def extract_entry(path: Path) -> EntryInfo:
    text = path.read_text(encoding="utf-8", errors="ignore")
    raw_front_matter, body = split_front_matter(text)
    meta = load_front_matter(raw_front_matter)
    title_match = TITLE_PATTERN.search(body)
    title = title_match.group(1).strip() if title_match else path.stem
    headings = [m.strip() for m in HEADING_PATTERN.findall(body)]
    old_tags = list(meta.get("tags", []) if isinstance(meta.get("tags"), list) else [])
    normalized_old_tags = []
    for tag in old_tags:
        normalized = normalize_tag(str(tag))
        if normalized in CANONICAL_TAGS and normalized not in normalized_old_tags:
            normalized_old_tags.append(normalized)
    tokens = tokenize(" ".join([title] + headings) + "\n" + body)
    title_tokens = tokenize(title)
    outgoing_links = [clean_link_path(link) for link in ENTRY_LINK_PATTERN.findall(body)]
    return EntryInfo(
        path=path,
        title=title,
        headings=headings,
        body=body,
        meta=meta,
        old_tags=old_tags,
        normalized_old_tags=normalized_old_tags,
        tokens=tokens,
        title_tokens=title_tokens,
        outgoing_links=outgoing_links,
    )


def clean_link_path(link: str) -> str:
    normalized = Path(link).as_posix()
    return normalized


def build_catalog() -> List[EntryInfo]:
    entries = []
    for path in sorted(ENTRIES_DIR.rglob("*.md")):
        if path.name.startswith("." ):
            continue
        entries.append(extract_entry(path))
    return entries


def score_from_text(entry: EntryInfo) -> Counter:
    scores: Counter = Counter()

    def add_score(tag: str, weight: float, text: str) -> None:
        if not text:
            return
        pattern = re.compile(rf"\b{re.escape(tag)}\b", re.I)
        matches = pattern.findall(text)
        if matches:
            scores[tag] += weight * len(matches)

    title_text = entry.title
    heading_text = "\n" + "\n".join(entry.headings)
    body_text = entry.body

    for canonical, info in CANONICAL_TAGS.items():
        keywords = set([canonical])
        keywords.update(info.get("alias", []))
        keywords.update(info.get("kw", []))
        for keyword in keywords:
            keyword_pattern = re.escape(keyword)
            if re.search(rf"\b{keyword_pattern}\b", title_text, re.I):
                scores[canonical] += 2.0
            heading_hits = re.findall(rf"\b{keyword_pattern}\b", heading_text, re.I)
            if heading_hits:
                scores[canonical] += 1.5 * len(heading_hits)
            body_hits = re.findall(rf"\b{keyword_pattern}\b", body_text, re.I)
            if body_hits:
                scores[canonical] += 1.0 * len(body_hits)

    for old_tag in entry.old_tags:
        normalized = normalize_tag(str(old_tag))
        if normalized in CANONICAL_TAGS:
            scores[normalized] += 1.2

    return scores


def compute_link_inheritance(entries: Sequence[EntryInfo]) -> Dict[str, List[str]]:
    normalized_map = {entry.normalized_path(): entry for entry in entries}
    inherited: Dict[str, List[str]] = defaultdict(list)
    for entry in entries:
        for link in entry.outgoing_links:
            target = normalized_map.get(link)
            if not target:
                continue
            for tag in target.normalized_old_tags[:MAX_INHERITED_TAGS]:
                inherited[entry.normalized_path()].append(tag)
    return inherited


def compute_tf_idf(entries: Sequence[EntryInfo]) -> Tuple[Dict[str, Dict[str, float]], Dict[str, float]]:
    df: Counter = Counter()
    doc_tokens: Dict[str, Counter] = {}
    for entry in entries:
        doc_tokens[entry.normalized_path()] = entry.tokens
        for token in entry.tokens:
            df[token] += 1

    n_docs = len(entries)
    idf: Dict[str, float] = {}
    for token, count in df.items():
        idf[token] = math.log((1 + n_docs) / (1 + count)) + 1

    tf_idf_vectors: Dict[str, Dict[str, float]] = {}
    for entry in entries:
        tokens = doc_tokens[entry.normalized_path()]
        total = sum(tokens.values()) or 1
        vector: Dict[str, float] = {}
        for token, freq in tokens.items():
            vector[token] = (freq / total) * idf[token]
        tf_idf_vectors[entry.normalized_path()] = vector

    return tf_idf_vectors, idf


def compute_title_tf_idf(entries: Sequence[EntryInfo]) -> Dict[str, Dict[str, float]]:
    df: Counter = Counter()
    vectors: Dict[str, Dict[str, float]] = {}
    for entry in entries:
        for token in entry.title_tokens:
            df[token] += 1

    n_docs = len(entries)
    idf: Dict[str, float] = {}
    for token, count in df.items():
        idf[token] = math.log((1 + n_docs) / (1 + count)) + 1

    for entry in entries:
        total = sum(entry.title_tokens.values()) or 1
        vector: Dict[str, float] = {}
        for token, freq in entry.title_tokens.items():
            vector[token] = (freq / total) * idf[token]
        vectors[entry.normalized_path()] = vector

    return vectors


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    common = set(vec_a).intersection(vec_b)
    numerator = sum(vec_a[token] * vec_b[token] for token in common)
    if not numerator:
        return 0.0
    norm_a = math.sqrt(sum(value * value for value in vec_a.values()))
    norm_b = math.sqrt(sum(value * value for value in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return numerator / (norm_a * norm_b)


def choose_tags(
    entry: EntryInfo,
    base_scores: Counter,
    inherited_tags: Dict[str, List[str]],
    similarity_tags: Dict[str, List[str]],
) -> List[str]:
    scores = Counter(base_scores)
    for tag in inherited_tags.get(entry.normalized_path(), []):
        scores[tag] += 0.8
    for tag in similarity_tags.get(entry.normalized_path(), []):
        scores[tag] += 0.6

    selected: List[str] = []
    for tag, score in scores.most_common():
        normalized = normalize_tag(tag)
        if normalized not in CANONICAL_TAGS:
            continue
        if score < TAG_SCORE_THRESHOLD:
            continue
        if normalized in selected:
            continue
        if is_noise_tag(normalized):
            continue
        selected.append(normalized)
        if len(selected) >= TAG_LIMIT:
            break
    return selected


def compute_similarity_tag_boost(
    entries: Sequence[EntryInfo],
    vectors: Dict[str, Dict[str, float]],
) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = defaultdict(list)
    for i, entry in enumerate(entries):
        vec_a = vectors.get(entry.normalized_path(), {})
        if not vec_a:
            continue
        similar_candidates: List[Tuple[float, EntryInfo]] = []
        for j, other in enumerate(entries):
            if i == j:
                continue
            vec_b = vectors.get(other.normalized_path(), {})
            if not vec_b:
                continue
            similarity = cosine_similarity(vec_a, vec_b)
            if similarity >= SIMILARITY_THRESHOLD:
                similar_candidates.append((similarity, other))
        similar_candidates.sort(key=lambda x: x[0], reverse=True)
        tags: List[str] = []
        for _, candidate in similar_candidates[:3]:
            for tag in candidate.normalized_old_tags:
                if tag not in tags:
                    tags.append(tag)
                if len(tags) >= MAX_INHERITED_TAGS:
                    break
            if len(tags) >= MAX_INHERITED_TAGS:
                break
        if tags:
            result[entry.normalized_path()] = tags
    return result


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def count_link_occurrences(body: str, target_path: str) -> int:
    pattern = re.compile(rf"\[[^\]]+\]\({re.escape(target_path)}\)")
    return len(pattern.findall(body))


def compute_related_candidates(
    entry: EntryInfo,
    all_entries: Sequence[EntryInfo],
    catalog_tags: Dict[str, List[str]],
    title_vectors: Dict[str, Dict[str, float]],
) -> List[Dict[str, object]]:
    me_path = entry.normalized_path()
    me_tags = set(catalog_tags.get(me_path, []))
    me_vec = title_vectors.get(me_path, {})
    me_dir = Path(me_path).parent

    candidates: List[Dict[str, object]] = []
    for other in all_entries:
        other_path = other.normalized_path()
        if other_path == me_path:
            continue
        if count_link_occurrences(entry.body, other_path) > 3:
            continue
        tags_b = set(catalog_tags.get(other_path, []))
        tag_overlap = jaccard(me_tags, tags_b)
        title_similarity = cosine_similarity(me_vec, title_vectors.get(other_path, {}))
        link_bonus = 0.0
        if other_path in entry.outgoing_links:
            link_bonus += 0.1
        if me_path in other.outgoing_links:
            link_bonus += 0.1
        directory_bonus = 0.05 if Path(other_path).parent == me_dir else 0.0
        score = 0.55 * tag_overlap + 0.25 * title_similarity + 0.10 * link_bonus + 0.10 * directory_bonus
        if score <= 0:
            continue
        candidates.append(
            {
                "path": other_path,
                "title": other.title,
                "score": score,
                "tag_overlap": tag_overlap,
                "title_similarity": title_similarity,
                "link_bonus": link_bonus,
                "directory_bonus": directory_bonus,
            }
        )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    selected: List[Dict[str, object]] = []
    threshold = RELATED_BASE_THRESHOLD
    for candidate in candidates:
        if candidate["score"] < threshold:
            continue
        selected.append(candidate)
        if len(selected) >= RELATED_LIMIT:
            break

    if len(selected) < 3:
        for candidate in candidates:
            if candidate in selected:
                continue
            if candidate["score"] < RELATED_FALLBACK_THRESHOLD:
                continue
            selected.append(candidate)
            if len(selected) >= RELATED_LIMIT:
                break

    return selected


def remove_related_section(body: str) -> str:
    return RELATED_SECTION_PATTERN.sub("\n", body)


def render_related_section(candidates: Sequence[Dict[str, object]]) -> str:
    if not candidates:
        return "\n## 相关条目\n- 暂无自动推荐（待人工补充）\n"
    lines = ["", "## 相关条目"]
    for candidate in candidates:
        reason_parts = [
            f"标签重叠={candidate['tag_overlap']:.2f}",
            f"标题相似度={candidate['title_similarity']:.2f}",
        ]
        if candidate["link_bonus"] > 0:
            reason_parts.append(f"互链共现={candidate['link_bonus']:.2f}")
        if candidate["directory_bonus"] > 0:
            reason_parts.append("同目录加成=0.05")
        reason = "；".join(reason_parts)
        lines.append(
            f"- [{candidate['title']}]({candidate['path']}) — 依据：{reason}"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def write_entry(entry: EntryInfo, tags: List[str], related: Sequence[Dict[str, object]]) -> None:
    new_meta = dict(entry.meta)
    new_meta["title"] = new_meta.get("title") or entry.title
    new_meta["tags"] = tags

    front_matter = "---\n" + yaml.safe_dump(new_meta, allow_unicode=True, sort_keys=False).strip() + "\n---\n"
    body_without_related = remove_related_section(entry.body).rstrip() + "\n\n"
    related_section = render_related_section(related)
    new_content = front_matter + body_without_related + related_section
    entry.path.write_text(new_content, encoding="utf-8")


def generate_reports(
    entries: Sequence[EntryInfo],
    final_tags: Dict[str, List[str]],
    related_data: Dict[str, List[Dict[str, object]]],
) -> None:
    ensure_output_dir()

    tag_report_lines = []
    related_report_lines = []
    changed_count = 0
    for entry in entries:
        path = entry.normalized_path()
        new_tags = final_tags[path]
        if entry.old_tags != new_tags:
            changed_count += 1
        tag_report_lines.append(
            json.dumps(
                {
                    "path": path,
                    "title": entry.title,
                    "old_tags": entry.old_tags,
                    "new_tags": new_tags,
                },
                ensure_ascii=False,
            )
        )
        related_report_lines.append(
            json.dumps(
                {
                    "path": path,
                    "title": entry.title,
                    "related": related_data.get(path, []),
                },
                ensure_ascii=False,
            )
        )

    (OUTPUT_DIR / "tag_report.jsonl").write_text("\n".join(tag_report_lines) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "related_report.jsonl").write_text("\n".join(related_report_lines) + "\n", encoding="utf-8")

    summary_lines = [
        "# 标签与相关条目自动化汇总",
        "",
        f"- 总计处理词条：{len(entries)}",
        f"- 标签发生变更：{changed_count}",
        f"- 相关条目已写回：{len(related_data)}",
        "",
        "## 人工复核建议",
        "- 抽查标签变化较大的条目，确认语义是否准确；",
        "- 对 `## 相关条目` 中得分接近阈值的条目进行人工校验；",
        "- 若某些重要词条未被 `index.md` 收录，请在后续 PR 中维护目录。",
    ]
    (OUTPUT_DIR / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def main() -> None:
    if not ENTRIES_DIR.exists():
        print("entries 目录不存在，已退出。", file=sys.stderr)
        sys.exit(1)

    ensure_output_dir()
    entries = build_catalog()
    if not entries:
        print("未找到任何词条。", file=sys.stderr)
        sys.exit(1)

    base_scores: Dict[str, Counter] = {}
    for entry in entries:
        base_scores[entry.normalized_path()] = score_from_text(entry)

    inherited_tags = compute_link_inheritance(entries)
    tf_idf_vectors, _ = compute_tf_idf(entries)
    title_vectors = compute_title_tf_idf(entries)
    similarity_tags = compute_similarity_tag_boost(entries, tf_idf_vectors)

    final_tags: Dict[str, List[str]] = {}
    for entry in entries:
        tags = choose_tags(
            entry,
            base_scores[entry.normalized_path()],
            inherited_tags,
            similarity_tags,
        )
        final_tags[entry.normalized_path()] = tags

    related_map: Dict[str, List[Dict[str, object]]] = {}
    for entry in entries:
        related_candidates = compute_related_candidates(entry, entries, final_tags, title_vectors)
        related_map[entry.normalized_path()] = related_candidates

    for entry in entries:
        write_entry(entry, final_tags[entry.normalized_path()], related_map[entry.normalized_path()])

    generate_reports(entries, final_tags, related_map)
    print("已完成标签与相关条目更新，并生成报告。")


if __name__ == "__main__":
    main()
