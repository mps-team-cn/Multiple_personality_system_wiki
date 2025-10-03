(function () {
  "use strict";

  var SITE_SUFFIX = " - Plurality Wiki";
  var HOMEPAGE_TITLE = "首页";

  // 将标题后缀插件注册进 Docsify，保持原有插件顺序
  function registerPlugin() {
    window.$docsify = window.$docsify || {};
    var originalPlugins = window.$docsify.plugins || [];
    window.$docsify.plugins = [].concat(titleSuffixPlugin, originalPlugins);
  }

  // 在首次挂载与路由切换后刷新页面标题
  function titleSuffixPlugin(hook, vm) {
    hook.mounted(function () {
      updateTitle(vm);
    });

    hook.doneEach(function () {
      updateTitle(vm);
    });
  }

  // 读取当前路由标题并附加站点后缀
  function updateTitle(vm) {
    document.title = appendSuffix(resolvePageTitle(vm));
  }

  // 保证标题存在且仅追加一次站点名称
  function appendSuffix(title) {
    var base = (title || "").trim();
    if (!base) {
      base = "Plurality Wiki";
    }
    if (base.endsWith(SITE_SUFFIX)) {
      return base;
    }
    return base + SITE_SUFFIX;
  }

  // 根据当前路由、文档结构和路径推断最合适的标题
  function resolvePageTitle(vm) {
    var route = vm && vm.route ? vm.route : {};
    var file = route.file || "";
    var homepage = vm && vm.config ? vm.config.homepage : null;

    if (isHomepageRoute(file, homepage, route)) {
      return HOMEPAGE_TITLE;
    }

    var section = document.querySelector(".markdown-section");
    if (section) {
      var heading = section.querySelector("h1, h2, h3, h4, h5, h6");
      if (heading) {
        var text = heading.textContent.trim();
        if (text) {
          return text;
        }
      }
    }

    if (route && typeof route.title === "string" && route.title.trim()) {
      return route.title.trim();
    }

    if (route && typeof route.path === "string" && route.path) {
      return extractNameFromPath(route.path);
    }

    return "Plurality Wiki";
  }

  // 判断当前路由是否首页，用于返回固定标题
  function isHomepageRoute(file, homepage, route) {
    if (homepage && filesEqual(file, homepage)) {
      return true;
    }

    if (!file && homepage) {
      return true;
    }

    var path = route && route.path ? route.path : "";
    if (!path || path === "/" || path === "#" || path === "#/") {
      return true;
    }

    return false;
  }

  // 从路径末尾提取文件名，兼容编码与后缀
  function extractNameFromPath(path) {
    var clean = String(path || "");
    clean = clean.replace(/^#?\/+/, "");
    var parts = clean.split(/[?#]/)[0].split("/");
    var last = parts.pop() || "";
    var decoded = decodeURIComponent(last);
    return decoded.replace(/\.(md|markdown|html)$/i, "").trim() || "Plurality Wiki";
  }

  // 对比两个文件名是否等价，忽略大小写与起始斜杠
  function filesEqual(a, b) {
    return normalizeFile(a) === normalizeFile(b);
  }

  // 标准化文件路径，供比较使用
  function normalizeFile(input) {
    return String(input || "")
      .replace(/^\/+/, "")
      .replace(/\\/g, "/")
      .toLowerCase();
  }

  registerPlugin();
})();
