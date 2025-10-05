/**
 * 核心工具函数模块
 * 提供前端各模块共用的工具函数
 */
(function (window) {
  "use strict";

  const PluralityUtils = {
    /**
     * 路径处理工具
     */
    path: {
      /**
       * 确保路径以斜杠结尾
       * @param {string} path - 输入路径
       * @returns {string} 处理后的路径
       */
      ensureTrailingSlash(path) {
        return path.endsWith("/") ? path : `${path}/`;
      },

      /**
       * 规范化路径,移除 ./ 和 .. 片段
       * @param {string} raw - 原始路径
       * @returns {string} 规范化后的路径
       */
      normalizePath(raw) {
        const [rawPath, query = ""] = raw.split("?");
        const segments = rawPath.split("/").filter(Boolean);
        const stack = [];

        for (const segment of segments) {
          if (segment === "..") {
            if (stack.length) stack.pop();
          } else if (segment !== ".") {
            stack.push(segment);
          }
        }

        const normalizedPath = stack.join("/");
        return normalizedPath + (query ? `?${query}` : "");
      },

      /**
       * 解析目标路径,处理相对路径和锚点
       * @param {string} href - 链接地址
       * @param {string} basePath - 基础路径
       * @param {object} currentLocation - 当前位置信息
       * @returns {string} 解析后的路径
       */
      resolveTarget(href, basePath = "", currentLocation = {}) {
        const [pathAndQuery = "", hashFragment = ""] = href.split("#");
        const [rawPath = "", rawQuery = ""] = pathAndQuery.split("?");
        const queryPart = rawQuery ? `?${rawQuery}` : "";

        const currentBaseSegments = (() => {
          const { hash } = currentLocation;
          if (!hash || !hash.startsWith("#/")) return [];

          const [currentPath = ""] = hash.slice(2).split("?");
          const segments = currentPath.split("/").filter(Boolean);
          if (segments.length) segments.pop();
          return segments;
        })();

        const isAbsolutePath =
          rawPath.startsWith("/") || rawPath.startsWith("entries/");
        const isRootDocumentLink =
          !isAbsolutePath &&
          !rawPath.startsWith(".") &&
          rawPath.length > 0 &&
          !rawPath.includes("/") &&
          /\.(md|html)$/i.test(rawPath);
        const baseTrimmed = basePath.replace(/^\/+|\/+$/g, "");
        let workingPath = rawPath.replace(/^\/+/, "");
        if (baseTrimmed && workingPath.startsWith(`${baseTrimmed}/`)) {
          workingPath = workingPath.slice(baseTrimmed.length + 1);
        }
        const pathSegments = workingPath
          .split("/")
          .filter((segment) => segment.length);

        const stack =
          isAbsolutePath || isRootDocumentLink ? [] : [...currentBaseSegments];

        for (const segment of pathSegments) {
          if (segment === ".") continue;
          if (segment === "..") {
            if (stack.length) stack.pop();
            continue;
          }
          stack.push(segment);
        }

        const resolvedPath = stack.join("/");
        const anchorQuery = hashFragment
          ? (queryPart ? `${queryPart}&` : "?") +
            `id=${encodeURIComponent(hashFragment)}`
          : queryPart;

        return `${resolvedPath}${anchorQuery}`;
      },

      /**
       * 将文件路径转换为路由路径
       * @param {string} filePath - 文件路径
       * @returns {string} 路由路径
       */
      toRoutePath(filePath) {
        const withoutExt = filePath.replace(/\.md$/i, "");
        const encoded = withoutExt
          .split("/")
          .filter(Boolean)
          .map((segment) => encodeURIComponent(segment))
          .join("/");
        return `#/${encoded}`;
      },

      /**
       * 从路由路径转换为仓库路径
       * @param {string} routePath - 路由路径
       * @returns {string|null} 仓库路径
       */
      routeToRepoPath(routePath) {
        if (!routePath) return null;
        let path = routePath.replace(/^\//, "");
        const [rawPath] = path.split("?");
        if (!rawPath) return null;
        const trimmed = rawPath.endsWith("/")
          ? rawPath.slice(0, -1)
          : rawPath;
        if (!trimmed) return null;
        const decoded = decodeURIComponent(trimmed);
        if (/\.[^./]+$/i.test(decoded)) {
          return decoded;
        }
        return `${decoded}.md`;
      },
    },

    /**
     * 日期时间工具
     */
    datetime: {
      /**
       * 格式化 ISO 日期字符串
       * @param {string} isoString - ISO 格式日期字符串
       * @param {string} format - 格式化模板 (默认: YYYY/MM/DD HH:mm:ss)
       * @returns {string|null} 格式化后的日期字符串
       */
      formatDate(isoString, format = "YYYY/MM/DD HH:mm:ss") {
        if (!isoString) return null;
        const date = new Date(isoString);
        if (Number.isNaN(date.getTime())) return null;
        const pad = (value) => String(value).padStart(2, "0");
        const year = date.getFullYear();
        const month = pad(date.getMonth() + 1);
        const day = pad(date.getDate());
        const hours = pad(date.getHours());
        const minutes = pad(date.getMinutes());
        const seconds = pad(date.getSeconds());

        return format
          .replace("YYYY", year)
          .replace("MM", month)
          .replace("DD", day)
          .replace("HH", hours)
          .replace("mm", minutes)
          .replace("ss", seconds);
      },
    },

    /**
     * HTML 处理工具
     */
    html: {
      /**
       * HTML 转义
       * @param {string} value - 需要转义的字符串
       * @returns {string} 转义后的字符串
       */
      escape(value) {
        return String(value)
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#39;");
      },

      /**
       * 从 HTML 中提取标题
       * @param {string} html - HTML 内容
       * @returns {Array} 标题数组
       */
      extractHeadings(html) {
        const headings = [];
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        const headingElements = tempDiv.querySelectorAll(
          "h1, h2, h3, h4, h5, h6"
        );
        headingElements.forEach((heading) => {
          headings.push({
            level: parseInt(heading.tagName.substring(1)),
            text: heading.textContent.trim(),
            id: heading.id || "",
          });
        });
        return headings;
      },
    },

    /**
     * 文本处理工具
     */
    text: {
      /**
       * 规范化文本,移除多余空白
       * @param {string} text - 输入文本
       * @returns {string} 规范化后的文本
       */
      normalize(text) {
        return text.replace(/\s+/g, " ").trim();
      },

      /**
       * 从路径提取回退标题
       * @param {string} path - 文件路径
       * @returns {string} 标题
       */
      fallbackTitle(path) {
        const segments = path
          .replace(/\.md$/i, "")
          .split("/")
          .filter(Boolean);
        if (!segments.length) return path;
        return segments[segments.length - 1].replace(/-/g, " ");
      },
    },

    /**
     * 数据获取工具
     */
    fetch: {
      /**
       * 创建带缓存的数据获取函数
       * @param {string} url - 数据 URL
       * @returns {Function} 返回 Promise 的获取函数
       */
      createCachedFetcher(url) {
        let promise = null;
        return function () {
          if (!promise) {
            promise = fetch(url, { cache: "no-store" })
              .then((response) => (response.ok ? response.json() : {}))
              .catch(() => ({}));
          }
          return promise;
        };
      },

      /**
       * 加载 Markdown 文件
       * @param {string} path - 文件路径
       * @returns {Promise<string>} Markdown 内容
       */
      loadMarkdown(path) {
        return fetch(`./${path}`, { cache: "no-store" })
          .then((response) => {
            if (!response.ok) throw new Error("Failed to load");
            return response.text();
          })
          .catch(() => "");
      },
    },

    /**
     * 链接判断工具
     */
    link: {
      /**
       * 判断是否应该内部处理链接
       * @param {string} href - 链接地址
       * @returns {boolean} 是否内部处理
       */
      shouldHandleInternally(href) {
        if (!href || href.startsWith("#")) return false;
        if (/^[a-zA-Z]+:/i.test(href)) return false;
        if (href.startsWith("//")) return false;
        return true;
      },
    },

    /**
     * 设备检测工具
     */
    device: {
      /**
       * 检测是否为移动端布局
       * @returns {boolean} 是否移动端
       */
      isMobile() {
        if (typeof window === "undefined") return false;
        if (typeof window.matchMedia === "function") {
          return window.matchMedia("(max-width: 768px)").matches;
        }
        return window.innerWidth <= 768;
      },
    },
  };

  // 导出到全局
  window.PluralityUtils = PluralityUtils;
})(window);
