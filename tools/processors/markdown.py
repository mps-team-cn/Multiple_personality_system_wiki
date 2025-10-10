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

from ..core.config import Config, load_config
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

# 列表项（无序和有序）
LIST_ITEM_RE = re.compile(r'^(\s*)([-*+]|\d+\.)\s+')
UNORDERED_MARKER_NEEDS_SPACE_RE = re.compile(r'^(\s*)(-(?!-)|\+(?!\+)|\*(?!\*))(?=\S)')
ORDERED_MARKER_NEEDS_SPACE_RE = re.compile(r'^(\s*)(\d+\.)(?=\S)')

# 强调标记（加粗、斜体）
# 优先匹配双标记(**/__),然后单标记(*/_)
EMPHASIS_SEGMENT_RE = re.compile(r'(\*\*|__|(?<!\*)\*(?!\*)|(?<!_)_(?!_))(.+?)(\1)')

# 列表项加粗冒号格式：-**text**: 或 -**text**：
LIST_BOLD_COLON_RE = re.compile(r'^(\s*)-\*\*([^*]+)\*\*[：:]\s*(.*)$')

# 加粗链接格式：**[文本](链接)**
BOLD_LINK_RE = re.compile(r'\*\*\[([^\]]+)\]\(([^\)]+)\)\*\*')

# 中文字符和标点
CHINESE_CHAR_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
CHINESE_PUNCT = r'[，。！？；：、''""（）《》【】…—]'

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
        self.config = config or load_config()
        self.rules = self._init_rules()

    def _init_rules(self) -> list[FixRule]:
        """初始化修复规则列表"""
        return [
            # === Markdownlint 标准规则 ===
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
                name="blockquote_blank",
                code="MD028",
                description="修复引用块中的空行",
                processor=fix_blockquote_blank
            ),
            FixRule(
                name="blank_around_fences",
                code="MD031",
                description="确保代码块前后空行",
                processor=ensure_blank_around_fences
            ),
            FixRule(
                name="blank_around_lists",
                code="MD032",
                description="确保列表前后空行",
                processor=ensure_blank_around_lists
            ),
            FixRule(
                name="bare_urls",
                code="MD034",
                description="转换裸链接为标准格式",
                processor=convert_bare_urls
            ),
            FixRule(
                name="emphasis_spaces",
                code="MD037",
                description="修复强调标记内空格",
                processor=fix_emphasis_spaces
            ),
            FixRule(
                name="fenced_code_language",
                code="MD040",
                description="为代码围栏添加语言标注",
                processor=fix_fenced_code_language
            ),

            # === 中文排版规则 ===
            FixRule(
                name="list_marker_spacing",
                code="CUSTOM001",
                description="确保列表标记后有空格",
                processor=normalize_list_marker_spacing
            ),
            FixRule(
                name="bold_chinese_spacing",
                code="CUSTOM002",
                description="确保加粗文本与中文间有空格",
                processor=fix_bold_spacing
            ),
            FixRule(
                name="list_bold_colon",
                code="CUSTOM003",
                description="修复列表加粗冒号格式",
                processor=fix_list_bold_colon
            ),
            FixRule(
                name="chinese_parentheses",
                code="CUSTOM004",
                description="链接文本括号全角化",
                processor=fix_parentheses_in_links
            ),
            FixRule(
                name="chinese_colon",
                code="CUSTOM005",
                description="参阅等冒号全角化",
                processor=fix_colon_before_links
            ),
            FixRule(
                name="nested_list_indentation",
                code="CUSTOM006",
                description="修复嵌套列表缩进为4空格",
                processor=fix_nested_list_indentation
            ),
        ]

    def process(self, text: str) -> str:
        """
        处理 Markdown 文本字符串

        Args:
            text: 输入的 Markdown 文本

        Returns:
            str: 处理后的 Markdown 文本
        """
        lines = text.splitlines()

        # 应用所有启用的规则
        for rule in self.rules:
            if rule.enabled and rule.processor:
                lines = rule.processor(lines)

        # MD047: 确保文件以单个换行结束
        result = ensure_single_trailing_newline("\n".join(lines))
        return result

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


def normalize_list_marker_spacing(lines: list[str]) -> list[str]:
    """
    确保列表标记后至少有一个空格

    Examples:
        -item -> - item
        +item -> + item
        1.item -> 1. item

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
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


def ensure_blank_around_fences(lines: list[str]) -> list[str]:
    """
    MD031: 代码块前后各留 1 个空行

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
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
    """
    MD032: 列表前后各留 1 个空行

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
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
    """
    MD037: 修复强调标记内的空格,并确保强调段前后留白

    Examples:
        ** text ** -> **text**
        中文**加粗**文字 -> 中文 **加粗** 文字
        **定义**：内容 -> **定义**：内容 (中文标点不加空格)

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    # 中文标点符号集合
    chinese_punct_set = set('，。！？；：、''""（）《》【】…—')

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

            # 只在非标点前加空格
            if pieces and last_char and not last_char.isspace() and last_char not in chinese_punct_set:
                # 检查是否为中文字符
                if CHINESE_CHAR_RE.search(last_char):
                    pieces.append(" ")
                    last_char = " "

            pieces.append(f"{start_tag}{content}{end_tag}")
            last_char = end_tag[-1]
            last_idx = match.end()

            # 只在非标点后加空格
            if match.end() < len(ln):
                next_char = ln[match.end()]
                if not next_char.isspace() and next_char not in chinese_punct_set:
                    # 检查下一个字符是否为中文
                    if CHINESE_CHAR_RE.search(next_char):
                        pieces.append(" ")
                        last_char = " "

        if last_idx < len(ln):
            tail = ln[last_idx:]
            pieces.append(tail)
        out.append("".join(pieces))

    return out


def fix_bold_spacing(lines: list[str]) -> list[str]:
    """
    确保加粗文本与中文之间有空格

    Examples:
        **中文**中文 -> **中文** 中文
        中文**中文** -> 中文 **中文**

    注意：加粗文本与中文标点之间不加空格

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    # 中文标点符号集合
    chinese_punct_set = set('，。！？；：、''""（）《》【】…—')

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

        # 使用精确的加粗匹配模式：确保 ** 成对出现
        # 匹配 **内容**，内容不包含 *
        bold_pattern = re.compile(r'\*\*([^*]+)\*\*')

        # 找到所有加粗标记的位置
        matches = list(bold_pattern.finditer(ln))
        if not matches:
            out.append(ln)
            continue

        # 从后往前处理，避免位置偏移
        for match in reversed(matches):
            start, end = match.span()

            # 检查加粗前面的字符
            if start > 0:
                prev_char = ln[start - 1]
                # 如果前面是中文字符（非标点非空格），加空格
                if CHINESE_CHAR_RE.search(prev_char) and prev_char not in chinese_punct_set and not prev_char.isspace():
                    ln = ln[:start] + ' ' + ln[start:]
                    end += 1  # 位置偏移

            # 检查加粗后面的字符
            if end < len(ln):
                next_char = ln[end]
                # 如果后面是中文字符（非标点非空格），加空格
                if CHINESE_CHAR_RE.search(next_char) and next_char not in chinese_punct_set and not next_char.isspace():
                    ln = ln[:end] + ' ' + ln[end:]

        out.append(ln)

    return out


def fix_list_bold_colon(lines: list[str]) -> list[str]:
    """
    修复列表项中粗体冒号格式

    与原工具 fix_list_bold_colon.py 保持一致：
    -**text**: -> - **text** :
    -**text**： -> - **text** :

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    out = []
    for ln in lines:
        match = LIST_BOLD_COLON_RE.match(ln)
        if match:
            indent = match.group(1)
            bold_text = match.group(2).strip()
            rest = match.group(3)
            # 与原工具保持一致：半角冒号，前后都有空格
            new_line = f"{indent}- **{bold_text}** : {rest}"
            out.append(new_line)
        else:
            out.append(ln)
    return out


def fix_parentheses_in_links(lines: list[str]) -> list[str]:
    """
    修复链接相关的括号格式：
    1. 链接文本中的半角括号 -> 全角括号
    2. 链接外的中文括号 -> 半角括号
    3. 加粗链接格式 **[文本](url)** -> [**文本**](url)

    Examples:
        [创伤(Trauma)](Trauma.md) -> [创伤（Trauma）](Trauma.md)
        （[链接](url)） -> ([链接](url))
        **[文本](url)** -> [**文本**](url)

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    out = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

    for ln in lines:
        # 1. 修复加粗链接格式
        ln = BOLD_LINK_RE.sub(r'[**\1**](\2)', ln)

        # 2. 修复链接文本中的括号
        def replacer(match):
            text = match.group(1)
            url = match.group(2)
            if '(' in text or ')' in text:
                new_text = text.replace('(', '（').replace(')', '）')
                return f'[{new_text}]({url})'
            return match.group(0)

        ln = link_pattern.sub(replacer, ln)

        # 3. 修复链接外的中文括号为半角
        # 匹配中文括号包裹的链接
        ln = re.sub(r'（(\[[^\]]+\]\([^\)]+\))）', r'(\1)', ln)

        out.append(ln)
    return out


def fix_colon_before_links(lines: list[str]) -> list[str]:
    """
    修复"参阅:"等冒号为全角冒号

    Examples:
        参阅: -> 参阅：
        参考: -> 参考：

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    patterns = [
        ('参阅:', '参阅：'),
        ('参考:', '参考：'),
        ('延伸阅读:', '延伸阅读：'),
        ('详细了解请参阅:', '详细了解请参阅：'),
    ]

    out = []
    for ln in lines:
        for old, new in patterns:
            ln = ln.replace(old, new)
        out.append(ln)
    return out


def fix_nested_list_indentation(lines: list[str]) -> list[str]:
    """
    修复嵌套列表缩进：将2空格缩进改为4空格缩进

    MkDocs 使用的 Python-Markdown 要求嵌套列表必须缩进4个空格（或1个tab）。
    2个空格的缩进会导致子列表无法正确渲染。

    Examples:
        - item1
          - subitem  ->  - item1
                             - subitem

    Args:
        lines: 文本行列表

    Returns:
        list[str]: 处理后的文本行列表
    """
    out = []
    in_fence = False

    for ln in lines:
        # 跳过代码块
        if FENCE_ANY_RE.match(ln):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue

        # 检测列表项：匹配缩进 + 列表标记
        match = LIST_ITEM_RE.match(ln)
        if match:
            indent = match.group(1)  # 缩进部分
            indent_len = len(indent)

            # 如果缩进不是4的倍数，调整为最接近的4的倍数
            if indent_len > 0 and indent_len % 4 != 0:
                # 计算应该的缩进量（向上取整到4的倍数）
                new_indent_len = ((indent_len + 3) // 4) * 4
                new_indent = ' ' * new_indent_len
                # 替换缩进部分
                ln = new_indent + ln[indent_len:]

        out.append(ln)

    return out


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


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Markdown 文档处理器 - 修复格式问题和中文排版"
    )
    parser.add_argument(
        "path",
        help="要处理的文件或目录路径"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="预览模式，不实际修改文件"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细输出"
    )

    args = parser.parse_args()

    # 设置日志级别
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    path = Path(args.path)

    if not path.exists():
        print(f"错误: 路径不存在: {path}")
        return 1

    print("=" * 60)
    print("Markdown 处理器")
    print("=" * 60)
    if args.dry_run:
        print("模式: 预览（不会修改文件）")
    print(f"路径: {path}")
    print()

    # 处理文件或目录
    if path.is_file():
        result = fix_markdown_file(path, dry_run=args.dry_run)
        if result.changed:
            print(f"[修改] {result.file_path.name}")
            print(f"  行数: {result.original_lines} → {result.final_lines}")
            print(f"  规则: {', '.join(result.applied_rules)}")
        else:
            print(f"[跳过] {result.file_path.name} (无需修改)")
    else:
        results = fix_markdown_directory(path, dry_run=args.dry_run)
        changed_count = sum(1 for r in results if r.changed)

        for result in results:
            if result.changed:
                print(f"[修改] {result.file_path.name}")
                if args.verbose:
                    print(f"  行数: {result.original_lines} → {result.final_lines}")
                    print(f"  规则: {', '.join(result.applied_rules)}")

        print()
        print("=" * 60)
        print(f"处理完成: {len(results)} 个文件，{changed_count} 个文件已修改")
        print("=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
