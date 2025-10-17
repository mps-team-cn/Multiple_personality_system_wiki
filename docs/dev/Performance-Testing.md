# 性能测试指南

本文档提供了测试网站性能的详细步骤和工具使用指南。

## 测试前准备

### 1. 确保使用隐身模式

浏览器扩展可能影响性能测试结果，建议使用隐身模式：

- **Chrome**: Ctrl+Shift+N (Windows/Linux) 或 Cmd+Shift+N (macOS)
- **Firefox**: Ctrl+Shift+P (Windows/Linux) 或 Cmd+Shift+P (macOS)
- **Edge**: Ctrl+Shift+N (Windows/Linux) 或 Cmd+Shift+N (macOS)

### 2. 清除缓存

测试前清除浏览器缓存，确保测试真实的首次加载性能：

1. 打开 Chrome DevTools (F12)
1. 右键点击刷新按钮
1. 选择 "清空缓存并硬性重新加载"

## 测试方法

### 方法一：Chrome DevTools Performance 面板

#### 步骤

1. 打开网站页面
1. 按 F12 打开 DevTools
1. 切换到 **Performance** 标签
1. 点击 **Record** 按钮（圆形图标）
1. 刷新页面或执行交互操作
1. 等待页面完全加载
1. 点击 **Stop** 按钮

#### 关键指标查看

**主线程活动**:

- 查看 **Main** 线程的火焰图
- 识别长任务（红色标记，> 50ms）
- 查看 JavaScript 执行时间

**INP (Interaction to Next Paint)**:

- 查看 **Interactions** 部分
- 每个交互的延迟时间应 < 200ms
- 红色标记表示需要优化

**示例分析**:

```
✅ 优化后应该看到:
- 主线程有更多空闲时间（白色区域）
- 长任务（> 50ms）数量减少
- DOMContentLoaded 后快速完成初始化
- 用户交互响应时间 < 200ms

❌ 优化前可能看到:
- 主线程持续繁忙（很少白色区域）
- 多个长任务连续执行
- DOMContentLoaded 后仍有大量 JavaScript 执行
- 用户交互响应时间 > 1000ms
```

### 方法二：Lighthouse CI

#### 在线测试

使用 Google PageSpeed Insights:

1. 访问 [PageSpeed Insights](https://pagespeed.web.dev/)
1. 输入网址: `https://wiki.mpsteam.cn`
1. 点击 "分析"
1. 等待测试完成（约 30-60 秒）

#### 本地测试

```bash
# 安装 Lighthouse CLI
npm install -g lighthouse

# 测试桌面版本
lighthouse https://wiki.mpsteam.cn \
  --output html \
  --output-path ./lighthouse-desktop.html \
  --preset=desktop

# 测试移动版本
lighthouse https://wiki.mpsteam.cn \
  --output html \
  --output-path ./lighthouse-mobile.html \
  --preset=mobile

# 只测试性能
lighthouse https://wiki.mpsteam.cn \
  --only-categories=performance \
  --output json \
  --output-path ./performance.json
```

#### 关键指标目标

| 指标                               | 目标值  | 说明         |
| ---------------------------------- | ------- | ------------ |
| **Performance Score**              | ≥ 90    | 总体性能评分 |
| **FCP (First Contentful Paint)**   | < 1.8s  | 首次内容绘制 |
| **LCP (Largest Contentful Paint)** | < 2.5s  | 最大内容绘制 |
| **TBT (Total Blocking Time)**      | < 200ms | 总阻塞时间   |
| **CLS (Cumulative Layout Shift)**  | < 0.1   | 累积布局偏移 |
| **SI (Speed Index)**               | < 3.4s  | 速度指数     |

### 方法三：WebPageTest

#### 在线测试

1. 访问 [WebPageTest](https://www.webpagetest.org/)
1. 输入网址: `https://wiki.mpsteam.cn`
1. 选择测试位置（推荐选择距离目标用户最近的位置）
1. 设置测试参数：
   - **Connection**: Cable, 4G, 3G 等
   - **Number of Tests to Run**: 3（建议多次测试取平均值）
1. 点击 "Start Test"

#### 关键查看项

**瀑布图 (Waterfall)**:

- 查看资源加载顺序
- 识别阻塞渲染的资源
- 查看是否有串行加载问题

**视频播放 (Filmstrip)**:

- 查看页面加载的视觉进度
- 识别白屏时间
- 查看首屏渲染速度

**Core Web Vitals**:

- LCP: 查看最大内容元素是什么
- FID: 查看首次交互延迟
- CLS: 查看是否有布局偏移

## 性能对比测试

### 优化前后对比

建议使用相同的测试条件进行对比：

1. **清除缓存**: 确保测试一致性
1. **相同网络条件**: 使用相同的网络模拟（如 Fast 3G）
1. **相同设备**: 使用相同的设备类型（桌面/移动）
1. **多次测试**: 至少测试 3 次取平均值

### 记录测试结果

| 指标              | 优化前   | 优化后 | 改进 |
| ----------------- | -------- | ------ | ---- |
| Performance Score | -        | -      | -    |
| LCP               | -        | -      | -    |
| TBT               | -        | -      | -    |
| CLS               | -        | -      | -    |
| INP (实测)        | 14,520ms | -      | -    |

## 实战演练：测试 INP 优化效果

### 步骤 1: 测试优化前 INP

1. 打开 Chrome DevTools
1. 切换到 **Performance** 标签
1. 点击 **Record**
1. 刷新页面
1. **等待 DOMContentLoaded 完成后**，立即点击页面上的链接
1. 停止录制
1. 查看 **Interactions** 部分的延迟时间

### 步骤 2: 应用优化

确认以下文件已更新：

- [x] `docs/assets/extra.js`
- [x] `docs/assets/search-phrase-default.js`
- [x] `docs/assets/giscus-loader.js`

### 步骤 3: 测试优化后 INP

重复步骤 1，对比结果。

### 步骤 4: 分析改进

**期望结果**:

- ✅ 交互延迟从 14,520ms 降低到 < 200ms
- ✅ 主线程在 DOMContentLoaded 后快速空闲
- ✅ 没有长时间阻塞的 JavaScript 任务

## 模拟慢速网络测试

### Chrome DevTools 网络限速

1. 打开 DevTools
1. 切换到 **Network** 标签
1. 点击 **No throttling** 下拉菜单
1. 选择网络速度：
   - **Fast 3G**: 模拟快速移动网络
   - **Slow 3G**: 模拟慢速移动网络
   - **Custom**: 自定义网络速度

### 推荐测试场景

| 场景     | 网络速度 | 用途         |
| -------- | -------- | ------------ |
| 最佳情况 | 无限速   | 基准性能测试 |
| 常见情况 | Fast 3G  | 模拟移动用户 |
| 最坏情况 | Slow 3G  | 压力测试     |

## 持续监控

### 使用 Google Analytics

如果启用了 Google Analytics，可以在 "体验" → "Web Vitals" 中查看真实用户数据：

- **LCP**: 加载性能
- **FID**: 交互性能
- **CLS**: 视觉稳定性

### 使用 Search Console

Google Search Console 提供 Core Web Vitals 报告：

1. 登录 [Search Console](https://search.google.com/search-console)
1. 选择网站
1. 查看 "体验" → "Core Web Vitals"
1. 查看移动端和桌面端的性能数据

### 设置性能预算

在 `lighthouserc.js` 中设置性能预算：

```javascript
module.exports = {
  ci: {
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
  },
};
```

## 故障排除

### INP 仍然很高

**可能原因**:

1. 浏览器扩展干扰 → 使用隐身模式
1. 缓存未清除 → 硬性刷新
1. 设备性能限制 → 使用 CPU 限速测试
1. 第三方脚本阻塞 → 检查 Network 面板

### LCP 不符合预期

**可能原因**:

1. 最大内容元素是大图片 → 优化图片
1. 关键 CSS 未内联 → 检查渲染阻塞资源
1. 字体加载延迟 → 使用系统字体

### CLS 出现波动

**可能原因**:

1. 图片未指定尺寸 → 添加 width/height 属性
1. 动态内容插入 → 为内容预留空间
1. 广告或 iframe → 固定容器尺寸

## 参考资源

- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse CLI](https://github.com/GoogleChrome/lighthouse)
- [Web Vitals](https://web.dev/vitals/)
- [WebPageTest](https://www.webpagetest.org/)
- [PageSpeed Insights](https://pagespeed.web.dev/)

## 更新日志

- 2025-10-16: 创建初始版本
  - 添加 Chrome DevTools 测试指南
  - 添加 Lighthouse CI 使用说明
  - 添加 WebPageTest 测试方法
  - 添加性能对比测试流程
