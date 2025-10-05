#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查 Markdown 中"非完整路径"的内部链接。

**MkDocs Material 迁移后的规则**：
1) 允许：外链(http/https/ftp/ftps)、mailto、tel、data、图片(![]())、锚点(#...)。
2) 允许：指向仓库根部的白名单文档（站点元文件），如 index.md / Glossary.md 等。
3) 要求：指向词条(内容页)的内部链接使用以下格式之一：
   - `entries/*.md` - 旧版 Docsify 完整路径（仍支持）
   - `docs/entries/*.md` - MkDocs 完整路径（推荐）
   - `../entries/*.md` 或 `entries/*.md` - MkDocs 相对路径（在 docs/ 目录内使用）
4) 禁止：./xxx.md、../xxx.md（非标准用法）、裸文件名 xxx.md、没有 .md 的"伪内部文件链接"。

用法：
    python tools/check_links.py [--root .] [--whitelist index.md Glossary.md ...]

退出码：
    0 = 全部合规
    1 = 存在违规
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Iterable

LINK_RE = re.compile(
    r'(?P<prefix>!?)\[(?P<text>[^\]]+)\]\((?P<target>[^()\s]+)(?:\s+"[^"]*")?\)',
    re.IGNORECASE,
)

# 外链/协议白名单
SCHEME_ALLOW = ("http://", "https://", "//", "ftp://", "ftps://", "mailto:", "tel:", "data:")
# 站内锚点 / docsify 路由锚
ANCHOR_ALLOW_PREFIX = ("#", "#/")  # 允许 #xxx 和 #/xxx 两种

# 根目录下允许直接链接的站点文件（不强制 entries/ 前缀）
ROOT_WHITELIST = {
    "README.md",
    "Main_Page.html",
    "index.md",
    "Glossary.md",
    "CONTRIBUTING.md",
    "changelog.md",
    "_sidebar.md",
    "_coverpage.md",
    "AGENTS.md",
    "tags.md",
}

def is_image(prefix: str) -> bool:
    return prefix == "!"

def is_external(target: str) -> bool:
    lower = target.lower()
    return lower.startswith(SCHEME_ALLOW)

def is_anchor(target: str) -> bool:
    return target.startswith(ANCHOR_ALLOW_PREFIX)

def is_root_whitelist(target: str, repo_root: Path) -> bool:
    # 仅接受纯文件名或相对根文件（不带子目录）
    p = Path(target)
    if p.suffix.lower() not in {".md", ".html"}:
        return False
    # 不允许子目录：如 docs/README.md 不在白名单里
    if len(p.parts) != 1:
        return False
    return p.name in ROOT_WHITELIST and (repo_root / p.name).exists()

def looks_like_internal_md(target: str) -> bool:
    """是否是看起来像内部 .md 链接（不含协议、非锚点、非图片资源）。"""
    if any(target.lower().startswith(s) for s in SCHEME_ALLOW):
        return False
    if target.startswith(ANCHOR_ALLOW_PREFIX):
        return False
    # 过滤可能的图片/资源文件
    pure = target.split("#", 1)[0]
    if Path(pure).suffix.lower() not in (".md", "", ".markdown"):
        return False
    return True

def is_valid_entries_path(target: str) -> bool:
    """
    是否满足词条路径规范（支持 MkDocs Material 迁移后的多种格式）

    允许的格式：
    - entries/*.md (旧版 Docsify)
    - docs/entries/*.md (MkDocs 完整路径)
    - ../entries/*.md (MkDocs 相对路径，从 docs/ 内部链接)
    """
    pure = target.split("#", 1)[0]
    p = Path(pure)

    if p.suffix.lower() != ".md":
        return False

    parts = p.parts

    # 格式 1: entries/*.md (Docsify 旧版)
    if len(parts) == 2 and parts[0].lower() == "entries":
        return True

    # 格式 2: docs/entries/*.md (MkDocs 完整路径)
    if len(parts) == 3 and parts[0].lower() == "docs" and parts[1].lower() == "entries":
        return True

    # 格式 3: ../entries/*.md (MkDocs 相对路径)
    if len(parts) == 3 and parts[0] == ".." and parts[1].lower() == "entries":
        return True

    return False

def find_md_files(root: Path) -> Iterable[Path]:
    return (p for p in root.rglob("*.md") if p.is_file())

def check_file(md_path: Path, repo_root: Path, whitelist_extra: List[str]) -> List[Tuple[int, str, str]]:
    violations = []
    content = md_path.read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(content.splitlines(), start=1):
        for m in LINK_RE.finditer(line):
            prefix = m.group("prefix") or ""
            target = m.group("target").strip()
            pure_target = target.split("#", 1)[0]

            # 跳过图片
            if is_image(prefix):
                continue
            # 外链与锚点允许
            if is_external(target) or is_anchor(target):
                continue
            # 允许根白名单
            if pure_target in whitelist_extra or is_root_whitelist(pure_target, repo_root):
                continue
            # 允许 docs/ 前缀的文档链接
            if pure_target.startswith("docs/"):
                candidate = repo_root / pure_target
                if candidate.exists():
                    continue
            # 允许指向非 entries/ 文件的相对路径
            if Path(pure_target).suffix.lower() == ".md":
                candidate = (md_path.parent / pure_target).resolve()
                try:
                    relative = candidate.relative_to(repo_root)
                except ValueError:
                    relative = None
                if candidate.exists() and (relative is None or relative.parts[0] != "entries"):
                    continue

            # 其余看起来像内部链接的做严格校验
            if looks_like_internal_md(target):
                # 1) 检查是否为有效的词条路径格式
                if not is_valid_entries_path(target):
                    # 若缺少 .md 后缀但明显想引用本地文件，也提示
                    if Path(pure_target).suffix == "":
                        violations.append((i, target, "内部链接缺少 .md 后缀或路径不完整；请使用 entries/*.md、docs/entries/*.md 或 ../entries/*.md"))
                    else:
                        violations.append((i, target, "内部链接路径不合规；应为 entries/*.md、docs/entries/*.md 或 ../entries/*.md"))
                # 通过的就不记录
            # 其它情况（比如资源文件）忽略
    return violations

def main():
    parser = argparse.ArgumentParser(description="检查 Markdown 内部链接是否为 entries/*.md 完整路径")
    parser.add_argument("--root", default=".", help="仓库根目录，默认 .")
    parser.add_argument("--whitelist", nargs="*", default=[], help="额外允许直链的根文件（例如 Main_Page.html）")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    extra = set(args.whitelist or [])
    ok = True
    total_violations = 0

    print(f"==> 扫描仓库：{repo_root}")

    for md in find_md_files(repo_root):
        rel = md.relative_to(repo_root)
        vio = check_file(md, repo_root, list(extra))
        if vio:
            ok = False
            print(f"\n[违规] {rel} ：")
            for line_no, target, reason in vio:
                print(f"  - 行 {line_no}: {target}\n    ↳ {reason}")
            total_violations += len(vio)

    if ok:
        print("\n✅ 所有 Markdown 内部链接均合规（entries/*.md 或白名单/外链/锚点）")
        sys.exit(0)
    else:
        print(f"\n❌ 检查完成，发现 {total_violations} 处不合规内部链接")
        sys.exit(1)

if __name__ == "__main__":
    main()
