/*
 * 抑郁自评量表(SDS)在线评估 - 纯前端实现
 * - 不存储数据(无 LocalStorage / 网络请求)
 * - 仅在包含 #sds-app 的页面激活
 * - 1-4 评分，自动计算粗分和标准分
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function nextFrame() {
    return new Promise((resolve) => requestAnimationFrame(resolve));
  }

  function fmt(n) {
    return (Math.round(n * 10) / 10).toFixed(1);
  }

  // SDS 反向题题号：2, 5, 6, 11, 12, 14, 16, 17, 18, 20
  const REVERSE_ITEMS = [2, 5, 6, 11, 12, 14, 16, 17, 18, 20];

  function isReverseItem(itemNumber) {
    return REVERSE_ITEMS.includes(itemNumber);
  }

  // SDS 严重程度分级
  function getSeverityLevel(standardScore) {
    if (standardScore >= 73) {
      return { text: '重度抑郁', class: 'severe' };
    } else if (standardScore >= 63) {
      return { text: '中度抑郁', class: 'moderate' };
    } else if (standardScore >= 53) {
      return { text: '轻度抑郁', class: 'mild' };
    } else {
      return { text: '无抑郁', class: 'none' };
    }
  }

  function bindItem(item) {
    const select = qs('select', item);
    const badge = qs('.sds-badge', item);
    if (!select || !badge) return;

    // 为下拉菜单添加可访问性属性
    const itemNumber = select.id.replace('item', '');
    const questionText = item.querySelector('td:nth-child(2)')?.textContent?.trim() || '';
    if (!select.hasAttribute('aria-label')) {
      select.setAttribute('aria-label', `题目 ${itemNumber}: ${questionText.substring(0, 30)}... - 评分 1 到 4`);
      select.setAttribute('tabindex', '0');
    }

    const update = () => {
      const rawValue = Number(select.value || 1);
      const actualValue = isReverseItem(itemNumber) ? (5 - rawValue) : rawValue;
      badge.textContent = actualValue;

      // 根据是否为反向题显示不同颜色
      if (isReverseItem(itemNumber)) {
        badge.style.background = 'color-mix(in srgb, #ff9800 15%, transparent)';
        badge.style.color = '#e65100';
      } else {
        badge.style.background = 'color-mix(in srgb, var(--md-primary-fg-color) 10%, transparent)';
        badge.style.color = 'var(--md-primary-fg-color)';
      }
    };

    select.addEventListener('change', update);
    update();
  }

  // 动态加载 html-to-image
  async function ensureHtmlToImage() {
    if (window.htmlToImage) return window.htmlToImage;
    const src = 'https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.min.js';
    await new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = () => reject(new Error('无法加载导出库'));
      document.head.appendChild(s);
    });
    return window.htmlToImage;
  }

  async function exportResultsImage(root) {
    const node = qs('#sds-results', root);
    if (!node) return;
    let wm = null;
    try {
      const h2i = await ensureHtmlToImage();
      const bg = getComputedStyle(document.body).backgroundColor || '#ffffff';

      // 添加水印
      wm = document.createElement('div');
      wm.className = 'sds-watermark';
      wm.textContent = 'wiki.mpsteam.cn';
      node.appendChild(wm);

      try { if (document.fonts && document.fonts.ready) await document.fonts.ready; } catch (_) { /* ignore */ }
      await nextFrame();
      await nextFrame();

      const width = Math.ceil(node.scrollWidth + 2);
      const height = Math.ceil(node.scrollHeight + 2);

      let dataUrl = await h2i.toJpeg(node, {
        width,
        height,
        cacheBust: true,
        pixelRatio: Math.min(2, window.devicePixelRatio || 1.5),
        backgroundColor: bg,
        style: {
          padding: '20px',
          boxSizing: 'border-box',
          backgroundColor: bg
        }
      });

      let blob = await (await fetch(dataUrl)).blob();
      if (blob && blob.size < 1500) {
        try {
          await nextFrame();
          dataUrl = await h2i.toPng(node, {
            width,
            height,
            cacheBust: true,
            pixelRatio: Math.min(2, window.devicePixelRatio || 1.5),
            backgroundColor: bg,
            style: {
              padding: '20px',
              boxSizing: 'border-box',
              backgroundColor: bg
            }
          });
          blob = await (await fetch(dataUrl)).blob();
        } catch (_) { /* ignore */ }
      }

      let file = null;
      const fileName = blob && blob.type === 'image/png' ? 'SDS-结果.png' : 'SDS-结果.jpg';
      try {
        file = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
      } catch (_) { /* ignore */ }

      if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: 'SDS 抑郁自评量表结果',
          text: '来自 wiki.mpsteam.cn'
        });
        return;
      }

      if (navigator.clipboard && window.ClipboardItem) {
        try {
          await navigator.clipboard.write([
            new ClipboardItem({ [blob.type]: blob })
          ]);
          alert('图片已复制，可直接粘贴到聊天');
          return;
        } catch (_) { /* ignore */ }
      }

      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error(err);
      alert('导出失败，请重试');
    } finally {
      if (wm && wm.parentNode) {
        try { wm.remove(); } catch (_) { /* ignore */ }
      }
    }
  }

  function collectScores(root) {
    const scores = [];
    qsa('.sds-item select', root).forEach((select) => {
      const itemNumber = parseInt(select.id.replace('item', ''));
      const rawValue = Number(select.value || 1);
      const actualValue = isReverseItem(itemNumber) ? (5 - rawValue) : rawValue;
      if (!Number.isNaN(actualValue)) scores.push(actualValue);
    });
    return scores;
  }

  function updateResults(root) {
    const scores = collectScores(root);
    const rawScore = scores.reduce((a, b) => a + b, 0);
    const standardScore = Math.round(rawScore * 1.25);

    // 更新粗分
    const rawScoreEl = qs('#sds-raw-score', root);
    if (rawScoreEl) rawScoreEl.textContent = rawScore;

    // 更新标准分
    const standardScoreEl = qs('#sds-standard-score', root);
    if (standardScoreEl) standardScoreEl.textContent = standardScore;

    // 更新抑郁指数
    const indexEl = qs('#sds-index', root);
    const index = rawScore / 80; // SDS 满分80分
    if (indexEl) indexEl.textContent = fmt(index * 100) + '%';

    // 更新严重程度
    const severityEl = qs('#sds-severity', root);
    const severity = getSeverityLevel(standardScore);
    if (severityEl) {
      severityEl.textContent = severity.text;
      severityEl.className = `sds-severity ${severity.class}`;
    }

    // 更新进度条
    const progressBar = qs('#sds-progress-bar', root);
    if (progressBar) {
      const percentage = Math.max(0, Math.min(100, standardScore));
      progressBar.style.width = percentage + '%';

      // 根据严重程度改变进度条颜色
      if (standardScore >= 73) {
        progressBar.style.background = 'linear-gradient(90deg, #f44336, #d32f2f)';
      } else if (standardScore >= 63) {
        progressBar.style.background = 'linear-gradient(90deg, #ff9800, #f57c00)';
      } else if (standardScore >= 53) {
        progressBar.style.background = 'linear-gradient(90deg, #81c784, #4caf50)';
      } else {
        progressBar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)';
      }
    }

    // 检查是否完成所有题目
    const completedCount = scores.length;
    const totalCount = 20; // SDS 共20题
    const completionRate = (completedCount / totalCount) * 100;

    const completionEl = qs('#sds-completion', root);
    if (completionEl) {
      completionEl.textContent = `${completedCount}/${totalCount} (${Math.round(completionRate)}%)`;
    }

    // 显示安全提示（如果标准分较高）
    const safetyAlert = qs('#sds-safety-alert', root);
    if (safetyAlert) {
      if (standardScore >= 63) { // 中度及以上显示提示
        safetyAlert.style.display = 'block';
      } else {
        safetyAlert.style.display = 'none';
      }
    }
  }

  function resetAll(root) {
    qsa('.sds-item select', root).forEach((select) => {
      select.value = '1'; // 重置为最低分
      select.dispatchEvent(new Event('change'));
    });
    updateResults(root);
  }

  function init(root) {
    // 绑定每一项的数值显示
    qsa('.sds-item', root).forEach(bindItem);

    // 重置按钮
    const resetBtn = qs('#sds-reset', root);
    if (resetBtn) resetBtn.addEventListener('click', () => resetAll(root));

    // 导出按钮
    const actions = qs('.sds-actions', root) || root;
    let exportBtn = qs('#sds-export', actions);
    if (!exportBtn) {
      exportBtn = document.createElement('button');
      exportBtn.id = 'sds-export';
      exportBtn.className = 'md-button md-button--primary';
      exportBtn.type = 'button';
      exportBtn.textContent = '导出图片';
      actions.appendChild(exportBtn);
    }
    exportBtn.addEventListener('click', () => exportResultsImage(root));

    // 实时更新结果
    root.addEventListener('change', (e) => {
      const t = e.target;
      if (t && t.matches('select')) updateResults(root);
    });

    // 初始计算一次
    updateResults(root);
  }

  function initIfPresent() {
    const app = document.getElementById('sds-app');
    if (!app) return;
    if (app.dataset.sdsInited === '1') return;
    app.dataset.sdsInited = '1';
    init(app);
  }

  // 常规页面加载
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initIfPresent);
  } else {
    initIfPresent();
  }

  // 兼容 MkDocs Material 的 instant navigation
  if (typeof window !== 'undefined' && window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => {
      setTimeout(initIfPresent, 0);
    });
  }
})();