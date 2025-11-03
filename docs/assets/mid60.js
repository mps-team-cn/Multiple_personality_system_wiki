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

  // ====== 全局子量表配置 ======
  const MID60_SUBSCALES = {
    amnesia: { items: [42, 45, 48, 58], cutoff: 10, label: '近因遗忘', group: 'did-osdd' },
    alter:   { items: [3, 36, 39, 49, 57], cutoff: 20, label: '替换人格觉察', group: 'did-osdd' },
    angry:   { items: [28, 33, 35, 46, 60], cutoff: 18, label: '愤怒侵入', group: 'did-osdd' },
    persec:  { items: [22, 37, 44, 56, 59], cutoff: 18, label: '迫害侵入', group: 'did-osdd' },
    dpdr:    { items: [2, 7, 9, 13, 25, 47, 50, 53], cutoff: 20, label: '人格解体/现实解体', group: 'dpdr' },
    distress:{ items: [1, 8, 20, 38, 43, 52], cutoff: 30, label: '记忆困扰', group: 'amnesia' },
    autobio: { items: [16, 19, 24, 29, 34], cutoff: 34, label: '自传记忆丧失', group: 'amnesia' },
    flash:   { items: [4, 15, 31, 40, 54], cutoff: 16, label: '闪回', group: 'ptsd' },
    body:    { items: [5, 10, 14, 18], cutoff: 10, label: '功能性神经症状', group: 'fnsd' },
    seizure: { items: [26], cutoff: 10, label: '心因性非癫痫发作（PNES）', group: 'fnsd' },
    trance:  { items: [21, 27, 30, 32, 41, 51], cutoff: 11.7, label: '恍惚', group: 'general' },
    confuse: { items: [6, 11, 12, 17, 23, 55], cutoff: 33.3, label: '自我困惑', group: 'general' }
  };

  // ====== 全局分组配置 ======
  const MID60_GROUP_CONFIG = {
    'did-osdd': {
      title: 'DID 与 OSDD',
      scales: ['amnesia', 'alter', 'angry', 'persec'],
      order: 1
    },
    'dpdr': {
      title: '人格解体 / 现实解体障碍（DP/DR）',
      scales: ['dpdr'],
      order: 2
    },
    'amnesia': {
      title: '解离性失忆',
      scales: ['distress', 'autobio'],
      order: 3
    },
    'ptsd': {
      title: '创伤后应激障碍（PTSD）',
      scales: ['flash'],
      order: 4
    },
    'fnsd': {
      title: '功能性神经症状障碍（FNSD）',
      scales: ['body', 'seizure'],
      order: 5
    },
    'general': {
      title: '一般解离子量表',
      scales: ['trance', 'confuse'],
      order: 6
    }
  };

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

      // 计算导出尺寸：使用 scrollWidth/scrollHeight 防止右侧被裁切
      const width = Math.ceil(node.scrollWidth + 2);   // 加 2 像素避免取整误差
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

      // 转成 Blob
      let blob = await (await fetch(dataUrl)).blob();
      // 若 JPEG 数据异常小，尝试 PNG 兜底（个别环境对 JPEG 支持异常会返回空白图）
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
      const subcard = out?.closest('.mid60-subcard');

      if (out) {
        // 手机端显示"当前值% / 临界值%"格式
        if (isMobile()) {
          out.textContent = `${fmt(v)}% / ${fmt(cutoff)}%`;
          // 添加原始值用于样式判断
          out.setAttribute('data-current', v);
          out.setAttribute('data-threshold', cutoff);
        } else {
          // 桌面端保持原有显示
          out.textContent = fmt(v);
          out.setAttribute('data-threshold', cutoff);
        }
      }

      if (bar) {
        bar.style.width = v + '%';
        // 根据是否超过临界值改变颜色
        if (v >= cutoff) {
          bar.style.background = 'linear-gradient(90deg, #f56c6c, #e94545)'; // 红色渐变
        } else {
          bar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)'; // 绿色渐变
        }
      }
      if (progressBar) {
        progressBar.setAttribute('aria-valuenow', Math.round(v));
      }

      // 手机端超阈值样式处理
      if (subcard && isMobile()) {
        if (v >= cutoff) {
          subcard.classList.add('over-threshold');
        } else {
          subcard.classList.remove('over-threshold');
        }
      }
    };

    // 计算并设置所有子量表
    Object.keys(MID60_SUBSCALES).forEach(key => {
      const scale = MID60_SUBSCALES[key];
      const mean = meanOf(scale.items);
      setSub(`mid60-${key}`, mean, scale.cutoff);
    });

    // 手机端/桌面端布局切换
    const results = qs('#mid60-results', root);
    const wasMobile = results && results.dataset.mobileMerged === '1';
    const isNowMobile = isMobile();

    if (isNowMobile && !wasMobile) {
      // 切换到移动端：构建移动端布局
      updateMobileLayout(root);
    } else if (!isNowMobile && wasMobile) {
      // 从移动端切换到桌面端：恢复原始布局
      restoreDesktopLayout(root);
    } else if (isNowMobile && wasMobile) {
      // 已经是移动端布局：只更新数值
      updateMobileLayout(root);
    }
  }

  // 恢复桌面端布局（当从移动端切换回桌面端时）
  function restoreDesktopLayout(root) {
    const results = qs('#mid60-results', root);
    if (!results || !results.dataset.mobileMerged) return;

    // 简单方案：给body添加一个类名，用CSS控制不同布局的显示/隐藏
    // 更优雅的方案是保存并恢复原始DOM，但这会增加复杂度
    // 当前方案：重新加载页面（用户调整窗口大小的场景较少）
    window.location.reload();
  }

  // 手机端卡片布局更新函数（按照期望图样：合并 DID/OSDD 为一张卡片，并为每组添加标题与总结）
  function updateMobileLayout(root) {
    const results = qs('#mid60-results', root);
    if (!results) return;

    // 标题文本到分组 key 的映射
    const titleToGroupKey = {
      '解离性身份障碍（DID）': 'did-osdd',
      'DID 与 OSDD': 'did-osdd',
      '人格解体/现实解体障碍（DP/DR）': 'dpdr',
      '解离性失忆': 'amnesia',
      '创伤后应激障碍（PTSD）': 'ptsd',
      '功能性神经症状障碍（FNSD/转换障碍）': 'fnsd',
      '一般解离子量表': 'general'
    };

    // 首次进入移动端时构建卡片结构（可重复调用，保证幂等）
    if (!results.dataset.mobileMerged) {
      // 收集所有标题 + 对应 subgrid
      const sections = [];
      qsa('.mid60-section-title', results).forEach((titleEl) => {
        const key = titleToGroupKey[titleEl.textContent.trim()];
        if (!key) return;
        let subgrid = titleEl.nextElementSibling;
        while (subgrid && !subgrid.classList?.contains('mid60-subgrid')) {
          subgrid = subgrid.nextElementSibling;
        }
        if (subgrid) sections.push({ key, titleEl, subgrid });
      });

      // 分组聚合：将同组的多个 subgrid 合并到一个新卡片容器中
      const grouped = {};
      sections.forEach(({ key, titleEl, subgrid }) => {
        (grouped[key] ||= { titles: [], subgrids: [] }).titles.push(titleEl);
        grouped[key].subgrids.push(subgrid);
      });

      const orderedKeys = Object.keys(MID60_GROUP_CONFIG)
        .sort((a, b) => (MID60_GROUP_CONFIG[a].order || 99) - (MID60_GROUP_CONFIG[b].order || 99))
        .filter((k) => grouped[k]);

      orderedKeys.forEach((key) => {
        const conf = MID60_GROUP_CONFIG[key];
        const bucket = grouped[key];
        const first = bucket.subgrids[0];

        // 新容器作为整组的卡片
        const card = document.createElement('div');
        card.className = 'mid60-subgrid';
        card.dataset.group = key;

        // 组标题（图标通过 CSS 伪元素渲染）
        const title = document.createElement('div');
        title.className = 'mid60-group-title';
        title.setAttribute('data-group', key);
        title.textContent = conf.title;
        card.appendChild(title);

        // 按配置顺序移动子量表项
        const moved = new Set();
        const findCardByScale = (scale) => {
          for (const sg of bucket.subgrids) {
            const badge = qs(`#mid60-${scale}-val`, sg);
            if (badge) return badge.closest('.mid60-subcard');
          }
          return null;
        };

        (conf.scales || []).forEach((scale) => {
          const itemCard = findCardByScale(scale);
          if (itemCard && !moved.has(itemCard)) {
            card.appendChild(itemCard);
            moved.add(itemCard);
          }
        });

        // 将剩余未被纳入顺序的子项也一并移动（容错）
        bucket.subgrids.forEach((sg) => {
          qsa('.mid60-subcard', sg).forEach((c) => {
            if (!moved.has(c)) card.appendChild(c);
          });
        });

        // 组总结占位
        const summary = document.createElement('div');
        summary.className = 'mid60-group-summary';
        card.appendChild(summary);

        // 插入到第一块原 subgrid 之前，并移除原标题和所有 subgrid
        results.insertBefore(card, first);
        bucket.titles.forEach((t) => t.remove());
        bucket.subgrids.forEach((sg) => sg.remove());
      });

      results.dataset.mobileMerged = '1';
    }

    // 刷新每组的状态总结（绿色=正常，红色=超阈值）
    qsa('.mid60-subgrid', results).forEach((card) => {
      const key = card.dataset.group || '';
      const summaryEl = qs('.mid60-group-summary', card);
      if (!summaryEl) return;

      const over = qsa('.mid60-subcard.over-threshold', card).length;
      const greenText = key === 'did-osdd' ? '全部低于临界值' : '正常范围';
      if (over === 0) {
        summaryEl.textContent = greenText;
        summaryEl.style.background = 'rgba(34, 197, 94, 0.15)';
        summaryEl.style.color = '#4ade80';
      } else {
        summaryEl.textContent = '存在临界超标';
        summaryEl.style.background = 'rgba(239, 68, 68, 0.15)';
        summaryEl.style.color = '#ef4444';
      }
    });
  }

  // 检查是否为移动端
  function isMobile() {
    return window.innerWidth <= 760;
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

    // 窗口大小变化监听器
    const handleResize = () => {
      updateResults(root);
    };
    window.addEventListener('resize', handleResize);

    // 保存清理函数以便后续调用
    root._mid60Cleanup = () => {
      window.removeEventListener('resize', handleResize);
    };

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
