/**
 * Docsify 配置模块
 * 集中管理 Docsify 的所有配置选项
 */
(function (window) {
  "use strict";

  const PluralityConfig = {
    /**
     * 创建 Docsify 配置
     * @param {object} options - 自定义配置选项
     * @returns {object} Docsify 配置对象
     */
    createConfig(options = {}) {
      const { pathname } = window.location;
      const basePath = PluralityUtils.path.ensureTrailingSlash(
        pathname.replace(/[^/]*$/, "")
      );

      return {
        name: options.name || "多意识体Wikipedia",
        repo: options.repo || "kuliantnt/plurality_wiki",
        basePath,

        // 导航/侧边
        loadNavbar: true,
        loadSidebar: true,
        subMaxLevel: 2,
        auto2top: true,

        // 首页直接展示 Main_Page(HTML 版本),无需封面
        coverpage: false,
        onlyCover: false,
        homepage: options.homepage || "Main_Page.html",

        // 自定义 404 页面
        notFoundPage: "_404.md",

        // 页脚
        footer: {
          copy:
            "<span>© " + new Date().getFullYear() + " plurality_wiki</span>",
          auth: "由 脸脸系统 编写",
          pre: "<hr/>",
          style: "text-align:center;",
        },

        // 分页
        pagination: {
          previousText: "上一页",
          nextText: "下一页",
          crossChapter: true,
        },

        // 别名
        alias: PluralityRouter.getAliasConfig(),

        // 格式化更新时间
        formatUpdated: "{YYYY}-{MM}-{DD} {HH}:{mm}",
      };
    },

    /**
     * 应用配置到 Docsify
     * @param {object} config - 配置对象
     */
    apply(config) {
      window.$docsify = Object.assign(window.$docsify || {}, config);
    },
  };

  // 导出到全局
  window.PluralityConfig = PluralityConfig;
})(window);
