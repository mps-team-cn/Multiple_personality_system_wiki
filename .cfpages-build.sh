#!/bin/bash
# Cloudflare Pages 构建脚本

set -e

echo "开始构建 Multiple Personality System Wiki (MkDocs Material)..."

# 安装 Python 依赖
echo "安装依赖..."
pip install -r requirements.txt

# 构建站点
echo "构建站点..."
mkdocs build

echo "构建完成!"
