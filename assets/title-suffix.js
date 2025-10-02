(function () {
  "use strict";

  var SITE_SUFFIX = " - Plurality Wiki";
  var HOMEPAGE_TITLE = "首页";

  function registerPlugin() {
    window.$docsify = window.$docsify || {};
    var originalPlugins = window.$docsify.plugins || [];
    window.$docsify.plugins = [].concat(titleSuffixPlugin, originalPlugins);
  }

  function titleSuffixPlugin(hook, vm) {
    hook.mounted(function () {
      updateTitle(vm);
    });

    hook.doneEach(function () {
      updateTitle(vm);
    });
  }

  function updateTitle(vm) {
    document.title = appendSuffix(resolvePageTitle(vm));
  }

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

  function extractNameFromPath(path) {
    var clean = String(path || "");
    clean = clean.replace(/^#?\/+/, "");
    var parts = clean.split(/[?#]/)[0].split("/");
    var last = parts.pop() || "";
    var decoded = decodeURIComponent(last);
    return decoded.replace(/\.(md|markdown|html)$/i, "").trim() || "Plurality Wiki";
  }

  function filesEqual(a, b) {
    return normalizeFile(a) === normalizeFile(b);
  }

  function normalizeFile(input) {
    return String(input || "")
      .replace(/^\/+/, "")
      .replace(/\\/g, "/")
      .toLowerCase();
  }

  registerPlugin();
})();
