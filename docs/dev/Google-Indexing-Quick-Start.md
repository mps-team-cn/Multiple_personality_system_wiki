# Google Indexing API 快速开始

5 分钟快速配置 Google Indexing API 自动提交工具。

## 第 1 步: 安装依赖

```bash
# 激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate.bat  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 第 2 步: 创建 Service Account

### 2.1 创建项目和启用 API

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 导航到 **APIs & Services** > **Library**
4. 搜索 "Indexing API" 并点击 **Enable**

### 2.2 创建 Service Account

1. 导航到 **IAM & Admin** > **Service Accounts**
2. 点击 **Create Service Account**
3. 名称: `wiki-indexing-bot`
4. 点击 **Create and Continue** > **Continue** > **Done**

### 2.3 创建密钥

1. 找到刚创建的 Service Account
2. 点击 **Actions** > **Manage keys**
3. 点击 **Add Key** > **Create new key**
4. 选择 **JSON** 格式
5. 点击 **Create**(文件会自动下载)

### 2.4 添加到 Search Console

1. 打开下载的 JSON 文件,复制 `client_email` 的值
2. 访问 [Google Search Console](https://search.google.com/search-console)
3. 选择网站属性
4. 导航到 **Settings** > **Users and permissions**
5. 点击 **Add user**
6. 粘贴 Service Account 邮箱
7. 权限选择 **Owner**
8. 点击 **Add**

## 第 3 步: 配置凭证

### 本地测试

```bash
# 方式 1: 环境变量
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"...",...}'

# 方式 2: 文件路径(推荐)
mv ~/Downloads/service-account-key.json ~/.config/gcloud/wiki-indexing-credentials.json
```

### GitHub Actions

1. 打开 JSON 文件,复制全部内容
2. 访问仓库 **Settings** > **Secrets and variables** > **Actions**
3. 点击 **New repository secret**
4. 名称: `GOOGLE_SERVICE_ACCOUNT_JSON`
5. 值: 粘贴 JSON 内容
6. 点击 **Add secret**

## 第 4 步: 测试运行

```bash
# Dry-run 测试(不实际提交)
python3 tools/submit_to_google_indexing.py --max-priority 1 --dry-run

# 如果使用文件路径
python3 tools/submit_to_google_indexing.py \
  --credentials ~/.config/gcloud/wiki-indexing-credentials.json \
  --max-priority 1 --dry-run
```

预期输出:

```
================================================================================
Google Indexing API 自动提交工具
网站地址: https://wiki.mpsteam.cn
模式: DRY-RUN (不会实际提交)
================================================================================

2025-01-17 10:00:00 [INFO] 生成 URL 列表...
2025-01-17 10:00:00 [INFO] 优先级 <= 1 的 URL: 15 个
2025-01-17 10:00:00 [INFO] 开始批量提交 15 个 URL

待提交的 URL (15 个):
--------------------------------------------------------------------------------
[优先级 1] https://wiki.mpsteam.cn/
[优先级 1] https://wiki.mpsteam.cn/QuickStart
[优先级 1] https://wiki.mpsteam.cn/entries/Core-Concepts-Guide
...
```

## 第 5 步: 正式提交

```bash
# 提交最高优先级 URL
python3 tools/submit_to_google_indexing.py --max-priority 1

# 提交高优先级 URL
python3 tools/submit_to_google_indexing.py --max-priority 2
```

## 常见问题

### Q1: 如何检查提交状态?

```bash
# 查看提交日志
cat google_indexing_log.json

# 或使用 jq 格式化
jq '.' google_indexing_log.json
```

### Q2: 如何查询 URL 索引状态?

```bash
python3 tools/submit_to_google_indexing.py \
  --query https://wiki.mpsteam.cn/entries/DID
```

### Q3: 权限错误(403)怎么办?

1. 确认 Service Account 邮箱已添加到 Search Console
2. 权限必须是 **Owner**(不是 Full)
3. 等待 5-10 分钟让权限生效

### Q4: 配额超限(429)怎么办?

默认配额是每天 200 个请求。建议:

```bash
# 分批提交
python3 tools/submit_to_google_indexing.py --limit 100
```

或申请配额提升(需要在 Google Cloud Console)。

### Q5: 如何在 CI/CD 中使用?

1. 复制 `.github/workflows/google-indexing.yml.example` 为 `google-indexing.yml`
2. 在 GitHub Secrets 中设置 `GOOGLE_SERVICE_ACCOUNT_JSON`
3. 手动触发 workflow 或等待定期执行

## 下一步

- 📖 阅读[完整文档](Google-Indexing-API-Guide.md)了解高级功能
- 🔧 查看[工具索引](Tools-Index.md)了解其他 SEO 工具
- 📊 使用[Google Search Console](https://search.google.com/search-console)监控索引状态

## 提交策略建议

### 分阶段提交(推荐)

```bash
# 第 1 天: 核心页面(优先级 1)
python3 tools/submit_to_google_indexing.py --max-priority 1

# 第 2 天: 高优先级词条(优先级 2)
python3 tools/submit_to_google_indexing.py --max-priority 2

# 后续: 定期更新
# 每周提交新增和更新的内容
```

### 限制数量策略

```bash
# 每天 50 个,避免超配额
python3 tools/submit_to_google_indexing.py --limit 50
```

### 定期自动化

使用 GitHub Actions 每周自动提交:

```yaml
schedule:
  - cron: '0 2 * * 0'  # 每周日 02:00 UTC
```

## 安全提示

- 🔒 **不要提交 JSON 文件到 Git**
- 🔑 使用环境变量或 GitHub Secrets
- 📝 定期轮换密钥(建议 90 天)
- 👀 监控 API 使用情况

---

**完整文档**: [Google Indexing API 使用指南](Google-Indexing-API-Guide.md)
