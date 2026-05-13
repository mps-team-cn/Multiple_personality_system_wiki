# Google Indexing API 提交工具

快速使用 Google Indexing API 批量提交 URL 到 Google Search Console。

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置凭证

将 Service Account JSON 设置为环境变量:

```bash
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
```

或使用文件:

```bash
python3 tools/submit_to_google_indexing.py --credentials /path/to/service-account.json
```

### 3. 运行工具

```bash

# Dry-run 模式(测试)

python3 tools/submit_to_google_indexing.py --dry-run

# 提交最高优先级 URL

python3 tools/submit_to_google_indexing.py --max-priority 1

# 提交前 50 个 URL

python3 tools/submit_to_google_indexing.py --limit 50
```

## 常用命令

```bash

# 只提交最高优先级(优先级 1)

python3 tools/submit_to_google_indexing.py --max-priority 1

# 提交优先级 1-2

python3 tools/submit_to_google_indexing.py --max-priority 2

# 限制提交数量

python3 tools/submit_to_google_indexing.py --limit 100

# 查询 URL 索引状态

python3 tools/submit_to_google_indexing.py --query https://wiki.mpsteam.cn/entries/DID

# 显示详细日志

python3 tools/submit_to_google_indexing.py --verbose
```

## 完整文档

详细配置、错误处理和最佳实践请参考：

📖 [**Google Indexing API 使用指南**](../docs/dev/Google-Indexing-API-Guide.md)

## 配额限制

- 默认每日配额: **200 个请求**
- 建议分批提交,避免超过配额
- 优先提交高权重 URL

## 安全提示

- 🔒 **不要提交 Service Account JSON 文件到 Git**
- 🔑 使用环境变量或 GitHub Secrets 存储凭证
- 📝 定期轮换 Service Account 密钥

## 相关工具

- `generate_seo_urls.py` - 生成高权重 URL 列表
- `check_descriptions.py` - 检查 SEO 描述覆盖率
- `add_descriptions.py` - 批量添加 SEO 描述
