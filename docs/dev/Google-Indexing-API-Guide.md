# Google Indexing API 使用指南

## 概述

Google Indexing API 允许网站主动通知 Google 有关页面的更新,从而加快索引速度。本项目提供了自动化提交工具,可以批量提交高权重 URL 到 Google Search Console。

## 功能特性

- **智能 URL 生成**: 基于 `generate_seo_urls.py` 生成的优先级 URL 列表
- **批量提交**: 支持最多 100 个 URL/批次的批量提交
- **配额管理**: 自动管理每日 200 请求限制(可配置)
- **错误处理**: 完善的重试机制和错误恢复
- **Dry-run 模式**: 测试模式,不实际提交
- **详细日志**: 完整的执行日志和提交记录
- **灵活配置**: 支持优先级筛选和数量限制

## 前置要求

### 1. 安装依赖

```bash

# 激活虚拟环境

python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# 或 venv\Scripts\activate.bat  # Windows

# 安装依赖

pip install -r requirements.txt
```

### 2. 创建 Google Service Account

#### 步骤 1: 创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目

#### 步骤 2: 启用 Indexing API

1. 在项目中导航到 **APIs & Services** > **Library**
2. 搜索 "Indexing API"
3. 点击 **Enable**

#### 步骤 3: 创建 Service Account

1. 导航到 **IAM & Admin** > **Service Accounts**
2. 点击 **Create Service Account**
3. 填写以下信息:
    - **Service account name**: `wiki-indexing-bot`
    - **Description**: `Multiple Personality System Wiki Indexing Bot`
4. 点击 **Create and Continue**
5. 跳过权限设置(点击 **Continue**)
6. 点击 **Done**

#### 步骤 4: 创建密钥

1. 找到刚创建的 Service Account
2. 点击右侧的 **Actions** > **Manage keys**
3. 点击 **Add Key** > **Create new key**
4. 选择 **JSON** 格式
5. 点击 **Create**
6. JSON 文件会自动下载,妥善保管

#### 步骤 5: 添加到 Search Console

1. 打开下载的 JSON 文件
2. 复制 `client_email` 字段的值(格式: `xxx@xxx.iam.gserviceaccount.com`)
3. 访问 [Google Search Console](https://search.google.com/search-console)
4. 选择您的网站属性
5. 导航到 **Settings** > **Users and permissions**
6. 点击 **Add user**
7. 粘贴 Service Account 邮箱地址
8. 权限选择 **Owner**
9. 点击 **Add**

### 3. 配置凭证

#### 方式 1: 环境变量(推荐用于 CI/CD)

```bash

# Linux/macOS

export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"...",...}'

# Windows PowerShell

$env:GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"...",...}'

# Windows CMD

set GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"...",...}
```

#### 方式 2: 本地文件(推荐用于本地测试)

```bash

# 将下载的 JSON 文件保存到安全位置

mv ~/Downloads/service-account-key.json ~/.config/gcloud/wiki-indexing-credentials.json

# 使用 --credentials 参数指定路径

python3 tools/submit_to_google_indexing.py --credentials ~/.config/gcloud/wiki-indexing-credentials.json
```

#### 方式 3: GitHub Secrets(推荐用于 GitHub Actions)

1. 打开 JSON 文件,复制全部内容
2. 访问 GitHub 仓库 **Settings** > **Secrets and variables** > **Actions**
3. 点击 **New repository secret**
4. **Name**: `GOOGLE_SERVICE_ACCOUNT_JSON`
5. **Value**: 粘贴 JSON 内容
6. 点击 **Add secret**

## 使用方法

### 基础用法

```bash

# 使用环境变量中的凭证

python3 tools/submit_to_google_indexing.py

# 指定凭证文件

python3 tools/submit_to_google_indexing.py --credentials /path/to/service-account.json
```

### 常用选项

```bash

# Dry-run 模式(测试,不实际提交)

python3 tools/submit_to_google_indexing.py --dry-run

# 只提交最高优先级 URL(优先级 1)

python3 tools/submit_to_google_indexing.py --max-priority 1

# 只提交高优先级 URL(优先级 1-2)

python3 tools/submit_to_google_indexing.py --max-priority 2

# 限制提交数量(避免超过配额)

python3 tools/submit_to_google_indexing.py --limit 50

# 组合使用

python3 tools/submit_to_google_indexing.py --max-priority 2 --limit 100 --dry-run

# 查询指定 URL 的索引状态

python3 tools/submit_to_google_indexing.py --query https://wiki.mpsteam.cn/entries/DID

# 显示详细日志

python3 tools/submit_to_google_indexing.py --verbose
```

### 完整参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--credentials` | `-c` | Service Account JSON 文件路径 | 从环境变量读取 |
| `--max-priority` | `-p` | 最大优先级 (1-5, 1=最高) | 5 |
| `--limit` | `-l` | 限制提交数量 | 无限制 |
| `--dry-run` | `-d` | Dry-run 模式,不实际提交 | False |
| `--query` | `-q` | 查询 URL 索引状态(不执行提交) | - |
| `--verbose` | `-v` | 显示详细日志 | False |

## 执行流程

### 1. 生成 URL 列表

工具会自动调用 `generate_seo_urls.py` 生成优先级 URL 列表:

- **优先级 1**: 首页、核心导览、关键工具页面
- **优先级 2**: 主题分区索引、高优先级词条

### 2. 过滤和排序

- 根据 `--max-priority` 过滤 URL
- 按优先级从低到高排序(优先级 1 最先提交)
- 应用 `--limit` 限制数量

### 3. 批量提交

- 每个 URL 发送一个 API 请求
- 自动处理错误和重试
- 避免触发速率限制(每次请求间隔 0.5 秒)
- 达到配额限制后自动停止

### 4. 生成报告

- 打印提交摘要(成功/失败/跳过)
- 保存提交记录到 `google_indexing_log.json`

## 配额管理

### 默认配额

- **每日限额**: 200 个请求
- **批量大小**: 100 个 URL/批次
- **速率限制**: 约 2 个请求/秒(建议)

### 配额策略建议

#### 策略 1: 分批提交(推荐)

```bash

# 第 1 天: 提交优先级 1

python3 tools/submit_to_google_indexing.py --max-priority 1

# 第 2 天: 提交优先级 2

python3 tools/submit_to_google_indexing.py --max-priority 2

# 第 3 天: 提交其他优先级

python3 tools/submit_to_google_indexing.py --max-priority 5 --limit 200
```

#### 策略 2: 限制数量

```bash

# 每天提交 50 个 URL,分 4 天完成

python3 tools/submit_to_google_indexing.py --limit 50
```

#### 策略 3: 定期更新

```bash

# 每周提交新增和更新的高优先级内容

python3 tools/submit_to_google_indexing.py --max-priority 2 --limit 100
```

### 申请配额提升

如果需要更高配额:

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 导航到 **IAM & Admin** > **Quotas**
3. 搜索 "Indexing API"
4. 选择要提升的配额
5. 点击 **Edit Quotas**
6. 填写申请表单

## 错误处理

### 常见错误及解决方案

#### 1. 权限错误 (403 Forbidden)

**错误信息**:

```text
✗ 权限不足 (403): https://wiki.mpsteam.cn/...
提示: 请确认 Service Account 已被添加为网站所有者
```

**解决方案**:

- 确认 Service Account 邮箱已添加到 Google Search Console
- 确认权限为 **Owner**
- 等待几分钟后重试(权限生效需要时间)

#### 2. 配额超限 (429 Too Many Requests)

**错误信息**:

```text
⚠ 配额超限 (429): https://wiki.mpsteam.cn/...
等待 X 秒后重试
```

**解决方案**:

- 工具会自动重试
- 如果持续失败,说明达到每日配额
- 明天继续提交剩余 URL
- 考虑申请配额提升

#### 3. 请求无效 (400 Bad Request)

**错误信息**:

```text
✗ 请求无效 (400): https://wiki.mpsteam.cn/...
```

**解决方案**:

- 检查 URL 格式是否正确
- 确认 URL 属于已验证的网站
- 查看详细错误信息

#### 4. 凭证错误

**错误信息**:

```text
未提供凭证: 请通过 --credentials 参数指定文件路径,或设置 GOOGLE_SERVICE_ACCOUNT_JSON 环境变量
```

**解决方案**:

- 检查环境变量是否正确设置
- 或使用 `--credentials` 参数指定文件路径
- 确认 JSON 文件格式正确

## CI/CD 集成

### GitHub Actions 示例

创建 `.github/workflows/google-indexing.yml`:

```yaml
name: Google Indexing API 提交

on:
  # 手动触发
  workflow_dispatch:
    inputs:
      max_priority:
        description: '最大优先级 (1-5)'
        required: true
        default: '2'
      limit:
        description: '限制数量'
        required: false

  # 每周执行
  schedule:

    - cron: '0 2 * * 0'  # 每周日 02:00 UTC

jobs:
  submit-to-google:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout 代码

        uses: actions/checkout@v4

      - name: 设置 Python

        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: 安装依赖

        run: |
          pip install -r requirements.txt

      - name: 提交到 Google Indexing API

        env:
          GOOGLE_SERVICE_ACCOUNT_JSON: ${{ secrets.GOOGLE_SERVICE_ACCOUNT_JSON }}
        run: |
          MAX_PRIORITY=${{ github.event.inputs.max_priority || '2' }}
          LIMIT=${{ github.event.inputs.limit || '' }}

          if [ -n "$LIMIT" ]; then
            python3 tools/submit_to_google_indexing.py --max-priority $MAX_PRIORITY --limit $LIMIT
          else
            python3 tools/submit_to_google_indexing.py --max-priority $MAX_PRIORITY
          fi

      - name: 上传提交日志

        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: google-indexing-log
          path: google_indexing_log.json
          retention-days: 30
```

### 手动触发

1. 访问 GitHub 仓库 **Actions** 标签
2. 选择 **Google Indexing API 提交** workflow
3. 点击 **Run workflow**
4. 选择参数(优先级、数量限制)
5. 点击 **Run workflow**

## 最佳实践

### 1. 渐进式提交

```bash

# 阶段 1: 测试配置(Dry-run)

python3 tools/submit_to_google_indexing.py --max-priority 1 --dry-run

# 阶段 2: 提交最高优先级

python3 tools/submit_to_google_indexing.py --max-priority 1

# 阶段 3: 提交高优先级

python3 tools/submit_to_google_indexing.py --max-priority 2

# 阶段 4: 定期更新

# 每周提交新增内容

```

### 2. 监控配额使用

```bash

# 查看提交日志

cat google_indexing_log.json

# 统计已提交 URL 数量

jq '.stats.submitted' google_indexing_log.json
```

### 3. 验证索引状态

```bash

# 查询单个 URL 的索引状态

python3 tools/submit_to_google_indexing.py --query https://wiki.mpsteam.cn/entries/DID

# 使用 Google Search Console 验证

# https://search.google.com/search-console

```

### 4. 定期维护

- **每周**: 提交新增和更新的高优先级内容
- **每月**: 全量提交所有优先级内容
- **按需**: 重大更新后立即提交相关 URL

## 安全注意事项

### 1. 保护 Service Account 凭证

- **禁止提交到 Git**: 将 `*.json` 添加到 `.gitignore`
- **限制文件权限**: `chmod 600 service-account.json`
- **使用环境变量**: 避免硬编码凭证
- **定期轮换**: 每 90 天更换密钥

### 2. 最小权限原则

- Service Account 只需要 **Indexing API** 权限
- Search Console 权限设置为 **Owner**(API 要求)

### 3. 监控异常活动

- 定期检查 Google Cloud Console 的 API 使用情况
- 启用 API 使用警报
- 审计 Service Account 密钥使用

## 故障排除

### 调试技巧

```bash

# 启用详细日志

python3 tools/submit_to_google_indexing.py --verbose

# 测试单个 URL

python3 tools/submit_to_google_indexing.py --limit 1 --dry-run

# 查询索引状态

python3 tools/submit_to_google_indexing.py --query https://wiki.mpsteam.cn/
```

### 日志位置

- **执行日志**: 控制台输出
- **提交记录**: `google_indexing_log.json`
- **CI 日志**: GitHub Actions Artifacts

### 联系支持

如果遇到问题:

1. 查看 [Google Indexing API 文档](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
2. 检查 [Google Cloud Console](https://console.cloud.google.com/) 的 API 状态
3. 访问 [Google Search Console](https://search.google.com/search-console) 验证权限

## 相关文档

- [generate_seo_urls.py 使用说明](../TEMPLATE_ENTRY.md)
- [SEO 优化指南](SEO_OPTIMIZATION.md)
- [工具索引](Tools-Index.md)
- [Google Indexing API 官方文档](https://developers.google.com/search/apis/indexing-api/v3/quickstart)

## 更新日志

- **2025-01-17**: 初始版本发布
    - 支持批量提交 URL
    - Service Account 认证
    - 配额管理和错误处理
    - Dry-run 模式
