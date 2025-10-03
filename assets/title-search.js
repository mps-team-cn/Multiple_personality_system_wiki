(function () {
  "use strict";

  const headingIndex = new Map();
  let searchElements = null;
  let indexPromise = null;
  let indexReady = false;
  let latestVM = null;
  let documentClickHandler = null;

  // 注册标题搜索插件，确保 formatUpdated 默认值存在
  function registerPlugin() {
    window.$docsify = window.$docsify || {};
    if (!window.$docsify.formatUpdated) {
      window.$docsify.formatUpdated = "{YYYY}-{MM}-{DD} {HH}:{mm}";
    }
    const originalPlugins = window.$docsify.plugins || [];
    window.$docsify.plugins = [].concat(titleSearchPlugin, originalPlugins);
  }

  // 通过 Docsify 生命周期钩子维护标题索引与交互行为
  function titleSearchPlugin(hook, vm) {
    latestVM = vm;

    hook.ready(function () {
      ensureIndex(vm);
    });

    hook.afterEach(function (html, next) {
      const path = normalizePath(vm.route.path || "");
      headingIndex.set(path, extractHeadingsFromHtml(html));
      next(html);
    });

    hook.mounted(function () {
      ensureSearchElements();
    });

    hook.doneEach(function () {
      ensureSearchElements();
      if (searchElements) {
        searchElements.results.classList.remove("is-open");
      }
    });
  }

  function isMobileLayout() {
    if (typeof window === "undefined") return false;
    if (typeof window.matchMedia === "function") {
      return window.matchMedia("(max-width: 768px)").matches;
    }
    return window.innerWidth <= 768;
  }

  function closeSidebarOnMobile() {
    if (!isMobileLayout()) return;
    const body = document.body;
    if (!body || body.classList.contains("close")) return;

    const toggle = document.querySelector(".sidebar-toggle");
    if (toggle && typeof toggle.click === "function") {
      toggle.click();
      return;
    }
    body.classList.add("close");
  }

  // 构建索引的惰性触发器，避免并发重复执行
  function ensureIndex(vm) {
    if (!indexPromise) {
      indexPromise = buildIndex(vm).finally(function () {
        indexReady = true;
      });
    }
    return indexPromise;
  }

  // 读取首页、索引与侧边栏 Markdown，提取所有标题供搜索使用
  async function buildIndex(vm) {
    const base = resolveBasePath(vm);
    const paths = new Set();

    const homepage = normalizePath(vm.config.homepage || "");
    if (homepage) {
      paths.add(homepage);
    }

    const indexFile = "index.md";
    const normalizedIndex = normalizePath(indexFile);
    if (normalizedIndex) {
      paths.add(normalizedIndex);
      try {
        const indexText = await fetchText(joinUrl(base, indexFile));
        parseSidebarLinks(indexText, paths);
      } catch (error) {
        console.warn("[title-search] 无法加载索引", error);
      }
    }

    const sidebarFile = resolveSidebarFile(vm.config.loadSidebar);
    if (sidebarFile) {
      try {
        const sidebarText = await fetchText(joinUrl(base, sidebarFile));
        parseSidebarLinks(sidebarText, paths);
      } catch (error) {
        console.warn("[title-search] 无法加载侧边栏", error);
      }
    }

    const tasks = Array.from(paths).map(async (path) => {
      try {
        const markdown = await fetchText(joinUrl(base, path));
        headingIndex.set(path, extractHeadingsFromMarkdown(markdown));
      } catch (error) {
        console.warn(`[title-search] 无法索引 ${path}`, error);
      }
    });

    await Promise.all(tasks);
  }

  // 按需在侧边栏插入搜索输入框并绑定交互
  function ensureSearchElements() {
    if (searchElements && searchElements.input.isConnected) {
      return;
    }

    const nav = document.querySelector(".app-nav");
    if (!nav) return;

    const wrapper = document.createElement("div");
    wrapper.className = "title-search title-search--nav";

    const input = document.createElement("input");
    input.type = "search";
    input.className = "title-search__input";
    input.placeholder = "搜索标题…";

    const results = document.createElement("ul");
    results.className = "title-search__results";

    wrapper.appendChild(input);
    wrapper.appendChild(results);

    nav.appendChild(wrapper);

    input.addEventListener("focus", () => {
      ensureIndex(latestVM || {});
      if (input.value.trim()) {
        results.classList.add("is-open");
      }
    });

    input.addEventListener("input", () => {
      renderResults(input.value.trim());
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        input.value = "";
        clearResults();
        input.blur();
      }
    });

    if (!documentClickHandler) {
      documentClickHandler = (event) => {
        if (!searchElements) return;
        if (!searchElements.wrapper.contains(event.target)) {
          searchElements.results.classList.remove("is-open");
        }
      };
      document.addEventListener("click", documentClickHandler);
    }

    searchElements = { wrapper, input, results };
  }

  // 根据关键字匹配标题索引，渲染下拉面板
  function renderResults(keyword) {
    if (!searchElements) return;
    const { results } = searchElements;
    results.innerHTML = "";

    if (!keyword) {
      results.classList.remove("is-open");
      return;
    }

    const normalized = keyword.toLowerCase();

    if (!indexReady) {
      const loadingItem = document.createElement("li");
      loadingItem.className = "title-search__item title-search__item--empty";
      loadingItem.textContent = "正在构建索引…";
      results.appendChild(loadingItem);
      results.classList.add("is-open");
      ensureIndex(latestVM || {});
      indexPromise.finally(() => {
        if (
          searchElements &&
          searchElements.input.value.trim().toLowerCase() === normalized
        ) {
          renderResults(searchElements.input.value.trim());
        }
      });
      return;
    }

    const matches = collectMatches(normalized);

    if (!matches.length) {
      const emptyItem = document.createElement("li");
      emptyItem.className = "title-search__item title-search__item--empty";
      emptyItem.textContent = "没有找到匹配的标题";
      results.appendChild(emptyItem);
      results.classList.add("is-open");
      return;
    }

    matches.forEach((item) => {
      const element = document.createElement("li");
      element.className = "title-search__item";

      const link = document.createElement("a");
      link.className = "title-search__link";
      link.href = toHash(item.path, item.id);
      link.textContent = item.text;
      link.addEventListener("click", () => {
        results.classList.remove("is-open");
        if (searchElements) {
          searchElements.input.blur();
        }
        setTimeout(closeSidebarOnMobile, 0);
      });

      const meta = document.createElement("span");
      meta.className = "title-search__meta";
      meta.textContent = item.pageTitle || item.path;

      element.appendChild(link);
      element.appendChild(meta);
      results.appendChild(element);
    });

    results.classList.add("is-open");
  }

  function clearResults() {
    if (!searchElements) return;
    searchElements.results.innerHTML = "";
    searchElements.results.classList.remove("is-open");
  }

  function collectMatches(keyword) {
    const results = [];

    headingIndex.forEach((entry, path) => {
      if (!entry) return;
      const { pageTitle, headings } = entry;
      headings.forEach((heading) => {
        if (!heading.text) return;
        if (heading.text.toLowerCase().includes(keyword)) {
          results.push({
            path,
            id: heading.id,
            text: heading.text,
            pageTitle,
          });
        }
      });
    });

    results.sort((a, b) => a.text.localeCompare(b.text, "zh-Hans-CN"));

    return results.slice(0, 50);
  }

  function extractHeadingsFromHtml(html) {
    const container = document.createElement("div");
    container.innerHTML = html;
    const nodes = Array.from(
      container.querySelectorAll("h1, h2, h3, h4, h5, h6")
    );

    if (!nodes.length) {
      return { pageTitle: "", headings: [] };
    }

    const headings = nodes.map((node) => ({
      text: node.textContent.trim(),
      id: node.id || "",
      level: Number(node.tagName.slice(1)),
    }));

    const primary = headings.find((item) => item.level === 1);
    const pageTitle = primary ? primary.text : headings[0].text;

    return { pageTitle, headings };
  }

  function extractHeadingsFromMarkdown(markdown) {
    const lines = markdown.split(/\r?\n/);
    const headings = [];
    let pageTitle = "";

    lines.forEach((line) => {
      const match = /^(#{1,6})\s+(.+?)\s*#*\s*$/.exec(line);
      if (!match) return;
      const level = match[1].length;
      const text = match[2].trim();
      if (!text) return;
      const id = slugify(text);
      headings.push({ text, id, level });
      if (!pageTitle && level === 1) {
        pageTitle = text;
      }
    });

    if (!pageTitle && headings.length) {
      pageTitle = headings[0].text;
    }

    return { pageTitle, headings };
  }

  function parseSidebarLinks(markdown, paths) {
    const pattern = /\[[^\]]+\]\(([^)]+)\)/g;
    let match;
    while ((match = pattern.exec(markdown))) {
      const raw = match[1].trim();
      if (!raw) continue;
      if (/^(https?:)?\/\//i.test(raw)) continue;
      if (raw.startsWith("mailto:")) continue;
      const clean = normalizePath(raw);
      if (!clean) continue;
      if (!/\.md$/i.test(clean)) continue;
      paths.add(clean);
    }
  }

  async function fetchText(url) {
    const response = await fetch(url, { cache: "force-cache" });
    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`);
    }
    return response.text();
  }

  function resolveBasePath(vm) {
    const base =
      vm && vm.config && typeof vm.config.basePath === "string"
        ? vm.config.basePath
        : "";
    if (!base) return "";
    return base.endsWith("/") ? base : `${base}/`;
  }

  function resolveSidebarFile(option) {
    if (!option) return null;
    if (typeof option === "string") return option;
    return "_sidebar.md";
  }

  function joinUrl(base, path) {
    if (/^(https?:)?\/\//i.test(path)) return path;
    const sanitized = path.replace(/^\/*/, "");
    if (!base) return sanitized;
    return `${base.replace(/\/?$/, "/")}${sanitized}`;
  }

  function normalizePath(rawPath) {
    if (!rawPath) return "";
    const [pathPart] = rawPath.split(/[?#]/);
    const segments = pathPart.split("/");
    const stack = [];
    segments.forEach((segment) => {
      if (!segment || segment === ".") return;
      if (segment === "..") {
        if (stack.length) stack.pop();
        return;
      }
      stack.push(segment);
    });
    return stack.join("/");
  }

  function slugify(text) {
    if (window.Docsify && typeof window.Docsify.slugify === "function") {
      return window.Docsify.slugify(text);
    }
    return text
      .toLowerCase()
      .trim()
      .replace(/[^\w\u4e00-\u9fa5\s-]/g, "")
      .replace(/\s+/g, "-");
  }

  function toHash(path, id) {
    const cleanPath = normalizePath(path).replace(/\.md$/i, "");
    const base = cleanPath ? `#/${cleanPath}` : "#/";
    if (!id) return base;
    return `${base}?id=${encodeURIComponent(id)}`;
  }

  registerPlugin();
})();
