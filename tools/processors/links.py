#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接处理器模块

提供 Markdown 文档中链接的检查、修复和验证功能,包括:
- 内部链接完整性检查
- 链接格式规范验证
- 相对路径检测和修复
- 白名单管理
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from ..core.config import Config
from ..core.logger import get_logger
from ..core.utils import read_file

logger = get_logger(__name__)


# ============================================================================
# 正则表达式模式
# ============================================================================

# Markdown 链接格式: [text](target) 或 ![alt](target)
LINK_RE = re.compile(
    r'(?P<prefix>!?)\[(?P<text>[^\]]+)\]\((?P<target>[^()\s]+)(?:\s+"[^"]*")?\)',
    re.IGNORECASE,
)


# ============================================================================
# 常量定义
# ============================================================================

# 外链协议白名单
SCHEME_ALLOW = (
    "http://",
    "https://",
    "//",
    "ftp://",
    "ftps://",
    "mailto:",
    "tel:",
    "data:"
)

# 站内锚点和 Docsify 路由
ANCHOR_ALLOW_PREFIX = ("#", "#/")

# 根目录下允许直接链接的站点文件(不强制 entries/ 前缀)
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


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class LinkViolation:
    """链接违规记录"""
    file_path: Path
    line_number: int
    target: str
    reason: str


@dataclass
class LinkCheckResult:
    """链接检查结果"""
    file_path: Path
    total_links: int
    violations: list[LinkViolation] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """是否全部合规"""
        return len(self.violations) == 0

    @property
    def violation_count(self) -> int:
        """违规数量"""
        return len(self.violations)


# ============================================================================
# 核心处理器类
# ============================================================================

class LinkProcessor:
    """
    链接处理器

    提供 Markdown 文档中链接的检查和验证功能
    """

    def __init__(
        self,
        config: Config | None = None,
        extra_whitelist: set[str] | None = None
    ):
        """
        初始化链接处理器

        Args:
            config: 配置对象,如果为 None 则使用默认配置
            extra_whitelist: 额外的白名单文件集合
        """
        self.config = config or Config.load()
        self.root_whitelist = ROOT_WHITELIST.copy()
        if extra_whitelist:
            self.root_whitelist.update(extra_whitelist)

    def check_file(
        self,
        file_path: Path,
        repo_root: Path
    ) -> LinkCheckResult:
        """
        检查单个文件中的链接

        Args:
            file_path: 要检查的文件路径
            repo_root: 仓库根目录

        Returns:
            LinkCheckResult: 检查结果对象
        """
        logger.debug(f"检查文件: {file_path}")

        violations = []
        total_links = 0

        content = read_file(file_path)
        for i, line in enumerate(content.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                total_links += 1
                prefix = match.group("prefix") or ""
                target = match.group("target").strip()
                pure_target = target.split("#", 1)[0]

                # 跳过图片
                if self._is_image(prefix):
                    continue

                # 外链和锚点允许
                if self._is_external(target) or self._is_anchor(target):
                    continue

                # 允许根白名单
                if (pure_target in self.root_whitelist or
                    self._is_root_whitelist(pure_target, repo_root)):
                    continue

                # 允许 docs/ 前缀的文档链接
                if pure_target.startswith("docs/"):
                    candidate = repo_root / pure_target
                    if candidate.exists():
                        continue

                # 允许指向非 entries/ 文件的相对路径
                if Path(pure_target).suffix.lower() == ".md":
                    candidate = (file_path.parent / pure_target).resolve()
                    try:
                        relative = candidate.relative_to(repo_root)
                    except ValueError:
                        relative = None
                    if candidate.exists() and (
                        relative is None or relative.parts[0] != "entries"
                    ):
                        continue

                # 其余看起来像内部链接的做严格校验
                if self._looks_like_internal_md(target):
                    # 1) 禁止 ./ 或 ../
                    if pure_target.startswith("./") or pure_target.startswith("../"):
                        violations.append(
                            LinkViolation(
                                file_path=file_path,
                                line_number=i,
                                target=target,
                                reason="禁止相对路径(./或../)，请改为 entries/*.md 完整路径"
                            )
                        )
                        continue

                    # 2) 必须是 entries/*.md
                    if not self._is_full_entries_path(target):
                        # 若缺少 .md 后缀但明显想引用本地文件,也提示
                        if Path(pure_target).suffix == "":
                            reason = "内部链接缺少 .md 后缀或路径不完整; 请使用 entries/*.md"
                        else:
                            reason = "内部链接路径不合规; 应为 entries/*.md 完整路径"

                        violations.append(
                            LinkViolation(
                                file_path=file_path,
                                line_number=i,
                                target=target,
                                reason=reason
                            )
                        )

        return LinkCheckResult(
            file_path=file_path,
            total_links=total_links,
            violations=violations
        )

    def check_directory(
        self,
        root_dir: Path
    ) -> list[LinkCheckResult]:
        """
        批量检查目录中所有 Markdown 文件的链接

        Args:
            root_dir: 根目录路径

        Returns:
            list[LinkCheckResult]: 所有文件的检查结果列表
        """
        logger.info(f"扫描目录: {root_dir}")

        # 查找所有 Markdown 文件
        files = list(self._find_md_files(root_dir))
        logger.info(f"找到 {len(files)} 个 Markdown 文件")

        # 检查所有文件
        results = []
        for file_path in files:
            try:
                result = self.check_file(file_path, root_dir)
                results.append(result)

                if not result.is_valid:
                    logger.warning(
                        f"文件 {file_path.name} 发现 {result.violation_count} 处违规"
                    )
            except Exception as e:
                logger.error(f"检查文件失败: {file_path}, 错误: {e}")

        return results

    def add_to_whitelist(self, filename: str) -> None:
        """添加文件到白名单"""
        self.root_whitelist.add(filename)
        logger.debug(f"已添加到白名单: {filename}")

    def remove_from_whitelist(self, filename: str) -> None:
        """从白名单移除文件"""
        if filename in self.root_whitelist:
            self.root_whitelist.remove(filename)
            logger.debug(f"已从白名单移除: {filename}")

    # ========================================================================
    # 私有辅助方法
    # ========================================================================

    @staticmethod
    def _is_image(prefix: str) -> bool:
        """检查是否为图片链接"""
        return prefix == "!"

    @staticmethod
    def _is_external(target: str) -> bool:
        """检查是否为外部链接"""
        lower = target.lower()
        return lower.startswith(SCHEME_ALLOW)

    @staticmethod
    def _is_anchor(target: str) -> bool:
        """检查是否为锚点链接"""
        return target.startswith(ANCHOR_ALLOW_PREFIX)

    def _is_root_whitelist(self, target: str, repo_root: Path) -> bool:
        """
        检查是否为根目录白名单文件

        仅接受纯文件名或相对根文件(不带子目录)
        """
        p = Path(target)
        if p.suffix.lower() not in {".md", ".html"}:
            return False

        # 不允许子目录: 如 docs/README.md 不在白名单里
        if len(p.parts) != 1:
            return False

        return p.name in self.root_whitelist and (repo_root / p.name).exists()

    @staticmethod
    def _looks_like_internal_md(target: str) -> bool:
        """
        检查是否看起来像内部 .md 链接

        (不含协议、非锚点、非图片资源)
        """
        if any(target.lower().startswith(s) for s in SCHEME_ALLOW):
            return False

        if target.startswith(ANCHOR_ALLOW_PREFIX):
            return False

        # 过滤可能的图片/资源文件
        pure = target.split("#", 1)[0]
        if Path(pure).suffix.lower() not in (".md", "", ".markdown"):
            return False

        return True

    @staticmethod
    def _is_full_entries_path(target: str) -> bool:
        """检查是否严格满足 entries/*.md 完整路径"""
        pure = target.split("#", 1)[0]
        p = Path(pure)
        return (
            p.suffix.lower() == ".md"
            and len(p.parts) == 2
            and p.parts[0].lower() == "entries"
        )

    @staticmethod
    def _find_md_files(root: Path) -> Iterable[Path]:
        """查找所有 Markdown 文件"""
        return (p for p in root.rglob("*.md") if p.is_file())


# ============================================================================
# 便捷函数
# ============================================================================

def check_links_in_file(
    file_path: Path | str,
    repo_root: Path | str,
    config: Config | None = None,
    extra_whitelist: set[str] | None = None
) -> LinkCheckResult:
    """
    检查单个文件中链接的便捷函数

    Args:
        file_path: 文件路径
        repo_root: 仓库根目录
        config: 配置对象
        extra_whitelist: 额外的白名单文件集合

    Returns:
        LinkCheckResult: 检查结果
    """
    processor = LinkProcessor(config, extra_whitelist)
    return processor.check_file(Path(file_path), Path(repo_root))


def check_links_in_directory(
    root_dir: Path | str,
    config: Config | None = None,
    extra_whitelist: set[str] | None = None
) -> list[LinkCheckResult]:
    """
    批量检查目录中所有文件链接的便捷函数

    Args:
        root_dir: 根目录路径
        config: 配置对象
        extra_whitelist: 额外的白名单文件集合

    Returns:
        list[LinkCheckResult]: 所有文件的检查结果列表
    """
    processor = LinkProcessor(config, extra_whitelist)
    return processor.check_directory(Path(root_dir))
