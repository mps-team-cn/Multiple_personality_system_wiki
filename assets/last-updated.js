(function () {
  "use strict";

  const cache = new Map();
  const CLASS_NAME = "last-updated-indicator";

  function registerPlugin() {
    window.$docsify = window.$docsify || {};
    if (!window.$docsify.formatUpdated) {
      window.$docsify.formatUpdated = "{YYYY}-{MM}-{DD} {HH}:{mm}";
    }
    const originalPlugins = window.$docsify.plugins || [];
    window.$docsify.plugins = [].concat(lastUpdatedPlugin, originalPlugins);
  }

  function lastUpdatedPlugin(hook, vm) {
    hook.beforeEach(function (content, next) {
      resolveLastModified(vm)
        .then(function (date) {
          vm.route.updated = date instanceof Date ? date : undefined;
        })
        .finally(function () {
          next(content);
        });
    });

    hook.doneEach(function () {
      renderLastUpdated(vm);
    });
  }

  function resolveLastModified(vm) {
    const file = vm.route && vm.route.file ? vm.route.file : resolveDefaultFile(vm);
    if (!file) return Promise.resolve(null);

    const base = vm.config && vm.config.basePath ? vm.config.basePath : "";
    const url = buildFileUrl(base, file);
    if (!url) return Promise.resolve(null);

    if (cache.has(url)) {
      return cache.get(url);
    }

    const promise = fetch(url, { method: "HEAD", cache: "no-store" })
      .then(function (response) {
        if (!response || !response.ok) return null;
        const header = response.headers ? response.headers.get("last-modified") : null;
        if (!header) return null;
        const parsed = new Date(header);
        return Number.isNaN(parsed.getTime()) ? null : parsed;
      })
      .catch(function () {
        return null;
      });

    cache.set(url, promise);
    return promise;
  }

  function resolveDefaultFile(vm) {
    const homepage = vm.config && vm.config.homepage ? vm.config.homepage : null;
    if (homepage) return homepage;
    return "README.md";
  }

  function buildFileUrl(basePath, filePath) {
    if (/^[a-zA-Z]+:\/\//.test(filePath) || filePath.startsWith("//")) {
      return filePath;
    }

    if (!basePath) {
      return filePath;
    }

    if (/^[a-zA-Z]+:\/\//.test(basePath) || basePath.startsWith("//")) {
      try {
        return new URL(filePath.replace(/^\//, ""), ensureTrailingSlash(basePath)).toString();
      } catch (error) {
        console.warn("[last-updated] 无法解析 URL", error);
        return filePath;
      }
    }

    const normalizedBase = ensureTrailingSlash(basePath);
    const normalizedFile = filePath.replace(/^\//, "");
    return normalizedBase + normalizedFile;
  }

  function ensureTrailingSlash(input) {
    return input.endsWith("/") ? input : input + "/";
  }

  function renderLastUpdated(vm) {
    const container = ensureContainer();
    if (!container) return;

    const value = vm.route && vm.route.updated instanceof Date ? vm.route.updated : null;
    const format = vm.config && vm.config.formatUpdated
      ? vm.config.formatUpdated
      : "{YYYY}-{MM}-{DD} {HH}:{mm}";

    container.textContent = value
      ? "最后更新：" + formatDate(value, format)
      : "最后更新：暂无记录";
  }

  function ensureContainer() {
    const contentRoot = document.querySelector(".content");
    if (!contentRoot) return null;

    let container = contentRoot.querySelector("." + CLASS_NAME);
    if (!container) {
      container = document.createElement("div");
      container.className = CLASS_NAME;
      container.style.cssText =
        "color:#999;font-size:12px;text-align:right;margin-top:1.5em;";
      contentRoot.appendChild(container);
    }

    return container;
  }

  function formatDate(date, template) {
    const map = {
      YYYY: date.getFullYear(),
      MM: pad(date.getMonth() + 1),
      DD: pad(date.getDate()),
      HH: pad(date.getHours()),
      mm: pad(date.getMinutes()),
      ss: pad(date.getSeconds()),
    };

    return template.replace(/\{(YYYY|MM|DD|HH|mm|ss)\}/g, function (_, token) {
      return map[token];
    });
  }

  function pad(value) {
    return String(value).padStart(2, "0");
  }

  registerPlugin();
})();
