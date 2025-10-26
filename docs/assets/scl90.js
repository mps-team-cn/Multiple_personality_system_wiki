/*
 * 症状自评量表修订版（SCL-90-R）在线评估 - 纯前端实现
 * - 不存储数据（无 LocalStorage / 网络请求）
 * - 仅在包含 #scl90-app 的页面激活
 * - 0-4 评分（SCL-90-R 标准），计算总分、因子分、阳性项目数、阳性症状均分
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function fmt(n) {
    return (Math.round(n * 100) / 100).toFixed(2);
  }

  // 九个因子的题目索引（从1开始）- SCL-90-R 标准
  const factors = {
    som: [1, 4, 12, 27, 40, 42, 48, 49, 52, 53, 56, 58], // 躯体化（12题）
    oc: [3, 9, 10, 28, 38, 45, 46, 51, 55, 65], // 强迫症状（10题）
    is: [6, 21, 34, 36, 37, 41, 61, 69, 73], // 人际敏感（9题）
    dep: [5, 14, 20, 22, 26, 29, 30, 31, 32, 54, 71, 79], // 抑郁（12题）
    anx: [17, 23, 33, 39, 57, 72, 78, 80, 86], // 焦虑（9题）
    hos: [11, 24, 63, 67, 74, 81], // 敌对（6题）
    phob: [13, 25, 47, 50, 70, 75, 82], // 恐怖（7题）
    par: [8, 18, 43, 68, 76, 83], // 偏执（6题）
    psy: [7, 16, 35, 62, 77, 84, 85, 87, 88, 90] // 精神病性（10题）
  };
  // 其他项目（不计入九个因子，仅计入总分和GSI）
  // 题目 19, 44, 59, 60, 64, 66, 89

  function bindItem(item) {
    const input = qs('input[type="range"]', item);
    const out = qs('output, .scl90-badge', item);
    if (!input || !out) return;

    // 可访问性属性
    const itemNumber = input.id.replace('item', '');
    const questionText = item.querySelector('td:nth-child(2)')?.textContent?.trim() || '';
    if (!input.hasAttribute('aria-label')) {
      input.setAttribute('aria-label', `题目 ${itemNumber}: ${questionText.substring(0, 30)}... - 评分 0 到 4`);
      input.setAttribute('tabindex', '0');
    }

    const update = () => {
      const val = Number(input.value || 0);
      out.textContent = val;
      try {
        out.setAttribute('aria-live', 'polite');
        if (!out.getAttribute('aria-label')) out.setAttribute('aria-label', '当前项评分');
      } catch (_) {}
    };
    input.addEventListener('input', update);
    update();
  }

  function collectValues(root) {
    const vals = [];
    for (let i = 1; i <= 90; i++) {
      const inp = qs(`#item${i}`, root);
      const v = inp ? Number(inp.value || 0) : 0;
      vals.push(Number.isFinite(v) ? v : 0);
    }
    return vals;
  }

  function calculateFactor(root, vals, items) {
    let sum = 0;
    items.forEach(idx => {
      sum += vals[idx - 1] || 0;
    });
    return sum / items.length;
  }

  function updateResults(root) {
    const vals = collectValues(root);
    const totalScore = vals.reduce((a, b) => a + b, 0);

    // GSI：所有90项的平均分
    const gsi = totalScore / 90;

    // 阳性项目数（评分 >= 1，SCL-90-R 标准）
    const pst = vals.filter(v => v >= 1).length;

    // 阳性症状均分
    const psdi = pst > 0 ? vals.filter(v => v >= 1).reduce((a, b) => a + b, 0) / pst : 0;

    // GSI 显示
    const gsiEl = qs('#scl90-gsi', root);
    const gsiBar = qs('#scl90-gsi-bar', root);
    const totalEl = qs('#scl90-total', root);
    const pstEl = qs('#scl90-pst', root);
    const psdiEl = qs('#scl90-psdi', root);

    if (gsiEl) gsiEl.textContent = fmt(gsi);
    if (totalEl) totalEl.textContent = totalScore;
    if (pstEl) pstEl.textContent = pst;
    if (psdiEl) psdiEl.textContent = fmt(psdi);

    if (gsiBar) {
      // GSI：0-4 转为 0-100%
      const percentage = Math.max(0, Math.min(100, (gsi / 4) * 100));
      gsiBar.style.width = percentage + '%';

      // 根据 GSI 设置进度条颜色（SCL-90-R 阈值：0.57-0.64）
      if (gsi >= 1.5) {
        gsiBar.style.background = 'linear-gradient(90deg, #f56c6c, #e94545)'; // 红色
      } else if (gsi >= 1.0) {
        gsiBar.style.background = 'linear-gradient(90deg, #e6a23c, #d89a2c)'; // 橙色
      } else if (gsi >= 0.6) {
        gsiBar.style.background = 'linear-gradient(90deg, #f0ad4e, #ec9c3e)'; // 黄色
      } else {
        gsiBar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)'; // 绿色
      }

      try {
        gsiBar.setAttribute('role', 'progressbar');
        gsiBar.setAttribute('aria-valuemin', '0');
        gsiBar.setAttribute('aria-valuemax', '4');
        gsiBar.setAttribute('aria-valuenow', fmt(gsi));
      } catch (_) {}
    }

    // 更新九个因子
    Object.keys(factors).forEach(key => {
      const factorScore = calculateFactor(root, vals, factors[key]);
      const valueEl = qs(`#scl90-${key}`, root);
      const barEl = qs(`#scl90-${key}-bar`, root);

      if (valueEl) valueEl.textContent = fmt(factorScore);
      if (barEl) {
        // 因子分：0-4 转为 0-100%
        const percentage = Math.max(0, Math.min(100, (factorScore / 4) * 100));
        barEl.style.width = percentage + '%';

        // 根据因子分设置颜色（SCL-90-R：因子分 >= 1.0 提示症状中等程度）
        if (factorScore >= 1.5) {
          barEl.style.background = 'linear-gradient(90deg, #f56c6c, #e94545)';
        } else if (factorScore >= 1.0) {
          barEl.style.background = 'linear-gradient(90deg, #e6a23c, #d89a2c)';
        } else if (factorScore >= 0.6) {
          barEl.style.background = 'linear-gradient(90deg, #f0ad4e, #ec9c3e)';
        } else {
          barEl.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)';
        }

        try {
          barEl.setAttribute('role', 'progressbar');
          barEl.setAttribute('aria-valuemin', '0');
          barEl.setAttribute('aria-valuemax', '4');
          barEl.setAttribute('aria-valuenow', fmt(factorScore));
        } catch (_) {}
      }
    });
  }

  function resetAll(root) {
    qsa('.scl90-item input[type="range"]', root).forEach((inp) => {
      inp.value = inp.getAttribute('value') || '0';
      inp.dispatchEvent(new Event('input'));
    });
    updateResults(root);
  }

  function init(root) {
    // 绑定每一项的数值显示
    qsa('.scl90-item', root).forEach(bindItem);

    // 重置按钮
    const resetBtn = qs('#scl90-reset', root);
    if (resetBtn) resetBtn.addEventListener('click', () => resetAll(root));

    // 实时更新：任意滑块变动即刷新结果
    root.addEventListener('input', (e) => {
      const t = e.target;
      if (t && t.matches('input[type="range"]')) updateResults(root);
    });

    // 初始计算一次
    updateResults(root);
  }

  function initIfPresent() {
    const app = document.getElementById('scl90-app');
    if (!app) return;
    if (app.dataset.scl90Inited === '1') return;
    app.dataset.scl90Inited = '1';
    init(app);
  }

  // 1) 常规页面加载
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initIfPresent);
  } else {
    initIfPresent();
  }

  // 2) 兼容 MkDocs Material 的 instant navigation（若未来开启）
  if (typeof window !== 'undefined' && window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => {
      // 内容区更新后再次尝试初始化
      setTimeout(initIfPresent, 0);
    });
  }
})();
