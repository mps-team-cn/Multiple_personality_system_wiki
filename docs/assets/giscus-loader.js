/**
 * Giscus 评论系统加载脚本
 * 根据页面 Frontmatter（comments: true）决定是否插入评论区。
 */
(function() {
  'use strict';

  const ROOT_SELECTOR = '[data-giscus-root]';
  const THREAD_SELECTOR = '[data-giscus-thread]';
  const SCRIPT_SELECTOR = 'script[data-giscus-script]';
  const DEFAULT_HOST = 'https://giscus.app';
  const RETRY_LIMIT = 6;

  let themeObserver = null;
  let giscusOrigin = DEFAULT_HOST;
  let giscusActive = false;

  /**
   * 获取当前页面主题（浅色 / 深色）。
   */
  function getCurrentTheme() {
    return document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'light';
  }

  /**
   * 将 host 转换为客户端脚本地址。
   */
  function resolveClientSrc(host) {
    if (!host) {
      return `${DEFAULT_HOST}/client.js`;
    }
    const trimmed = host.replace(/\s+/g, '');
    if (!trimmed) {
      return `${DEFAULT_HOST}/client.js`;
    }
    if (trimmed.endsWith('.js')) {
      return trimmed;
    }
    return `${trimmed.replace(/\/$/, '')}/client.js`;
  }

  /**
   * 解析配置。
   */
  function parseConfig(root) {
    const dataset = root.dataset;
    const host = dataset.giscusHost && dataset.giscusHost.trim()
      ? dataset.giscusHost.trim()
      : DEFAULT_HOST;
    const clientSrc = resolveClientSrc(host);

    let origin = DEFAULT_HOST;
    try {
      origin = new URL(clientSrc).origin;
    } catch (error) {
      origin = DEFAULT_HOST;
    }

    return {
      repo: dataset.giscusRepo,
      repoId: dataset.giscusRepoId,
      category: dataset.giscusCategory,
      categoryId: dataset.giscusCategoryId,
      mapping: dataset.giscusMapping || 'pathname',
      strict: dataset.giscusStrict || '0',
      reactionsEnabled: dataset.giscusReactionsEnabled || '1',
      emitMetadata: dataset.giscusEmitMetadata || '0',
      inputPosition: dataset.giscusInputPosition || 'top',
      theme: dataset.giscusTheme || 'preferred_color_scheme',
      lang: dataset.giscusLang || 'zh-CN',
      loading: dataset.giscusLoading || 'lazy',
      host,
      clientSrc,
      origin
    };
  }

  /**
   * 清理已有的 Giscus 实例。
   */
  function cleanup() {
    document.querySelectorAll(SCRIPT_SELECTOR).forEach(node => node.remove());
    document.querySelectorAll('iframe.giscus-frame').forEach(node => node.remove());
    document.querySelectorAll(THREAD_SELECTOR).forEach(node => {
      node.innerHTML = '';
    });
    giscusActive = false;
  }

  /**
   * 同步 Giscus 主题（必要时重试）。
   */
  function syncThemeWithRetry(attempts = RETRY_LIMIT) {
    if (!giscusActive || attempts <= 0) {
      return;
    }

    const frame = document.querySelector('iframe.giscus-frame');
    if (!frame || !frame.contentWindow) {
      window.setTimeout(() => syncThemeWithRetry(attempts - 1), 400);
      return;
    }

    const theme = getCurrentTheme();
    frame.contentWindow.postMessage(
      { giscus: { setConfig: { theme } } },
      giscusOrigin
    );
  }

  /**
   * 监听主题切换。
   */
  function ensureThemeObserver() {
    if (themeObserver) {
      return;
    }

    themeObserver = new MutationObserver(() => {
      syncThemeWithRetry();
    });

    themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['data-md-color-scheme']
    });
  }

  /**
   * 加载 Giscus。
   */
  function loadGiscus() {
    const root = document.querySelector(ROOT_SELECTOR);

    if (!root) {
      cleanup();
      return;
    }

    const config = parseConfig(root);

    if (!config.repo || !config.repoId || !config.category || !config.categoryId) {
      console.warn('[giscus] 配置字段缺失，已跳过评论加载。');
      cleanup();
      return;
    }

    cleanup();

    const thread = root.querySelector(THREAD_SELECTOR) || root;
    const script = document.createElement('script');

    script.src = config.clientSrc;
    script.dataset.giscusScript = 'true';
    script.async = true;
    script.crossOrigin = 'anonymous';

    const attributes = {
      'data-repo': config.repo,
      'data-repo-id': config.repoId,
      'data-category': config.category,
      'data-category-id': config.categoryId,
      'data-mapping': config.mapping,
      'data-strict': config.strict,
      'data-reactions-enabled': config.reactionsEnabled,
      'data-emit-metadata': config.emitMetadata,
      'data-input-position': config.inputPosition,
      'data-theme': config.theme,
      'data-lang': config.lang,
      'data-loading': config.loading
    };

    if (config.host && config.host !== DEFAULT_HOST) {
      attributes['data-host'] = config.host.replace(/\/$/, '');
    }

    Object.entries(attributes).forEach(([key, value]) => {
      if (value !== undefined && value !== null && `${value}`.trim() !== '') {
        script.setAttribute(key, value);
      }
    });

    thread.appendChild(script);

    giscusOrigin = config.origin;
    giscusActive = true;

    ensureThemeObserver();
    syncThemeWithRetry();
  }

  /**
   * 页面导航后的统一入口。
   */
  function handlePageChange() {
    window.requestAnimationFrame(loadGiscus);
  }

  document.addEventListener('DOMContentLoaded', handlePageChange);

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(handlePageChange);
  }
})();
