# 性能优化 Pull Request

## 优化类型

请勾选适用的优化类型：

- [ ] JavaScript 性能优化
- [ ] CSS 性能优化
- [ ] 资源加载优化
- [ ] 第三方脚本优化
- [ ] 图片优化
- [ ] 字体优化
- [ ] 其他（请说明）

## 优化描述

### 问题描述

简要描述发现的性能问题：

- 影响的指标：LCP / FID / INP / CLS / TBT / 其他
- 问题严重程度：严重 / 中等 / 轻微
- 影响范围：全站 / 特定页面 / 特定功能

### 解决方案

描述实施的优化方案：

1.
2.
3.

### 技术细节

涉及的技术手段（如适用）：

- [ ] 事件委托 (Event Delegation)
- [ ] requestIdleCallback / requestAnimationFrame
- [ ] Intersection Observer
- [ ] 延迟加载 (Lazy Loading)
- [ ] 代码分割 (Code Splitting)
- [ ] 缓存优化
- [ ] 其他（请说明）

## 性能测试结果

### 优化前

| 指标 | 数值 | 截图/链接 |
|-----|------|----------|
| Performance Score | | |
| LCP | | |
| FID / INP | | |
| TBT | | |
| CLS | | |

### 优化后

| 指标 | 数值 | 截图/链接 |
|-----|------|----------|
| Performance Score | | |
| LCP | | |
| FID / INP | | |
| TBT | | |
| CLS | | |

### 改进幅度

| 指标 | 改进 | 达标情况 |
|-----|------|---------|
| Performance Score | +X 分 | ✅ / ❌ |
| LCP | -Xms | ✅ / ❌ |
| FID / INP | -Xms | ✅ / ❌ |
| TBT | -Xms | ✅ / ❌ |
| CLS | -X | ✅ / ❌ |

## 测试清单

请确认以下测试已完成：

### 功能测试

- [ ] 优化后功能正常工作
- [ ] 没有引入新的 bug
- [ ] 降级方案测试通过（旧浏览器兼容性）
- [ ] 移动端测试通过

### 性能测试

- [ ] Chrome DevTools Performance 测试
- [ ] Lighthouse CI 测试（桌面 + 移动）
- [ ] 慢速网络测试（Fast 3G / Slow 3G）
- [ ] 多次测试取平均值

### 浏览器兼容性

- [ ] Chrome (最新版本)
- [ ] Firefox (最新版本)
- [ ] Safari (最新版本)
- [ ] Edge (最新版本)
- [ ] 移动浏览器（iOS Safari / Chrome Mobile）

## 风险评估

### 潜在风险

描述优化可能带来的风险：

- 兼容性风险：
- 功能影响：
- 回退方案：

### 回滚计划

如果优化导致问题，如何快速回滚：

1.
2.
3.

## 文档更新

- [ ] 更新了 [Performance-Optimization.md](../docs/dev/Performance-Optimization.md)
- [ ] 更新了相关技术文档
- [ ] 添加了必要的代码注释

## 相关链接

- Issue: #
- 相关 PR: #
- Lighthouse 报告:
- WebPageTest 报告:

## 审查要点

请审查者特别关注：

1.
2.
3.

## 额外说明

（可选）其他需要说明的内容：

---

## Checklist

提交前请确认：

- [ ] 已阅读 [性能优化指南](../docs/dev/Performance-Optimization.md)
- [ ] 已完成所有性能测试
- [ ] 已更新相关文档
- [ ] 已在本地验证功能正常
- [ ] 已测试浏览器兼容性
- [ ] 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/)
