/*
 * 躯体形式解离问卷（SDQ‑20）在线评估 - 纯前端实现
 * - 不存储数据（无 LocalStorage / 网络请求）
 * - 仅在包含 #sdq20-app 的页面激活
 * - 1-5 评分，转换为百分比显示（便于可视化）
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function fmt(n) {
    return (Math.round(n * 10) / 10).toFixed(1);
  }

  function levelText(score) {
    // 参考研究文献的区间（仅供参考，非诊断标准）
    if (score >= 50) return '高度躯体解离症状（常见于 DID，需专业评估）';
    if (score >= 40) return '显著躯体解离症状（常见于 DDNOS/OSDD，建议专业评估）';
    if (score >= 30) return '中度躯体解离症状（可能存在解离障碍，建议临床评估）';
    if (score >= 25) return '轻度躯体解离症状（建议结合临床观察）';
    return '低躯体解离症状（结合具体困扰评估）';
  }

  function bindItem(item) {
    const input = qs('input[type="range"]', item);
    const out = qs('output, .sdq20-badge', item);
    if (!input || !out) return;

    // 清理历史遗留的刻度包装（如存在则移除 wrapper 与 marks）
    try {
      const p = input.parentElement;
      if (p && p.classList && p.classList.contains('sdq20-slider-wrap')) {
        const host = p.parentElement || item;
        host.insertBefore(input, p);
        p.remove();
      }
    } catch (_) { /* ignore */ }

    // 为滑块添加可访问性属性
    const itemNumber = input.id.replace('item', '');
    const questionText = item.querySelector('td:nth-child(2)')?.textContent?.trim() || '';
    if (!input.hasAttribute('aria-label')) {
      input.setAttribute('aria-label', `题目 ${itemNumber}: ${questionText.substring(0, 30)}... - 评分 1 到 5`);
      input.setAttribute('tabindex', '0');
    }

    const update = () => {
      const val = Number(input.value || 1);
      out.textContent = val;
      // 可访问性：输出区域在数值变化时进行友好播报
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
    qsa('.sdq20-item input[type="range"]', root).forEach((inp) => {
      const v = Number(inp.value || 1);
      if (!Number.isNaN(v)) vals.push(v);
    });
    return vals;
  }

  function updateResults(root) {
    const vals = collectValues(root);
    const totalScore = vals.reduce((a, b) => a + b, 0);
    const n = vals.length || 1;

    // 总分显示
    const scoreEl = qs('#sdq20-score', root);
    const lvlEl = qs('#sdq20-level', root);
    const bar = qs('#sdq20-bar', root);

    if (scoreEl) scoreEl.textContent = totalScore;
    if (lvlEl) lvlEl.textContent = levelText(totalScore);

    if (bar) {
      // 将总分转换为百分比用于进度条显示（20-100分转为0-100%）
      const percentage = Math.max(0, Math.min(100, ((totalScore - 20) / 80) * 100));
      bar.style.width = percentage + '%';

      // 根据分数设置进度条颜色
      if (totalScore >= 50) {
        bar.style.background = 'linear-gradient(90deg, #f56c6c, #e94545)'; // 红色
      } else if (totalScore >= 40) {
        bar.style.background = 'linear-gradient(90deg, #e6a23c, #d89a2c)'; // 橙色
      } else if (totalScore >= 30) {
        bar.style.background = 'linear-gradient(90deg, #f0ad4e, #ec9c3e)'; // 黄色
      } else {
        bar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)'; // 绿色
      }

      // 可访问性：进度条角色与实时值
      try {
        bar.setAttribute('role', 'progressbar');
        bar.setAttribute('aria-valuemin', '20');
        bar.setAttribute('aria-valuemax', '100');
        bar.setAttribute('aria-valuenow', String(totalScore));
      } catch (_) {}
    }

    // SDQ-5 子集（题目 4, 8, 13, 15, 18）
    const sdq5Items = [4, 8, 13, 15, 18];
    const sdq5Score = sdq5Items.reduce((sum, idx) => {
      const inp = qs(`#item${idx}`, root);
      const v = inp ? Number(inp.value || 1) : 1;
      return sum + (Number.isFinite(v) ? v : 1);
    }, 0);

    const sdq5El = qs('#sdq20-sdq5', root);
    const sdq5Bar = qs('#sdq20-sdq5-bar', root);

    if (sdq5El) sdq5El.textContent = sdq5Score;
    if (sdq5Bar) {
      // SDQ-5: 5-25分转为0-100%
      const percentage = Math.max(0, Math.min(100, ((sdq5Score - 5) / 20) * 100));
      sdq5Bar.style.width = percentage + '%';

      // 根据 SDQ-5 分数设置颜色
      if (sdq5Score >= 15) {
        sdq5Bar.style.background = 'linear-gradient(90deg, #f56c6c, #e94545)';
      } else if (sdq5Score >= 10) {
        sdq5Bar.style.background = 'linear-gradient(90deg, #f0ad4e, #ec9c3e)';
      } else {
        sdq5Bar.style.background = 'linear-gradient(90deg, #4fc08d, #3fb489)';
      }

      try {
        sdq5Bar.setAttribute('role', 'progressbar');
        sdq5Bar.setAttribute('aria-valuemin', '5');
        sdq5Bar.setAttribute('aria-valuemax', '25');
        sdq5Bar.setAttribute('aria-valuenow', String(sdq5Score));
      } catch (_) {}
    }
  }

  function resetAll(root) {
    qsa('.sdq20-item input[type="range"]', root).forEach((inp) => {
      inp.value = inp.getAttribute('value') || '1';
      inp.dispatchEvent(new Event('input'));
    });
    updateResults(root);
  }

  function init(root) {
    // 绑定每一项的数值显示
    qsa('.sdq20-item', root).forEach(bindItem);

    // 重置按钮
    const resetBtn = qs('#sdq20-reset', root);
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
    const app = document.getElementById('sdq20-app');
    if (!app) return;
    if (app.dataset.sdq20Inited === '1') return;
    app.dataset.sdq20Inited = '1';
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
