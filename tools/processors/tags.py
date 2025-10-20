#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签处理器模块

提供标签提取、归一化和相关条目分析功能,包括:
- 标签归一化和同义词映射
- 基于内容的智能标签提取
- 相关条目计算和推荐
- 批量标签重建

基于 retag_and_related.py 和 generate_tags_index.py 重构
"""

from __future__ import annotations

import re
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, MutableMapping

from ..core.config import Config
from ..core.frontmatter import FrontmatterParser, FrontmatterError
from ..core.logger import get_logger
from ..core.utils import read_file, write_file

logger = get_logger(__name__)


# ============================================================================
# 常量定义
# ============================================================================

# 同义词映射表 - 将不同表述归一化为统一标签
SYNONYM_MAP = {
    "多重人格": "多意识体",
    "多重人格障碍": "多意识体",
    "多重系统": "多意识体",
    "多意识体系统": "多意识体",
    "分离性身份障碍": "解离性身份障碍",
    "分离性身份辨识障碍": "解离性身份障碍",
    "解离症状": "解离",
    "解离状态": "解离",
    "解离体验": "解离",
    "心理创伤": "创伤",
    "创伤事件": "创伤",
    "复杂创伤": "创伤",
    "DID": "解离性身份障碍_DID",
    "did": "解离性身份障碍_DID",
    "OSDD": "其他特定解离性障碍_OSDD",
    "osdd": "其他特定解离性障碍_OSDD",
    "PTSD": "创伤后应激障碍_PTSD",
    "ptsd": "创伤后应激障碍_PTSD",
    "ADHD": "注意力缺陷多动障碍_ADHD",
    "adhd": "注意力缺陷多动障碍_ADHD",
    "admin": "管理员",
    "Admin": "管理员",
}

# 停用标签 - 这些不应该作为标签
STOP_TAGS = {
    "简介", "定义", "参考", "参考资料", "参考文献",
    "---", "----", "相关条目", "模板", "条目",
    "外部链接", "许可", "版权", "转载", "来源",
    "目录", "更新", "同义词", "延伸阅读", "注释",
}

# 不应该作为标签的标题前缀
HEADING_SKIP_PREFIXES = (
    "与", "在", "于", "用于", "用以", "作为",
    "针对", "围绕", "关于", "包含", "通过",
)

# 不应该作为标签的标题后缀
HEADING_SKIP_SUFFIXES = (
    "的比较", "的区别", "的区分", "的并列",
    "的交集", "的联系", "的关系",
)

# 允许的纯 ASCII 标签(缩写)
ALLOWED_ASCII_TAGS = {
    "DID", "OSDD", "PTSD", "CPTSD", "DPDR",
    "ADHD", "BPD", "NPD", "SSD", "ANP", "EP",
}

# 标签数量限制
MIN_TAGS = 3
MAX_TAGS = 8

# 正则表达式
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
ASCII_RE = re.compile(r"[A-Za-z]")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+)")
RELATED_BLOCK_RE = re.compile(
    r"^## 相关条目\b.*?(?=^## |\Z)",
    re.MULTILINE | re.DOTALL
)


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class TagInfo:
    """标签信息"""
    original: str
    normalized: str
    source: str  # 'frontmatter', 'heading', 'content', 'index'
    weight: float = 1.0


@dataclass
class EntryRecord:
    """词条记录"""
    path: Path
    title: str
    tags: list[str]
    tokens: Counter = field(default_factory=Counter)
    original_tags: list[str] = field(default_factory=list)


@dataclass
class RelatedEntry:
    """相关条目"""
    path: Path
    title: str
    score: float
    common_tags: list[str]


@dataclass
class TagProcessResult:
    """标签处理结果"""
    file_path: Path
    original_tags: list[str]
    new_tags: list[str]
    changed: bool


# ============================================================================
# 核心处理器类
# ============================================================================

class TagProcessor:
    """
    标签处理器

    提供标签提取、归一化和相关条目分析功能
    """

    def __init__(self, config: Config | None = None):
        """
        初始化标签处理器

        Args:
            config: 配置对象,如果为 None 则使用默认配置
        """
        self.config = config or Config.load()
        self.parser = FrontmatterParser()
        self.synonym_map = SYNONYM_MAP.copy()
        self.stop_tags = STOP_TAGS.copy()

    def normalize_tag(self, tag: str) -> str:
        """
        归一化标签

        - 清理空白字符和标点
        - 应用同义词映射
        - 统一大小写格式

        Args:
            tag: 原始标签

        Returns:
            str: 归一化后的标签
        """
        # 基础清理
        tag = tag.strip()
        if not tag:
            return ""

        # 替换全角空格和特殊空白
        tag = tag.replace("　", " ")
        tag = re.sub(r"[\u3000\u200b]+", " ", tag)

        # 移除标点符号
        tag = re.sub(
            r"[，,。；;：:！!？?（）()\[\]【】<>《》""\"'·•…、/\\|]+",
            " ",
            tag
        )

        # 压缩空白
        tag = re.sub(r"\s+", " ", tag).strip()

        if not tag:
            return ""

        # 应用同义词映射
        lower_tag = tag.lower()
        if lower_tag in self.synonym_map:
            tag = self.synonym_map[lower_tag]
        elif tag in self.synonym_map:
            tag = self.synonym_map[tag]

        # ASCII 标签大写处理
        if re.fullmatch(r"[A-Za-z0-9\- ]+", tag):
            upper = tag.upper()
            if len(upper.replace(" ", "")) <= 6:
                tag = upper
            else:
                tag = upper.title()

        return tag

    def is_valid_tag(self, tag: str) -> bool:
        """
        检查标签是否有效

        Args:
            tag: 标签文本

        Returns:
            bool: 是否为有效标签
        """
        if not tag or tag in self.stop_tags:
            return False

        # 长度限制
        if len(tag) > 18:
            return False

        # 过滤纯数字和年份
        if re.fullmatch(r"\d+(?:年|年代)?", tag):
            return False

        # 检查中英文混合
        has_cn = bool(CHINESE_RE.search(tag))
        has_en = bool(ASCII_RE.search(tag))

        if has_cn and has_en:
            # 中英文混合时,英文部分必须全大写
            ascii_letters = "".join(ch for ch in tag if ch.isalpha())
            if ascii_letters and not ascii_letters.isupper():
                return False

        # 过滤中文空格分隔的情况
        if has_cn and " " in tag:
            parts = [p for p in tag.split(" ") if p]
            if parts and all(CHINESE_RE.search(p) for p in parts):
                return False

        # 纯英文标签需要在白名单中
        if not has_cn and has_en:
            condensed = tag.replace("-", "").replace(" ", "")
            if condensed in ALLOWED_ASCII_TAGS:
                return True
            return False

        return True

    def should_skip_heading(self, heading: str) -> bool:
        """
        检查标题是否应该跳过(不作为标签)

        Args:
            heading: 标题文本

        Returns:
            bool: 是否应该跳过
        """
        # 数字和年份
        if re.fullmatch(r"\d+(?:年|年代)?", heading):
            return True

        # 以特定前缀开头
        for prefix in HEADING_SKIP_PREFIXES:
            if heading.startswith(prefix) and len(heading) > len(prefix):
                return True

        # 以特定后缀结尾
        for suffix in HEADING_SKIP_SUFFIXES:
            if heading.endswith(suffix):
                return True

        return False

    def extract_tags_from_file(
        self,
        file_path: Path
    ) -> list[TagInfo]:
        """
        从文件中提取标签

        包括:
        - Frontmatter 中的 tags
        - 二级标题
        - 内容关键词

        Args:
            file_path: 文件路径

        Returns:
            list[TagInfo]: 提取的标签信息列表
        """
        logger.debug(f"提取标签: {file_path}")

        tags = []
        content = read_file(file_path)

        # 1. 解析 Frontmatter
        try:
            metadata = self.parser.parse(content)

            # 从 Frontmatter 提取标签
            if "tags" in metadata:
                fm_tags = metadata["tags"]
                if isinstance(fm_tags, list):
                    for tag in fm_tags:
                        normalized = self.normalize_tag(str(tag))
                        if normalized and self.is_valid_tag(normalized):
                            tags.append(TagInfo(
                                original=str(tag),
                                normalized=normalized,
                                source="frontmatter",
                                weight=2.0  # Frontmatter 标签权重更高
                            ))

        except FrontmatterError as e:
            logger.warning(f"解析 Frontmatter 失败: {file_path}, {e}")

        # 2. 从标题提取标签
        lines = content.splitlines()
        for line in lines:
            match = HEADING_RE.match(line)
            if match:
                level = len(match.group(1))
                heading = match.group(2).strip()

                # 只处理二级和三级标题
                if level in (2, 3):
                    if self.should_skip_heading(heading):
                        continue

                    normalized = self.normalize_tag(heading)
                    if normalized and self.is_valid_tag(normalized):
                        tags.append(TagInfo(
                            original=heading,
                            normalized=normalized,
                            source="heading",
                            weight=1.5 if level == 2 else 1.0
                        ))

        return tags

    def generate_tags_for_file(
        self,
        file_path: Path,
        dry_run: bool = False
    ) -> TagProcessResult:
        """
        为文件生成并更新标签

        Args:
            file_path: 文件路径
            dry_run: 是否为预览模式

        Returns:
            TagProcessResult: 处理结果
        """
        logger.debug(f"生成标签: {file_path}")

        content = read_file(file_path)

        # 解析当前 Frontmatter
        try:
            metadata = self.parser.parse(content)
            original_tags = metadata.get("tags", [])
            if not isinstance(original_tags, list):
                original_tags = []
        except FrontmatterParseError:
            original_tags = []

        # 提取标签
        tag_infos = self.extract_tags_from_file(file_path)

        # 按权重和频率排序
        tag_counter: Counter = Counter()
        for info in tag_infos:
            tag_counter[info.normalized] += info.weight

        # 选择最佳标签
        new_tags = []
        for tag, _ in tag_counter.most_common(MAX_TAGS):
            if len(new_tags) >= MAX_TAGS:
                break
            if tag not in new_tags:
                new_tags.append(tag)

        # 确保最少标签数
        if len(new_tags) < MIN_TAGS:
            # 保留原有标签补充
            for tag in original_tags:
                normalized = self.normalize_tag(str(tag))
                if normalized and normalized not in new_tags:
                    new_tags.append(normalized)
                if len(new_tags) >= MIN_TAGS:
                    break

        changed = (new_tags != original_tags)

        # 更新文件
        if changed and not dry_run:
            self._update_tags_in_file(file_path, new_tags)
            logger.info(f"已更新标签: {file_path.name}")

        return TagProcessResult(
            file_path=file_path,
            original_tags=original_tags,
            new_tags=new_tags,
            changed=changed
        )

    def _update_tags_in_file(
        self,
        file_path: Path,
        new_tags: list[str]
    ) -> None:
        """
        更新文件中的标签

        Args:
            file_path: 文件路径
            new_tags: 新标签列表
        """
        content = read_file(file_path)

        try:
            metadata = self.parser.parse(content)
            metadata["tags"] = new_tags

            # 重新写入
            new_content = self.parser.dump(metadata, content)
            write_file(file_path, new_content)

        except FrontmatterError as e:
            logger.error(f"更新标签失败: {file_path}, {e}")

    def generate_tags_index(
        self,
        entries_dir: Path,
        output_path: Path | None = None
    ) -> str:
        """
        生成标签索引文档

        Args:
            entries_dir: 词条目录
            output_path: 输出文件路径,如果为 None 则只返回内容

        Returns:
            str: 生成的索引内容
        """
        logger.info(f"生成标签索引: {entries_dir}")

        # 收集所有标签
        tag_entries: dict[str, list[tuple[str, Path]]] = defaultdict(list)

        for file_path in entries_dir.glob("*.md"):
            try:
                content = read_file(file_path)
                metadata = self.parser.parse(content)

                title = metadata.get("title", file_path.stem)
                tags = metadata.get("tags", [])

                if isinstance(tags, list):
                    for tag in tags:
                        tag_str = str(tag).strip()
                        if tag_str:
                            tag_entries[tag_str].append((title, file_path))

            except Exception as e:
                logger.error(f"处理文件失败: {file_path}, {e}")

        # 生成索引内容
        lines = [
            "# 标签索引",
            "",
            "按标签分类的词条列表。",
            "",
        ]

        for tag in sorted(tag_entries.keys()):
            entries = tag_entries[tag]
            lines.append(f"## {tag}")
            lines.append("")

            for title, path in sorted(entries, key=lambda x: x[0]):
                rel_path = f"entries/{path.name}"
                lines.append(f"- [{title}]({rel_path})")

            lines.append("")

        index_content = "\n".join(lines)

        # 写入文件
        if output_path:
            write_file(output_path, index_content)
            logger.info(f"已生成标签索引: {output_path}")

        return index_content

    def add_synonym(self, original: str, replacement: str) -> None:
        """添加同义词映射"""
        self.synonym_map[original] = replacement
        logger.debug(f"添加同义词: {original} -> {replacement}")

    def add_stop_tag(self, tag: str) -> None:
        """添加停用标签"""
        self.stop_tags.add(tag)
        logger.debug(f"添加停用标签: {tag}")


# ============================================================================
# 便捷函数
# ============================================================================

def extract_tags(
    file_path: Path | str,
    config: Config | None = None
) -> list[TagInfo]:
    """
    从文件提取标签的便捷函数

    Args:
        file_path: 文件路径
        config: 配置对象

    Returns:
        list[TagInfo]: 提取的标签信息列表
    """
    processor = TagProcessor(config)
    return processor.extract_tags_from_file(Path(file_path))


def generate_tags(
    file_path: Path | str,
    dry_run: bool = False,
    config: Config | None = None
) -> TagProcessResult:
    """
    为文件生成标签的便捷函数

    Args:
        file_path: 文件路径
        dry_run: 是否为预览模式
        config: 配置对象

    Returns:
        TagProcessResult: 处理结果
    """
    processor = TagProcessor(config)
    return processor.generate_tags_for_file(Path(file_path), dry_run=dry_run)


def generate_tags_index(
    entries_dir: Path | str,
    output_path: Path | str | None = None,
    config: Config | None = None
) -> str:
    """
    生成标签索引的便捷函数

    Args:
        entries_dir: 词条目录
        output_path: 输出文件路径
        config: 配置对象

    Returns:
        str: 生成的索引内容
    """
    processor = TagProcessor(config)
    output = Path(output_path) if output_path else None
    return processor.generate_tags_index(Path(entries_dir), output)
