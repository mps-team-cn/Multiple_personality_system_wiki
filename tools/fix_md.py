#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_md.py v3

批量修复 Markdown 常见 Lint 问题：
- MD012: 连续空行压缩为 1
- MD022: 标题上下各留 1 个空行（文件开头除外；末尾只保证下方不是紧贴内容）
- MD031: 代码块前后各留 1 个空行
- MD032: 列表前后各留 1 个空行
- MD037: 修复强调标记内的空格（** ** → ****）
- MD040: 无语言的代码围栏补为 ```text
- MD009: 去掉行尾空白（含全角空格、NBSP 等 Unicode 空白）
- MD034: 裸链接 -> [url](url)（非代码块）
- MD047: 文件以单个换行结束
- MD028: 引用块中的"裸空行" -> 用 `> ` 占位

仍需人工处理：MD024（重复标题）、MD052（参考式链接缺定义）、MD042/MD051（README 徽章与锚点）。
"""

from __future__ import annotations
import argparse
import re
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = {
    "node_modules",
    "tools/pdf_export/vendor",
    ".git",
    "legacy",
}

# 识别标题行
HEADING_RE = re.compile(r'^(#{1,6})\s+\S')
# 任何围栏与只有 ``` 的围栏
FENCE_ANY_RE = re.compile(r'^```')
FENCE_START_RE = re.compile(r'^```(\s*)$')
FENCE_LANG_RE  = re.compile(r'^```[A-Za-z0-9_\-+.]')
# 列表项（无序和有序）
LIST_ITEM_RE = re.compile(r'^(\s*)([-*+]|\d+\.)\s+')
UNORDERED_MARKER_NEEDS_SPACE_RE = re.compile(r'^(\s*)(-(?!-)|\+(?!\+)|\*(?!\*))(?=\S)')
ORDERED_MARKER_NEEDS_SPACE_RE = re.compile(r'^(\s*)(\d+\.)(?=\S)')
# 强调标记内的空格
EMPHASIS_SEGMENT_RE = re.compile(r'(\*\*|__)(.+?)(\1)')
# 裸链接
BARE_URL_RE = re.compile(r'(?<!\])(?<!\))(?P<url>https?://[^\s<>\)\]]+)', re.IGNORECASE)
# 行尾 Unicode 空白（含全角空格/窄不换行空格等）
TRAIL_WS_RE = re.compile(r'[\t \u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]+$')

def should_exclude(p: Path, exclude_dirs: set[str]) -> bool:
    parts = set(p.parts)
    return any(ex in parts for ex in exclude_dirs)

def strip_trailing_spaces(lines: list[str]) -> list[str]:
    return [TRAIL_WS_RE.sub('', ln) for ln in lines]

def compress_blank_lines(lines: list[str]) -> list[str]:
    out, blank = [], 0
    for ln in lines:
        if ln.strip() == "":
            blank += 1
            if blank <= 1:
                out.append("")
        else:
            blank = 0
            out.append(ln)
    return out

def normalize_list_marker_spacing(lines: list[str]) -> list[str]:
    """确保列表标记后至少有一个空格,即便原本缺失而未匹配到列表模式。"""
    out: list[str] = []
    in_fence = False
    for ln in lines:
        if FENCE_ANY_RE.match(ln):
            in_fence = not in_fence
            out.append(ln)
            continue
        if not in_fence:
            ln = UNORDERED_MARKER_NEEDS_SPACE_RE.sub(r'\1\2 ', ln, count=1)
            ln = ORDERED_MARKER_NEEDS_SPACE_RE.sub(r'\1\2 ', ln, count=1)
        out.append(ln)
    return out

def ensure_blank_around_headings(lines: list[str]) -> list[str]:
    """
    MD022：保证标题前后各 1 个空行：
    - 前：非文件首行且上一行非空 -> 插入空行
    - 后：下一行存在且不是空行/围栏结束 -> 插入空行
    （注：标准要求“上下各一空行”，后一空行更容易被忽略）
    """
    # 先处理“前空行”
    out = []
    for i, ln in enumerate(lines):
        if i > 0 and HEADING_RE.match(ln) and (out and out[-1].strip() != ""):
            out.append("")  # 标题上方加空行
        out.append(ln)

    # 再处理“后空行”
    i = 0
    res = []
    while i < len(out):
        res.append(out[i])
        if HEADING_RE.match(out[i]):
            # 若后面还有一行且不是空行/围栏结尾，就补一行空行
            nxt = out[i+1] if i+1 < len(out) else None
            if nxt is not None and nxt.strip() != "":
                res.append("")  # 标题下方加空行
        i += 1
    return res

def fix_fenced_code_language(lines: list[str]) -> list[str]:
    out, in_fence = [], False
    for ln in lines:
        if not in_fence:
            if FENCE_ANY_RE.match(ln):
                if FENCE_LANG_RE.match(ln):
                    in_fence = True; out.append(ln)
                elif FENCE_START_RE.match(ln):
                    in_fence = True; out.append("```text")
                else:
                    in_fence = True; out.append("```text")
            else:
                out.append(ln)
        else:
            if FENCE_ANY_RE.match(ln):
                in_fence = False; out.append("```")
            else:
                out.append(ln)
    return out

def fix_blockquote_blank(lines: list[str]) -> list[str]:
    new = lines[:]
    for i in range(1, len(new) - 1):
        if new[i].strip() == "" and new[i-1].lstrip().startswith(">") and new[i+1].lstrip().startswith(">"):
            new[i] = "> "
    return new

def convert_bare_urls(lines: list[str]) -> list[str]:
    out, in_fence = [], False
    for ln in lines:
        if FENCE_ANY_RE.match(ln):
            in_fence = not in_fence
            out.append(ln); continue
        if in_fence:
            out.append(ln); continue
        if "](" in ln or "<http" in ln:
            out.append(ln); continue

        out.append(BARE_URL_RE.sub(lambda m: f'[{m.group("url")}]({m.group("url")})', ln))
    return out

def ensure_blank_around_fences(lines: list[str]) -> list[str]:
    """MD031: 代码块前后各留 1 个空行"""
    out = []
    in_fence = False

    for i, ln in enumerate(lines):
        is_fence = FENCE_ANY_RE.match(ln) is not None

        if is_fence:
            # 围栏开始：前面需要空行
            if not in_fence and i > 0 and out and out[-1].strip() != "":
                out.append("")
            out.append(ln)
            # 切换围栏状态
            in_fence = not in_fence
            # 围栏结束：后面需要空行
            if not in_fence and i + 1 < len(lines) and lines[i + 1].strip() != "":
                out.append("")
        else:
            out.append(ln)

    return out

def ensure_blank_around_lists(lines: list[str]) -> list[str]:
    """MD032: 列表前后各留 1 个空行"""
    out = []
    in_list = False

    for i, ln in enumerate(lines):
        is_list_item = LIST_ITEM_RE.match(ln) is not None
        is_blank = ln.strip() == ""

        # 列表开始：前面加空行
        if is_list_item and not in_list:
            if i > 0 and out and out[-1].strip() != "":
                out.append("")
            in_list = True

        # 列表结束：后面加空行
        if in_list and not is_list_item and not is_blank:
            if out and out[-1].strip() != "":
                out.append("")
            in_list = False

        out.append(ln)

    return out

def fix_emphasis_spaces(lines: list[str]) -> list[str]:
    """MD037: 修复强调标记内的空格,并确保强调段前后留白"""
    out, in_fence = [], False
    for ln in lines:
        # 跳过代码块
        if FENCE_ANY_RE.match(ln):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue

        matches = list(EMPHASIS_SEGMENT_RE.finditer(ln))
        if not matches:
            out.append(ln)
            continue

        pieces: list[str] = []
        last_idx = 0
        last_char = ""

        for match in matches:
            if match.start() > last_idx:
                segment = ln[last_idx : match.start()]
                pieces.append(segment)
                if segment:
                    last_char = segment[-1]

            start_tag, content, end_tag = match.groups()
            content = content.strip()

            if pieces and last_char and not last_char.isspace():
                pieces.append(" ")
                last_char = " "

            pieces.append(f"{start_tag}{content}{end_tag}")
            last_char = end_tag[-1]
            last_idx = match.end()

            if match.end() < len(ln):
                next_char = ln[match.end()]
                if not next_char.isspace():
                    pieces.append(" ")
                    last_char = " "

        if last_idx < len(ln):
            tail = ln[last_idx:]
            pieces.append(tail)
        out.append("".join(pieces))

    return out

def ensure_single_trailing_newline(text: str) -> str:
    return text.rstrip("\n") + "\n"

def process_file(p: Path, dry_run=False) -> bool:
    original = p.read_text(encoding="utf-8", errors="ignore")
    lines = original.splitlines()

    lines = strip_trailing_spaces(lines)       # MD009（含全角空格）
    lines = fix_emphasis_spaces(lines)         # MD037（强调标记空格）
    lines = compress_blank_lines(lines)        # MD012
    lines = normalize_list_marker_spacing(lines)
    lines = ensure_blank_around_headings(lines)# MD022（前后）
    lines = ensure_blank_around_fences(lines)  # MD031（代码块前后空行）
    lines = ensure_blank_around_lists(lines)   # MD032（列表前后空行）
    lines = fix_fenced_code_language(lines)    # MD040
    lines = fix_blockquote_blank(lines)        # MD028
    lines = convert_bare_urls(lines)           # MD034

    new_text = ensure_single_trailing_newline("\n".join(lines))  # MD047
    changed = (new_text != original)
    if changed and not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument(
        "--paths",
        nargs="*",
        help="仅处理指定的相对路径(文件或目录)。为空时遍历 root 下全部 Markdown。",
    )
    ap.add_argument(
        "--extra-exclude",
        nargs="*",
        default=(),
        help="追加排除目录名称（相对于 root 的路径片段）。",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    exclude_dirs = set(DEFAULT_EXCLUDE_DIRS)
    exclude_dirs.update(args.extra_exclude)

    candidates: list[Path] = []
    if args.paths:
        for rel in args.paths:
            target = (root / rel).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                print(f"忽略越界路径: {rel}")
                continue
            if not target.exists():
                print(f"忽略不存在的路径: {rel}")
                continue
            if target.is_dir():
                candidates.extend(target.rglob("*.md"))
            elif target.is_file() and target.suffix.lower() == ".md":
                candidates.append(target)
    else:
        candidates = list(root.rglob("*.md"))

    files: list[Path] = []
    seen: set[Path] = set()
    for p in candidates:
        if should_exclude(p, exclude_dirs):
            continue
        if p in seen:
            continue
        seen.add(p)
        files.append(p)
    changed = []
    for p in files:
        if process_file(p, dry_run=args.dry_run):
            changed.append(str(p.relative_to(root)))

    if args.dry_run:
        print("将修改：\n" + "\n".join(" - " + f for f in changed) if changed else "无需修改")
    else:
        print("已修改：\n" + "\n".join(" - " + f for f in changed) if changed else "无文件变更。")

if __name__ == "__main__":
    main()
