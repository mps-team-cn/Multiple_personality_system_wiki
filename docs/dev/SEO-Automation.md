# SEO 自动化指南

本文档介绍 MPS Wiki 的搜索引擎优化(SEO)自动化策略和工具。

## 概览

MPS Wiki 使用多种 SEO 策略来提升搜索引擎可见性:

- **IndexNow 协议**: 主动推送 URL 更新到 Bing、Yandex 等搜索引擎
- **Google Indexing API**: 直接通知 Google 索引新内容
- **自动生成 sitemap.xml**: MkDocs 自动生成完整站点地图
- **结构化数据**: 通过 Frontmatter 提供丰富的元数据

## IndexNow 集成

### 什么是 IndexNow?

[IndexNow](https://www.indexnow.org/) 是一个开放协议,允许网站**主动通知搜索引擎内容已更新**,而不是等待爬虫被动发现。

**支持的搜索引擎**:

- ✅ **Microsoft Bing**
- ✅ **Yandex**
- ✅ **Naver**
- ✅ **Seznam**
- ⏳ **百度**(测试中)
- ❌ Google(尚未支持,但 Microsoft 正在推动标准化)

**优势**:

- ⚡ **加速索引**: 将索引时间从数天缩短到数小时
- 🔄 **实时更新**: 内容修改后立即通知搜索引擎
- 🌍 **多引擎覆盖**: 一次提交,多个搜索引擎自动同步
- 💰 **完全免费**: 无需 API 密钥或付费订阅

### 工作原理

1. **验证所有权**: 在网站根目录放置验证密钥文件
2. **推送 URL**: 通过 API 提交更新的 URL 列表
3. **自动抓取**: 搜索引擎接收通知后优先抓取这些页面

### 密钥文件

密钥文件位于: `21560e3c9db64767914ef22b96cd7660.txt`

**重要**: 该文件必须在站点根目录可访问:

```
https://wiki.mpsteam.cn/21560e3c9db64767914ef22b96cd7660.txt
```

部署时确保 MkDocs 将该文件复制到构建输出(`site/`)目录。

### 自动化工作流

#### GitHub Actions 集成

IndexNow 推送已集成到 CI/CD 流程,配置文件: [`.github/workflows/indexnow-push.yml`](../../.github/workflows/indexnow-push.yml)

**触发条件**:

1. **自动触发**: 在 GitHub Pages 部署成功后自动运行
2. **手动触发**: 在 Actions 页面手动运行,可选择推送模式:
   - `recent`: 仅推送最近修改的 50 个词条(默认)
   - `all`: 推送所有 URL(适用于重大更新或首次集成)

**执行流程**:

```yaml
1. 检出代码(包含完整 Git 历史)
2. 构建站点(生成 sitemap.xml)
3. 运行 submit_to_indexnow.py
4. 自动提交 URL 列表到 IndexNow API
```

#### 手动使用

如果需要在本地手动推送:

```bash
# 1. 先构建站点(生成 sitemap.xml)
mkdocs build

# 2. 推送最近修改的 50 个词条
python3 tools/submit_to_indexnow.py --recent 50

# 3. 推送所有 URL(重大更新时)
python3 tools/submit_to_indexnow.py --all

# 4. 推送指定 URL
python3 tools/submit_to_indexnow.py --urls \
  https://wiki.mpsteam.cn/entries/谵妄.html \
  https://wiki.mpsteam.cn/entries/融合.html

# 5. 测试模式(不实际发送)
python3 tools/submit_to_indexnow.py --recent 50 --dry-run
```

### 工具说明: `submit_to_indexnow.py`

完整工具文档: [`tools/submit_to_indexnow.py`](../../tools/submit_to_indexnow.py)

**核心功能**:

- 📄 **自动解析 sitemap.xml**: 获取所有可索引 URL
- 🔍 **智能筛选**: 基于 Git 历史检测最近修改的词条
- 📦 **批量提交**: 一次最多提交 1000 个 URL
- ✅ **错误处理**: 详细的响应状态码说明和错误提示

**返回码说明**:

| HTTP 状态码 | 含义 | 处理建议 |
|---------|------|---------|
| 200 | ✅ 成功接收 | 无需操作,索引将在数小时内更新 |
| 202 | ⏳ 已接收,正在验证密钥 | 等待几分钟后重试,确保密钥文件可访问 |
| 400 | ❌ 请求格式错误 | 检查 JSON 格式和 URL 编码 |
| 403 | ❌ 密钥验证失败 | 确认密钥文件在根目录且内容正确 |
| 422 | ❌ URL 格式错误 | 检查 URL 是否包含非法字符或协议错误 |
| 429 | ⚠️ 请求过于频繁 | 等待几小时后重试 |

### 验证密钥状态

**首次推送**时,可能会遇到 `403 - SiteVerificationNotCompleted` 错误:

```json
{
  "code": "SiteVerificationNotCompleted",
  "message": "Site Verification is not completed. Please wait for some time..."
}
```

**解决方法**:

1. 确认密钥文件已部署到生产环境
2. 访问 `https://wiki.mpsteam.cn/21560e3c9db64767914ef22b96cd7660.txt` 确认可访问
3. 等待 5-30 分钟让 Bing 完成验证
4. 重新运行推送

**验证工具**:

```bash
# 检查密钥文件是否可访问
curl https://wiki.mpsteam.cn/21560e3c9db64767914ef22b96cd7660.txt

# 预期输出:
# 21560e3c9db64767914ef22b96cd7660
```

## Google Indexing API

### 配置说明

参考现有文档: [`tools/README_GOOGLE_INDEXING.md`](../../tools/README_GOOGLE_INDEXING.md)

**主要步骤**:

1. 在 Google Cloud Console 创建服务账号
2. 启用 Indexing API
3. 在 Google Search Console 添加服务账号为网站所有者
4. 下载 JSON 密钥文件
5. 配置 GitHub Secrets

### 工作流集成

配置文件示例: [`.github/workflows/google-indexing.yml.example`](../../.github/workflows/google-indexing.yml.example)

## SEO 最佳实践

### Frontmatter 优化

每个词条都应包含完整的 SEO 元数据:

```yaml
---
title: 词条标题
description: 简洁的描述(建议 120-160 字符,用于搜索结果摘要)
tags:
  - 诊断与临床
  - DID
keywords: 关键词1, 关键词2, 关键词3
updated: 2025-01-15
---
```

**工具支持**:

- `check_descriptions.py`: 检查 description 覆盖率
- `add_descriptions.py`: 批量添加 SEO 描述

### URL 结构优化

MkDocs 默认使用目录结构生成 URL:

```
docs/entries/谵妄.md → https://wiki.mpsteam.cn/entries/谵妄.html
```

**优化建议**:

- ✅ 使用有意义的文件名(中文词条名)
- ✅ 保持 URL 简短且描述性强
- ❌ 避免深层嵌套(最多 3 层)

### 站点地图管理

MkDocs 自动生成 `sitemap.xml`,无需手动维护。

**查看站点地图**:

```bash
# 本地构建
mkdocs build

# 查看生成的 sitemap
cat site/sitemap.xml
```

**生产环境**:

```
https://wiki.mpsteam.cn/sitemap.xml
```

## 性能监控

### 索引状态检查

**Bing Webmaster Tools**:

1. 访问 [Bing Webmaster Tools](https://www.bing.com/webmasters)
2. 添加 `wiki.mpsteam.cn`
3. 查看 "Site Explorer" → "IndexNow" 部分

**Google Search Console**:

1. 访问 [Google Search Console](https://search.google.com/search-console)
2. 添加 `wiki.mpsteam.cn`
3. 查看 "Coverage" 和 "Indexing API" 状态

### 搜索可见性跟踪

定期检查关键词排名:

- 多意识体系统
- 解离性身份障碍
- DID
- OSDD
- 人格切换

**工具推荐**:

- [Google Analytics](https://analytics.google.com/)
- [Bing Webmaster Tools](https://www.bing.com/webmasters)

## 常见问题

### Q: IndexNow 和 sitemap 有什么区别?

**A**: 两者互补:

- **sitemap.xml**: 被动的 URL 列表,搜索引擎定期抓取
- **IndexNow**: 主动通知,内容更新后立即推送

建议**同时使用**以获得最佳效果。

### Q: IndexNow 会立即索引我的页面吗?

**A**: 不一定。IndexNow 只是通知搜索引擎"这个 URL 更新了",实际索引时间取决于:

- 网站权威性
- 内容质量
- 服务器性能
- 搜索引擎负载

通常在**数小时到 1-2 天**内完成索引。

### Q: 为什么 Google 不支持 IndexNow?

**A**: Google 有自己的 Indexing API。IndexNow 是由 Microsoft 主导的开放标准,Google 尚未官方加入,但业界正在推动标准化。

### Q: 我应该多久推送一次?

**A**:

- ✅ **推荐**: 每次重大内容更新后推送(已通过 CI 自动化)
- ⚠️ **避免**: 频繁推送相同 URL(可能触发限流)
- 💡 **最佳实践**: 每次部署后自动推送最近修改的词条

### Q: IndexNow 会消耗搜索引擎配额吗?

**A**: 不会。IndexNow 是完全免费的协议,没有配额限制。但建议避免滥用(如每分钟多次推送)。

## 相关文档

- [工具索引](Tools-Index.md)
- [Google Indexing API 配置](../../tools/README_GOOGLE_INDEXING.md)
- [性能优化指南](Performance-Optimization.md)
- [Cloudflare Pages 部署](CLOUDFLARE_PAGES.md)

## 参考资源

- [IndexNow 官方文档](https://www.indexnow.org/)
- [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a)
- [Google Indexing API](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
- [MkDocs SEO Plugin](https://github.com/squidfunk/mkdocs-material/blob/master/docs/plugins/meta.md)
