"""
配置管理系统
提供统一的配置加载和管理功能
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class MarkdownConfig:
    """Markdown 处理配置。"""
    line_length: int = 120
    trailing_spaces: bool = True
    header_blank_lines: bool = True
    code_block_language: bool = True
    list_indentation: int = 2
    strong_style: str = "consistent"  # consistent, asterisk, underscore


@dataclass
class ValidationConfig:
    """校验配置。"""
    required_fields: List[str] = field(default_factory=lambda: ["title", "tags", "updated"])
    max_title_length: int = 100
    min_tags_count: int = 1
    max_tags_count: int = 10
    allowed_tags: Optional[List[str]] = None
    forbidden_tags: Optional[List[str]] = None
    check_internal_links: bool = True
    check_external_links: bool = False


@dataclass
class GenerationConfig:
    """生成器配置。"""
    search_index_output: str = "assets/search-index.json"
    tags_index_output: str = "tags.md"
    changelog_output: str = "changelog.md"
    validation_report_output: str = "docs/VALIDATION_REPORT.md"
    include_drafts: bool = False
    sort_by: str = "title"  # title, updated, filename


@dataclass
class PathConfig:
    """路径配置。"""
    entries_dir: str = "entries"
    assets_dir: str = "assets"
    docs_dir: str = "docs"
    output_dir: str = "dist"
    template_dir: str = "templates"
    ignore_patterns: List[str] = field(default_factory=lambda: [
        "node_modules",
        ".git",
        "__pycache__",
        "*.pyc",
        ".DS_Store"
    ])


@dataclass
class LoggingConfig:
    """日志配置。"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class Config:
    """主配置类。"""
    markdown: MarkdownConfig = field(default_factory=MarkdownConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    def __post_init__(self):
        """初始化后处理。"""
        # 确保路径为绝对路径
        if hasattr(self, '_base_path') and self._base_path:
            self._make_paths_absolute(self._base_path)

    def _make_paths_absolute(self, base_path: Path):
        """将相对路径转换为绝对路径。"""
        base = Path(base_path)

        # 处理路径配置
        for path_field in ['entries_dir', 'assets_dir', 'docs_dir', 'output_dir', 'template_dir']:
            current_path = getattr(self.paths, path_field)
            if not Path(current_path).is_absolute():
                setattr(self.paths, path_field, str(base / current_path))

        # 处理输出路径配置
        for output_field in ['search_index_output', 'tags_index_output', 'changelog_output', 'validation_report_output']:
            current_path = getattr(self.generation, output_field)
            if not Path(current_path).is_absolute():
                setattr(self.generation, output_field, str(base / current_path))

        # 处理日志文件路径
        if self.logging.file_path and not Path(self.logging.file_path).is_absolute():
            self.logging.file_path = str(base / self.logging.file_path)


class ConfigManager:
    """配置管理器。"""

    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        初始化配置管理器。

        Args:
            config_file: 配置文件路径，默认为 tools/config.json
        """
        self.logger = get_logger(self.__class__.__name__)

        # 确定配置文件路径
        if config_file:
            self.config_file = Path(config_file)
        else:
            # 默认配置文件位置
            current_dir = Path(__file__).parent
            self.config_file = current_dir / "config.json"

        self.config = Config()
        self._base_path = None

    def load_config(self, base_path: Optional[Union[str, Path]] = None) -> Config:
        """
        加载配置。

        Args:
            base_path: 基础路径，用于解析相对路径

        Returns:
            配置对象
        """
        if base_path:
            self._base_path = Path(base_path).resolve()

        # 尝试加载配置文件
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                self._update_config_from_dict(config_data)
                self.logger.info(f"已加载配置文件: {self.config_file}")
            except Exception as e:
                self.logger.error(f"加载配置文件失败: {e}")
                self.logger.info("使用默认配置")
        else:
            self.logger.info("配置文件不存在，使用默认配置")
            # 尝试创建默认配置文件
            self.save_config()

        # 设置基础路径
        if self._base_path:
            self.config._base_path = self._base_path
            self.config._make_paths_absolute(self._base_path)

        return self.config

    def save_config(self, config: Optional[Config] = None) -> None:
        """
        保存配置到文件。

        Args:
            config: 要保存的配置对象，默认为当前配置
        """
        if config is None:
            config = self.config

        try:
            # 确保目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # 转换为字典并保存
            config_dict = asdict(config)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)

            self.logger.info(f"配置已保存到: {self.config_file}")
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")

    def update_config(self, **kwargs) -> None:
        """
        更新配置。

        Args:
            **kwargs: 配置更新参数
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.debug(f"更新配置: {key} = {value}")
            else:
                self.logger.warning(f"未知配置项: {key}")

    def _update_config_from_dict(self, config_data: Dict[str, Any]) -> None:
        """从字典更新配置。"""
        for section_name, section_data in config_data.items():
            if hasattr(self.config, section_name) and isinstance(section_data, dict):
                section = getattr(self.config, section_name)
                for key, value in section_data.items():
                    if hasattr(section, key):
                        setattr(section, key, value)
                        self.logger.debug(f"更新配置: {section_name}.{key} = {value}")

    def get_env_config(self) -> Dict[str, Any]:
        """从环境变量获取配置覆盖。"""
        env_config = {}

        # 定义环境变量映射
        env_mappings = {
            'TOOLS_LOG_LEVEL': ('logging', 'level'),
            'TOOLS_LOG_FILE': ('logging', 'file_path'),
            'TOOLS_ENTRIES_DIR': ('paths', 'entries_dir'),
            'TOOLS_ASSETS_DIR': ('paths', 'assets_dir'),
            'TOOLS_DOCS_DIR': ('paths', 'docs_dir'),
            'TOOLS_OUTPUT_DIR': ('paths', 'output_dir'),
            'TOOLS_STRICT_MODE': ('validation', 'strict_mode'),
        }

        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                if section not in env_config:
                    env_config[section] = {}

                # 尝试转换数据类型
                if key in ['level']:
                    env_config[section][key] = value
                elif key.endswith('_dir') or key.endswith('_file'):
                    env_config[section][key] = value
                elif value.lower() in ['true', 'false']:
                    env_config[section][key] = value.lower() == 'true'
                else:
                    try:
                        env_config[section][key] = int(value)
                    except ValueError:
                        env_config[section][key] = value

        return env_config


# 全局配置管理器实例
_config_manager = None


def get_config_manager(config_file: Optional[Union[str, Path]] = None) -> ConfigManager:
    """获取全局配置管理器实例。"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager


def load_config(base_path: Optional[Union[str, Path]] = None) -> Config:
    """加载配置。"""
    return get_config_manager().load_config(base_path)


def get_config() -> Config:
    """获取当前配置。"""
    if _config_manager is None:
        return load_config()
    return _config_manager.config