"""
核心模块包
提供统一的基础功能和服务
"""

__version__ = "1.0.0"
__author__ = "Plurality Wiki Team"

from .frontmatter import FrontmatterParser
from .config import Config
from .logger import setup_logger
from .utils import *

__all__ = [
    'FrontmatterParser',
    'Config',
    'setup_logger'
]