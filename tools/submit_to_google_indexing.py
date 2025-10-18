#!/usr/bin/env python3
"""
Google Indexing API 自动提交工具
使用 Google Indexing API 批量提交 URL 到 Google Search Console 以加速索引

功能特性:
- 读取由 generate_seo_urls.py 生成的 URL 列表
- 支持批量提交(最多 100 个 URL/批次)
- Service Account JSON 认证
- 智能配额管理(默认 200 请求/天)
- 重试机制处理临时错误
- 详细的日志输出
- Dry-run 模式用于测试

使用示例:
    # 使用环境变量中的 Service Account JSON
    python3 tools/submit_to_google_indexing.py

    # 指定 JSON 文件路径
    python3 tools/submit_to_google_indexing.py --credentials /path/to/service-account.json

    # Dry-run 模式
    python3 tools/submit_to_google_indexing.py --dry-run

    # 指定优先级(1=最高,2=高)
    python3 tools/submit_to_google_indexing.py --max-priority 2

    # 限制提交数量
    python3 tools/submit_to_google_indexing.py --limit 50

    # 自动确认提交(用于自动化场景,跳过交互式确认)
    python3 tools/submit_to_google_indexing.py --yes
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("错误: 缺少必需的 Google API 库")
    print("请运行: pip install google-auth google-api-python-client")
    sys.exit(1)

# 导入 URL 生成器
try:
    from generate_seo_urls import generate_url_list, BASE_URL
except ImportError:
    print("错误: 无法导入 generate_seo_urls 模块")
    print("请确保 generate_seo_urls.py 在同一目录下")
    sys.exit(1)

# Google Indexing API 配置
SCOPES = ["https://www.googleapis.com/auth/indexing"]
API_SERVICE_NAME = "indexing"
API_VERSION = "v3"
BATCH_SIZE = 100  # Google API 批量请求限制
DAILY_QUOTA = 200  # 默认配额
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # 秒

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class GoogleIndexingClient:
    """Google Indexing API 客户端"""

    def __init__(self, credentials_path: Optional[str] = None, dry_run: bool = False):
        """
        初始化客户端

        Args:
            credentials_path: Service Account JSON 文件路径
            dry_run: 是否为 dry-run 模式
        """
        self.dry_run = dry_run
        self.service = None
        self.submitted_count = 0
        self.failed_count = 0
        self.skipped_count = 0

        if not dry_run:
            self._initialize_service(credentials_path)

    def _initialize_service(self, credentials_path: Optional[str] = None):
        """初始化 Google API 服务"""
        try:
            # 从文件或环境变量获取凭证
            if credentials_path:
                logger.info(f"从文件加载凭证: {credentials_path}")
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path, scopes=SCOPES
                )
            else:
                # 尝试从环境变量加载
                creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
                if not creds_json:
                    raise ValueError(
                        "未提供凭证: 请通过 --credentials 参数指定文件路径,或设置 "
                        "GOOGLE_SERVICE_ACCOUNT_JSON 环境变量"
                    )

                logger.info("从环境变量 GOOGLE_SERVICE_ACCOUNT_JSON 加载凭证")
                creds_info = json.loads(creds_json)
                credentials = service_account.Credentials.from_service_account_info(
                    creds_info, scopes=SCOPES
                )

            # 构建 API 服务
            self.service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
            logger.info("Google Indexing API 服务初始化成功")

        except FileNotFoundError:
            logger.error(f"凭证文件不存在: {credentials_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON 格式错误: {e}")
            raise
        except Exception as e:
            logger.error(f"初始化失败: {e}")
            raise

    def submit_url(self, url: str, url_type: str = "URL_UPDATED") -> bool:
        """
        提交单个 URL

        Args:
            url: 要提交的 URL
            url_type: 请求类型 (URL_UPDATED 或 URL_DELETED)

        Returns:
            bool: 是否成功
        """
        if self.dry_run:
            logger.info(f"[DRY-RUN] 将提交: {url}")
            return True

        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                body = {
                    "url": url,
                    "type": url_type
                }

                response = self.service.urlNotifications().publish(body=body).execute()
                logger.info(f"✓ 成功提交: {url}")
                self.submitted_count += 1
                return True

            except HttpError as e:
                error_details = e.error_details if hasattr(e, 'error_details') else str(e)

                # 处理特定错误
                if e.resp.status == 403:
                    logger.error(f"✗ 权限不足 (403): {url}")
                    logger.error("  提示: 请确认 Service Account 已被添加为网站所有者")
                    self.failed_count += 1
                    return False
                elif e.resp.status == 429:
                    logger.warning(f"⚠ 配额超限 (429): {url}")
                    if attempt < RETRY_ATTEMPTS:
                        delay = RETRY_DELAY * attempt
                        logger.info(f"  等待 {delay} 秒后重试 (尝试 {attempt}/{RETRY_ATTEMPTS})")
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"✗ 达到最大重试次数: {url}")
                        self.failed_count += 1
                        return False
                elif e.resp.status == 400:
                    logger.error(f"✗ 请求无效 (400): {url}")
                    logger.error(f"  详情: {error_details}")
                    self.failed_count += 1
                    return False
                else:
                    logger.error(f"✗ HTTP 错误 ({e.resp.status}): {url}")
                    logger.error(f"  详情: {error_details}")
                    if attempt < RETRY_ATTEMPTS:
                        delay = RETRY_DELAY * attempt
                        logger.info(f"  等待 {delay} 秒后重试 (尝试 {attempt}/{RETRY_ATTEMPTS})")
                        time.sleep(delay)
                        continue
                    self.failed_count += 1
                    return False

            except Exception as e:
                logger.error(f"✗ 提交失败: {url}")
                logger.error(f"  错误: {type(e).__name__}: {e}")
                if attempt < RETRY_ATTEMPTS:
                    delay = RETRY_DELAY * attempt
                    logger.info(f"  等待 {delay} 秒后重试 (尝试 {attempt}/{RETRY_ATTEMPTS})")
                    time.sleep(delay)
                    continue
                self.failed_count += 1
                return False

        return False

    def submit_batch(self, urls: List[str]) -> Dict[str, int]:
        """
        批量提交 URL

        Args:
            urls: URL 列表

        Returns:
            dict: 统计信息 {submitted, failed, skipped}
        """
        total = len(urls)
        logger.info(f"开始批量提交 {total} 个 URL")

        for i, url in enumerate(urls, 1):
            logger.info(f"进度: [{i}/{total}]")

            # 检查配额限制
            if not self.dry_run and self.submitted_count >= DAILY_QUOTA:
                logger.warning(f"⚠ 达到每日配额限制 ({DAILY_QUOTA} 个请求)")
                self.skipped_count += total - i + 1
                break

            self.submit_url(url)

            # 避免触发速率限制
            if not self.dry_run and i < total:
                time.sleep(0.5)

        return {
            "submitted": self.submitted_count,
            "failed": self.failed_count,
            "skipped": self.skipped_count
        }

    def get_metadata(self, url: str) -> Optional[Dict]:
        """
        查询 URL 的索引状态

        Args:
            url: 要查询的 URL

        Returns:
            dict: 元数据信息,失败返回 None
        """
        if self.dry_run:
            logger.info(f"[DRY-RUN] 将查询: {url}")
            return None

        try:
            response = self.service.urlNotifications().getMetadata(url=url).execute()
            return response
        except HttpError as e:
            if e.resp.status == 404:
                logger.info(f"URL 未被索引: {url}")
            else:
                logger.error(f"查询失败 ({e.resp.status}): {url}")
            return None
        except Exception as e:
            logger.error(f"查询失败: {type(e).__name__}: {e}")
            return None


def load_url_list(max_priority: int = 5, limit: Optional[int] = None) -> List[Tuple[int, str, str]]:
    """
    加载 URL 列表

    Args:
        max_priority: 最大优先级(1-5,1 为最高)
        limit: 限制数量

    Returns:
        list: [(优先级, URL, 描述)]
    """
    logger.info("生成 URL 列表...")
    urls = generate_url_list()

    # 按优先级过滤
    urls = [u for u in urls if u[0] <= max_priority]
    logger.info(f"优先级 <= {max_priority} 的 URL: {len(urls)} 个")

    # 按优先级排序(优先级低的数字先提交)
    urls.sort(key=lambda x: (x[0], x[1]))

    # 限制数量
    if limit and limit > 0:
        urls = urls[:limit]
        logger.info(f"限制提交数量为: {limit} 个")

    return urls


def print_summary(stats: Dict[str, int], start_time: float):
    """打印提交摘要"""
    elapsed = time.time() - start_time
    total = stats["submitted"] + stats["failed"] + stats["skipped"]

    print("\n" + "=" * 80)
    print("提交摘要")
    print("=" * 80)
    print(f"总计:   {total} 个 URL")
    print(f"成功:   {stats['submitted']} 个")
    print(f"失败:   {stats['failed']} 个")
    print(f"跳过:   {stats['skipped']} 个")
    print(f"用时:   {elapsed:.2f} 秒")
    print("=" * 80)

    if stats["failed"] > 0:
        print("\n⚠ 部分 URL 提交失败,请查看上方日志了解详情")

    if stats["skipped"] > 0:
        print(f"\n💡 有 {stats['skipped']} 个 URL 因配额限制未提交")
        print("   建议明天继续提交剩余 URL")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Google Indexing API 自动提交工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用环境变量中的凭证
  python3 %(prog)s

  # 指定凭证文件
  python3 %(prog)s --credentials /path/to/service-account.json

  # Dry-run 模式
  python3 %(prog)s --dry-run

  # 只提交最高优先级的 URL
  python3 %(prog)s --max-priority 1

  # 限制提交数量
  python3 %(prog)s --limit 50

  # 自动确认提交(用于 CI/CD 或定时任务)
  python3 %(prog)s --yes

  # 组合使用
  python3 %(prog)s --max-priority 2 --limit 100 --yes

环境变量:
  GOOGLE_SERVICE_ACCOUNT_JSON  Service Account JSON 内容
        """
    )

    parser.add_argument(
        "--credentials",
        "-c",
        type=str,
        help="Service Account JSON 文件路径(可选,默认从环境变量读取)"
    )

    parser.add_argument(
        "--max-priority",
        "-p",
        type=int,
        default=5,
        choices=[1, 2, 3, 4, 5],
        help="最大优先级 (1=最高, 5=最低, 默认: 5)"
    )

    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="限制提交数量(可选)"
    )

    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Dry-run 模式,不实际提交"
    )

    parser.add_argument(
        "--query",
        "-q",
        type=str,
        help="查询指定 URL 的索引状态(不执行提交)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="显示详细日志"
    )

    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="自动确认提交,跳过交互式确认(用于自动化场景)"
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    print("=" * 80)
    print("Google Indexing API 自动提交工具")
    print(f"网站地址: {BASE_URL}")
    if args.dry_run:
        print("模式: DRY-RUN (不会实际提交)")
    print("=" * 80)
    print()

    try:
        # 初始化客户端
        client = GoogleIndexingClient(
            credentials_path=args.credentials,
            dry_run=args.dry_run
        )

        # 查询模式
        if args.query:
            logger.info(f"查询 URL 索引状态: {args.query}")
            metadata = client.get_metadata(args.query)
            if metadata:
                print("\n索引元数据:")
                print(json.dumps(metadata, indent=2, ensure_ascii=False))
            else:
                print("\n无索引数据")
            return

        # 加载 URL 列表
        urls = load_url_list(
            max_priority=args.max_priority,
            limit=args.limit
        )

        if not urls:
            logger.warning("没有找到符合条件的 URL")
            return

        # 显示待提交的 URL
        print(f"\n待提交的 URL ({len(urls)} 个):")
        print("-" * 80)
        for priority, url, desc in urls[:10]:  # 只显示前 10 个
            print(f"[优先级 {priority}] {url}")
        if len(urls) > 10:
            print(f"... 还有 {len(urls) - 10} 个 URL")
        print("-" * 80)
        print()

        # 确认提交(除非使用了 --yes 参数)
        if not args.dry_run and not args.yes:
            response = input("确认提交? (y/N): ")
            if response.lower() != 'y':
                logger.info("已取消")
                return

        # 批量提交
        start_time = time.time()
        url_list = [url for _, url, _ in urls]
        stats = client.submit_batch(url_list)

        # 打印摘要
        print_summary(stats, start_time)

        # 保存提交记录
        if not args.dry_run and stats["submitted"] > 0:
            log_file = Path(__file__).parent.parent / "google_indexing_log.json"
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "stats": stats,
                "submitted_urls": url_list[:stats["submitted"]]
            }

            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)

            logger.info(f"提交记录已保存到: {log_file}")

    except KeyboardInterrupt:
        logger.warning("\n用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"执行失败: {type(e).__name__}: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
