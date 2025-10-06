# CSS 样式文件管理指南

## 📁 文件结构

```text
docs/assets/
├── extra.css              # 通用样式（当前默认，适用所有主题）
├── extra-material.css     # Material 主题专用增强样式
├── extra-common.css       # 通用样式源文件（备份）
└── extra.js              # 通用 JavaScript 脚本
```

## 🎯 使用策略

### Material 主题（推荐）

**使用文件**: `extra-material.css`

**包含功能**:

- ✅ Material CSS 变量自定义
- ✅ 卡片网格悬停效果
- ✅ 告示框样式增强
- ✅ 深色模式优化
- ✅ 表格美化（Material 风格）
- ✅ 搜索结果优化
- ✅ 导航增强
- ✅ 滚动条美化

**配置**:

```yaml

# mkdocs.yml

extra_css:

  - assets/extra-material.css

```

### ReadTheDocs / MkDocs 默认 / 其他主题

**使用文件**: `extra.css`

**包含功能**:

- ✅ 中文字体优化
- ✅ 基础表格美化
- ✅ 代码块样式
- ✅ 引用块样式
- ✅ 链接样式
- ✅ 打印样式
- ✅ 响应式优化

**配置**:

```yaml

# mkdocs.yml.readthedocs 或 mkdocs.yml.mkdocs

extra_css:

  - assets/extra.css

```

## 🔄 切换主题时的处理

### 自动处理（推荐）

使用预配置的主题文件，CSS 引用已自动设置：

```bash

# 切换到 Material（使用 extra-material.css）

cp mkdocs.yml.material-backup mkdocs.yml

# 切换到 ReadTheDocs（使用 extra.css）

cp mkdocs.yml.readthedocs mkdocs.yml

# 切换到 MkDocs 默认（使用 extra.css）

cp mkdocs.yml.mkdocs mkdocs.yml
```

### 手动调整

如果需要手动调整 CSS 引用：

```yaml

# Material 主题

extra_css:

  - assets/extra-material.css

# 其他主题

extra_css:

  - assets/extra.css

```

## 🔗 标题锚点样式

-**目标**：隐藏 Material 主题默认的段落锚点符号（`¶`），同时保留跳转与键盘焦点能力。
-**实现位置**：`assets/extra-material.css` 与 `assets/extra.css` 均新增 `.headerlink` 规则，统一控制所有主题的标题锚点表现。
-**交互反馈**：默认状态下锚点完全透明，用户在标题上移动或通过键盘聚焦时依旧可以点击，焦点态会出现描边提示，确保无障碍体验。
-**维护建议**：如需恢复默认外观，可删除或注释对应的 `.headerlink` 样式段；若要改用自定义图标，可在同一区块覆盖 `::after` 的内容。

## 📝 自定义样式

### 添加自定义 CSS

1.**不影响现有样式**：在对应文件末尾追加

```css
/* 添加到 extra-material.css 或 extra.css */

/* 自定义样式 */
.my-custom-class {
  color: red;
}
```

2.**创建新的 CSS 文件**：

```bash

# 创建新文件

touch docs/assets/custom.css
```

```yaml

# 在 mkdocs.yml 中引用

extra_css:

  - assets/extra-material.css
  - assets/custom.css  # 你的自定义样式

```

### 覆盖默认样式

使用更高的 CSS 优先级：

```css
/* 使用 !important（谨慎使用）*/
body {
  font-family: "Comic Sans MS" !important;
}

/* 或使用更具体的选择器 */
.md-typeset body {
  font-family: "Comic Sans MS";
}
```

## 🎨 样式定制示例

### 修改主题色

**Material 主题**:

```css
/* extra-material.css */
:root {
  --md-primary-fg-color: #FF6B6B;  /* 红色 */
  --md-accent-fg-color: #4ECDC4;   /* 青色 */
}
```

**通用主题**:

```css
/* extra.css */
a {
  color: #FF6B6B;
}

table thead {
  background-color: rgba(255, 107, 107, 0.1);
}
```

### 修改字体

```css
/* 全局字体 */
body {
  font-family: "思源黑体", "Source Han Sans", sans-serif;
}

/* 代码字体 */
code, pre {
  font-family: "Fira Code", "Cascadia Code", monospace;
}
```

### 调整间距

```css
/* 增加段落间距 */
p {
  margin: 1.5rem 0;
}

/* 调整标题间距 */
h2 {
  margin-top: 3rem;
  margin-bottom: 1rem;
}
```

## ⚠️ 注意事项

### Material 专用样式不适用于其他主题

`extra-material.css` 中使用了 Material 特定的：

- CSS 变量（`--md-*`）
- 类名（`.md-*`）
- 组件选择器

这些在其他主题中**不会生效**，需要使用通用的 CSS 选择器。

### 避免样式冲突

1.**不要同时引用两个样式文件**：

```yaml

# ❌ 错误：可能导致样式冲突

extra_css:

  - assets/extra-material.css
  - assets/extra.css

# ✅ 正确：根据主题选择一个

extra_css:

  - assets/extra-material.css  # 仅 Material

```

2.**使用特定的类名前缀**：

```css
/* 自定义样式使用前缀避免冲突 */
.pw-custom-button {  /* pw = Plurality Wiki */
  /* ... */
}
```

### 浏览器兼容性

某些现代 CSS 特性可能不支持旧浏览器：

- `color-mix()` - 需要较新浏览器
- CSS 变量 - IE11 不支持
- `backdrop-filter` - 部分浏览器不支持

如需兼容旧浏览器，使用 fallback：

```css
/* Fallback 示例 */
.box {
  background-color: #4FC08D;  /* 旧浏览器 */
  background-color: color-mix(in srgb, #4FC08D 80%, transparent);  /* 新浏览器 */
}
```

## 📊 样式对比

| 特性 | extra-material.css | extra.css |
|------|-------------------|-----------|
| Material 变量 | ✅ | ❌ |
| 卡片网格增强 | ✅ | ❌ |
| 告示框增强 | ✅ | ❌ |
| 深色模式优化 | ✅ | ❌ |
| 中文字体优化 | ✅ | ✅ |
| 表格美化 | ✅ | ✅ |
| 代码块样式 | ✅ | ✅ |
| 打印样式 | ✅ | ✅ |
| 响应式优化 | ✅ | ✅ |
| 通用主题兼容 | ❌ | ✅ |

## 🔍 调试 CSS

### 检查样式是否加载

1. 打开浏览器开发者工具（F12）
2. 进入 Network 标签
3. 刷新页面
4. 查找 `extra-material.css` 或 `extra.css`
5. 确认 Status 为 200

### 检查样式是否生效

1. 右键点击元素 → 检查
2. 查看 Computed 标签
3. 确认样式来源

### 常见问题

**样式没有生效**：

- 检查文件路径是否正确
- 清除浏览器缓存（Ctrl + Shift + R）
- 检查 CSS 选择器是否正确

**主题色没有改变**：

- Material 主题：检查 `mkdocs.yml` 中的 `theme.palette` 配置
- 通用主题：检查 CSS 变量或直接样式

**深色模式样式错误**：

- Material：使用 `[data-md-color-scheme="slate"]` 选择器
- 通用：使用 `@media (prefers-color-scheme: dark)` 媒体查询

## 📚 参考资源

-**Material CSS 变量**: [https://squidfunk.github.io/mkdocs-material/customization/#css-variables](https://squidfunk.github.io/mkdocs-material/customization/#css-variables)
-**MDN CSS 文档**: [https://developer.mozilla.org/zh-CN/docs/Web/CSS](https://developer.mozilla.org/zh-CN/docs/Web/CSS)
-**Can I Use**: [https://caniuse.com/](https://caniuse.com/) (检查 CSS 兼容性)

---

**最后更新**: 2025-10-05
