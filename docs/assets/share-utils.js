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

  function flashDownloadFeedback(trigger) {
    if (!trigger || typeof trigger.textContent !== 'string') return;

    const originalText = trigger.dataset.exportOriginalText || trigger.textContent;
    trigger.dataset.exportOriginalText = originalText;
    trigger.textContent = '已开始下载';

    window.setTimeout(() => {
      trigger.textContent = originalText;
    }, 1800);
  }

  async function deliverExport(options) {
    const {
      file,
      blob,
      dataUrl,
      fileName,
      title,
      text = '来自 wiki.mpsteam.cn',
      trigger
    } = options;

    const preferShare = shouldPreferNativeShare();

    if (preferShare && file && navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({
        files: [file],
        title,
        text
      });
      return 'shared';
    }

    if (preferShare && blob && navigator.clipboard && window.ClipboardItem) {
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ [blob.type]: blob })
        ]);
        alert('图片已复制，可直接粘贴到聊天');
        return 'copied';
      } catch (_) { /* ignore */ }
    }

    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    flashDownloadFeedback(trigger);
    return 'downloaded';
  }

  if (typeof window !== 'undefined') {
    window.MPSShareUtils = window.MPSShareUtils || {};
    window.MPSShareUtils.shouldPreferNativeShare = shouldPreferNativeShare;
    window.MPSShareUtils.deliverExport = deliverExport;
  }
})();
