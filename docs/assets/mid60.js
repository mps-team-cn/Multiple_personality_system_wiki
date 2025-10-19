/*
 * 多维解离量表(MID‑60)在线评估 - 纯前端实现
 * - 不存储数据(无 LocalStorage / 网络请求)
 * - 仅在包含 #mid60-app 的页面激活
 * - 0-10 评分,转换为百分比显示
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  // 等待一帧（用于确保挂载后的布局/样式可用）
  function nextFrame() {
    return new Promise((resolve) => requestAnimationFrame(resolve));
  }

  function fmt(n) {
    return (Math.round(n * 10) / 10).toFixed(1);
  }

  function levelText(avg) {
    if (avg >= 64) return '严重的解离和创伤后症状';
    if (avg >= 41) return '可能患有 DID 或严重解离障碍和 PTSD';
    if (avg >= 31) return '可能存在解离障碍(如 OSDD 或 DID)和 PTSD';
    if (avg >= 21) return '可能存在解离障碍和/或 PTSD';
    if (avg >= 15) return '轻度解离症状,可能存在 PTSD 或轻度解离障碍';
    if (avg >= 7) return '很少有诊断意义的解离体验';
    return '无解离体验';
  }

  function bindItem(item) {
    const input = qs('input[type="range"]', item);
    const out = qs('output, .mid60-badge', item);
    if (!input || !out) return;

    // 清理历史遗留的刻度包装（若存在则移除 wrapper 与 marks）
    try {
      const p = input.parentElement;
      if (p && p.classList && p.classList.contains('mid60-slider-wrap')) {
        const host = p.parentElement || item;
        host.insertBefore(input, p);
        p.remove();
      }
    } catch (_) { /* ignore */ }

    // 为滑块添加可访问性属性
    const itemNumber = input.id.replace('item', '');
    const questionText = item.querySelector('td:nth-child(2)')?.textContent?.trim() || '';
    if (!input.hasAttribute('aria-label')) {
      input.setAttribute('aria-label', `题目 ${itemNumber}: ${questionText.substring(0, 30)}... - 频率评分 0 到 10`);
      input.setAttribute('tabindex', '0');
    }

    // 交互策略（Android/MUI/Ant 风格）：
    // - 允许点击轨道跳转
    // - 支持拖动
    // - 保留页面纵向滚动优先（见 CSS touch-action: pan-y）
    // 不再阻止键盘/轨道点击等默认行为

    // 已取消刻度（marks），保留原生轨道点击与拖动交互

    const update = () => {
      // MID-60: 0-10 转换为 0-100 百分比
      const percentage = Number(input.value || 0) * 10;
      out.textContent = fmt(percentage);
    };
    input.addEventListener('input', update);
    update();
  }

  // 动态加载 html-to-image（仅在导出时加载）
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
    const node = qs('#mid60-results', root);
    if (!node) return;
    let wm = null;
    try {
      const h2i = await ensureHtmlToImage();
      // 背景色：使用页面背景，避免透明导致聊天软件黑底
      const bg = getComputedStyle(document.body).backgroundColor || '#ffffff';

      // 在实际节点上临时添加水印（导出后移除）
      wm = document.createElement('div');
      wm.className = 'mid60-watermark';
      wm.textContent = 'wiki.mpsteam.cn';
      node.appendChild(wm);

      // 等待字体与一两个帧，确保布局稳定
      try { if (document.fonts && document.fonts.ready) await document.fonts.ready; } catch (_) { /* ignore */ }
      await nextFrame();
      await nextFrame();

      let dataUrl = await h2i.toJpeg(node, {
        cacheBust: true,
        pixelRatio: Math.min(2, window.devicePixelRatio || 1.5),
        backgroundColor: bg,
        style: {
          padding: '20px',
          boxSizing: 'border-box',
          backgroundColor: bg
        }
      });

      // 转成 Blob
      let blob = await (await fetch(dataUrl)).blob();
      // 若 JPEG 数据异常小，尝试 PNG 兜底（个别环境对 JPEG 支持异常会返回空白图）
      if (blob && blob.size < 1500) {
        try {
          await nextFrame();
          dataUrl = await h2i.toPng(node, {
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
      const fileName = blob && blob.type === 'image/png' ? 'MID-60-结果.png' : 'MID-60-结果.jpg';
      try {
        file = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
      } catch (_) { /* 某些旧浏览器不支持 File 构造器 */ }

      // 优先使用系统分享（移动端友好）
      if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: 'MID‑60 结果',
          text: '来自 wiki.mpsteam.cn'
        });
        return;
      }

      // 次选：复制到剪贴板（部分浏览器支持）
      if (navigator.clipboard && window.ClipboardItem) {
        try {
          await navigator.clipboard.write([
            new ClipboardItem({ [blob.type]: blob })
          ]);
          alert('图片已复制，可直接粘贴到聊天');
          return;
        } catch (_) { /* 忽略 */ }
      }

      // 兜底：触发下载
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

  function collectValues(root) {
    const vals = [];
    qsa('.mid60-item input[type="range"]', root).forEach((inp) => {
      const v = Number(inp.value || 0) * 10; // 转换为百分比
      if (!Number.isNaN(v)) vals.push(v);
    });
    return vals;
  }

  function updateResults(root) {
    const vals = collectValues(root);
    const n = vals.length || 1;
    const avg = vals.reduce((a, b) => a + b, 0) / n;

    const avgEl = qs('#mid60-avg', root);
    const lvlEl = qs('#mid60-level', root);
    const bar = qs('#mid60-bar', root);
    const progressBar = bar?.parentElement;

    if (avgEl) avgEl.textContent = fmt(avg);
    if (lvlEl) lvlEl.textContent = levelText(avg);
    if (bar) bar.style.width = Math.max(0, Math.min(100, avg)) + '%';
    if (progressBar) progressBar.setAttribute('aria-valuenow', Math.round(avg));

    // 安全提示:检查题目 22, 44, 58 (自伤/自杀相关)
    const item22 = qs('#item22', root);
    const item44 = qs('#item44', root);
    const item58 = qs('#item58', root);
    const safetyAlert = qs('#mid60-safety-alert', root);

    if (safetyAlert) {
      const highRiskThreshold = 5; // 滑块值 >= 5 (即 50%) 触发提示
      const v22 = item22 ? Number(item22.value) : 0;
      const v44 = item44 ? Number(item44.value) : 0;
      const v58 = item58 ? Number(item58.value) : 0;

      if (v22 >= highRiskThreshold || v44 >= highRiskThreshold || v58 >= highRiskThreshold) {
        safetyAlert.style.display = 'block';
      } else {
        safetyAlert.style.display = 'none';
      }
    }

    // 子量表定义(基于 NovoPsych 资料)
    const subscales = {
      // DID
      amnesia: { items: [42, 45, 48, 58], cutoff: 10 },

      // DID / OSDD-1
      alter: { items: [3, 36, 39, 49, 57], cutoff: 20 },
      angry: { items: [28, 33, 35, 46, 60], cutoff: 18 },
      persec: { items: [22, 37, 44, 56, 59], cutoff: 18 },

      // DP/DR
      dpdr: { items: [2, 7, 9, 13, 25, 47, 50, 53], cutoff: 20 },

      // 解离性失忆
      distress: { items: [1, 8, 20, 38, 43, 52], cutoff: 30 },
      autobio: { items: [16, 19, 24, 29, 34], cutoff: 34 },

      // PTSD
      flash: { items: [4, 15, 31, 40, 54], cutoff: 16 },

      // 转换障碍
      body: { items: [5, 10, 14, 18], cutoff: 10 },
      seizure: { items: [26], cutoff: 10 },

      // 一般子量表
      trance: { items: [21, 27, 30, 32, 41, 51], cutoff: 11.7 },
      confuse: { items: [6, 11, 12, 17, 23, 55], cutoff: 33.3 }
    };

    const valueOf = (idx) => {
      const inp = qs(`#item${idx}`, root);
      const v = inp ? Number(inp.value || 0) * 10 : 0; // 转换为百分比
      return Number.isFinite(v) ? v : 0;
    };

    const meanOf = (arr) => arr.reduce((s, i) => s + valueOf(i), 0) / (arr.length || 1);

    const setSub = (idBase, val, cutoff) => {
      const v = Math.max(0, Math.min(100, val));
      const out = qs(`#${idBase}-val`, root);
      const bar = qs(`#${idBase}-bar`, root);
      const progressBar = bar?.parentElement;

      if (out) out.textContent = fmt(v);
      if (bar) {
        bar.style.width = v + '%';
        // 根据是否超过临界值改变颜色
        if (v > cutoff) {
          bar.style.background = 'linear-gradient(90deg, #f56c6c, #e94545)'; // 红色渐变
        } else {
          bar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)'; // 绿色渐变
        }
      }
      if (progressBar) {
        progressBar.setAttribute('aria-valuenow', Math.round(v));
      }
    };

    // 计算并设置所有子量表
    Object.keys(subscales).forEach(key => {
      const scale = subscales[key];
      const mean = meanOf(scale.items);
      setSub(`mid60-${key}`, mean, scale.cutoff);
    });
  }

  function resetAll(root) {
    qsa('.mid60-item input[type="range"]', root).forEach((inp) => {
      inp.value = inp.getAttribute('value') || '0';
      inp.dispatchEvent(new Event('input'));
    });
    updateResults(root);
  }

  function init(root) {
    // 绑定每一项的数值显示
    qsa('.mid60-item', root).forEach(bindItem);

    // 重置按钮
    const resetBtn = qs('#mid60-reset', root);
    if (resetBtn) resetBtn.addEventListener('click', () => resetAll(root));

    // 导出按钮（移动端友好：系统分享 + 下载兜底）
    const actions = qs('.mid60-actions', root) || root;
    let exportBtn = qs('#mid60-export', actions);
    if (!exportBtn) {
      exportBtn = document.createElement('button');
      exportBtn.id = 'mid60-export';
      exportBtn.className = 'md-button md-button--primary';
      exportBtn.type = 'button';
      exportBtn.textContent = '导出图片';
      actions.appendChild(exportBtn);
    }
    exportBtn.addEventListener('click', () => exportResultsImage(root));

    // 实时更新:任意滑块变动即刷新结果
    root.addEventListener('input', (e) => {
      const t = e.target;
      if (t && t.matches('input[type="range"]')) updateResults(root);
    });

    // 初始计算一次
    updateResults(root);
  }

  function initIfPresent() {
    const app = document.getElementById('mid60-app');
    if (!app) return;
    if (app.dataset.mid60Inited === '1') return;
    app.dataset.mid60Inited = '1';
    init(app);
  }

  // 1) 常规页面加载
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initIfPresent);
  } else {
    initIfPresent();
  }

  // 2) 兼容 MkDocs Material 的 instant navigation
  if (typeof window !== 'undefined' && window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => {
      setTimeout(initIfPresent, 0);
    });
  }
})();
