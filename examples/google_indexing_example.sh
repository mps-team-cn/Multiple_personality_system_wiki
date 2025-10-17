#!/bin/bash
# Google Indexing API 提交示例脚本
# 演示如何在不同场景下使用 submit_to_google_indexing.py

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Google Indexing API 提交示例"
echo "=========================================="
echo ""

# 检查凭证
if [ -z "$GOOGLE_SERVICE_ACCOUNT_JSON" ]; then
    echo -e "${YELLOW}警告: 未设置 GOOGLE_SERVICE_ACCOUNT_JSON 环境变量${NC}"
    echo "请先设置凭证:"
    echo "  export GOOGLE_SERVICE_ACCOUNT_JSON='{\"type\":\"service_account\",...}'"
    echo ""
    echo "或使用 --credentials 参数指定文件路径"
    echo ""
fi

# 场景 1: Dry-run 测试
echo -e "${GREEN}场景 1: Dry-run 测试${NC}"
echo "测试配置是否正确,不实际提交 URL"
echo "命令: python3 tools/submit_to_google_indexing.py --max-priority 1 --dry-run"
echo ""
read -p "按 Enter 继续..."
python3 tools/submit_to_google_indexing.py --max-priority 1 --dry-run
echo ""

# 场景 2: 提交最高优先级 URL
echo -e "${GREEN}场景 2: 提交最高优先级 URL${NC}"
echo "提交优先级 1 的核心页面和工具"
echo "命令: python3 tools/submit_to_google_indexing.py --max-priority 1"
echo ""
read -p "确认提交? (y/N): " confirm
if [ "$confirm" = "y" ]; then
    python3 tools/submit_to_google_indexing.py --max-priority 1
else
    echo "已跳过"
fi
echo ""

# 场景 3: 限制提交数量
echo -e "${GREEN}场景 3: 限制提交数量${NC}"
echo "每天提交 50 个 URL,避免超过配额"
echo "命令: python3 tools/submit_to_google_indexing.py --max-priority 2 --limit 50"
echo ""
read -p "确认提交? (y/N): " confirm
if [ "$confirm" = "y" ]; then
    python3 tools/submit_to_google_indexing.py --max-priority 2 --limit 50
else
    echo "已跳过"
fi
echo ""

# 场景 4: 查询索引状态
echo -e "${GREEN}场景 4: 查询 URL 索引状态${NC}"
echo "查询指定 URL 的索引元数据"
echo "命令: python3 tools/submit_to_google_indexing.py --query https://wiki.mpsteam.cn/entries/DID"
echo ""
read -p "按 Enter 继续..."
python3 tools/submit_to_google_indexing.py --query https://wiki.mpsteam.cn/entries/DID
echo ""

# 场景 5: 显示详细日志
echo -e "${GREEN}场景 5: 显示详细日志${NC}"
echo "启用 verbose 模式查看详细信息"
echo "命令: python3 tools/submit_to_google_indexing.py --max-priority 1 --limit 5 --verbose --dry-run"
echo ""
read -p "按 Enter 继续..."
python3 tools/submit_to_google_indexing.py --max-priority 1 --limit 5 --verbose --dry-run
echo ""

echo "=========================================="
echo "示例演示完成"
echo "=========================================="
echo ""
echo "更多信息请参考:"
echo "  docs/dev/Google-Indexing-API-Guide.md"
echo "  tools/README_GOOGLE_INDEXING.md"
