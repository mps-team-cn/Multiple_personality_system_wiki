/**
 * Google Tag Manager / gtag 延迟加载
 * 策略：首次用户交互后加载，或 3 秒超时兜底
 *
 * 依赖：在模板中通过 window.GA_MEASUREMENT_ID 注入 GA Measurement ID
 */
(function () {
  'use strict';

  var LOADED = false;

  function getMeasurementId() {
    // 优先从全局变量读取（由模板注入）
    if (typeof window.GA_MEASUREMENT_ID === 'string' && window.GA_MEASUREMENT_ID.trim()) {
      return window.GA_MEASUREMENT_ID.trim();
    }
    // 兼容：从 meta[name="ga-measurement-id"] 读取（如有）
    var meta = document.querySelector('meta[name="ga-measurement-id"]');
    if (meta && meta.content) return meta.content.trim();
    return '';
  }

  function loadGTM() {
    if (LOADED) return;
    var id = getMeasurementId();
    if (!id) {
      // 未配置 Measurement ID 时不加载
      return;
    }

    LOADED = true;
    try {
      // 创建 GTM / gtag 脚本
      var script = document.createElement('script');
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
      script.async = true;
      document.head.appendChild(script);

      // 初始化 dataLayer / gtag
      window.dataLayer = window.dataLayer || [];
      function gtag(){ dataLayer.push(arguments); }
      window.gtag = gtag;

      gtag('js', new Date());
      gtag('config', id, {
        page_path: window.location.pathname
      });
    } catch (e) {
      // 静默失败，避免阻塞主流程
      console && console.warn && console.warn('[GTM Loader] Failed:', e);
    }
  }

  // 用户交互后加载
  var events = ['scroll', 'mousemove', 'touchstart', 'click', 'keydown'];
  events.forEach(function (event) {
    document.addEventListener(event, function handler() {
      loadGTM();
      // 清理所有监听器
      events.forEach(function (e) {
        document.removeEventListener(e, handler, { passive: true });
      });
    }, { once: true, passive: true });
  });

  // 兜底：3 秒后加载，防止数据完全丢失
  setTimeout(loadGTM, 3000);
})();

