(function () {
  const DATA_URL = "./assets/last-updated.json";
  const LIMIT = 3;
  const CARD_SELECTOR = ".js-recent-home";
  const LIST_SELECTOR = ".js-recent-home-list";
  const STATE_ATTR = "data-recent-home-initialized";

  let updatesPromise = null;
  const titleCache = new Map();

  // 从 last-updated.json 拉取最近更新数据，并复用同一 Promise 防止重复请求
  function fetchUpdates() {
    if (!updatesPromise) {
      updatesPromise = fetch(DATA_URL, { cache: "no-store" })
        .then((response) => (response.ok ? response.json() : {}))
        .catch(() => ({}));
    }
    return updatesPromise;
  }

  // 将原始更新信息整理成按更新时间倒序排序且数量受限的卡片列表
  function toItems(map) {
    return Object.keys(map || {})
      .map((path) => ({ path, info: map[path] || {} }))
      .filter((item) => item.info && item.info.updated)
      .sort((a, b) => {
        const aTime = new Date(a.info.updated).getTime();
        const bTime = new Date(b.info.updated).getTime();
        const aInvalid = Number.isNaN(aTime);
        const bInvalid = Number.isNaN(bTime);
        if (aInvalid && bInvalid) return 0;
        if (aInvalid) return 1;
        if (bInvalid) return -1;
        return bTime - aTime;
      })
      .slice(0, LIMIT);
  }

  // 将词条相对路径转成 Docsify 需要的 hash 形式，兼容中文与特殊字符
  function toRoutePath(path) {
    const withoutExt = path.replace(/\.md$/i, "");
    const encoded = withoutExt
      .split("/")
      .filter(Boolean)
      .map((segment) => encodeURIComponent(segment))
      .join("/");
    return `#/${encoded}`;
  }

  // 若无法解析 Markdown 标题时，回退使用路径末段作为展示文案
  function fallbackTitle(path) {
    const segments = path
      .replace(/\.md$/i, "")
      .split("/")
      .filter(Boolean);
    if (!segments.length) return path;
    return segments[segments.length - 1].replace(/-/g, " ");
  }

  // 基础的 HTML 转义，避免用户生成内容打破结构
  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  // 异步加载 Markdown，缓存 Promise 并提取一级标题作为卡片标题
  function loadTitle(path) {
    if (!path) return Promise.resolve("");
    if (titleCache.has(path)) {
      return titleCache.get(path);
    }

    const promise = fetch(`./${path}`, { cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to load entry");
        return response.text();
      })
      .then((text) => {
        const match = text.match(/^#\s+(.+)$/m);
        if (match && match[1]) {
          return match[1].trim();
        }
        return fallbackTitle(path);
      })
      .catch(() => fallbackTitle(path));

    titleCache.set(path, promise);
    return promise;
  }

  // 将 ISO 字符串格式化为 YYYY/MM/DD，供卡片右下角展示
  function formatDate(isoString) {
    if (!isoString) return "";
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) return "";
    const pad = (value) => String(value).padStart(2, "0");
    const year = date.getFullYear();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    return `${year}/${month}/${day}`;
  }

  // 在真实数据返回前展示加载态，提升感知反馈
  function setLoading(list) {
    if (!list) return;
    list.innerHTML =
      '<li class="recent-updates-item recent-updates-item--loading">加载中…</li>';
  }

  // 根据数据渲染列表，如无数据或请求失败则输出对应提示
  function render(list, items, isError) {
    if (!list) return;

    if (!items.length) {
      const text = isError
        ? "无法加载最近更新，请稍后再试。"
        : "暂无最近更新。";
      const stateClass = isError
        ? "recent-updates-item--error"
        : "recent-updates-item--empty";
      list.innerHTML = `<li class="recent-updates-item ${stateClass}">${escapeHtml(
        text
      )}</li>`;
      return;
    }

    const html = items
      .map(({ path, info, title }) => {
        const displayTitle = escapeHtml(title || fallbackTitle(path));
        const href = toRoutePath(path);
        const iso = info && info.updated ? escapeHtml(info.updated) : "";
        const formattedDate = formatDate(info && info.updated);
        const dateBlock = formattedDate
          ? `<time datetime="${iso}">${escapeHtml(formattedDate)}</time>`
          : "";
        return `
          <li class="recent-updates-item">
            <a href="${href}">${displayTitle}</a>
            ${dateBlock ? `<span class="recent-updates-meta">${dateBlock}</span>` : ""}
          </li>
        `;
      })
      .join("");

    list.innerHTML = html;
  }

  // 将首页最近更新卡片接入数据源，仅初始化一次避免重复绑定
  function enhanceRecentCard() {
    const container = document.querySelector(CARD_SELECTOR);
    if (!container || container.getAttribute(STATE_ATTR) === "1") {
      return;
    }

    const list = container.querySelector(LIST_SELECTOR);
    if (!list) return;

    container.setAttribute(STATE_ATTR, "1");
    setLoading(list);

    fetchUpdates()
      .then((map) => {
        const items = toItems(map);
        return Promise.all(
          items.map(async (item) => ({
            ...item,
            title: await loadTitle(item.path),
          }))
        );
      })
      .then((itemsWithTitle) => {
        render(list, itemsWithTitle, false);
      })
      .catch(() => {
        render(list, [], true);
      });
  }

  window.$docsify = window.$docsify || {};
  const userPlugins = window.$docsify.plugins || [];
  window.$docsify.plugins = [].concat(function (hook) {
    hook.doneEach(enhanceRecentCard);
  }, userPlugins);
})();
