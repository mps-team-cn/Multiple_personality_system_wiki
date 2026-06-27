#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库干净版导出工具

将 docs/entries/*.md 转换为适合 qq-maid-bot KNOWLEDGE_DIR 的干净 Markdown：
  - 保留 Frontmatter 和正文知识
  - 删除导航章节（相关条目、参见、参考资料等）
  - 清理 MkDocs admonition 语法，保留有效正文
  - Markdown 链接转纯文字
  - 删除图片和脚注
  - 删除模板化站点免责声明

用法：
    uv run python3 tools/export_knowledge.py \\
        --input docs/entries \\
        --output dist/knowledge/entries

    make knowledge

多次执行结果稳定，不修改源文件。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set, Tuple


# ── 集中维护的模板文本列表 ──────────────────────────────────
# 这些是站点模板重复套话，在导出时删除。

TEMPLATE_TEXTS: List[str] = [
    # 标准免责声明 variants
    "本站资料仅供参考，不构成医疗建议。若需诊断或治疗，请联系持证专业人员。",
    "本站资料仅供参考，不构成医疗建议。若需诊断或治疗，请联系持证专业人员",
    "本站资料仅供参考,不构成医疗建议。若需诊断或治疗,请联系持证专业人员。",
    "如果您有紧急情况或需要专业帮助，请立即联系当地紧急服务或心理健康专业人员。",
    # 触发警告
    "内容涉及创伤、精神健康、自我认同等敏感议题，阅读时请留意自身状态。",
    "内容涉及创伤、精神健康、自我认同等敏感议题,阅读时请留意自身状态。",
]

TEMPLATE_TEXT_PATTERNS: List[re.Pattern] = [
    # 可配置的正则模式，用于匹配有细微变化的模板文本
    re.compile(
        r"本站资料仅供参考[，,]\s*不构成医疗建议[。.]\s*"
        r"若需诊断或治疗[，,]\s*请联系持证专业人员[。.]?"
    ),
    re.compile(
        r"如果您有紧急情况或需要专业帮助[，,]\s*"
        r"请立即联系当地紧急服务或心理健康专业人员[。.]?"
    ),
    re.compile(
        r"内容涉及创伤[、,]\s*精神健康[、,]\s*自我认同等敏感议题[，,]\s*"
        r"阅读时请留意自身状态[。.]?"
    ),
]


# ── 导航章节标题（删除该标题及其以下全部内容直到下一个同级/更高级标题） ──

NAV_SECTION_HEADINGS: List[re.Pattern] = [
    re.compile(r"^#{2,6}\s*相关条目\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*关联条目\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*参见\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*另见\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*See also\s*[#:：]*$", re.IGNORECASE),
]

REF_SECTION_HEADINGS: List[re.Pattern] = [
    re.compile(r"^#{2,6}\s*延伸阅读\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*参考与延伸阅读\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*参考文献\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*参考资料\s*[#:：\s]*$"),
    re.compile(r"^#{2,6}\s*外部链接\s*[#:：\s]*$"),
]

ALL_SECTION_HEADINGS: List[re.Pattern] = NAV_SECTION_HEADINGS + REF_SECTION_HEADINGS


# ── 统计报告 ──

@dataclass
class ExportStats:
    """单文件导出统计。"""
    nav_sections_removed: int = 0
    ref_sections_removed: int = 0
    links_converted: int = 0
    admonitions_cleaned: int = 0
    images_removed: int = 0
    footnotes_removed: int = 0
    template_texts_removed: int = 0
    error: Optional[str] = None

    def merge(self, other: ExportStats) -> None:
        self.nav_sections_removed += other.nav_sections_removed
        self.ref_sections_removed += other.ref_sections_removed
        self.links_converted += other.links_converted
        self.admonitions_cleaned += other.admonitions_cleaned
        self.images_removed += other.images_removed
        self.footnotes_removed += other.footnotes_removed
        self.template_texts_removed += other.template_texts_removed


# ── 核心处理 ──

def _is_heading(line: str) -> bool:
    """判断一行是否为 Markdown 标题。"""
    stripped = line.strip()
    return stripped.startswith("#") and stripped[0] == "#"


def _heading_level(line: str) -> int:
    """返回标题层级（1-6），不是标题返回 0。"""
    stripped = line.strip()
    if not (stripped.startswith("#") and stripped[0] == "#"):
        return 0
    level = 0
    for ch in stripped:
        if ch == "#":
            level += 1
        else:
            break
    return level


def _is_nav_heading(line: str) -> bool:
    """检查一行是否为需要删除的导航章节标题。"""
    for pattern in ALL_SECTION_HEADINGS:
        if pattern.match(line):
            return True
    return False


def _is_ref_heading(line: str) -> bool:
    """检查一行是否为参考/文献章节标题。"""
    for pattern in REF_SECTION_HEADINGS:
        if pattern.match(line):
            return True
    return False


def _clean_admonition_block(
    lines: List[str], start_idx: int, stats: ExportStats
) -> Tuple[List[str], int]:
    """
    处理 admonition 块（以 `!!!` 或 `???` 开头）。
    
    返回 (处理后行列表, 下一个要处理的行索引)。
    处理后行列表可能为空（空admonition）或包含去除缩进的正文。
    """
    line = lines[start_idx]
    stripped = line.rstrip()
    
    # 匹配 !!! type "title" 或 ??? type "title"
    m = re.match(r'^[!?]{3}\s+(\w+)(?:\s+"([^"]*)")?\s*$', stripped)
    if not m:
        # 可能是 !!! type 无标题
        m = re.match(r'^[!?]{3}\s+(\w+)\s*$', stripped)
    if not m:
        return [line], start_idx + 1  # fallback: 保持原样
    
    admon_type = m.group(1)
    _admon_title = m.group(2) if m.lastindex and m.lastindex >= 2 else ""
    
    # 收集正文行（缩进的内容）
    body_lines: List[str] = []
    idx = start_idx + 1
    indent: Optional[str] = None
    
    while idx < len(lines):
        l = lines[idx]
        if l.strip() == "":
            body_lines.append(l)
            idx += 1
            continue
        # 检测缩进
        leading_space = len(l) - len(l.lstrip())
        if leading_space < 4 and l.strip():
            # 缩进不足，说明 admonition 结束
            break
        if indent is None:
            indent = " " * leading_space
        # 去除共同缩进
        if indent and l.startswith(indent):
            body_lines.append(l[len(indent):])
        else:
            body_lines.append(l)
        idx += 1
    
    # 去除首尾空行
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    while body_lines and body_lines[-1].strip() == "":
        body_lines.pop()
    
    # 检查是否为纯模板文本
    body_text = " ".join(l.strip() for l in body_lines if l.strip())
    is_template = any(
        tmpl in body_text for tmpl in TEMPLATE_TEXTS
    ) or any(p.search(body_text) for p in TEMPLATE_TEXT_PATTERNS)
    
    if is_template:
        stats.template_texts_removed += 1
        stats.admonitions_cleaned += 1
        return [], idx
    
    if not body_lines:
        # 空 admonition
        stats.admonitions_cleaned += 1
        return [], idx
    
    stats.admonitions_cleaned += 1
    
    # 对 ??? 可折叠块（FAQ 问题），保留标题文字
    if stripped.startswith("???"):
        title = (_admon_title or "").strip()
        if title:
            body_lines.insert(0, f"**{title}**\n")
    
    return body_lines, idx


def _is_footnote_def(line: str) -> bool:
    """检查是否为脚注定义行如 [^ref]: ..."""
    return bool(re.match(r'^\[\^[^\]]+\]:\s*', line.strip()))


def _remove_images_from_line(line: str, stats: ExportStats) -> str:
    """
    从行中删除所有 Markdown 图片语法 ![...](...)，包括 SVG/PNG/JPG 等。
    返回处理后行内容（保留原始缩进）。
    """
    img_pattern = re.compile(r'!\[[^\]]*\]\([^)]+\)')
    new_line, count = img_pattern.subn("", line)
    stats.images_removed += count
    if count > 0:
        # 删除图片后清理多余空格，但保留缩进
        indent = line[:len(line) - len(line.lstrip())]
        rest = new_line.strip()
        return indent + rest if rest else ""
    return line


def _convert_links_in_line(line: str) -> Tuple[str, int]:
    """
    将行内 Markdown 链接 [text](url) / [text](url "title") 替换为纯文字。
    返回 (新行, 转换次数)。
    
    注意：图片语法 ![...](...) 不在此处理（另有专门删除步骤）。
    """
    count = 0
    new_line = line
    
    # 匹配非图片的 Markdown 链接
    # 规则：排除 ! 开头的，匹配 [text](url) 和 [text](url "title") 以及 [text](<url>)
    link_pattern = re.compile(
        r'(?<!!)\[(?P<text>[^\]]+)\]\('
        r'(?:<(?P<bracket_url>[^>]+)>|(?P<url>[^)\s]+(?:\([^)]*\))?[^)\s]*))'
        r'(?:\s+"[^"]*")?\s*\)'
    )
    
    def _replacer(m: re.Match) -> str:
        nonlocal count
        text = m.group("text")
        if text:
            count += 1
            return text
        return m.group(0)
    
    new_line = link_pattern.sub(_replacer, new_line)
    return new_line, count


def _count_heading_in_text(text: str) -> int:
    """统计文本中包含的导航章节数量（用于粗略统计）。"""
    count = 0
    for line in text.split("\n"):
        if _is_nav_heading(line):
            count += 1
    return count


def _remove_footnote_defs(text: str, stats: ExportStats) -> str:
    """
    删除脚注定义 [^ref]: ... 及其缩进后续行。
    """
    lines = text.split("\n")
    result: List[str] = []
    skip_until = -1
    
    for i, line in enumerate(lines):
        if i < skip_until:
            continue
        if _is_footnote_def(line):
            stats.footnotes_removed += 1
            # 跳过后续缩进行
            j = i + 1
            while j < len(lines):
                l = lines[j]
                if l.strip() == "" or l.startswith(" ") or l.startswith("\t"):
                    j += 1
                else:
                    break
            skip_until = j
            continue
        result.append(line)
    
    return "\n".join(result)


def _remove_inline_footnotes_global(text: str) -> Tuple[str, int]:
    """删除正文中所有行内脚注引用 [^ref]。"""
    fn_pattern = re.compile(r'\[\^[^\]]+\]')
    new_text, count = fn_pattern.subn("", text)
    return new_text, count


def process_entry(content: str, stats: ExportStats) -> str:
    """
    对单个词条内容执行全部清洗，返回清洗后的 Markdown。
    """
    # ── 分离 Frontmatter ──
    lines = content.split("\n")
    frontmatter_lines: List[str] = []
    body_start = 0
    
    if lines and lines[0].strip() == "---":
        # 查找结束 ---
        i = 1
        while i < len(lines):
            if lines[i].strip() == "---":
                frontmatter_lines = lines[:i+1]
                body_start = i + 1
                break
            i += 1
    
    body_lines = lines[body_start:] if body_start > 0 else lines
    
    # ── 处理正文 ──
    cleaned_lines: List[str] = []
    skip_until = -1
    
    i = 0
    while i < len(body_lines):
        if i < skip_until:
            i += 1
            continue
        
        line = body_lines[i]
        
        # 1) 检测导航/参考章节标题 → 删除该章节
        if _is_nav_heading(line):
            heading_level = _heading_level(line)
            if _is_ref_heading(line):
                stats.ref_sections_removed += 1
            else:
                stats.nav_sections_removed += 1
            # 删除后面的内容直到下一个同级或更高级标题
            j = i + 1
            while j < len(body_lines):
                next_line = body_lines[j]
                if _is_heading(next_line) and _heading_level(next_line) <= heading_level:
                    break
                j += 1
            i = j
            continue
        
        # 2) 检测 admonition
        stripped_line = line.lstrip()
        if stripped_line.startswith("!!!") or stripped_line.startswith("???"):
            processed, next_idx = _clean_admonition_block(body_lines, i, stats)
            if processed:
                # 对 admonition 正文也执行链接转换（脚注留到全局阶段）
                for pl in processed:
                    pl_clean, lc = _convert_links_in_line(pl)
                    stats.links_converted += lc
                    cleaned_lines.append(pl_clean)
            i = next_idx
            continue
        
        # 3) 删除行内图片（包括 SVG/PNG/JPG 等）
        line_no_img = _remove_images_from_line(line, stats)
        
        # 4) 转换链接（非图片）
        new_line, link_count = _convert_links_in_line(line_no_img)
        stats.links_converted += link_count
        
        cleaned_lines.append(new_line)
        i += 1
    
    # ── 重建正文 ──
    body_text = "\n".join(cleaned_lines)
    
    # ── 删除脚注定义（必须在删除行内脚注引用之前） ──
    body_text = _remove_footnote_defs(body_text, stats)
    
    # ── 删除行内脚注引用 ──
    body_text, fn_count = _remove_inline_footnotes_global(body_text)
    stats.footnotes_removed += fn_count
    
    # ── 删除模板文本（admonition 外的自由文本） ──
    for tmpl in TEMPLATE_TEXTS:
        while tmpl in body_text:
            stats.template_texts_removed += 1
            body_text = body_text.replace(tmpl, "")
    for pattern in TEMPLATE_TEXT_PATTERNS:
        body_text, count = pattern.subn("", body_text)
        stats.template_texts_removed += count
    
    # ── 清理空行和孤立分隔线 ──
    body_text = _cleanup_whitespace(body_text)
    
    # ── 合并 Frontmatter 和清洗后的正文 ──
    if frontmatter_lines:
        result = "\n".join(frontmatter_lines) + "\n" + body_text
    else:
        result = body_text
    
    return result


def _remove_inline_footnotes_in_line(line: str) -> Tuple[str, int]:
    """删除行内脚注引用，返回 (新行, 删除数量)。"""
    fn_pattern = re.compile(r'\[\^[^\]]+\]')
    new_line, count = fn_pattern.subn("", line)
    # 行中可能有多处脚注引用，subn 已经处理了全部
    return new_line, count


def _cleanup_whitespace(text: str) -> str:
    """
    清理：
      - 删除章节后产生的孤立水平分隔线（连续3+ - 或 *）
      - 空标题（## 后面只有空白）
      - 空列表项（- 或 * 后面只有空白）
      - 连续超过两个空行 → 保留两个
      - 文件开头或结尾多余空行
    """
    lines = text.split("\n")
    result: List[str] = []
    
    for line in lines:
        stripped = line.strip()
        
        # 空标题
        if re.match(r'^#{1,6}\s*$', line):
            continue
        
        # 孤立分隔线（前面是空行或文件开头，后面也是空行或文件结尾）
        # 简单地过滤掉分隔线行
        if re.match(r'^[-*_]{3,}\s*$', stripped) and not stripped.startswith("---"):
            # 跳过可能的分隔线（--- 是 Frontmatter 分隔符，不删）
            continue
        
        # 空列表项
        if re.match(r'^[\s]*[-*+]\s*$', line):
            continue
        if re.match(r'^[\s]*\d+\.\s*$', line):
            continue
        
        result.append(line)
    
    text = "\n".join(result)
    
    # 连续超过两个空行 → 保留两个
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 文件开头和结尾空行
    text = text.strip()
    
    return text


# ── 安全检查 ──

# 禁止的输出目录列表（相对路径会自动解析为绝对路径比较）
FORBIDDEN_OUTPUT_DIRS: Set[str] = {
    "/",
}


def check_output_safety(input_dir: Path, output_dir: Path) -> None:
    """
    检查输出目录安全性。
    
    Raises:
        ValueError: 如果输出目录不安全。
    """
    input_resolved = input_dir.resolve()
    output_resolved = output_dir.resolve()
    
    # 输入输出不能相同
    if input_resolved == output_resolved:
        raise ValueError(
            f"输入目录和输出目录不能相同: {input_resolved}"
        )
    
    repo_root = Path(__file__).resolve().parent.parent
    
    # 输出目录不能是仓库根目录或 docs/entries/
    forbidden = [
        repo_root,
        repo_root / "docs" / "entries",
        input_resolved,
    ]
    for forbidden_path in forbidden:
        if output_resolved == forbidden_path:
            raise ValueError(
                f"输出目录不得为禁止目录: {output_resolved}"
            )
    
    # 输出目录不能位于 docs/ 下（包括 docs/ 本身）
    if str(output_resolved).startswith(str(repo_root / "docs")):
        raise ValueError(
            f"输出目录不得位于 docs/ 下: {output_resolved}"
        )


# ── 主入口 ──

@dataclass
class ExportResult:
    """导出结果。"""
    scanned: int = 0
    exported: int = 0
    failed: int = 0
    errors: List[Tuple[str, str]] = field(default_factory=list)  # (filename, error)
    total_stats: ExportStats = field(default_factory=ExportStats)


def export_knowledge(input_dir: Path, output_dir: Path) -> ExportResult:
    """
    执行知识导出。
    
    Args:
        input_dir: 源词条目录（如 docs/entries/）
        output_dir: 输出目录（如 dist/knowledge/entries/）
    
    Returns:
        导出结果对象。
    """
    result = ExportResult()
    
    # 安全检查
    check_output_safety(input_dir, output_dir)
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 清理旧生成文件，但只限 .md 文件以避免误删
    if output_dir.exists():
        for old_file in output_dir.glob("*.md"):
            old_file.unlink()
    
    # 扫描输入文件
    md_files = sorted(input_dir.glob("*.md"))
    result.scanned = len(md_files)
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            stats = ExportStats()
            cleaned = process_entry(content, stats)
            
            # 写入输出
            output_path = output_dir / md_file.name
            output_path.write_text(cleaned + "\n", encoding="utf-8")
            
            result.exported += 1
            if stats.error:
                result.failed += 1
                result.errors.append((md_file.name, stats.error))
            result.total_stats.merge(stats)
        except Exception as e:
            result.failed += 1
            result.errors.append((md_file.name, str(e)))
    
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="知识库干净版导出工具 - 将 wiki 词条导出为适合全文检索的干净 Markdown",
    )
    parser.add_argument(
        "--input", "-i",
        default="docs/entries",
        help="源词条目录（默认: docs/entries）",
    )
    parser.add_argument(
        "--output", "-o",
        default="dist/knowledge/entries",
        help="输出目录（默认: dist/knowledge/entries）",
    )
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.is_dir():
        print(f"错误: 输入目录不存在: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = export_knowledge(input_dir, output_dir)
    except ValueError as e:
        print(f"安全错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 输出统计报告
    stats = result.total_stats
    print(f"\n{'='*50}")
    print(f"  知识库导出完成")
    print(f"{'='*50}")
    print(f"  扫描文件数:        {result.scanned}")
    print(f"  成功导出文件数:    {result.exported}")
    print(f"  失败/跳过文件数:   {result.failed}")
    print(f"  ─────────────────────────────")
    print(f"  删除导航章节数:    {stats.nav_sections_removed}")
    print(f"  删除参考章节数:    {stats.ref_sections_removed}")
    print(f"  转换链接数:        {stats.links_converted}")
    print(f"  清理 admonition 数: {stats.admonitions_cleaned}")
    print(f"  删除图片数:        {stats.images_removed}")
    print(f"  删除脚注数:        {stats.footnotes_removed}")
    print(f"  删除模板文本数:    {stats.template_texts_removed}")
    print(f"  输出目录:          {output_dir.resolve()}")
    print(f"{'='*50}\n")
    
    if result.errors:
        print("失败文件详情:")
        for fname, err in result.errors:
            print(f"  ❌ {fname}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
