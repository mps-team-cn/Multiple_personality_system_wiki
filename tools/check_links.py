#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查 Markdown 内部链接是否符合项目规范

遵循 docs/contributing/技术约定.md 中的链接管理规范：

1. 词条间链接：直接使用文件名（如 `DID.md`）
2. 词条到其他目录：使用 `../` 相对路径（如 `../contributing/index.md`）
3. 其他目录到词条：使用 `../entries/` 路径（如 `../entries/DID.md`）
4. 禁止：绝对路径（如 `/docs/entries/DID.md`）

用法：
    python tools/check_links.py [--root .]

退出码：
    0 = 全部合规
    1 = 存在违规
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Set

# 链接正则：匹配 [text](url) 或 [text](<url>) 格式，支持可选的标题
LINK_RE = re.compile(
    r'(?P<prefix>!?)\[(?P<text>[^\]]+)\]\((?:<(?P<target_bracket>[^>]+)>|(?P<target>[^()\s]+))(?:\s+"[^"]*")?\)',
    re.IGNORECASE,
)

# 外链协议白名单
EXTERNAL_SCHEMES = ("http://", "https://", "//", "ftp://", "ftps://", "mailto:", "tel:", "data:")

# 锚点前缀
ANCHOR_PREFIXES = ("#", "#/")


def is_image(prefix: str) -> bool:
    """检查是否为图片链接"""
    return prefix == "!"


def is_external(target: str) -> bool:
    """检查是否为外部链接"""
    return target.lower().startswith(EXTERNAL_SCHEMES)


def is_anchor(target: str) -> bool:
    """检查是否为锚点链接"""
    return target.startswith(ANCHOR_PREFIXES)


def is_absolute_path(target: str) -> bool:
    """检查是否为绝对路径（禁止）"""
    return target.startswith("/")


def get_file_context(file_path: Path, repo_root: Path) -> str:
    """
    判断文件所在的上下文位置

    Returns:
        'entries' - 在 docs/entries/ 目录
        'docs_subdir' - 在 docs/ 的子目录下 (如 docs/contributing/)
        'docs_root' - 在 docs/ 根目录下 (如 docs/Glossary.md)
        'root' - 在仓库根目录
        'other' - 其他位置
    """
    try:
        rel_path = file_path.relative_to(repo_root)
        parts = rel_path.parts

        # docs/entries/ 目录
        if len(parts) >= 2 and parts[0] == "docs" and parts[1] == "entries":
            return "entries"

        # docs/ 根目录 (文件直接在 docs/ 下)
        if len(parts) == 2 and parts[0] == "docs":
            return "docs_root"

        # docs/ 子目录 (在 docs/ 的子目录中)
        if len(parts) > 2 and parts[0] == "docs":
            return "docs_subdir"

        # 仓库根目录
        if len(parts) == 1:
            return "root"

        return "other"
    except ValueError:
        return "other"


def validate_link(
    target: str,
    source_context: str,
    source_file: Path,
    repo_root: Path
) -> Tuple[bool, str]:
    """
    验证链接是否符合规范

    Args:
        target: 链接目标
        source_context: 源文件上下文 ('entries', 'docs', 'root', 'other')
        source_file: 源文件路径
        repo_root: 仓库根目录

    Returns:
        (is_valid, error_message)
    """
    # 移除锚点部分
    pure_target = target.split("#", 1)[0]
    if not pure_target:  # 纯锚点
        return True, ""

    # 检查是否为绝对路径（禁止）
    if is_absolute_path(pure_target):
        return False, f"禁止使用绝对路径，请使用相对路径（如 `../entries/xxx.md`）"

    # 解析目标路径
    target_path = Path(pure_target)

    # 只检查 .md 文件链接
    if target_path.suffix.lower() != ".md":
        # 非 .md 文件（如图片、其他资源），检查路径是否存在
        resolved = (source_file.parent / pure_target).resolve()
        try:
            resolved.relative_to(repo_root)
            if not resolved.exists():
                return False, f"文件不存在：{pure_target}"
        except ValueError:
            return False, f"路径超出仓库范围：{pure_target}"
        return True, ""

    # === 检查 .md 文件链接 ===

    # 尝试解析目标文件的实际位置
    resolved = (source_file.parent / pure_target).resolve()

    # 检查文件是否存在
    if not resolved.exists():
        return False, f"文件不存在：{pure_target}"

    # 获取目标文件的上下文
    try:
        target_rel = resolved.relative_to(repo_root)
        target_parts = target_rel.parts
    except ValueError:
        return False, f"路径超出仓库范围：{pure_target}"

    # 判断目标是否在 docs/entries/
    target_in_entries = (
        len(target_parts) >= 2 and
        target_parts[0] == "docs" and
        target_parts[1] == "entries"
    )

    # === 根据源文件上下文和目标位置验证链接格式 ===

    if source_context == "entries":
        # 词条文件 (docs/entries/xxx.md)

        if target_in_entries:
            # 链接到其他词条：应该直接使用文件名
            # 正确：DID.md
            # 错误：../entries/DID.md, docs/entries/DID.md

            if target_path.parts == (target_path.name,):
                # 只有文件名，符合规范
                return True, ""
            else:
                return False, (
                    f"词条间链接应直接使用文件名\n"
                    f"    当前：{pure_target}\n"
                    f"    应改为：{target_path.name}"
                )
        else:
            # 链接到其他目录：应该使用 ../ 开头的相对路径
            # 正确：../contributing/index.md, ../dev/xxx.md

            if not pure_target.startswith("../"):
                return False, (
                    f"词条链接到其他目录应使用 `../` 相对路径\n"
                    f"    当前：{pure_target}\n"
                    f"    提示：从 docs/entries/ 到目标需要先 ../ 回到 docs/"
                )
            return True, ""

    elif source_context == "docs_subdir":
        # docs/ 的子目录 (如 docs/contributing/)

        if target_in_entries:
            # 链接到词条：应该使用 ../entries/ 路径
            if pure_target.startswith("../entries/"):
                return True, ""
            else:
                return False, (
                    f"从 docs/ 子目录链接到词条应使用 `../entries/` 路径\n"
                    f"    当前：{pure_target}\n"
                    f"    应改为：../entries/{target_path.name}"
                )
        else:
            # 链接到非词条文件：相对路径即可
            return True, ""

    elif source_context in ("docs_root", "root"):
        # docs/ 根目录或仓库根目录的文件

        if target_in_entries:
            # 链接到词条：应该使用 entries/ 或 docs/entries/ 格式
            # 从 docs/ 根目录：entries/DID.md
            # 从仓库根目录：docs/entries/DID.md

            if source_context == "docs_root":
                # 从 docs/ 根目录
                if pure_target.startswith("entries/"):
                    return True, ""
                else:
                    return False, (
                        f"从 docs/ 根目录链接到词条应使用 `entries/` 路径\n"
                        f"    当前：{pure_target}\n"
                        f"    应改为：entries/{target_path.name}"
                    )
            else:
                # 从仓库根目录
                if pure_target.startswith("docs/entries/"):
                    return True, ""
                else:
                    return False, (
                        f"从仓库根目录链接到词条应使用 `docs/entries/` 路径\n"
                        f"    当前：{pure_target}\n"
                        f"    应改为：docs/entries/{target_path.name}"
                    )
        else:
            # 链接到非词条文件：相对路径即可
            return True, ""

    else:
        # 其他位置（如 tools/）
        # 不做严格限制，只要文件存在即可
        return True, ""


def check_file(md_path: Path, repo_root: Path) -> List[Tuple[int, str, str]]:
    """
    检查单个 Markdown 文件的链接

    Returns:
        违规列表：[(行号, 目标, 错误信息), ...]
    """
    violations = []
    source_context = get_file_context(md_path, repo_root)

    try:
        content = md_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [(0, str(md_path), f"读取文件失败：{e}")]

    for i, line in enumerate(content.splitlines(), start=1):
        for m in LINK_RE.finditer(line):
            prefix = m.group("prefix") or ""
            # 支持尖括号包裹的 URL：[text](<url>) 或 [text](url)
            target = (m.group("target_bracket") or m.group("target") or "").strip()

            # 跳过图片、外链、锚点
            if is_image(prefix) or is_external(target) or is_anchor(target):
                continue

            # 验证链接
            is_valid, error = validate_link(target, source_context, md_path, repo_root)
            if not is_valid:
                violations.append((i, target, error))

    return violations


def find_md_files(root: Path, exclude_dirs: Set[str] = None) -> List[Path]:
    """查找所有 Markdown 文件"""
    if exclude_dirs is None:
        exclude_dirs = {
            "node_modules",
            ".git",
            "__pycache__",
            "venv",
            ".venv",
            "tools/pdf_export/vendor",
        }

    md_files = []
    for md in root.rglob("*.md"):
        # 检查是否在排除目录中
        if any(excluded in md.parts for excluded in exclude_dirs):
            continue
        md_files.append(md)

    return sorted(md_files)


def main():
    parser = argparse.ArgumentParser(
        description="检查 Markdown 内部链接是否符合项目规范",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
链接规范：
  1. 词条间链接：直接使用文件名（如 DID.md）
  2. 词条到其他目录：使用 ../ 相对路径（如 ../contributing/index.md）
  3. 其他目录到词条：使用 ../entries/ 路径（如 ../entries/DID.md）
  4. 禁止：绝对路径（如 /docs/entries/DID.md）

详见：docs/contributing/技术约定.md
        """
    )
    parser.add_argument("--root", default=".", help="仓库根目录，默认为当前目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")

    args = parser.parse_args()

    repo_root = Path(args.root).resolve()

    if not repo_root.exists():
        print(f"错误：目录不存在：{repo_root}")
        sys.exit(1)

    print("=" * 70)
    print("Markdown 链接规范检查")
    print("=" * 70)
    print(f"扫描目录：{repo_root}")
    print()

    # 查找所有 Markdown 文件
    md_files = find_md_files(repo_root)
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    print()

    # 检查所有文件
    total_violations = 0
    files_with_violations = 0

    for md_file in md_files:
        rel_path = md_file.relative_to(repo_root)
        violations = check_file(md_file, repo_root)

        if violations:
            files_with_violations += 1
            total_violations += len(violations)

            print(f"[违规] {rel_path}")
            for line_no, target, error in violations:
                print(f"  行 {line_no}: {target}")
                for error_line in error.split("\n"):
                    print(f"    {error_line}")
                print()
        elif args.verbose:
            print(f"[通过] {rel_path}")

    # 输出总结
    print("=" * 70)
    if total_violations == 0:
        print("[OK] 所有链接均符合规范")
        sys.exit(0)
    else:
        print(f"[FAIL] 发现 {total_violations} 处违规链接（{files_with_violations} 个文件）")
        print()
        print("提示：")
        print("  - 词条间链接使用文件名：DID.md")
        print("  - 词条到其他目录使用：../contributing/index.md")
        print("  - 其他目录到词条使用：../entries/DID.md")
        print("  - 详见：docs/contributing/技术约定.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
