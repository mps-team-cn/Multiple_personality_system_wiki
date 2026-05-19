/**
 * 量表导出相关的共享判定工具。
 * 当前用于区分“移动端优先系统分享”和“桌面端直接下载”。
 */
(function () {
  function shouldPreferNativeShare() {
    const uaData = navigator.userAgentData;
    if (uaData && typeof uaData.mobile === 'boolean') {
      return uaData.mobile;
    }

    const ua = navigator.userAgent || '';
    if (/Android|iPhone|iPad|iPod|Windows Phone|Mobile/i.test(ua)) {
      return true;
    }

    // iPadOS 13+ 可能伪装为桌面端 UA，但仍然具备多点触控。
    if (/Macintosh/i.test(ua) && navigator.maxTouchPoints > 1) {
      return true;
    }

    return !!(window.matchMedia && window.matchMedia('(max-width: 760px) and (pointer: coarse)').matches);
  }

  if (typeof window !== 'undefined') {
    window.MPSShareUtils = Object.assign({}, window.MPSShareUtils, {
      shouldPreferNativeShare
    });
  }
})();
