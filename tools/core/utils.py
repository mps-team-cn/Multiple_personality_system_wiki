"""
通用工具函数模块
提供各种辅助功能和工具函数
"""

from __future__ import annotations

import hashlib
import re
import time
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

from .logger import get_logger
from .config import get_config

logger = get_logger(__name__)


def get_file_hash(file_path: Union[str, Path], algorithm: str = "md5") -> str:
    """
    计算文件的哈希值。

    Args:
        file_path: 文件路径
        algorithm: 哈希算法

    Returns:
        哈希值字符串
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()


def find_files(
    root_dir: Union[str, Path],
    pattern: str = "*.md",
    recursive: bool = True,
    ignore_patterns: Optional[List[str]] = None
) -> Generator[Path, None, None]:
    """
    查找文件。

    Args:
        root_dir: 根目录
        pattern: 文件模式
        recursive: 是否递归查找
        ignore_patterns: 忽略的模式列表

    Yields:
        找到的文件路径
    """
    root_path = Path(root_dir)
    if not root_path.exists():
        logger.warning(f"目录不存在: {root_path}")
        return

    if ignore_patterns is None:
        config = get_config()
        ignore_patterns = config.paths.ignore_patterns

    def should_ignore(file_path: Path) -> bool:
        """检查文件是否应该被忽略。"""
        file_str = str(file_path)
        for pattern in ignore_patterns:
            if pattern in file_str:
                return True
        return False

    if recursive:
        for file_path in root_path.rglob(pattern):
            if not should_ignore(file_path):
                yield file_path
    else:
        for file_path in root_path.glob(pattern):
            if not should_ignore(file_path):
                yield file_path


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    获取文件信息。

    Args:
        file_path: 文件路径

    Returns:
        文件信息字典
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    stat = file_path.stat()

    return {
        'path': str(file_path),
        'name': file_path.name,
        'stem': file_path.stem,
        'suffix': file_path.suffix,
        'size': stat.st_size,
        'modified_time': stat.st_mtime,
        'created_time': stat.st_ctime,
        'is_file': file_path.is_file(),
        'is_dir': file_path.is_dir()
    }


def safe_read_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    安全读取文件。

    Args:
        file_path: 文件路径
        encoding: 文件编码

    Returns:
        文件内容

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 编码错误
        OSError: 其他读取错误
    """
    file_path = Path(file_path)
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise
    except UnicodeDecodeError as e:
        logger.error(f"文件编码错误 {file_path}: {e}")
        raise
    except OSError as e:
        logger.error(f"读取文件失败 {file_path}: {e}")
        raise


def safe_write_file(
    file_path: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
    create_dirs: bool = True
) -> None:
    """
    安全写入文件。

    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 文件编码
        create_dirs: 是否创建目录
    """
    file_path = Path(file_path)

    if create_dirs:
        file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        logger.debug(f"文件写入成功: {file_path}")
    except OSError as e:
        logger.error(f"写入文件失败 {file_path}: {e}")
        raise


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小。

    Args:
        size_bytes: 字节数

    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_timestamp(timestamp: float) -> str:
    """
    格式化时间戳。

    Args:
        timestamp: 时间戳

    Returns:
        格式化后的时间字符串
    """
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def normalize_text(text: str) -> str:
    """
    规范化文本。

    Args:
        text: 输入文本

    Returns:
        规范化后的文本
    """
    # 替换中文标点为英文标点
    text = re.sub(r'[，。！？；：""''（）【】]', lambda m: {
        '，': ',', '。': '.', '！': '!', '？': '?',
        '；': ';', '：': ':', '"': '"', "'": "'",
        '（': '(', '）': ')', '【': '[', '】': ']'
    }[m.group()], text)

    # 统一空格
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def extract_links_from_content(content: str) -> List[str]:
    """
    从内容中提取链接。

    Args:
        content: 文本内容

    Returns:
        链接列表
    """
    # Markdown 链接
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    # 直接链接
    direct_links = re.findall(r'https?://[^\s]+', content)

    links = [link for _, link in md_links] + direct_links
    return list(set(links))  # 去重


def is_markdown_file(file_path: Union[str, Path]) -> bool:
    """
    检查是否为 Markdown 文件。

    Args:
        file_path: 文件路径

    Returns:
        是否为 Markdown 文件
    """
    file_path = Path(file_path)
    return file_path.suffix.lower() in ['.md', '.markdown']


def validate_filename(filename: str) -> bool:
    """
    验证文件名是否有效。

    Args:
        filename: 文件名

    Returns:
        是否有效
    """
    if not filename:
        return False

    # 检查无效字符
    invalid_chars = '<>:"/\\|?*'
    if any(char in filename for char in invalid_chars):
        return False

    # 检查长度
    if len(filename) > 255:
        return False

    # 检查保留名称
    reserved_names = {'CON', 'PRN', 'AUX', 'NUL'}
    if filename.upper() in reserved_names:
        return False

    return True


def create_backup(file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Path:
    """
    创建文件备份。

    Args:
        file_path: 原始文件路径
        backup_dir: 备份目录

    Returns:
        备份文件路径
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if backup_dir:
        backup_dir = Path(backup_dir)
    else:
        backup_dir = file_path.parent / "backups"

    backup_dir.mkdir(parents=True, exist_ok=True)

    # 生成备份文件名
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = backup_dir / backup_name

    # 复制文件
    safe_write_file(backup_path, safe_read_file(file_path))

    logger.info(f"创建备份: {backup_path}")
    return backup_path


def clean_old_backups(backup_dir: Union[str, Path], max_count: int = 10) -> List[Path]:
    """
    清理旧备份文件。

    Args:
        backup_dir: 备份目录
        max_count: 保留的最大数量

    Returns:
        删除的备份文件列表
    """
    backup_dir = Path(backup_dir)
    if not backup_dir.exists():
        return []

    # 获取所有备份文件并按修改时间排序
    backup_files = []
    for file_path in backup_dir.iterdir():
        if file_path.is_file():
            backup_files.append((file_path.stat().st_mtime, file_path))

    backup_files.sort(reverse=True)

    # 删除多余的备份
    deleted_files = []
    for _, file_path in backup_files[max_count:]:
        try:
            file_path.unlink()
            deleted_files.append(file_path)
            logger.debug(f"删除旧备份: {file_path}")
        except OSError as e:
            logger.error(f"删除备份文件失败 {file_path}: {e}")

    return deleted_files


def timing(func):
    """
    装饰器：测量函数执行时间。
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f"{func.__name__} 执行时间: {end_time - start_time:.3f} 秒")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: Tuple = (Exception,)):
    """
    装饰器：重试机制。

    Args:
        max_attempts: 最大重试次数
        delay: 重试延迟（秒）
        exceptions: 捕获的异常类型
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"{func.__name__} 重试失败: {e}")
                        raise
                    logger.warning(f"{func.__name__} 第 {attempt + 1} 次重试: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


def chunked_list(lst: List[Any], chunk_size: int) -> Generator[List[Any], None, None]:
    """
    将列表分块。

    Args:
        lst: 输入列表
        chunk_size: 块大小

    Yields:
        分块后的列表
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个字典。

    Args:
        *dicts: 要合并的字典

    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    扁平化嵌套字典。

    Args:
        d: 嵌套字典
        parent_key: 父键
        sep: 分隔符

    Returns:
        扁平化后的字典
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# 为向后兼容和简洁性提供的别名
read_file = safe_read_file
write_file = safe_write_file