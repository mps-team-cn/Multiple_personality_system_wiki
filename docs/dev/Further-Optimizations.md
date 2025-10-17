# 进一步优化建议（基于 Lighthouse Treemap 分析）

## 测试数据概览

**总传输大小**: 150.0 KiB

**资源分布**:

- 🔴 Google Tag Manager: 72.9 KiB (49%)
- 🟡 glightbox.min.js: 15.6 KiB (10%)
- 🟢 自定义脚本: 5.6 KiB (3.7%)
- 🟢 其他资源: 55.9 KiB (37%)

## 优化机会

### 1. Google Tag Manager 延迟加载（高优先级）

**问题**: GTM 占用 72.9 KiB (49%)，是最大的 JavaScript 资源。

**当前影响**:

- 阻塞主线程
- 增加 TTI (Time to Interactive)
- 可能导致 INP 升高

**优化方案**:

#### 方案 A: 用户交互后加载（推荐）

```javascript
// 在 extra.js 中添加
function loadGoogleTagManager() {
  if (window.gtmLoaded) return;
  window.gtmLoaded = true;

  const script = document.createElement('script');
  script.src = 'https://www.googletagmanager.com/gtag/js?id=YOUR_ID';
  script.async = true;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_ID');
}

// 用户交互后加载
['scroll', 'mousemove', 'touchstart', 'click'].forEach(event => {
  document.addEventListener(event, loadGoogleTagManager, {
    once: true,
    passive: true
  });
});

// 超时后也加载（确保数据收集）
setTimeout(loadGoogleTagManager, 3000);
```

**预期效果**:

- ✅ 减少初始加载 72.9 KiB
- ✅ 降低 INP 约 50-100ms
- ✅ 提升 TTI 约 200-500ms

#### 方案 B: 使用 Partytown（高级）

```html
<!-- 在 overrides/main.html 中 -->
<script type="text/partytown">
  // Google Analytics 代码在 Web Worker 中运行
</script>
```

**优势**:

- 在 Web Worker 中运行，不阻塞主线程
- 保持完整的分析功能

______________________________________________________________________

### 2. glightbox 按需加载（中优先级）

**问题**: glightbox.min.js (15.6 KiB) 用于图片灯箱，但不是所有页面都需要。

**优化方案**:

```javascript
// 检测页面是否有图片
function hasImages() {
  return document.querySelectorAll('.md-content img').length > 0;
}

// 按需加载 glightbox
if (hasImages()) {
  scheduleIdleTask(() => {
    // MkDocs Material 会自动加载 glightbox
    // 或者手动加载：
    // import('path/to/glightbox').then(GLightbox => {
    //   GLightbox({ ... });
    // });
  });
}
```

**预期效果**:

- ✅ 无图片页面减少 15.6 KiB
- ✅ 有图片页面保持功能完整

**注意**: 需要检查 MkDocs Material 是否支持动态加载。

______________________________________________________________________

### 3. Cloudflare Insights 延迟加载（低优先级）

**问题**: Cloudflare Beacon 加载两次 (6.6 KiB × 2)。

**检查项**:

1. 是否重复配置了 Cloudflare Analytics？
1. 是否可以合并为一次加载？

**优化方案**:

```javascript
// 延迟加载 Cloudflare Insights
setTimeout(() => {
  if (window.cloudflareInsights) return;

  const script = document.createElement('script');
  script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  script.defer = true;
  document.head.appendChild(script);
}, 5000);  // 5秒后加载
```

**预期效果**:

- ✅ 减少初始加载 13.2 KiB
- ✅ 不影响分析数据（延迟收集可接受）

______________________________________________________________________

### 4. 字体加载优化（低优先级）

虽然图中未显示字体，但建议检查：

```css
/* 使用 font-display: swap 确保文本立即可见 */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;  /* 关键 */
}
```

______________________________________________________________________

## 优化优先级矩阵

| 优化项             | 收益  | 难度  | 优先级     | 预期改进              |
| ------------------ | ----- | ----- | ---------- | --------------------- |
| GTM 延迟加载       | 🔴 高 | 🟢 低 | ⭐⭐⭐⭐⭐ | -72.9 KiB, -200ms TTI |
| glightbox 按需加载 | 🟡 中 | 🟡 中 | ⭐⭐⭐     | -15.6 KiB (部分页面)  |
| Cloudflare 延迟    | 🟢 低 | 🟢 低 | ⭐⭐       | -13.2 KiB             |
| 字体优化           | 🟢 低 | 🟢 低 | ⭐         | 视觉稳定性            |

## 实施步骤

### 第一阶段（立即实施）

1. **GTM 延迟加载**

   ```bash
   # 1. 编辑 extra.js
   # 2. 添加延迟加载逻辑
   # 3. 测试 GA 数据是否正常收集
   ```

1. **验证效果**

   ```bash
   lighthouse https://wiki.mpsteam.cn --output html
   # 检查 JavaScript execution time 是否减少
   ```

### 第二阶段（测试验证）

1. **glightbox 优化**

   - 检查 MkDocs Material 配置
   - 测试动态加载可行性
   - 验证图片灯箱功能

1. **Cloudflare Insights**

   - 检查是否重复加载
   - 考虑延迟加载

### 第三阶段（持续监控）

1. **监控指标**

   - Google Analytics 数据完整性
   - 用户行为分析准确性
   - Core Web Vitals 改善情况

1. **A/B 测试**

   - 对比优化前后的分析数据
   - 确保优化不影响业务需求

## 预期性能提升

### 优化前（当前）

| 指标     | 当前值    | 目标值    |
| -------- | --------- | --------- |
| Total JS | 150.0 KiB | < 100 KiB |
| INP      | ~200ms    | < 200ms   |
| TTI      | ~3.5s     | < 2.5s    |

### 优化后（预期）

如果实施所有优化：

| 指标           | 预期值  | 改进  |
| -------------- | ------- | ----- |
| **Initial JS** | ~50 KiB | ↓ 66% |
| **INP**        | ~100ms  | ↓ 50% |
| **TTI**        | ~2.0s   | ↓ 43% |

**关键改进**:

- ✅ GTM 延迟加载: -72.9 KiB
- ✅ glightbox 按需: -15.6 KiB (部分)
- ✅ Cloudflare 延迟: -13.2 KiB

**总计可减少**: ~100 KiB (67%)

## 代码示例

### 完整的 GTM 延迟加载实现

```javascript
/**
 * Google Tag Manager 延迟加载
 * 策略：用户交互后加载，或 3 秒超时
 */
(function() {
  'use strict';

  let gtmLoaded = false;

  function loadGTM() {
    if (gtmLoaded) return;
    gtmLoaded = true;

    console.log('[Performance] Loading GTM after user interaction');

    // 创建 GTM 脚本
    const script = document.createElement('script');
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
    script.async = true;
    document.head.appendChild(script);

    // 初始化 dataLayer
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX', {
      'page_path': window.location.pathname
    });
  }

  // 用户交互事件
  const events = ['scroll', 'mousemove', 'touchstart', 'click', 'keydown'];

  events.forEach(event => {
    document.addEventListener(event, function handler() {
      loadGTM();
      // 移除所有监听器
      events.forEach(e => {
        document.removeEventListener(e, handler);
      });
    }, { once: true, passive: true });
  });

  // 超时后加载（确保数据收集）
  setTimeout(loadGTM, 3000);
})();
```

### MkDocs 配置调整

```yaml
# mkdocs.yml
extra:
  analytics:
    # provider: google  # 禁用内置的 GA
    # property: G-XXXXXXXXXX

    # 使用自定义加载脚本
    feedback: false  # 可选：禁用反馈功能

extra_javascript:
  - assets/extra.js
  - assets/gtm-loader.js  # 新增：GTM 延迟加载脚本
```

## 监控和验证

### 1. Lighthouse CI 配置

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['https://wiki.mpsteam.cn'],
      numberOfRuns: 3,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'bootup-time': ['error', { maxNumericValue: 2000 }],
        'total-byte-weight': ['warn', { maxNumericValue: 200000 }],
        'interactive': ['error', { maxNumericValue: 2500 }],
      },
    },
  },
};
```

### 2. 性能监控脚本

```javascript
// 记录性能指标
window.addEventListener('load', () => {
  if ('PerformanceObserver' in window) {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        console.log('[Performance]', entry.name, entry.duration);
      }
    });

    observer.observe({ entryTypes: ['navigation', 'resource'] });
  }
});
```

## 注意事项

### Google Analytics 数据完整性

**问题**: 延迟加载 GTM 可能导致：

1. 跳出率统计不准确（用户快速离开）
1. 页面停留时间偏差
1. 部分会话丢失

**解决方案**:

1. **设置合理的延迟时间**（建议 3 秒）
1. **监控数据变化**，对比优化前后
1. **保留关键事件的即时上报**（如购买、注册）

### 渐进式实施

建议采用以下步骤：

1. **第一周**: GTM 延迟加载，监控 GA 数据
1. **第二周**: 如果数据正常，继续优化 glightbox
1. **第三周**: 全面监控，评估效果

### 回滚计划

如果发现问题：

```javascript
// 紧急回滚：恢复即时加载
// 1. 注释掉延迟加载脚本
// 2. 恢复 mkdocs.yml 中的 analytics 配置
// 3. 重新构建和部署
```

## 相关资源

- [Partytown - Run Third-Party Scripts in Web Worker](https://partytown.builder.io/)
- [Google Analytics - Delayed Loading](https://developers.google.com/analytics/devguides/collection/gtagjs)
- [Lighthouse - JavaScript Boot-up Time](https://web.dev/bootup-time/)
- [Resource Hints - Prefetch/Preconnect](https://web.dev/preconnect-and-dns-prefetch/)

## 更新日志

- 2025-10-16: 创建初始版本
  - 基于 Lighthouse Treemap 分析
  - 识别 GTM 为最大性能瓶颈
  - 提供延迟加载方案
  - 预估 67% JavaScript 减少
