#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 文档修复工具 - 独立脚本入口

用法:
  python tools/fix_markdown.py docs/entries/Tulpa.md          # 处理单个文件
  python tools/fix_markdown.py docs/entries/                   # 处理整个目录
  python tools/fix_markdown.py docs/entries/ --dry-run         # 预览模式
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.processors.markdown import main

if __name__ == "__main__":
    sys.exit(main())
