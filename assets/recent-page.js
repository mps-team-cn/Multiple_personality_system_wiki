(function () {
  const RECENT_ROUTE = "/recent";
  const DATA_URL = "./assets/last-updated.json";
  const ENTRY_LIMIT = 20;
  const CONTAINER_CLASS = "recent-page";

  let cachedPromise = null;

  // 读取 last-updated.json 并利用缓存 Promise 避免多次网络请求
  function fetchUpdates() {
    if (!cachedPromise) {
      cachedPromise = fetch(DATA_URL, { cache: "no-store" })
        .then((response) => (response.ok ? response.json() : {}))
        .catch(() => ({}));
    }
    return cachedPromise;
  }

  // 将词条路径转换为 Docsify 可识别的 hash 链接，确保中文安全编码
  function toRoutePath(filePath) {
    const withoutExt = filePath.replace(/\.md$/i, "");
    const encoded = withoutExt
      .split("/")
      .filter(Boolean)
      .map((segment) => encodeURIComponent(segment))
      .join("/");
    return `#/${encoded}`;
  }

  let titleCachePromise = null;

  // 从 index.md 提取侧边链接，构建路径与标题的映射缓存
  function fetchTitleMap() {
    if (!titleCachePromise) {
      titleCachePromise = fetch("./index.md", { cache: "no-store" })
        .then((response) => (response.ok ? response.text() : ""))
        .then((content) => {
          if (!content) return {};
          const map = {};
          const linkRegExp = /\[([^\]]+)\]\((entries\/[^)]+?\.md)\)/g;
          let match = linkRegExp.exec(content);
          while (match) {
            const [, title, linkPath] = match;
            const normalizedPath = linkPath.split("#")[0];
            map[normalizedPath] = title.trim();
            match = linkRegExp.exec(content);
          }
          return map;
        })
        .catch(() => ({}));
    }
    return titleCachePromise;
  }

  // 优先使用索引中的标题，否则用路径末段回退展示
  function toDisplayName(filePath, titleMap) {
    if (titleMap && titleMap[filePath]) {
      return titleMap[filePath];
    }
    const withoutExt = filePath.replace(/\.md$/i, "");
    const segments = withoutExt.split("/").filter(Boolean);
    const lastSegment = segments[segments.length - 1] || withoutExt;
    return decodeURIComponent(lastSegment).replace(/-/g, " ");
  }

  // 按 YYYY/MM/DD HH:mm 输出更新时间，展示在最近更新列表
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

  // 标准化 Docsify 路径对象，保证匹配 /recent 路由时不受尾部斜杠影响
  function normalizeRoutePath(route) {
    if (!route || !route.path) return "";
    const [path] = String(route.path).split("?");
    const trimmed = path.replace(/\/+$/, "");
    if (!trimmed) return "/";
    return trimmed.startsWith("/") ? trimmed : `/${trimmed}`;
  }

  // 构造指向仓库提交的外链，截取前 7 位作为短哈希
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

  // 生成完整的 HTML 片段，缺省时展示友好提示
  function renderList(items, titleMap) {
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
        const displayName = toDisplayName(path, titleMap);
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

  // 根据更新时间排序并裁剪条目，传递给渲染函数
  function generateContent(map, titleMap) {
    const items = Object.keys(map || {})
      .map((path) => ({ path, info: map[path] || {} }))
      .filter((item) => item.info && item.info.updated)
      .sort((a, b) => {
        const aTime = new Date(a.info.updated).getTime();
        const bTime = new Date(b.info.updated).getTime();
        return Number.isNaN(bTime) - Number.isNaN(aTime) || bTime - aTime;
      })
      .slice(0, ENTRY_LIMIT);

    return renderList(items, titleMap);
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

      Promise.all([fetchUpdates(), fetchTitleMap()])
        .then(([map, titleMap]) => {
          next(generateContent(map, titleMap));
        })
        .catch(() => {
          next(generateContent({}, {}));
        });
    });
  }, userPlugins);
})();
