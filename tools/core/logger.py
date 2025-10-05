"""
统一的日志记录机制
提供配置化的日志记录功能
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, Union

# 全局日志记录器缓存
_loggers = {}


def setup_logger(
    name: str,
    level: str = "INFO",
    format_string: Optional[str] = None,
    file_path: Optional[Union[str, Path]] = None,
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    console: bool = True
) -> logging.Logger:
    """
    设置日志记录器。

    Args:
        name: 日志记录器名称
        level: 日志级别
        format_string: 日志格式字符串
        file_path: 日志文件路径
        max_file_size: 最大文件大小（字节）
        backup_count: 备份文件数量
        console: 是否输出到控制台

    Returns:
        配置好的日志记录器
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # 清除现有的处理器
    logger.handlers.clear()

    # 设置默认格式
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)

    # 控制台处理器
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # 文件处理器
    if file_path:
        try:
            from logging.handlers import RotatingFileHandler

            log_file = Path(file_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_file_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # 如果文件处理器设置失败，至少保证控制台输出正常
            logger.error(f"设置日志文件处理器失败: {e}")

    # 缓存日志记录器
    _loggers[name] = logger
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器。

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器实例
    """
    if name in _loggers:
        return _loggers[name]

    # 返回根日志记录器
    return logging.getLogger(name)


def configure_logging(config):
    """
    根据配置设置日志。

    Args:
        config: 日志配置对象
    """
    setup_logger(
        name="tools",
        level=config.level,
        format_string=config.format,
        file_path=config.file_path,
        max_file_size=config.max_file_size,
        backup_count=config.backup_count,
        console=True
    )


def set_log_level(level: str) -> None:
    """
    设置所有日志记录器的级别。

    Args:
        level: 日志级别
    """
    log_level = getattr(logging, level.upper())
    for logger in _loggers.values():
        logger.setLevel(log_level)


def add_file_handler(logger: logging.Logger, file_path: Union[str, Path]) -> None:
    """
    为日志记录器添加文件处理器。

    Args:
        logger: 日志记录器
        file_path: 日志文件路径
    """
    try:
        from logging.handlers import RotatingFileHandler

        log_file = Path(file_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except Exception as e:
        logger.error(f"添加文件处理器失败: {e}")


def get_child_logger(parent_name: str, child_name: str) -> logging.Logger:
    """
    获取子日志记录器。

    Args:
        parent_name: 父日志记录器名称
        child_name: 子日志记录器名称

    Returns:
        子日志记录器
    """
    full_name = f"{parent_name}.{child_name}"
    return get_logger(full_name)