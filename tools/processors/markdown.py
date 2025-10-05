#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 处理器模块

提供统一的 Markdown 文档修复和处理功能,包括:
- MD009: 行尾空白清理
- MD012: 连续空行压缩
- MD022: 标题前后空行
- MD028: 引用块空行修复
- MD034: 裸链接转换
- MD040: 代码围栏语言标注
- MD047: 文件结尾换行
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ..core.config import Config
from ..core.logger import get_logger
from ..core.utils import read_file, write_file

logger = get_logger(__name__)


# ============================================================================
# 正则表达式模式
# ============================================================================

# 识别标题行
HEADING_RE = re.compile(r'^(#{1,6})\s+\S')

# 代码围栏相关
FENCE_ANY_RE = re.compile(r'^```')
FENCE_START_RE = re.compile(r'^```(\s*)$')
FENCE_LANG_RE = re.compile(r'^```[A-Za-z0-9_\-+.]')

# 裸链接
BARE_URL_RE = re.compile(
    r'(?<!\])(?<!\))(?P<url>https?://[^\s<>\)\]]+)',
    re.IGNORECASE
)

# 行尾 Unicode 空白(含全角空格、窄不换行空格等)
TRAIL_WS_RE = re.compile(
    r'[\t \u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]+$'
)


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class FixRule:
    """Markdown 修复规则定义"""
    name: str
    code: str
    description: str
    enabled: bool = True
    processor: Callable[[list[str]], list[str]] = None


@dataclass
class ProcessResult:
    """处理结果"""
    file_path: Path
    changed: bool
    original_lines: int
    final_lines: int
    applied_rules: list[str]


# ============================================================================
# 核心处理器类
# ============================================================================

class MarkdownProcessor:
    """
    Markdown 文档处理器

    提供可配置的 Markdown 修复规则和批量处理能力
    """

    def __init__(self, config: Config | None = None):
        """
        初始化处理器

        Args:
            config: 配置对象,如果为 None 则使用默认配置
        """
        self.config = config or Config.load()
        self.rules = self._init_rules()

    def _init_rules(self) -> list[FixRule]:
        """初始化修复规则列表"""
        return [
            FixRule(
                name="trailing_whitespace",
                code="MD009",
                description="移除行尾空白字符",
                processor=strip_trailing_spaces
            ),
            FixRule(
                name="compress_blank_lines",
                code="MD012",
                description="压缩连续空行",
                processor=compress_blank_lines
            ),
            FixRule(
                name="blank_around_headings",
                code="MD022",
                description="确保标题前后空行",
                processor=ensure_blank_around_headings
            ),
            FixRule(
                name="fenced_code_language",
                code="MD040",
                description="为代码围栏添加语言标注",
                processor=fix_fenced_code_language
            ),
            FixRule(
                name="blockquote_blank",
                code="MD028",
                description="修复引用块中的空行",
                processor=fix_blockquote_blank
            ),
            FixRule(
                name="bare_urls",
                code="MD034",
                description="转换裸链接为标准格式",
                processor=convert_bare_urls
            ),
        ]

    def process_file(
        self,
        file_path: Path,
        dry_run: bool = False
    ) -> ProcessResult:
        """
        处理单个 Markdown 文件

        Args:
            file_path: 文件路径
            dry_run: 是否为预览模式

        Returns:
            ProcessResult: 处理结果对象
        """
        logger.debug(f"处理文件: {file_path}")

        # 读取原始内容
        original = read_file(file_path)
        lines = original.splitlines()
        original_count = len(lines)

        # 应用所有启用的规则
        applied_rules = []
        for rule in self.rules:
            if rule.enabled and rule.processor:
                logger.debug(f"应用规则: {rule.code} - {rule.name}")
                lines = rule.processor(lines)
                applied_rules.append(rule.code)

        # MD047: 确保文件以单个换行结束
        new_text = ensure_single_trailing_newline("\n".join(lines))
        final_count = len(new_text.splitlines())

        # 检查是否有变更
        changed = (new_text != original)

        # 非预览模式下写入文件
        if changed and not dry_run:
            write_file(file_path, new_text)
            logger.info(f"已修复: {file_path.name}")

        return ProcessResult(
            file_path=file_path,
            changed=changed,
            original_lines=original_count,
            final_lines=final_count,
            applied_rules=applied_rules
        )

    def process_directory(
        self,
        root_dir: Path,
        dry_run: bool = False,
        exclude_dirs: set[str] | None = None
    ) -> list[ProcessResult]:
        """
        批量处理目录中的所有 Markdown 文件

        Args:
            root_dir: 根目录路径
            dry_run: 是否为预览模式
            exclude_dirs: 要排除的目录名集合

        Returns:
            list[ProcessResult]: 所有文件的处理结果列表
        """
        if exclude_dirs is None:
            exclude_dirs = {
                "node_modules",
                "tools/pdf_export/vendor",
                ".git",
                "__pycache__"
            }

        logger.info(f"扫描目录: {root_dir}")

        # 查找所有 Markdown 文件
        files = [
            p for p in root_dir.rglob("*.md")
            if not self._should_exclude(p, exclude_dirs)
        ]

        logger.info(f"找到 {len(files)} 个 Markdown 文件")

        # 处理所有文件
        results = []
        for file_path in files:
            try:
                result = self.process_file(file_path, dry_run=dry_run)
                results.append(result)
            except Exception as e:
                logger.error(f"处理文件失败: {file_path}, 错误: {e}")

        return results

    @staticmethod
    def _should_exclude(path: Path, exclude_dirs: set[str]) -> bool:
        """检查路径是否应该被排除"""
        parts = set(path.parts)
        return any(ex in parts for ex in exclude_dirs)

    def enable_rule(self, rule_code: str) -> None:
        """启用指定规则"""
        for rule in self.rules:
            if rule.code == rule_code:
                rule.enabled = True
                logger.debug(f"已启用规则: {rule_code}")
                return
        logger.warning(f"未找到规则: {rule_code}")

    def disable_rule(self, rule_code: str) -> None:
        """禁用指定规则"""
        for rule in self.rules:
            if rule.code == rule_code:
                rule.enabled = False
                logger.debug(f"已禁用规则: {rule_code}")
                return
        logger.warning(f"未找到规则: {rule_code}")


# ============================================================================
# 修复规则实现函数
# ============================================================================

def strip_trailing_spaces(lines: list[str]) -> list[str]:
    """
    MD009: 移除行尾空白字符(包括全角空格、NBSP等Unicode空白)

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    return [TRAIL_WS_RE.sub('', ln) for ln in lines]


def compress_blank_lines(lines: list[str]) -> list[str]:
    """
    MD012: 压缩连续空行为单个空行

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
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


def ensure_blank_around_headings(lines: list[str]) -> list[str]:
    """
    MD022: 确保标题前后各有一个空行

    规则:
    - 前: 非文件首行且上一行非空 -> 插入空行
    - 后: 下一行存在且不是空行 -> 插入空行

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    # 第一步: 处理标题前的空行
    out = []
    for i, ln in enumerate(lines):
        if i > 0 and HEADING_RE.match(ln) and (out and out[-1].strip() != ""):
            out.append("")  # 标题上方加空行
        out.append(ln)

    # 第二步: 处理标题后的空行
    i = 0
    res = []
    while i < len(out):
        res.append(out[i])
        if HEADING_RE.match(out[i]):
            # 若后面还有一行且不是空行,就补一行空行
            nxt = out[i + 1] if i + 1 < len(out) else None
            if nxt is not None and nxt.strip() != "":
                res.append("")  # 标题下方加空行
        i += 1
    return res


def fix_fenced_code_language(lines: list[str]) -> list[str]:
    """
    MD040: 为没有语言标注的代码围栏添加默认语言(text)

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    out, in_fence = [], False
    for ln in lines:
        if not in_fence:
            if FENCE_ANY_RE.match(ln):
                if FENCE_LANG_RE.match(ln):
                    # 已经有语言标注
                    in_fence = True
                    out.append(ln)
                elif FENCE_START_RE.match(ln):
                    # 没有语言标注,添加 text
                    in_fence = True
                    out.append("```text")
                else:
                    # 其他情况,默认添加 text
                    in_fence = True
                    out.append("```text")
            else:
                out.append(ln)
        else:
            if FENCE_ANY_RE.match(ln):
                # 围栏结束
                in_fence = False
                out.append("```")
            else:
                out.append(ln)
    return out


def fix_blockquote_blank(lines: list[str]) -> list[str]:
    """
    MD028: 修复引用块中的空行(应该使用 '> ' 而不是完全空行)

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    new = lines[:]
    for i in range(1, len(new) - 1):
        # 如果当前行为空,且上下行都是引用块,则将空行改为 '> '
        if (new[i].strip() == "" and
            new[i - 1].lstrip().startswith(">") and
            new[i + 1].lstrip().startswith(">")):
            new[i] = "> "
    return new


def convert_bare_urls(lines: list[str]) -> list[str]:
    """
    MD034: 将裸URL转换为标准Markdown链接格式 [url](url)

    注意:
    - 跳过代码块内的URL
    - 跳过已经是链接格式的URL

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    out, in_fence = [], False
    for ln in lines:
        # 检测代码围栏
        if FENCE_ANY_RE.match(ln):
            in_fence = not in_fence
            out.append(ln)
            continue

        # 代码块内不处理
        if in_fence:
            out.append(ln)
            continue

        # 跳过已经是链接格式的行
        if "](" in ln or "<http" in ln:
            out.append(ln)
            continue

        # 转换裸URL
        out.append(
            BARE_URL_RE.sub(
                lambda m: f'[{m.group("url")}]({m.group("url")})',
                ln
            )
        )
    return out


def ensure_single_trailing_newline(text: str) -> str:
    """
    MD047: 确保文件以单个换行符结束

    Args:
        text: 文本内容

    Returns:
        str: 处理后的文本内容
    """
    return text.rstrip("\n") + "\n"


# ============================================================================
# 便捷函数
# ============================================================================

def fix_markdown_file(
    file_path: Path | str,
    dry_run: bool = False,
    config: Config | None = None
) -> ProcessResult:
    """
    修复单个 Markdown 文件的便捷函数

    Args:
        file_path: 文件路径
        dry_run: 是否为预览模式
        config: 配置对象

    Returns:
        ProcessResult: 处理结果
    """
    processor = MarkdownProcessor(config)
    return processor.process_file(Path(file_path), dry_run=dry_run)


def fix_markdown_directory(
    root_dir: Path | str,
    dry_run: bool = False,
    exclude_dirs: set[str] | None = None,
    config: Config | None = None
) -> list[ProcessResult]:
    """
    批量修复目录中所有 Markdown 文件的便捷函数

    Args:
        root_dir: 根目录路径
        dry_run: 是否为预览模式
        exclude_dirs: 要排除的目录名集合
        config: 配置对象

    Returns:
        list[ProcessResult]: 所有文件的处理结果列表
    """
    processor = MarkdownProcessor(config)
    return processor.process_directory(
        Path(root_dir),
        dry_run=dry_run,
        exclude_dirs=exclude_dirs
    )
