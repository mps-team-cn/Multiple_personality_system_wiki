/**
 * 插件管理器
 * 统一管理 Docsify 插件的注册和生命周期
 */
(function (window) {
  "use strict";

  const PluralityPluginManager = {
    plugins: [],

    /**
     * 注册插件
     * @param {Function} plugin - 插件函数
     * @param {number} priority - 优先级 (数字越小优先级越高)
     */
    register(plugin, priority = 50) {
      if (typeof plugin !== "function") {
        console.error("插件必须是函数");
        return;
      }

      this.plugins.push({ plugin, priority });
      this.plugins.sort((a, b) => a.priority - b.priority);
    },

    /**
     * 应用所有插件到 Docsify
     */
    apply() {
      window.$docsify = window.$docsify || {};
      const existingPlugins = window.$docsify.plugins || [];

      window.$docsify.plugins = []
        .concat(this.plugins.map((p) => p.plugin))
        .concat(existingPlugins);
    },

    /**
     * 创建最后更新时间插件
     * @param {object} options - 配置选项
     * @returns {Function} 插件函数
     */
    createLastUpdatedPlugin(options = {}) {
      const PLACEHOLDER_ID = options.placeholderId || "__last-updated__";
      const DATA_URL = options.dataUrl || "./assets/last-updated.json";

      let lastUpdatedMapPromise = null;

      function loadMap() {
        if (!lastUpdatedMapPromise) {
          lastUpdatedMapPromise = PluralityUtils.fetch
            .createCachedFetcher(DATA_URL)();
        }
        return lastUpdatedMapPromise;
      }

      function injectPlaceholder(html) {
        const placeholder = `\n<div id="${PLACEHOLDER_ID}" style="font-size:0.9em;opacity:.8;margin:8px 0;"></div>`;
        if (/<h1[^>]*>[\s\S]*?<\/h1>/i.test(html)) {
          return html.replace(/(<h1[^>]*>[\s\S]*?<\/h1>)/i, `$1${placeholder}`);
        }
        return `${placeholder}\n${html}`;
      }

      return function (hook, vm) {
        hook.afterEach(function (html, next) {
          next(injectPlaceholder(html));
        });

        hook.doneEach(async function () {
          const container = document.getElementById(PLACEHOLDER_ID);
          if (!container) return;

          const repoPath = PluralityUtils.path.routeToRepoPath(
            vm.route && vm.route.path
          );
          const map = await loadMap();
          const info = repoPath && map[repoPath];

          if (info && info.updated) {
            const formatted = PluralityUtils.datetime.formatDate(info.updated);
            const shortHash = info.commit ? info.commit.slice(0, 7) : "";
            if (formatted) {
              container.innerHTML = `🕒 最后更新：<strong>${formatted}</strong>${
                shortHash ? `（<code>${shortHash}</code>）` : ""
              }`;
              container.style.display = "";
              return;
            }
          }

          container.innerHTML = "";
          container.style.display = "none";
        });
      };
    },

    /**
     * 创建暗黑模式切换器
     * @param {object} options - 配置选项
     * @returns {object} 切换器对象
     */
    createThemeToggler(options = {}) {
      const key = options.storageKey || "theme-dark";
      const root = document.documentElement;

      // 初始化主题
      const saved = localStorage.getItem(key);
      if (saved === "1") root.classList.add("dark");

      return {
        toggle() {
          root.classList.toggle("dark");
          localStorage.setItem(
            key,
            root.classList.contains("dark") ? "1" : "0"
          );
        },
        isDark() {
          return root.classList.contains("dark");
        },
        setDark(isDark) {
          if (isDark) {
            root.classList.add("dark");
            localStorage.setItem(key, "1");
          } else {
            root.classList.remove("dark");
            localStorage.setItem(key, "0");
          }
        },
      };
    },

    /**
     * 创建移动端侧边栏管理器
     * @returns {object} 侧边栏管理器对象
     */
    createSidebarManager() {
      return {
        isMobile() {
          return PluralityUtils.device.isMobile();
        },
        close() {
          if (!this.isMobile()) return;
          const body = document.body;
          if (!body || body.classList.contains("close")) return;

          const toggle = document.querySelector(".sidebar-toggle");
          if (toggle && typeof toggle.click === "function") {
            toggle.click();
            return;
          }
          body.classList.add("close");
        },
      };
    },
  };

  // 导出到全局
  window.PluralityPluginManager = PluralityPluginManager;
})(window);
