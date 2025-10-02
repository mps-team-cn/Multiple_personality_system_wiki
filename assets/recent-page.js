(function () {
  const RECENT_ROUTE = "/recent";
  const DATA_URL = "./assets/last-updated.json";
  const ENTRY_LIMIT = 20;
  const CONTAINER_CLASS = "recent-page";

  let cachedPromise = null;

  function fetchUpdates() {
    if (!cachedPromise) {
      cachedPromise = fetch(DATA_URL, { cache: "no-store" })
        .then((response) => (response.ok ? response.json() : {}))
        .catch(() => ({}));
    }
    return cachedPromise;
  }

  function toRoutePath(filePath) {
    const withoutExt = filePath.replace(/\.md$/i, "");
    const encoded = withoutExt
      .split("/")
      .filter(Boolean)
      .map((segment) => encodeURIComponent(segment))
      .join("/");
    return `#/${encoded}`;
  }

  function toDisplayName(filePath) {
    return filePath.replace(/\.md$/i, "").replace(/^entries\//i, "");
  }

  function formatDate(isoString) {
    if (!isoString) return "";
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) return "";
    const pad = (value) => String(value).padStart(2, "0");
    const year = date.getFullYear();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    return `${year}/${month}/${day} ${hours}:${minutes}`;
  }

  function normalizeRoutePath(route) {
    if (!route || !route.path) return "";
    const [path] = String(route.path).split("?");
    const trimmed = path.replace(/\/+$/, "");
    if (!trimmed) return "/";
    return trimmed.startsWith("/") ? trimmed : `/${trimmed}`;
  }

  function buildCommitLink(commit) {
    if (!commit) return "";
    const repo = (window.$docsify && window.$docsify.repo) || "";
    if (!repo) return "";

    const normalizedRepo = repo.replace(/\.git$/, "");
    const url = /^(https?:)?\/\//i.test(normalizedRepo)
      ? `${normalizedRepo.replace(/\/+$/, "")}/commit/${commit}`
      : `https://github.com/${normalizedRepo.replace(/^\/+/, "")}/commit/${commit}`;

    return `<a href="${url}" target="_blank" rel="noopener">${commit.slice(
      0,
      7
    )}</a>`;
  }

  function renderList(items) {
    if (!items.length) {
      return `
        <section class="${CONTAINER_CLASS}">
          <h1>最近更新</h1>
          <p>暂无最近更新记录。</p>
        </section>
      `;
    }

    const listItems = items
      .map(({ path, info }) => {
        const displayName = toDisplayName(path);
        const formattedDate = formatDate(info.updated);
        const commitLink = buildCommitLink(info.commit);
        const meta = [formattedDate, commitLink]
          .filter(Boolean)
          .join(" · ");
        return `
          <li>
            <a href="${toRoutePath(path)}">${displayName}</a>
            ${meta ? `<div class="meta">${meta}</div>` : ""}
          </li>
        `;
      })
      .join("");

    return `
      <section class="${CONTAINER_CLASS}">
        <h1>最近更新</h1>
        <p>以下列表基于仓库同步的 <code>last-updated.json</code> 自动生成。</p>
        <ol>
          ${listItems}
        </ol>
      </section>
    `;
  }

  function generateContent(map) {
    const items = Object.keys(map || {})
      .map((path) => ({ path, info: map[path] || {} }))
      .filter((item) => item.info && item.info.updated)
      .sort((a, b) => {
        const aTime = new Date(a.info.updated).getTime();
        const bTime = new Date(b.info.updated).getTime();
        return Number.isNaN(bTime) - Number.isNaN(aTime) || bTime - aTime;
      })
      .slice(0, ENTRY_LIMIT);

    return renderList(items);
  }

  window.$docsify = window.$docsify || {};
  const userPlugins = window.$docsify.plugins || [];

  window.$docsify.plugins = [].concat(function (hook, vm) {
    hook.afterEach(function (html, next) {
      const currentPath = normalizeRoutePath(vm.route);
      if (currentPath !== RECENT_ROUTE) {
        next(html);
        return;
      }

      fetchUpdates()
        .then((map) => {
          next(generateContent(map));
        })
        .catch(() => {
          next(generateContent({}));
        });
    });
  }, userPlugins);
})();
