(function () {
  const DATA_URL = "./assets/last-updated.json";
  const LIMIT = 3;
  const CARD_SELECTOR = ".js-recent-home";
  const LIST_SELECTOR = ".js-recent-home-list";
  const STATE_ATTR = "data-recent-home-initialized";

  let updatesPromise = null;
  const titleCache = new Map();

  function fetchUpdates() {
    if (!updatesPromise) {
      updatesPromise = fetch(DATA_URL, { cache: "no-store" })
        .then((response) => (response.ok ? response.json() : {}))
        .catch(() => ({}));
    }
    return updatesPromise;
  }

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

  function toRoutePath(path) {
    const withoutExt = path.replace(/\.md$/i, "");
    const encoded = withoutExt
      .split("/")
      .filter(Boolean)
      .map((segment) => encodeURIComponent(segment))
      .join("/");
    return `#/${encoded}`;
  }

  function fallbackTitle(path) {
    const segments = path
      .replace(/\.md$/i, "")
      .split("/")
      .filter(Boolean);
    if (!segments.length) return path;
    return segments[segments.length - 1].replace(/-/g, " ");
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

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

  function setLoading(list) {
    if (!list) return;
    list.innerHTML =
      '<li class="recent-updates-item recent-updates-item--loading">加载中…</li>';
  }

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
