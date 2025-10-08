# 前端架构说明

本文档说明 Multiple personality system Wiki 前端的模块化架构设计。

## 概述

前端采用模块化设计，将原本内联在 `index.html` 中的 200+ 行 JavaScript 代码重构为清晰的模块化结构，提高代码的可维护性和可扩展性。

## 核心模块

所有核心模块位于 `assets/core/` 目录下：

### 1. utils.js - 核心工具函数库

提供前端各模块共用的工具函数，包括：

- **路径处理** (`PluralityUtils.path`)

  - `ensureTrailingSlash(path)` - 确保路径以斜杠结尾
  - `normalizePath(raw)` - 规范化路径，移除 `./` 和 `..` 片段
  - `resolveTarget(href, basePath, currentLocation)` - 解析目标路径，处理相对路径和锚点
  - `toRoutePath(filePath)` - 将文件路径转换为路由路径
  - `routeToRepoPath(routePath)` - 将路由路径转换为仓库路径

- **日期时间** (`PluralityUtils.datetime`)

  - `formatDate(isoString, format)` - 格式化 ISO 日期字符串

- **HTML 处理** (`PluralityUtils.html`)

  - `escape(value)` - HTML 转义
  - `extractHeadings(html)` - 从 HTML 中提取标题

- **文本处理** (`PluralityUtils.text`)

  - `normalize(text)` - 规范化文本，移除多余空白
  - `fallbackTitle(path)` - 从路径提取回退标题

- **数据获取** (`PluralityUtils.fetch`)

  - `createCachedFetcher(url)` - 创建带缓存的数据获取函数
  - `loadMarkdown(path)` - 加载 Markdown 文件

- **链接判断** (`PluralityUtils.link`)

  - `shouldHandleInternally(href)` - 判断是否应该内部处理链接

- **设备检测** (`PluralityUtils.device`)

  - `isMobile()` - 检测是否为移动端布局

### 2. router.js - 路由管理模块

负责处理 Docsify 的路由规范化和链接拦截：

- **PluralityRouter.init(config)** - 初始化路由管理器
- **PluralityRouter.setupHashCanonicalizer()** - 设置 hash 规范化处理
- **PluralityRouter.setupLinkInterceptor()** - 设置链接拦截处理
- **PluralityRouter.getAliasConfig()** - 获取别名配置

### 3. plugin-manager.js - 插件管理器

统一管理 Docsify 插件的注册和生命周期：

- **PluralityPluginManager.register(plugin, priority)** - 注册插件（支持优先级）
- **PluralityPluginManager.apply()** - 应用所有插件到 Docsify
- **PluralityPluginManager.createLastUpdatedPlugin(options)** - 创建最后更新时间插件
- **PluralityPluginManager.createThemeToggler(options)** - 创建暗黑模式切换器
- **PluralityPluginManager.createSidebarManager()** - 创建侧边栏管理器

### 4. config.js - Docsify 配置模块

集中管理 Docsify 的所有配置选项：

- **PluralityConfig.createConfig(options)** - 创建 Docsify 配置
- **PluralityConfig.apply(config)** - 应用配置到 Docsify

### 5. init.js - 应用初始化模块

整合所有核心模块，提供统一的初始化接口：

- **PluralityApp.init(options)** - 初始化应用
- **PluralityApp.registerCorePlugins()** - 注册核心插件
- **PluralityApp.getThemeToggler()** - 获取主题切换器
- **PluralityApp.getSidebarManager()** - 获取侧边栏管理器

## 功能插件

位于 `assets/` 目录的独立功能插件：

- **title-search.js** - 标题搜索功能
- **title-suffix.js** - 页面标题后缀控制
- **typography.js** - 中英混排排版优化
- **table-responsive.js** - 表格响应式卡片化
- **frontmatter-strip.js** - Frontmatter 移除
- **recent-home.js** - 首页最近更新模块
- **recent-page.js** - 最近更新页面自动生成

## 使用方式

### 在 index.html 中初始化

```html
<!-- 核心模块 -->
<script src="./assets/core/utils.js"></script>
<script src="./assets/core/router.js"></script>
<script src="./assets/core/plugin-manager.js"></script>
<script src="./assets/core/config.js"></script>
<script src="./assets/core/init.js"></script>

<!-- 初始化应用 -->
<script>
  (function () {
    PluralityApp.init({
      name: "多重人格系统Wikipedia",
      repo: "mps-team-cn/Multiple_personality_system_wiki",
      homepage: "Main_Page.html",
    });
  })();
</script>
```

### 在插件中使用工具函数

```javascript
// 使用路径工具
const routePath = PluralityUtils.path.toRoutePath("entries/example.md");

// 使用日期格式化
const formatted = PluralityUtils.datetime.formatDate(isoString);

// 使用 HTML 转义
const safe = PluralityUtils.html.escape(userInput);
```

### 注册自定义插件

```javascript
// 创建插件函数
function myPlugin(hook, vm) {
  hook.doneEach(function () {
    // 插件逻辑
  });
}

// 注册插件（优先级：数字越小优先级越高）
PluralityPluginManager.register(myPlugin, 30);
```

## 架构优势

### 1. 模块化

- 代码按功能划分为独立模块
- 每个模块职责单一、边界清晰
- 便于理解和维护

### 2. 可复用性

- 工具函数可在多个插件间共享
- 减少代码重复
- 提高开发效率

### 3. 可扩展性

- 插件管理器支持优先级控制
- 易于添加新功能模块
- 不影响现有代码

### 4. 可维护性

- 集中管理配置
- 统一的初始化流程
- 清晰的依赖关系

### 5. 向后兼容

- 保持所有现有功能不变
- 平滑迁移，无需修改现有插件
- 支持渐进式重构

## 开发指南

### 添加新工具函数

在 `assets/core/utils.js` 的 `PluralityUtils` 对象中添加：

```javascript
const PluralityUtils = {
  // 现有工具...

  // 添加新的工具分类
  myCategory: {
    myFunction(param) {
      // 实现
    }
  }
};
```

### 创建新插件

1. 在 `assets/` 目录创建插件文件
2. 使用 IIFE 模式封装
3. 通过 `PluralityPluginManager.register()` 注册
4. 在 `index.html` 中引入

```javascript
(function () {
  "use strict";

  function myPlugin(hook, vm) {
    // 使用工具函数
    const utils = PluralityUtils;

    hook.doneEach(function () {
      // 插件逻辑
    });
  }

  // 注册插件
  PluralityPluginManager.register(myPlugin, 50);
})();
```

### 修改配置

在 `PluralityApp.init()` 调用时传入配置选项：

```javascript
PluralityApp.init({
  name: "站点名称",
  repo: "github-repo",
  homepage: "首页文件",
  // 其他选项...
});
```

## 迁移说明

### 从旧版本迁移

1. **备份原文件**

   ```bash
   cp index.html index.html.old
   ```

2. **替换 index.html**

   - 使用新的模块化版本

3. **测试功能**

   - 启动本地服务器
   - 验证所有功能正常

4. **逐步优化现有插件**

   - 使用 `PluralityUtils` 替换重复代码
   - 通过 `PluralityPluginManager` 统一注册

## 注意事项

1. **加载顺序**

   - 核心模块必须在功能插件之前加载
   - `init.js` 必须最后加载

2. **全局对象**

   - 所有核心模块导出到全局命名空间
   - 避免与其他库冲突

3. **向后兼容**

   - 现有插件无需立即修改
   - 可渐进式采用新工具函数

## 故障排查

### 常见问题

**Q: 页面无法加载**

- 检查核心模块文件路径是否正确
- 确认加载顺序正确

**Q: 插件不工作**

- 检查插件是否正确注册
- 确认插件在 Docsify 核心之前加载

**Q: 路由不正常**

- 检查 `PluralityRouter.init()` 是否被调用
- 确认 basePath 配置正确

## 更新日志

### v2.2.0 (2025-10-05)

- ✨ 完成前端模块化重构
- 📦 创建核心工具模块系统
- 🔧 统一插件管理机制
- 📝 添加架构文档

## 参考资料

- [Docsify 官方文档](https://docsify.js.org/)
- [项目 AGENTS.md](../../AGENTS.md)
- [工具文档](../../tools/README.md)
