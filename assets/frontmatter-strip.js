(function () {
  "use strict";

  // Docsify 默认不会解析 frontmatter，本插件负责在渲染前移除这部分元数据
  function stripFrontmatter(raw) {
    if (typeof raw !== "string") return raw;
    if (!/^---\s*\n/.test(raw)) return raw;

    const lines = raw.split(/\r?\n/);
    let closingIndex = -1;

    for (let index = 1; index < lines.length; index += 1) {
      if (/^---\s*$/.test(lines[index])) {
        closingIndex = index;
        break;
      }
    }

    if (closingIndex === -1) return raw;

    const bodyLines = lines.slice(closingIndex + 1);

    while (bodyLines.length && bodyLines[0].trim() === "") {
      bodyLines.shift();
    }

    return bodyLines.join("\n");
  }

  function frontmatterStripPlugin(hook) {
    hook.beforeEach(function (content, next) {
      next(stripFrontmatter(content));
    });
  }

  function registerPlugin() {
    window.$docsify = window.$docsify || {};
    const existing = window.$docsify.plugins || [];
    window.$docsify.plugins = [].concat(frontmatterStripPlugin, existing);
  }

  registerPlugin();
})();
