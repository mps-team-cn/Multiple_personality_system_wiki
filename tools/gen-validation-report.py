#!/usr/bin/env python3
"""Generate validation report for entries based on project guidelines."""
from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.pdf_export.pdf_export.frontmatter import FrontmatterError, load_entry_document
ENTRIES_DIR = ROOT / "docs" / "entries"
TEMPLATE_PATH = ROOT / "docs" / "TEMPLATE_ENTRY.md"
REPORT_PATH = ROOT / "docs" / "VALIDATION_REPORT.md"
CONTRIBUTING_PATH = ROOT / "docs" / "contributing" / "index.md"

Heading = Tuple[int, str]


def _load_text(path: Path) -> Sequence[str]:
    """Read a text file and return stripped lines."""
    return path.read_text(encoding="utf-8").splitlines()


def extract_diagnosis_template_headings(lines: Sequence[str]) -> List[Heading]:
    """Extract heading definitions from the diagnosis template section."""
    headings: List[Heading] = []
    in_section = False
    in_code_block = False
    heading_pattern = re.compile(r"^(#+)\s+(.+?)\s*$")

    for line in lines:
        striped = line.strip()
        if striped.startswith("```"):
            if in_section:
                in_code_block = not in_code_block
            continue
        if in_code_block:
            match = heading_pattern.match(line)
            if not match:
                continue
            level = len(match.group(1))
            title = match.group(2).strip()
            if not title or title.startswith("条目中文名"):
                # 一级标题在其它检查中处理，此处忽略模板中的演示标题
                continue
            headings.append((level, title))
            continue
        if line.startswith("## "):
            in_section = striped == "## 诊断与临床"
            in_code_block = False
            continue
        if not in_section:
            continue
    return headings


def collect_headings(lines: Sequence[str]) -> List[Heading]:
    """Collect markdown headings from a document."""
    pattern = re.compile(r"^(#+)\s+(.+?)\s*$")
    results: List[Heading] = []
    for raw in lines:
        match = pattern.match(raw)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        results.append((level, title))
    return results


def check_title_format(headings: Sequence[Heading]) -> List[str]:
    """Validate the first level-1 heading according to CONTRIBUTING rules."""
    issues: List[str] = []
    first_heading = next((item for item in headings if item[0] == 1), None)
    if first_heading is None:
        issues.append("缺少一级标题（# 标题）")
        return issues
    text = first_heading[1]
    if "（" not in text or "）" not in text:
        issues.append("一级标题未包含“中文名（English/缩写）”格式的全角括号")
    return issues


def build_report(
    title_issues: Dict[Path, List[str]],
    structure_issues: Dict[Path, List[str]],
    template_headings: Sequence[Heading],
) -> str:
    """Assemble the markdown validation report."""
    now = _dt.datetime.now().astimezone()
    heading_labels = [f"{'#' * level} {title}" for level, title in template_headings]

    lines: List[str] = []
    lines.append("# 自动校对报告")
    lines.append("")
    lines.append(f"生成时间：{now.isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(
        "本报告依据《CONTRIBUTING.md》与《docs/TEMPLATE_ENTRY.md》自动生成，用于辅助校对。"
    )
    lines.append("")
    lines.append("## 检查范围")
    lines.append("- `entries/` 目录下的全部 Markdown 词条")
    lines.append(
        "- 一级标题格式需符合《CONTRIBUTING.md》要求：`中文名（English/缩写）`"
    )
    lines.append("- Frontmatter 含 `诊断与临床` 标签的词条额外检查模板章节：")
    for label in heading_labels:
        lines.append(f"  - {label}")
    lines.append("")

    if not title_issues and not structure_issues:
        lines.append("当前未检测到结构性问题。👏")
        return "\n".join(lines) + "\n"

    if title_issues:
        lines.append("## 一级标题格式问题")
        for path in sorted(title_issues):
            display = path.as_posix()
            for issue in title_issues[path]:
                lines.append(f"- `{display}`：{issue}")
        lines.append("")

    if structure_issues:
        lines.append("## 诊断与临床结构缺失")
        for path in sorted(structure_issues):
            display = path.as_posix()
            missing = structure_issues[path]
            lines.append(f"- `{display}`")
            lines.append("  - 缺失章节：" + ", ".join(missing))
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    if not CONTRIBUTING_PATH.exists():
        raise FileNotFoundError(f"未找到贡献指南：{CONTRIBUTING_PATH}")
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"未找到词条模板：{TEMPLATE_PATH}")

    template_lines = _load_text(TEMPLATE_PATH)
    template_headings = extract_diagnosis_template_headings(template_lines)

    title_issues: Dict[Path, List[str]] = {}
    structure_issues: Dict[Path, List[str]] = {}

    template_lookup = {
        (level, title): f"{'#' * level} {title}" for level, title in template_headings
    }

    for md_path in sorted(ENTRIES_DIR.glob("*.md")):
        try:
            document = load_entry_document(md_path)
        except FrontmatterError as error:  # pragma: no cover - 配置异常时失败
            raise RuntimeError(f"解析 {md_path} 的 Frontmatter 失败: {error}") from error

        lines = document.body.splitlines()
        headings = collect_headings(lines)
        issues = check_title_format(headings)
        if issues:
            title_issues[md_path.relative_to(ROOT)] = issues

        if "诊断与临床" not in document.tags:
            continue

        present = {(level, title) for level, title in headings if level >= 2}
        missing_labels: List[str] = []
        for item, label in template_lookup.items():
            if item not in present:
                missing_labels.append(label)
        if missing_labels:
            structure_issues[md_path.relative_to(ROOT)] = missing_labels

    report_text = build_report(title_issues, structure_issues, template_headings)
    REPORT_PATH.write_text(report_text, encoding="utf-8")


if __name__ == "__main__":
    main()
