/**
 * 路由管理模块
 * 处理 Docsify 的路由规范化和链接拦截
 */
(function (window) {
  "use strict";

  const PluralityRouter = {
    /**
     * 初始化路由管理器
     * @param {object} config - 配置对象
     * @param {string} config.basePath - 基础路径
     */
    init(config = {}) {
      this.config = config;
      this.setupHashCanonicalizer();
      this.setupLinkInterceptor();
    },

    /**
     * 设置 hash 规范化处理
     */
    setupHashCanonicalizer() {
      const canonicalizeHash = (() => {
        let adjusting = false;

        const updateHash = (hash, notifyRouter) => {
          const { origin, pathname, search } = window.location;
          const newUrl = `${origin}${pathname}${search}${hash}`;

          adjusting = true;
          history.replaceState(null, "", newUrl);

          if (notifyRouter) {
            const event =
              typeof HashChangeEvent === "function"
                ? new HashChangeEvent("hashchange")
                : new Event("hashchange");
            window.dispatchEvent(event);
          }

          adjusting = false;
        };

        return (notifyRouter = false) => {
          if (adjusting) return;

          const { hash } = window.location;
          if (!hash || !hash.startsWith("#/")) return;

          const normalizedPath = PluralityUtils.path.normalizePath(
            hash.slice(2)
          );
          const normalizedHash = `#/${normalizedPath}`;

          if (normalizedHash !== hash) {
            updateHash(normalizedHash, notifyRouter);
          }
        };
      })();

      window.addEventListener("hashchange", () => canonicalizeHash(true), true);
      canonicalizeHash();

      this.canonicalizeHash = canonicalizeHash;
    },

    /**
     * 设置链接拦截处理
     */
    setupLinkInterceptor() {
      const self = this;

      document.addEventListener("click", (event) => {
        const anchor = event.target.closest("a[href]");
        if (!anchor) return;
        if (
          anchor.target &&
          anchor.target !== "" &&
          anchor.target !== "_self"
        )
          return;

        const href = anchor.getAttribute("href");
        if (!PluralityUtils.link.shouldHandleInternally(href)) return;

        event.preventDefault();

        const target = PluralityUtils.path.resolveTarget(
          href,
          self.config.basePath,
          window.location
        );
        const normalized = PluralityUtils.path.normalizePath(target);
        const cleanPath = normalized.replace(/\.md(?=$|\?)/i, "");
        const newHash = `#/${cleanPath}`;

        if (window.location.hash !== newHash) {
          window.location.hash = newHash;
        } else {
          self.canonicalizeHash(true);
        }
      });
    },

    /**
     * 获取别名配置
     * @returns {object} 别名映射对象
     */
    getAliasConfig() {
      return {
        "/.*/_navbar.md": "_navbar.md",
        "/.*/_sidebar.md": "_sidebar.md",
      };
    },
  };

  // 导出到全局
  window.PluralityRouter = PluralityRouter;
})(window);
