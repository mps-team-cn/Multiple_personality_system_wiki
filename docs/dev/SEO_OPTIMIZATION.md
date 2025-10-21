# SEO 优化实施文档

本文档记录了对 Multiple Personality System Wiki 实施的 SEO 优化措施。

## 实施日期

2025-10-13

## 优化内容概述

### 1. robots.txt

**文件位置**: `docs/robots.txt`

**内容**:

- 允许所有搜索引擎爬虫访问
- 排除 admin/、dev/、tools/ 目录
- 提供 sitemap.xml 位置
- 针对百度和必应设置爬取速率限制

**验证方式**: 访问 [https://wiki.mpsteam.cn/robots.txt](https://wiki.mpsteam.cn/robots.txt)

### 2. Open Graph 和 Twitter Card Meta 标签

**文件位置**: `overrides/main.html`

**实现功能**:

- Open Graph 标签用于社交媒体分享（Facebook、LinkedIn 等）
- Twitter Card 标签用于 Twitter 分享
- 动态读取页面的 title 和 description
- 自动从 Frontmatter 提取 description 字段
- 支持自定义分享图片（og-banner.png 和 twitter-banner.png）

**字段说明**:

- `og:site_name`: 网站名称
- `og:type`: 内容类型（website）
- `og:title`: 页面标题
- `og:description`: 页面描述
- `og:image`: 分享图片
- `og:locale`: 语言地区（zh_CN）

**验证方式**:

- Facebook: [https://developers.facebook.com/tools/debug/](https://developers.facebook.com/tools/debug/)
- Twitter: [https://cards-dev.twitter.com/validator](https://cards-dev.twitter.com/validator)
- LinkedIn: [https://www.linkedin.com/post-inspector/](https://www.linkedin.com/post-inspector/)

### 3. JSON-LD 结构化数据

**文件位置**: `docs/assets/extra.js`

**实现功能**:

- 自动为所有页面添加 WebSite 类型的结构化数据
- 词条页面额外添加 Article 和 MedicalWebPage 类型
- 包含搜索功能的 potentialAction
- 支持面包屑导航结构化数据（预留功能）

**数据类型**:

```json
{
  "@type": "WebSite",
  "name": "Multiple Personality System Wiki - 多意识体系统百科",
  "description": "专业的多意识体系统（MPS）、解离障碍（DID/OSDD）与创伤疗愈中文知识库",
  "inLanguage": "zh-CN",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://wiki.mpsteam.cn/search/?q={search_term_string}"
  }
}
```

**验证方式**:

- Google Rich Results Test: [https://search.google.com/test/rich-results](https://search.google.com/test/rich-results)
- Schema.org Validator: [https://validator.schema.org/](https://validator.schema.org/)

### 4. Meta Description 优化

**文件位置**: `mkdocs.yml`

**原描述**:

```text
多意识体系统（Multiple Personality System）与创伤相关主题的中文知识库
```

**优化后** (155 字符):

```text
专业的多意识体系统（MPS）、解离障碍（DID/OSDD）与创伤疗愈中文知识库。提供解离性身份障碍、Tulpa 创造、心理健康的全面指南与深入解析
```

**优化要点**:

- 增加了核心关键词：解离障碍、DID/OSDD、Tulpa
- 突出了网站的专业性
- 明确了内容范围（全面指南与深入解析）
- 符合搜索引擎推荐的 120-155 字符长度

### 5. Keywords Meta 标签

**文件位置**: `overrides/main.html`

**基础关键词**:

```text
多意识体系统,解离障碍,DID,OSDD,创伤疗愈,心理健康,Tulpa,多意识体系统
```

**动态关键词策略**:

- 基础关键词 (8 个) + 页面 tags (最多 4 个) = 最终关键词 (最多 12 个)
- 自动从页面 Frontmatter 的 tags 字段提取前 4 个标签
- 与基础关键词合并后截取前 12 个

**注意事项**:

- 严格控制在 8-12 个关键词之间
- 避免关键词堆砌
- 确保关键词与页面内容相关

### 6. 词条模板更新

**文件位置**: `docs/TEMPLATE_ENTRY.md`

**新增字段**:

```yaml
description: 简洁准确的词条描述，用于搜索引擎显示（120-155 字符，包含核心关键词）
```

**使用指南**:

- 每个新词条必须包含 description 字段
- 描述应包含词条的核心关键词
- 长度控制在 120-155 字符之间
- 描述应该简洁、准确、吸引人

**示例**:

```yaml
---
title: 解离性身份障碍（Dissociative Identity Disorder，DID）
description: 深入解析解离性身份障碍（DID）的诊断标准、临床表现与治疗方法。了解多重人格障碍的本质、创伤根源及康复路径
tags:

  - 诊断与临床
  - 解离
  - DID

---
```

## 关键词策略

### 主要关键词

1. 多意识体系统 / Multiple Personality System / MPS
2. 解离障碍 / Dissociative Disorders
3. 解离性身份障碍 / DID
4. 其他特定解离性障碍 / OSDD
5. 创伤疗愈 / Trauma Healing
6. Tulpa / 图帕
7. 心理健康 / Mental Health
8. 复杂性创伤 / CPTSD

### 长尾关键词

1. 如何理解多重人格
2. 解离性障碍自我疗愈
3. 创伤后应对指南
4. Tulpa 创造教程
5. DID 诊断标准
6. 多意识体系统运作机制

### 中文 SEO 特点

1. 使用简体中文为主
2. 包含常用的英文缩写（DID、OSDD、PTSD 等）
3. 注意中英文混排的关键词组合
4. 考虑口语化的搜索习惯

## 待完成事项

### 必须完成

- [ ] 创建 og-banner.png（推荐尺寸：1200x630px）
- [ ] 创建 twitter-banner.png（推荐尺寸：1200x600px）
- [x] 提交网站到 Google Search Console（已完成 2025-10-14）
- [x] 提交网站到必应网站管理员工具（已完成 2025-10-14）
- [-] ~~提交网站到百度站长平台~~（暂不提交）

### 建议完成

- [x] 为主要词条添加 description 字段（已完成 140 个词条，覆盖率 50.2%）
- [x] 为主要导航页面添加独特 description（已完成 12 个关键页面）
- [x] 创建 Meta Description 检测工具 `tools/check_meta_descriptions.py`
- [ ] 为剩余词条添加 description 字段（139 个待完成）
- [ ] 优化图片 alt 标签
- [ ] 添加内部链接优化
- [ ] 创建 FAQ 页面（Schema.org FAQPage）
- [ ] 监控关键词排名
- [ ] 定期更新 sitemap

## 验证和测试

### SEO 工具

1. **Google Search Console**: 监控索引状态、搜索表现
2. **百度站长平台**: 监控百度收录情况
3. **Google PageSpeed Insights**: 检查页面加载速度
4. **Google Rich Results Test**: 验证结构化数据
5. **Schema.org Validator**: 验证 JSON-LD 格式

### 手动测试

```bash

# 构建网站

mkdocs build

# 检查 robots.txt

cat site/robots.txt

# 检查首页 meta 标签

grep -E "og:|twitter:" site/index.html

# 检查 JSON-LD

grep "application/ld+json" site/index.html

# 检查 description

grep 'meta name="description"' site/index.html
```

### 浏览器测试

1. 打开开发者工具
2. 查看 Network 面板，确认资源加载正常
3. 查看 Console，确认没有 JavaScript 错误
4. 查看 Elements，检查 meta 标签是否正确

## 性能优化

### Core Web Vitals 优化

**问题**: `navigation.instant` 功能导致 INP (Interaction to Next Paint) 过高

- **原因**: `js-focus-visible.js` 脚本在即时导航模式下被重复执行
- **影响**: INP 达到 1,576ms，严重影响用户体验
- **解决方案**: 禁用 `navigation.instant` 系列功能

**优化配置** (`mkdocs.yml`):

```yaml
features:
  # 已禁用以优化性能
  # - navigation.instant
  # - navigation.instant.prefetch
  # - navigation.instant.progress

  # 保留其他功能

  - navigation.tracking
  - navigation.tabs
  - navigation.top

  # ... 其他功能
```

**预期效果**:

- ✅ INP: 1,576ms → 300-500ms
- ✅ 更快的交互响应
- ⚠️ 页面跳转改为完整刷新(但 SEO 不受影响)

## 性能监控

### 关键指标

- **收录量**: 搜索引擎收录的页面数量
- **关键词排名**: 目标关键词的搜索排名
- **点击率 (CTR)**: 搜索结果的点击率
- **Core Web Vitals**:
    - LCP (Largest Contentful Paint) < 2.5s
    - INP (Interaction to Next Paint) < 200ms
    - CLS (Cumulative Layout Shift) < 0.1
- **跳出率**: 用户离开网站的比例

### 建议监控频率

- 每周: 检查收录量和主要关键词排名
- 每月: 分析 Search Console 数据，调整策略
- 每季度: 全面 SEO 审计，更新优化策略

## 参考资源

1. [Google 搜索中心](https://developers.google.com/search)
2. [百度搜索资源平台](https://ziyuan.baidu.com/)
3. [Schema.org](https://schema.org/)
4. [Open Graph Protocol](https://ogp.me/)
5. [Twitter Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards)

## 更新日志

### 2025-10-21

- **Meta Description 重复问题修复**：
    - 修复 Bing Webmaster Tools 报告的重复 Meta Descriptions 问题
    - 为主要导航页面添加独特的 description 字段：
        - 首页 (index.md)
        - 快速开始 (QuickStart.md)
        - 前言 (Preface.md)
        - 贡献指南及子页面 (contributing/)
        - 标签索引、更新日志等辅助页面
    - 创建 `tools/check_meta_descriptions.py` 工具用于检测重复和缺失的 Meta Descriptions
    - 词条 description 覆盖率从 15.7% 提升至 50.2%（140/279 个词条）
    - 所有导航页面现在都有独特的 Meta Description,避免使用默认的 site_description

### 2025-10-14

- **性能优化**：
    - 禁用 `navigation.instant` 系列功能以优化页面交互性能
    - 预期 INP (Interaction to Next Paint) 从 1,576ms 降低至 300-500ms
    - 权衡：页面跳转改为完整刷新(传统模式)，但 SEO 和功能不受影响
- **SEO 优化修正**：
    - 修复 SearchAction.target 为 Material 搜索路由格式：`/search/?q={query}`
    - 优化 keywords 字段策略：基础 8 个 + 页面 tags 前 4 个，总数控制在 12 个以内
    - 排除内部文档页面(404.md, ADMIN_GUIDE.md 等)避免被搜索引擎索引
- 完成 Google Search Console 提交
- 完成必应网站管理员工具提交
- 确认暂不提交百度站长平台
- 为 32 个核心词条添加 description 字段
    - 包含 DID、OSDD、Tulpa、CPTSD、PTSD 等主要诊断词条
    - 包含 System、Alter、Front、Switch 等系统运作核心概念
    - 包含 Grounding、Trauma、Trigger、Flashback 等创伤相关词条
    - 包含各类成员角色：Host、Protector、Persecutor、Child Alter（儿童人格）、Caregiver、Gatekeeper 等
    - 创建自动化工具 `tools/check_descriptions.py` 和 `tools/add_descriptions.py`

### 2025-10-13

- 初始 SEO 优化实施
- 添加 robots.txt
- 实现 Open Graph 和 Twitter Card
- 实现 JSON-LD 结构化数据
- 优化 meta description
- 更新词条模板

---

**维护者**: MPS Team
**最后更新**: 2025-10-21
