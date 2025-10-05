/**
 * Plurality Wiki 前端初始化模块
 * 整合所有核心模块,提供统一的初始化接口
 */
(function (window) {
  "use strict";

  const PluralityApp = {
    /**
     * 初始化应用
     * @param {object} options - 配置选项
     */
    init(options = {}) {
      // 1. 创建并应用 Docsify 配置
      const config = PluralityConfig.createConfig(options);
      PluralityConfig.apply(config);

      // 2. 初始化路由管理器
      PluralityRouter.init({
        basePath: config.basePath,
      });

      // 3. 注册核心插件
      this.registerCorePlugins();

      // 4. 初始化主题切换器
      this.themeToggler = PluralityPluginManager.createThemeToggler();
      window.toggleTheme = () => this.themeToggler.toggle();

      // 5. 初始化侧边栏管理器
      this.sidebarManager = PluralityPluginManager.createSidebarManager();

      // 6. 应用所有插件
      PluralityPluginManager.apply();

      return this;
    },

    /**
     * 注册核心插件
     */
    registerCorePlugins() {
      // 注册最后更新时间插件
      const lastUpdatedPlugin =
        PluralityPluginManager.createLastUpdatedPlugin({
          placeholderId: "__last-updated__",
          dataUrl: "./assets/last-updated.json",
        });

      PluralityPluginManager.register(lastUpdatedPlugin, 10);
    },

    /**
     * 获取主题切换器
     * @returns {object} 主题切换器对象
     */
    getThemeToggler() {
      return this.themeToggler;
    },

    /**
     * 获取侧边栏管理器
     * @returns {object} 侧边栏管理器对象
     */
    getSidebarManager() {
      return this.sidebarManager;
    },
  };

  // 导出到全局
  window.PluralityApp = PluralityApp;
})(window);
