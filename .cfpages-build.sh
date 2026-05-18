#!/bin/bash
# Cloudflare Pages 构建脚本

set -e

echo "开始构建 Multiple Personality System Wiki (MkDocs Material)..."

# 安装依赖
echo "安装依赖..."
export PATH="$(python3 -m site --user-base)/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
    python3 -m pip install --user uv
    hash -r
fi

uv sync

# 构建站点
echo "构建站点..."
export DISABLE_MKDOCS_2_WARNING=true
uv run mkdocs build

echo "构建完成!"
