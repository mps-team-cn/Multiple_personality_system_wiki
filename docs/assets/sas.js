/*
 * 焦虑自评量表(SAS)在线评估 - 纯前端实现
 * - 不存储数据(无 LocalStorage / 网络请求)
 * - 仅在包含 #sas-app 的页面激活
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

  // SAS 反向题题号：5, 9, 13, 17, 19
  const REVERSE_ITEMS = [5, 9, 13, 17, 19];

  function isReverseItem(itemNumber) {
    return REVERSE_ITEMS.includes(itemNumber);
  }

  // SAS 焦虑程度分级
  function getAnxietyLevel(standardScore) {
    if (standardScore >= 70) {
      return { text: '重度焦虑', class: 'extreme' };
    } else if (standardScore >= 60) {
      return { text: '中度焦虑', class: 'severe' };
    } else if (standardScore >= 50) {
      return { text: '轻度焦虑', class: 'moderate' };
    } else if (standardScore >= 40) {
      return { text: '可能有焦虑', class: 'mild' };
    } else {
      return { text: '正常', class: 'normal' };
    }
  }

  function bindItem(item) {
    const select = qs('select', item);
    const badge = qs('.sas-badge', item);
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
        badge.style.background = 'color-mix(in srgb, #9c27b0 15%, transparent)';
        badge.style.color = '#7b1fa2';
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
    const node = qs('#sas-results', root);
    if (!node) return;
    let wm = null;
    try {
      const h2i = await ensureHtmlToImage();
      const bg = getComputedStyle(document.body).backgroundColor || '#ffffff';

      // 添加水印
      wm = document.createElement('div');
      wm.className = 'sas-watermark';
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
      const fileName = blob && blob.type === 'image/png' ? 'SAS-结果.png' : 'SAS-结果.jpg';
      try {
        file = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
      } catch (_) { /* ignore */ }

      if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: 'SAS 焦虑自评量表结果',
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
    qsa('.sas-item select', root).forEach((select) => {
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
    const rawScoreEl = qs('#sas-raw-score', root);
    if (rawScoreEl) rawScoreEl.textContent = rawScore;

    // 更新标准分
    const standardScoreEl = qs('#sas-standard-score', root);
    if (standardScoreEl) standardScoreEl.textContent = standardScore;

    // 更新焦虑指数
    const indexEl = qs('#sas-index', root);
    const index = rawScore / 80; // SAS 满分80分
    if (indexEl) indexEl.textContent = fmt(index * 100) + '%';

    // 更新焦虑程度
    const anxietyEl = qs('#sas-anxiety', root);
    const anxiety = getAnxietyLevel(standardScore);
    if (anxietyEl) {
      anxietyEl.textContent = anxiety.text;
      anxietyEl.className = `sas-anxiety ${anxiety.class}`;
    }

    // 更新进度条
    const progressBar = qs('#sas-progress-bar', root);
    if (progressBar) {
      const percentage = Math.max(0, Math.min(100, (standardScore / 80) * 100));
      progressBar.style.width = percentage + '%';

      // 根据焦虑程度改变进度条颜色
      if (standardScore >= 70) {
        progressBar.style.background = 'linear-gradient(90deg, #f44336, #d32f2f)';
      } else if (standardScore >= 60) {
        progressBar.style.background = 'linear-gradient(90deg, #ff9800, #f57c00)';
      } else if (standardScore >= 50) {
        progressBar.style.background = 'linear-gradient(90deg, #9c27b0, #7b1fa2)';
      } else if (standardScore >= 40) {
        progressBar.style.background = 'linear-gradient(90deg, #81c784, #4caf50)';
      } else {
        progressBar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)';
      }
    }

    // 检查是否完成所有题目
    const completedCount = scores.length;
    const totalCount = 20; // SAS 共20题
    const completionRate = (completedCount / totalCount) * 100;

    const completionEl = qs('#sas-completion', root);
    if (completionEl) {
      completionEl.textContent = `${completedCount}/${totalCount} (${Math.round(completionRate)}%)`;
    }

    // 更新子量表分数（心理焦虑、躯体焦虑等）
    updateSubscales(root, scores);

    // 显示安全提示（如果标准分较高）
    const safetyAlert = qs('#sas-safety-alert', root);
    if (safetyAlert) {
      if (standardScore >= 60) { // 中度及以上显示提示
        safetyAlert.style.display = 'block';
      } else {
        safetyAlert.style.display = 'none';
      }
    }
  }

  function updateSubscales(root, allScores) {
    // SAS 子量表定义（简化版本，实际应用中可根据需要调整）
    const subscales = {
      // 心理焦虑症状
      mental: {
        name: '心理焦虑',
        items: [1, 3, 7, 8, 15, 16, 18, 20], // 不包括反向题
        maxScore: 32
      },
      // 躯体焦虑症状
      physical: {
        name: '躯体焦虑',
        items: [2, 4, 6, 10, 12, 14], // 不包括反向题
        maxScore: 24
      },
      // 精神运动性焦虑
      motor: {
        name: '精神运动性',
        items: [9, 11, 13, 17, 19], // 包括反向题
        maxScore: 20
      }
    };

    Object.keys(subscales).forEach(key => {
      const scale = subscales[key];
      let score = 0;

      scale.items.forEach(itemNum => {
        const select = qs(`#item${itemNum}`, root);
        if (select) {
          const rawValue = Number(select.value || 1);
          const actualValue = isReverseItem(itemNum) ? (5 - rawValue) : rawValue;
          score += actualValue;
        }
      });

      const percentage = Math.max(0, Math.min(100, (score / scale.maxScore) * 100));

      // 更新子量表显示
      const scoreEl = qs(`#sas-${key}-score`, root);
      if (scoreEl) scoreEl.textContent = `${score}/${scale.maxScore}`;

      const barEl = qs(`#sas-${key}-bar`, root);
      if (barEl) barEl.style.width = percentage + '%';
    });
  }

  function resetAll(root) {
    qsa('.sas-item select', root).forEach((select) => {
      select.value = '1'; // 重置为最低分
      select.dispatchEvent(new Event('change'));
    });
    updateResults(root);
  }

  function init(root) {
    // 绑定每一项的数值显示
    qsa('.sas-item', root).forEach(bindItem);

    // 重置按钮
    const resetBtn = qs('#sas-reset', root);
    if (resetBtn) resetBtn.addEventListener('click', () => resetAll(root));

    // 导出按钮
    const actions = qs('.sas-actions', root) || root;
    let exportBtn = qs('#sas-export', actions);
    if (!exportBtn) {
      exportBtn = document.createElement('button');
      exportBtn.id = 'sas-export';
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
    const app = document.getElementById('sas-app');
    if (!app) return;
    if (app.dataset.sasInited === '1') return;
    app.dataset.sasInited = '1';
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