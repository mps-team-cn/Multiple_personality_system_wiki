#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow 自动推送工具

用途: 在 Wiki 内容更新后，主动向 Bing/Yandex 等搜索引擎推送 URL
协议: https://www.indexnow.org/
支持的搜索引擎: Bing, Yandex, Naver, Seznam, 百度(测试中)
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import requests

# 配置常量
INDEXNOW_API = "https://api.indexnow.org/indexnow"
SITE_HOST = "wiki.mpsteam.cn"
# FIXME: 密钥不应硬编码在代码中。请将已泄露的 key 轮换后改为从环境变量读取。
INDEXNOW_KEY = os.environ.get("INDEXNOW_API_KEY", "21560e3c9db64767914ef22b96cd7660")
KEY_LOCATION = f"https://{SITE_HOST}/{INDEXNOW_KEY}.txt"

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SITEMAP_PATH = PROJECT_ROOT / "site" / "sitemap.xml"

# 密钥文件路径 (MkDocs 会将 docs/ 下的文件复制到 site/)
KEY_FILE_PATH = PROJECT_ROOT / "docs" / f"{INDEXNOW_KEY}.txt"


def parse_sitemap(sitemap_path: Path) -> List[str]:
    """
    解析 sitemap.xml 获取所有 URL

    Args:
        sitemap_path: sitemap.xml 文件路径

    Returns:
        URL 列表
    """
    urls = []

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        # 处理 XML 命名空间
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        for url_elem in root.findall('sm:url', ns):
            loc_elem = url_elem.find('sm:loc', ns)
            if loc_elem is not None and loc_elem.text:
                urls.append(loc_elem.text)

        print(f"✓ 从 sitemap.xml 解析到 {len(urls)} 个 URL")

    except FileNotFoundError:
        print(f"✗ 未找到 sitemap.xml: {sitemap_path}", file=sys.stderr)
        print("  请先运行 mkdocs build 生成站点", file=sys.stderr)
    except ET.ParseError as e:
        print(f"✗ sitemap.xml 解析失败: {e}", file=sys.stderr)

    return urls


def get_changed_entries(max_count: Optional[int] = None) -> List[str]:
    """
    获取最近修改的词条 URL (基于 Git 历史)

    Args:
        max_count: 最多返回多少个文件（注意：不是提交数）

    Returns:
        URL 列表
    """
    import subprocess

    try:
        # 获取最近修改的 docs/entries/ 下的文件
        # 使用足够大的提交数来确保能找到足够的文件
        cmd = [
            'git', 'log',
            '--pretty=format:',
            '--name-only',
            '--diff-filter=AM',  # 只关注新增和修改
            '-n', '1000',  # 查看最近 1000 次提交
            '--', 'docs/entries/'
        ]

        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )

        # 提取唯一的文件路径（保持顺序）
        seen = set()
        files = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line and line not in seen:
                seen.add(line)
                files.append(line)

        # 如果指定了 max_count，限制文件数量
        if max_count is not None:
            files = files[:max_count]

        # 转换为 URL
        urls = []
        for file in files:
            if file.endswith('.md'):
                # docs/entries/融合.md -> https://wiki.mpsteam.cn/entries/系统运作/融合.html
                # 需要从 sitemap 中匹配实际路径
                filename = Path(file).stem
                urls.append(filename)

        print(f"✓ 检测到 {len(urls)} 个最近修改的词条")
        return urls

    except subprocess.CalledProcessError as e:
        print(f"✗ Git 命令执行失败: {e}", file=sys.stderr)
        return []


def filter_urls_by_pattern(all_urls: List[str], patterns: List[str]) -> List[str]:
    """
    根据文件名模式筛选 URL

    Args:
        all_urls: 所有 URL 列表
        patterns: 文件名模式列表 (不含 .html)

    Returns:
        匹配的 URL 列表
    """
    matched = []

    for url in all_urls:
        for pattern in patterns:
            if pattern in url:
                matched.append(url)
                break

    return matched


def submit_to_indexnow(urls: List[str], dry_run: bool = False) -> bool:
    """
    向 IndexNow API 提交 URL 列表

    Args:
        urls: 要提交的 URL 列表
        dry_run: 是否为测试模式 (不实际发送请求)

    Returns:
        是否提交成功
    """
    if not urls:
        print("⚠ 没有 URL 需要提交")
        return False

    # IndexNow 建议一次最多提交 10,000 个 URL
    # 但实际使用中建议分批,每次不超过 1000 个
    MAX_BATCH_SIZE = 1000

    if len(urls) > MAX_BATCH_SIZE:
        print(f"⚠ URL 数量 ({len(urls)}) 超过建议上限,将只提交前 {MAX_BATCH_SIZE} 个")
        urls = urls[:MAX_BATCH_SIZE]

    payload = {
        "host": SITE_HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }

    print(f"\n📤 准备提交 {len(urls)} 个 URL 到 IndexNow")
    print(f"   主机: {SITE_HOST}")
    print(f"   密钥位置: {KEY_LOCATION}")

    if dry_run:
        print("\n🔍 [测试模式] 不会实际发送请求")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return True

    try:
        response = requests.post(
            INDEXNOW_API,
            json=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=30
        )

        # IndexNow API 响应说明:
        # 200: 成功接收
        # 202: 已接收但可能需要验证密钥
        # 400: 请求格式错误
        # 403: 密钥验证失败
        # 422: URL 格式错误或包含不允许的 URL
        # 429: 请求过于频繁

        if response.status_code in [200, 202]:
            print(f"✓ 提交成功! (HTTP {response.status_code})")
            if response.status_code == 202:
                print("  注意: 搜索引擎可能正在验证密钥,请确保密钥文件可访问")
            return True
        else:
            print(f"✗ 提交失败! HTTP {response.status_code}", file=sys.stderr)
            print(f"  响应: {response.text}", file=sys.stderr)
            return False

    except requests.Timeout:
        print("✗ 请求超时", file=sys.stderr)
        return False
    except requests.RequestException as e:
        print(f"✗ 网络请求失败: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='向 IndexNow 提交 URL 以加速搜索引擎索引',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 提交整个 sitemap
  python submit_to_indexnow.py --all

  # 只提交最近修改的 50 个词条
  python submit_to_indexnow.py --recent 50

  # 提交指定的 URL
  python submit_to_indexnow.py --urls https://wiki.mpsteam.cn/entries/融合.html

  # 测试模式 (不实际发送)
  python submit_to_indexnow.py --all --dry-run

注意事项:
  - IndexNow 协议由 Bing、Yandex 等支持,Google 尚未加入
  - 提交不保证立即索引,但通常可将索引时间从数天缩短到数小时
  - 建议在每次重大内容更新后运行,无需频繁提交相同 URL
  - 密钥文件必须在网站根目录可访问: https://wiki.mpsteam.cn/{key}.txt
        """
    )

    # 互斥的 URL 来源选项
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '--all',
        action='store_true',
        help='提交 sitemap.xml 中的所有 URL'
    )
    source_group.add_argument(
        '--recent',
        type=int,
        metavar='N',
        help='提交最近修改的 N 个词条'
    )
    source_group.add_argument(
        '--urls',
        nargs='+',
        metavar='URL',
        help='提交指定的 URL 列表'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='测试模式,不实际发送请求'
    )

    args = parser.parse_args()

    # 收集要提交的 URL
    urls_to_submit = []

    if args.all:
        # 提交整个 sitemap
        if not SITEMAP_PATH.exists():
            print("✗ sitemap.xml 不存在,请先运行 mkdocs build", file=sys.stderr)
            return 1
        urls_to_submit = parse_sitemap(SITEMAP_PATH)

    elif args.recent:
        # 提交最近修改的词条
        if not SITEMAP_PATH.exists():
            print("✗ sitemap.xml 不存在,请先运行 mkdocs build", file=sys.stderr)
            return 1

        all_urls = parse_sitemap(SITEMAP_PATH)
        changed_patterns = get_changed_entries(args.recent)
        urls_to_submit = filter_urls_by_pattern(all_urls, changed_patterns)

        if not urls_to_submit:
            print("⚠ 未找到匹配的 URL,将回退到提交所有 URL")
            urls_to_submit = all_urls

    elif args.urls:
        # 使用指定的 URL
        urls_to_submit = args.urls

    # 执行提交
    success = submit_to_indexnow(urls_to_submit, dry_run=args.dry_run)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
