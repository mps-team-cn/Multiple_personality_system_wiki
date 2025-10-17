# 性能优化指南（Performance Optimization）

本文档记录了 Multiple Personality System Wiki 的性能优化措施和最佳实践。

## 核心 Web Vitals 目标

| 指标                            | 目标值  | 说明             |
| ------------------------------- | ------- | ---------------- |
| LCP (Largest Contentful Paint)  | < 2.5s  | 最大内容绘制时间 |
| INP (Interaction to Next Paint) | < 200ms | 交互到下次绘制   |
| CLS (Cumulative Layout Shift)   | < 0.1   | 累积布局偏移     |

## 已实施的优化措施

### 1. JavaScript 性能优化

#### 1.1 事件委托 (Event Delegation)

**问题** ：为每个元素单独添加事件监听器会消耗大量内存和 CPU。

**解决方案** ：使用事件委托，在父元素上监听事件。

```javascript
// ❌ 不推荐：为每个链接添加监听器
links.forEach(link => {
  link.addEventListener('click', handler);
});

// ✅ 推荐：使用事件委托
content.addEventListener('click', function(e) {
  const link = e.target.closest('a');
  if (!link) return;
  // 处理逻辑
}, { capture: true });
```

**应用位置** ：

- [extra.js](../assets/extra.js): 外部链接处理、复制按钮
- [search-phrase-default.js](../assets/search-phrase-default.js): 搜索表单提交

#### 1.2 requestIdleCallback 延迟执行

**问题** ：页面加载时执行大量 JavaScript 会阻塞主线程。

**解决方案** ：使用 `requestIdleCallback` 延迟非关键任务。

```javascript
function scheduleIdleTask(callback) {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(callback, { timeout: 2000 });
  } else {
    setTimeout(callback, 1);
  }
}

// 非关键任务延迟执行
scheduleIdleTask(() => {
  addExternalLinkIcons();
  enhanceBackToTop();
});
```

**应用位置** ：

- [extra.js](../assets/extra.js): 外部链接图标、返回顶部
- [giscus-loader.js](../assets/giscus-loader.js): 评论系统加载

#### 1.3 Intersection Observer 可见性检测

**问题** ：一次性处理所有元素会导致页面卡顿。

**解决方案** ：使用 Intersection Observer 只处理可见元素。

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // 元素进入视口，开始处理
      processElement(entry.target);
      observer.unobserve(entry.target);
    }
  });
}, { rootMargin: '50px' });

elements.forEach(el => observer.observe(el));
```

**应用位置** ：

- [extra.js](../assets/extra.js): 外部链接批量处理
- [giscus-loader.js](../assets/giscus-loader.js): 评论系统懒加载

### 2. Giscus 评论系统优化

#### 2.1 用户交互检测

**策略** ：只有在用户开始交互（点击、滚动、键盘输入）后才加载评论系统。

```javascript
let userInteracted = false;

const detectInteraction = () => {
  userInteracted = true;
  // 移除监听器
};

['click', 'scroll', 'keydown', 'touchstart'].forEach(event => {
  document.addEventListener(event, detectInteraction, {
    capture: true,
    passive: true,
    once: true
  });
});
```

#### 2.2 三层延迟加载

1. **视口检测**: 使用 Intersection Observer 检测评论区是否进入视口
1. **用户交互**: 等待用户开始交互（或 3 秒超时）
1. **空闲时加载**: 使用 requestIdleCallback 在浏览器空闲时加载

**效果** ：将评论系统加载延迟到用户真正需要时，显著降低初始 INP。

### 3. 搜索脚本优化

#### 3.1 延迟初始化

```javascript
// 使用 requestIdleCallback 延迟初始化
if ('requestIdleCallback' in window) {
  requestIdleCallback(initSearchOptimization, { timeout: 1000 });
} else {
  setTimeout(initSearchOptimization, 100);
}
```

#### 3.2 Passive 事件监听器

```javascript
document.addEventListener('submit', handler, {
  capture: true,
  passive: true  // 不调用 preventDefault()
});
```

**效果** ：告诉浏览器不会阻止默认行为，允许并行处理滚动等操作。

### 4. MkDocs 配置优化

#### 4.1 禁用的功能

以下功能已在 `mkdocs.yml` 中禁用以提升性能：

```yaml
features:
  # - navigation.instant          # 禁用即时加载
  # - navigation.instant.prefetch # 禁用预加载
  # - search.highlight            # 禁用搜索高亮
```

**原因** ：

- `navigation.instant`: 虽然加快导航，但会增加初始加载时间
- `search.highlight`: 会在搜索结果页面执行大量 DOM 操作

#### 4.2 启用的优化

```yaml
plugins:
  - minify:           # 压缩 HTML/CSS/JS
      minify_html: true
      minify_js: true
      minify_css: true
```

### 5. 字体优化

#### 5.1 使用系统字体

```css
:root {
  --md-text-font:
    -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Microsoft YaHei", "Segoe UI", sans-serif;
}
```

**优势** ：

- 零网络请求
- 即时可用
- 跨平台一致性

#### 5.2 禁用 Google Fonts

```yaml
theme:
  font: false  # 不加载外部字体
```

## 性能监测

### 使用 Lighthouse

```bash
# 本地测试
lighthouse https://wiki.mpsteam.cn --output html --output-path ./lighthouse-report.html

# 移动端测试
lighthouse https://wiki.mpsteam.cn --preset=mobile --output html
```

### 使用 Chrome DevTools

1. 打开 Chrome DevTools (F12)
1. 切换到 **Performance** 标签
1. 点击 **Record** 按钮
1. 刷新页面或执行操作
1. 停止录制，分析报告

### 关键指标查看

1. 打开 **Network** 标签
1. 启用 **Disable cache**
1. 选择 **Slow 3G** 或 **Fast 3G** 模拟慢速网络
1. 刷新页面，观察加载时间

## 性能问题排查

### INP 过高 (> 200ms)

**可能原因** ：

1. 同步 JavaScript 执行时间过长
1. 大量 DOM 操作
1. 事件监听器过多
1. 第三方脚本阻塞

**排查方法** ：

1. Chrome DevTools → Performance → 记录交互
1. 查看 **Main** 线程的长任务 (Long Tasks)
1. 识别阻塞的 JavaScript 函数

**解决方案** ：

- 使用 `requestIdleCallback` 延迟非关键任务
- 使用事件委托减少监听器数量
- 将长任务拆分为多个小任务
- 延迟加载第三方脚本

### LCP 过高 (> 2.5s)

**可能原因** ：

1. 大图片未优化
1. 关键 CSS/JS 阻塞渲染
1. 字体加载延迟
1. 服务器响应慢

**解决方案** ：

- 图片使用 WebP 格式
- 关键 CSS 内联到 HTML
- 使用系统字体
- 启用 CDN 和缓存

### CLS 过高 (> 0.1)

**可能原因** ：

1. 图片未指定尺寸
1. 广告/iframe 动态插入
1. Web 字体加载导致文本移动

**解决方案** ：

- 为图片设置 `width` 和 `height`
- 为动态内容预留空间
- 使用 `font-display: swap`

## 最佳实践

### 1. 新增 JavaScript 功能

- ✅ 使用事件委托而非逐个绑定
- ✅ 使用 `requestIdleCallback` 延迟非关键任务
- ✅ 使用 Intersection Observer 处理可见性
- ✅ 添加 `passive: true` 到滚动/触摸监听器
- ❌ 避免在 `DOMContentLoaded` 中执行耗时操作
- ❌ 避免同步 `querySelectorAll` + `forEach`

### 2. 新增第三方脚本

- ✅ 使用 `async` 或 `defer` 属性
- ✅ 使用 Intersection Observer 延迟加载
- ✅ 检查是否支持 `requestIdleCallback`
- ❌ 避免在 `<head>` 中同步加载
- ❌ 避免阻塞关键渲染路径

### 3. 新增 CSS 样式

- ✅ 使用 CSS 变量统一管理
- ✅ 使用 `will-change` 优化动画
- ✅ 避免复杂的选择器
- ❌ 避免强制同步布局 (Forced Reflow)
- ❌ 避免过度使用 `box-shadow` 和 `filter`

## 性能优化检查清单

在发布新版本前，请确认以下事项：

- [ ] 运行 Lighthouse 测试，确保所有核心指标达标
- [ ] 在慢速 3G 网络下测试加载速度
- [ ] 检查 Chrome DevTools Performance 面板
- [ ] 验证所有图片已优化
- [ ] 确认第三方脚本使用延迟加载
- [ ] 检查是否有未使用的 CSS/JS
- [ ] 验证移动端体验

## 参考资源

- [Web Vitals 官方文档](https://web.dev/vitals/)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [MDN: requestIdleCallback](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback)
- [Chrome DevTools 性能分析](https://developer.chrome.com/docs/devtools/performance/)

## 微优化技巧

### 1. 避免重复处理

为已处理的元素添加标记，避免重复执行相同操作：

```javascript
const processElement = (element) => {
  // 检查是否已处理
  if (element.dataset.processed) return;

  // 执行处理逻辑
  // ...

  // 标记为已处理
  element.dataset.processed = '1';
};
```

### 2. 事件节流 (Throttle)

对于高频触发的事件（如滚动、resize），使用节流限制执行频率：

```javascript
let throttleTimer = null;

observer = new MutationObserver(() => {
  if (throttleTimer) return;

  throttleTimer = setTimeout(() => {
    // 执行逻辑
    throttleTimer = null;
  }, 100);  // 100ms 内只执行一次
});
```

### 3. 精确的选择器

使用更精确的选择器避免误匹配：

```javascript
// ❌ 过于宽泛
const form = e.target.closest('form');

// ✅ 更精确
const form = e.target.closest('form[role="search"]');
const isMkDocsSearch = input.classList.contains('md-search__input');
```

## 更新日志

- 2025-10-16: 第二版，添加微优化技巧

  - 添加重复处理检测标记
  - 为主题同步添加节流优化
  - 为搜索表单添加更精确的检测
  - 将面包屑结构化数据移至空闲任务

- 2025-10-16: 初始版本，记录现有优化措施

  - 实施事件委托优化
  - 实施 requestIdleCallback 延迟执行
  - 优化 Giscus 加载策略
  - 优化搜索脚本初始化
