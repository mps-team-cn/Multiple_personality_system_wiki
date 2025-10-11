# Giscus 评论系统集成指南

本文档说明如何在 Multiple Personality System Wiki 中集成 Giscus 评论系统，并针对中国用户访问进行优化。

## 什么是 Giscus

[Giscus](https://giscus.app/zh-CN) 是一个基于 GitHub Discussions 的评论系统，通过 GitHub App 实现：

- ✅ 开源且免费
- ✅ 无需数据库，数据存储在 GitHub Discussions
- ✅ 支持 Markdown、代码高亮、LaTeX 公式
- ✅ 支持多语言、主题自定义
- ✅ 支持反应表情、评论回复、评论排序
- ✅ 访客可以通过 GitHub 账号登录评论

## 为什么选择 Giscus

对比其他评论系统：

| 评论系统 | 优点 | 缺点 |
|---------|------|------|
| **Giscus** | 开源免费、数据可控、Markdown 支持好 | 依赖 GitHub（中国访问受限）|
| Disqus | 功能强大、访问稳定 | 广告多、隐私问题、加载慢 |
| Gitalk | 基于 GitHub Issues | 需要初始化每个页面、不支持嵌套回复 |
| Waline | 国内访问好、支持匿名评论 | 需要自建后端服务 |

**选择建议**：Giscus 适合技术文档类项目，社区参与度高，且本项目已使用 GitHub 托管。

## 中国用户访问问题与优化方案

### 问题说明

Giscus 依赖以下 GitHub 资源：

- `giscus.app` - Giscus 服务
- `github.com` - 用户登录和 API
- `avatars.githubusercontent.com` - 用户头像
- GitHub OAuth 认证流程

在中国大陆，GitHub 访问可能出现：

- 🔴 间歇性无法访问
- 🟡 加载缓慢（特别是头像）
- 🟡 OAuth 认证失败

### 优化方案对比

#### 方案 1：Cloudflare Workers 代理（推荐）

通过 Cloudflare Workers 代理 Giscus 请求，提高访问稳定性。

**优点**：

- ✅ 项目已部署在 Cloudflare Pages，可充分利用 Cloudflare 网络
- ✅ 免费额度充足（每天 10 万次请求）
- ✅ 配置相对简单
- ✅ 支持缓存用户头像

**缺点**：

- ⚠️ 需要额外维护 Worker 脚本
- ⚠️ OAuth 认证流程仍依赖 GitHub

**实施步骤**：

1. 创建 Cloudflare Worker
2. 配置代理规则（见下文"实施方案 1"）
3. 修改 Giscus 配置使用代理域名

#### 方案 2：混合方案（Giscus + Waline 备选）

默认使用 Giscus，为中国用户提供 Waline 备选入口。

**优点**：

- ✅ 兼顾国内外用户体验
- ✅ Waline 支持匿名评论，降低参与门槛

**缺点**：

- ⚠️ 需要维护两套评论系统
- ⚠️ 需要部署 Waline 后端（可使用 Vercel/Cloudflare Workers）
- ⚠️ 评论数据分散

#### 方案 3：仅提示用户使用代理（简单方案）

在评论区上方添加友好提示。

**优点**：

- ✅ 实现简单，无需额外服务

**缺点**：

- ⚠️ 依赖用户自行解决访问问题
- ⚠️ 影响用户体验

**推荐配置**（方案 3）：

```html
<div class="giscus-notice" style="padding: 12px; margin-bottom: 16px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
  <p style="margin: 0; font-size: 14px; color: #856404;">
    💡 <strong>访问提示</strong>：评论系统基于 GitHub Discussions。
    如无法加载，请检查网络连接或稍后重试。
  </p>
</div>
```

## 基础配置步骤

### 1. 启用 GitHub Discussions

1. 进入仓库 `mps-team-cn/Multiple_personality_system_wiki`
2. **Settings** → **General** → **Features**
3. 勾选 ✅ **Discussions**

### 2. 安装 Giscus App

1. 访问 [Giscus App](https://github.com/apps/giscus)
2. 点击 **Install**
3. 选择仓库 `mps-team-cn/Multiple_personality_system_wiki`
4. 授权必要权限（Discussions 读写）

### 3. 获取配置代码

访问 [giscus.app/zh-CN](https://giscus.app/zh-CN)，填写以下信息：

#### 基础配置

- **仓库**：`mps-team-cn/Multiple_personality_system_wiki`
- **Discussion 分类**：推荐使用 `Announcements` 或新建 `Comments` 分类
    - ⚠️ 必须选择 **公告（Announcement）** 类型分类，普通分类不支持

#### 功能配置

- **页面 ↔️ Discussions 映射关系**：
    - 推荐 `pathname`（使用页面路径作为标识）
    - 或 `og:title`（使用页面标题）
- **Discussion 分类**：推荐新建 `Comments` 分类
- **特性**：
    - ✅ 启用主评论区懒加载
    - ✅ 将评论框放在评论上方（可选）
- **主题**：选择 `preferred_color_scheme`（跟随系统）

#### 生成的配置

系统会生成类似以下的代码：

```html
<script src="https://giscus.app/client.js"
        data-repo="mps-team-cn/Multiple_personality_system_wiki"
        data-repo-id="YOUR_REPO_ID"
        data-category="Comments"
        data-category-id="YOUR_CATEGORY_ID"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
```

## MkDocs Material 集成方法

### 方法 1：通过自定义模板（推荐）

#### 步骤 1：创建主题覆盖目录

```bash
mkdir -p overrides/partials
```

#### 步骤 2：创建评论区组件

创建 `overrides/partials/comments.html`：

```html
{% if page.meta.comments %}
<hr>
<div class="giscus-container">
  <!-- 中国用户访问提示 -->
  <div class="giscus-notice" style="padding: 12px; margin-bottom: 16px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
    <p style="margin: 0; font-size: 14px; color: #856404;">
      💡 <strong>访问提示</strong>：评论系统基于 GitHub Discussions。
      如无法加载，请检查网络连接或<a href="https://github.com/mps-team-cn/Multiple_personality_system_wiki/discussions" target="_blank">直接前往 GitHub Discussions</a> 参与讨论。
    </p>
  </div>

  <!-- Giscus 评论组件 -->
  <script src="https://giscus.app/client.js"
          data-repo="mps-team-cn/Multiple_personality_system_wiki"
          data-repo-id="YOUR_REPO_ID"
          data-category="Comments"
          data-category-id="YOUR_CATEGORY_ID"
          data-mapping="pathname"
          data-strict="0"
          data-reactions-enabled="1"
          data-emit-metadata="0"
          data-input-position="top"
          data-theme="preferred_color_scheme"
          data-lang="zh-CN"
          data-loading="lazy"
          crossorigin="anonymous"
          async>
  </script>
</div>
{% endif %}
```

#### 步骤 3：集成到内容模板

创建 `overrides/partials/content.html`：

```html
<!-- 从父模板继承 -->
{% extends "base.html" %}

<!-- 在内容区域添加评论 -->
{% block content %}
  {{ super() }}

  <!-- 在页面内容后添加评论区 -->
  {% include "partials/comments.html" %}
{% endblock %}
```

#### 步骤 4：启用自定义主题目录

修改 `mkdocs.yml`：

```yaml
theme:
  name: material
  custom_dir: overrides  # 取消注释此行
```

#### 步骤 5：在页面 Frontmatter 启用评论

在需要评论的页面（如词条）中添加：

```yaml
---
title: 词条标题
comments: true  # 启用评论
---
```

### 方法 2：通过全局 JavaScript（快速方案）

如果不想修改模板，可以通过 JavaScript 动态插入。

#### 步骤 1：创建 Giscus 加载脚本

创建 `docs/assets/giscus-loader.js`：

```javascript
// Giscus 评论系统加载器
(function() {
  'use strict';

  // 检查是否应该加载评论
  function shouldLoadComments() {
    // 从页面 meta 中检查是否启用评论
    const metaComments = document.querySelector('meta[name="page-comments"]');
    return metaComments && metaComments.content === 'true';
  }

  // 创建访问提示
  function createNotice() {
    const notice = document.createElement('div');
    notice.className = 'giscus-notice';
    notice.style.cssText = 'padding: 12px; margin-bottom: 16px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;';
    notice.innerHTML = `
      <p style="margin: 0; font-size: 14px; color: #856404;">
        💡 <strong>访问提示</strong>：评论系统基于 GitHub Discussions。
        如无法加载，请检查网络连接或<a href="https://github.com/mps-team-cn/Multiple_personality_system_wiki/discussions" target="_blank">直接前往 GitHub Discussions</a> 参与讨论。
      </p>
    `;
    return notice;
  }

  // 加载 Giscus
  function loadGiscus() {
    const article = document.querySelector('article');
    if (!article) return;

    const container = document.createElement('div');
    container.className = 'giscus-container';

    // 添加提示
    container.appendChild(createNotice());

    // 创建 Giscus 脚本
    const script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    script.setAttribute('data-repo', 'mps-team-cn/Multiple_personality_system_wiki');
    script.setAttribute('data-repo-id', 'YOUR_REPO_ID');
    script.setAttribute('data-category', 'Comments');
    script.setAttribute('data-category-id', 'YOUR_CATEGORY_ID');
    script.setAttribute('data-mapping', 'pathname');
    script.setAttribute('data-strict', '0');
    script.setAttribute('data-reactions-enabled', '1');
    script.setAttribute('data-emit-metadata', '0');
    script.setAttribute('data-input-position', 'top');
    script.setAttribute('data-theme', 'preferred_color_scheme');
    script.setAttribute('data-lang', 'zh-CN');
    script.setAttribute('data-loading', 'lazy');
    script.crossOrigin = 'anonymous';
    script.async = true;

    container.appendChild(script);
    article.appendChild(container);
  }

  // 初始化
  document.addEventListener('DOMContentLoaded', function() {
    if (shouldLoadComments()) {
      loadGiscus();
    }
  });
})();
```

#### 步骤 2：添加到 MkDocs 配置

修改 `mkdocs.yml`：

```yaml
extra_javascript:

  - assets/extra.js
  - assets/giscus-loader.js  # 新增

```

## 实施方案 1：Cloudflare Worker 代理

### Worker 脚本示例

创建新的 Cloudflare Worker，代码如下：

```javascript
// Giscus 代理 Worker
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // 代理 Giscus 主服务
  if (url.pathname.startsWith('/giscus/')) {
    const targetPath = url.pathname.replace('/giscus/', '/')
    const targetUrl = `https://giscus.app${targetPath}${url.search}`

    return fetch(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    })
  }

  // 代理 GitHub 头像（启用缓存）
  if (url.pathname.startsWith('/avatars/')) {
    const targetPath = url.pathname.replace('/avatars/', '/')
    const targetUrl = `https://avatars.githubusercontent.com${targetPath}`

    const response = await fetch(targetUrl)
    const newResponse = new Response(response.body, response)

    // 添加缓存头
    newResponse.headers.set('Cache-Control', 'public, max-age=86400')
    return newResponse
  }

  return new Response('Not Found', { status: 404 })
}
```

### 配置 Worker 路由

1. 部署 Worker（如命名为 `giscus-proxy`）
2. 绑定自定义域名或使用 Worker 域名（如 `giscus-proxy.your-account.workers.dev`）
3. 修改 Giscus 脚本配置：

```javascript
// 将 Giscus CDN 替换为 Worker 代理
script.src = 'https://your-worker-domain.workers.dev/giscus/client.js';
```

**注意**：Worker 方案复杂度较高，建议先实施方案 3（仅提示），观察用户反馈后决定是否升级。

## 样式自定义

### 主题跟随

Giscus 支持根据页面主题切换：

```javascript
// 监听主题切换
const observer = new MutationObserver(() => {
  const isDark = document.body.getAttribute('data-md-color-scheme') === 'slate';
  const theme = isDark ? 'dark' : 'light';

  // 向 Giscus iframe 发送消息
  const giscusFrame = document.querySelector('iframe.giscus-frame');
  if (giscusFrame) {
    giscusFrame.contentWindow.postMessage(
      { giscus: { setConfig: { theme } } },
      'https://giscus.app'
    );
  }
});

observer.observe(document.body, {
  attributes: true,
  attributeFilter: ['data-md-color-scheme']
});
```

**注意**：如将 Giscus 客户端托管到自定义域名（例如通过 Cloudflare Worker 代理为 <https://comments.example.com/giscus/client.js>），需要同步调整以下两处配置以避免 `postMessage` 目标域不匹配：

1. 将上述代码中的目标域从 <https://giscus.app> 替换为自定义域，例如 <https://comments.example.com>。
2. 设置 `data-giscus-host`（或直接更新 `script.src`）指向同一域名，确保评论 iframe 与消息发送目标一致。

### CSS 样式调整

在 `docs/assets/extra-material.css` 中添加：

```css
/* Giscus 评论区样式 */
.giscus-container {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--md-default-fg-color--lightest);
}

/* 深色模式下的提示框 */
[data-md-color-scheme="slate"] .giscus-notice {
  background: #3a3a2a !important;
  border-left-color: #ffb300 !important;
}

[data-md-color-scheme="slate"] .giscus-notice p {
  color: #ffd54f !important;
}
```

## 部署清单

- [ ] 启用仓库 GitHub Discussions
- [ ] 安装 Giscus App 并授权
- [ ] 创建 Discussions 分类（如 `Comments`）
- [ ] 获取 `data-repo-id` 和 `data-category-id`
- [ ] 选择集成方法（模板覆盖或 JS 加载）
- [ ] 修改配置文件替换占位符
- [ ] 添加访问提示（中国用户）
- [ ] 测试本地预览
- [ ] 推送到 GitHub 触发 Cloudflare Pages 构建
- [ ] 验证评论功能（登录、发表、回复、表情）
- [ ] 检查主题切换是否正常
- [ ] （可选）配置 Cloudflare Worker 代理

## 故障排查

### 问题 1：评论区无法加载

**可能原因**：

- ❌ Discussions 未启用
- ❌ Giscus App 未安装或权限不足
- ❌ `data-repo-id` 或 `data-category-id` 错误
- ❌ 网络问题（中国用户）

**解决方法**：

1. 检查 GitHub 仓库设置
2. 重新安装 Giscus App
3. 访问 [giscus.app](https://giscus.app/zh-CN) 重新获取配置
4. 测试 GitHub 连接性

### 问题 2：评论无法提交

**可能原因**：

- ❌ 未登录 GitHub
- ❌ GitHub OAuth 认证失败（中国用户）
- ❌ 仓库权限问题

**解决方法**：

1. 确保用户已登录 GitHub
2. 检查 Giscus App 权限
3. 引导用户使用代理或直接在 GitHub Discussions 评论

### 问题 3：主题切换不生效

**检查**：

- 确认已添加主题切换监听脚本
- 检查浏览器控制台是否有 CORS 错误
- 验证 `data-theme` 配置

### 问题 4：中国用户访问缓慢

**优化建议**：

1. 启用 `data-loading="lazy"`（懒加载）
2. 实施 Cloudflare Worker 代理
3. 在页面醒目位置添加"直接前往 GitHub Discussions"链接

### 问题 5：提交评论提示 `{"error":"Discussion not found"}`

**现象描述**：用户填写评论内容后，弹出 JSON 提示 `{"error":"Discussion not found"}`，评论不会被写入，同时浏览器控制台常伴随以下日志：

- 控制台网络日志：`GET ... 404 (Not Found)`（请求地址为 <https://giscus.app/api/discussions?...&term=undefined...>）
- 控制台信息：`[giscus] Discussion not found. A new discussion will be created if a comment/reaction is submitted.`

**常见原因**：

- ❌ `data-giscus-strict="1"` 且对应讨论尚未存在
- ❌ Giscus App 未被授予在目标仓库创建 Discussion 的权限
- ❌ 选用的 `categoryId` 不允许外部用户创建讨论或已被删除
- ❌ 页面 `data-giscus-mapping` 与仓库中已存在的 Discussion 标识不一致
- ❌ 站点构建时注入的 `data-giscus-term`、`data-giscus-mapping` 值为空（请求参数中的 `term=undefined` 即是此类线索）

**处理步骤**：

1. 登录仓库设置页面，确认 Giscus App 在 **Repository access** 中已包含当前仓库，并拥有 `Read and write` 权限。
2. 打开 GitHub Discussions，确认配置使用的分类仍存在且接受新讨论；如被删除，请重新创建并更新 `data-giscus-category-id`。
3. 若启用了严格匹配（`data-giscus-strict="1"`），请在对应分类中手动创建一个 Discussion，并确保其标题或路径与 `data-giscus-mapping` 规则匹配；或将严格模式改回 `0` 允许 Giscus 自动创建讨论。
4. 使用浏览器开发者工具检查页面最终生成的 `data-giscus-repo-id`、`data-giscus-category-id`、`data-giscus-mapping`、`data-giscus-term` 等属性是否与最新配置一致。若看到 `term=undefined`，说明构建未注入标识符，需要回溯页面模板或 JavaScript 注入逻辑，确保 `data-mapping` 对应的值（例如 `pathname`）在构建期可解析并写入。
5. 如仍无法创建，使用维护者账号直接在仓库 Discussions 中发起一次评论，确认可以手动写入，然后重新尝试页面评论。
6. 若控制台出现多条“Discussion not found”提示，请确认评论组件未被重复加载（例如 SPA 页面跳转后未清理旧 iframe），必要时在路由切换前调用 `giscusFrame.remove()` 仅保留一份实例。

## 备选方案

如果 Giscus 不适合项目需求，可考虑：

### Waline

- **官网**：<https://waline.js.org/>
- **优点**：国内访问友好、支持匿名评论、多种部署方式
- **缺点**：需要自建后端（可用 Vercel 免费部署）

### Utterances

- **官网**：<https://utteranc.es/>
- **优点**：基于 GitHub Issues、配置简单
- **缺点**：不支持嵌套回复、每个页面需手动初始化 Issue

## 参考资源

- [Giscus 官方文档](https://giscus.app/zh-CN)
- [MkDocs Material 自定义主题](https://squidfunk.github.io/mkdocs-material/customization/)
- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)
- [GitHub Discussions API](https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions)

## 维护建议

1. **定期检查**：每月检查评论系统运行状态
2. **监控反馈**：关注用户关于评论功能的反馈
3. **更新文档**：记录配置变更和问题解决方案
4. **备份评论**：GitHub Discussions 数据已由 GitHub 保存，建议定期导出备份

---

**文档版本**：v1.0
**最后更新**：2025-10-10
**维护者**：项目核心团队
