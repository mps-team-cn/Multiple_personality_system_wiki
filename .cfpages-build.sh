#!/bin/bash
# Cloudflare Pages 构建脚本

set -e

echo "开始构建 Multiple Personality System Wiki (MkDocs Material)..."

# 安装依赖
echo "安装依赖..."
pip3 install uv
uv sync

# 构建站点
echo "构建站点..."
uv run mkdocs build

echo "构建完成!"
