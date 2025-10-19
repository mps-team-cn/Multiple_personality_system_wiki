/*
 * 解离经验量表（DES‑II）在线评估 - 纯前端实现
 * - 不存储数据（无 LocalStorage / 网络请求）
 * - 仅在包含 #des2-app 的页面激活
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function fmt(n) {
    return (Math.round(n * 10) / 10).toFixed(1);
  }

  function levelText(avg) {
    if (avg >= 46) return '极高（务必结合临床评估）';
    if (avg >= 30) return '高（建议尽快专业评估）';
    if (avg >= 20) return '中度（建议进一步临床评估）';
    if (avg >= 12) return '轻度（建议结合情境观察）';
    return '低（结合具体困扰与功能评估）';
  }

  function bindItem(item) {
    const input = qs('input[type="range"]', item);
    const out = qs('output, .des2-badge', item);
    if (!input || !out) return;

    // 限制交互：仅允许拖动改变数值（禁用滚轮与键盘调整）
    try {
      // 禁用鼠标滚轮改变数值
      input.addEventListener('wheel', (e) => {
        e.preventDefault();
      }, { passive: false });

      // 禁用键盘调整（方向键、Home/End、PageUp/PageDown、+/-）
      input.addEventListener('keydown', (e) => {
        const k = e.key;
        if (
          k === 'ArrowLeft' || k === 'ArrowRight' ||
          k === 'ArrowUp' || k === 'ArrowDown' ||
          k === 'Home' || k === 'End' ||
          k === 'PageUp' || k === 'PageDown' ||
          k === '+' || k === '-'
        ) {
          e.preventDefault();
          e.stopPropagation();
        }
      });
    } catch (_) { /* 忽略环境差异 */ }

    // 限制交互：禁止点击轨道直接跳值（需要最小拖拽位移）
    (function enforceDragOnly(el) {
      const STATE = {
        down: false,
        moved: false,
        startX: 0,
        startVal: String(el.value || '0'),
        pid: null,
      };
      const THRESHOLD = 5; // 像素阈值，超过视为拖动

      // 捕获阶段拦截 click：若未发生有效拖动，则还原数值并阻止默认跳转
      el.addEventListener('click', (e) => {
        if (!STATE.moved) {
          e.preventDefault();
          e.stopPropagation();
          if (el.value !== STATE.startVal) {
            el.value = STATE.startVal;
            el.dispatchEvent(new Event('input', { bubbles: true }));
          }
        }
        STATE.down = false;
        STATE.moved = false;
        STATE.pid = null;
      }, true);

      const onPointerDown = (e) => {
        STATE.down = true;
        STATE.moved = false;
        STATE.startX = e.clientX || 0;
        STATE.startVal = String(el.value || '0');
        if (e.pointerId != null) STATE.pid = e.pointerId;
      };

      const onPointerMove = (e) => {
        if (!STATE.down) return;
        if (STATE.pid != null && e.pointerId != null && e.pointerId !== STATE.pid) return;
        const dx = Math.abs((e.clientX || 0) - STATE.startX);
        if (dx > THRESHOLD) STATE.moved = true;
      };

      const onPointerUpCancel = () => {
        STATE.down = false;
        STATE.pid = null;
      };

      // Pointer Events 优先
      el.addEventListener('pointerdown', onPointerDown);
      el.addEventListener('pointermove', onPointerMove);
      el.addEventListener('pointerup', onPointerUpCancel);
      el.addEventListener('pointercancel', onPointerUpCancel);

      // 兼容旧浏览器：鼠标 & 触摸
      el.addEventListener('mousedown', (e) => onPointerDown(e));
      el.addEventListener('mousemove', (e) => onPointerMove(e));
      window.addEventListener('mouseup', onPointerUpCancel);
      el.addEventListener('touchstart', (e) => onPointerDown(e.touches[0] || e));
      el.addEventListener('touchmove', (e) => onPointerMove(e.touches[0] || e));
      window.addEventListener('touchend', onPointerUpCancel);
      window.addEventListener('touchcancel', onPointerUpCancel);
    })(input);

    const update = () => {
      out.textContent = input.value;
      // 可访问性：输出区域在数值变化时进行友好播报
      try {
        out.setAttribute('aria-live', 'polite');
        if (!out.getAttribute('aria-label')) out.setAttribute('aria-label', '当前项百分比');
      } catch (_) {}
    };
    input.addEventListener('input', update);
    update();
  }

  function collectValues(root) {
    const vals = [];
    qsa('.des2-item input[type="range"]', root).forEach((inp) => {
      const v = Number(inp.value || 0);
      if (!Number.isNaN(v)) vals.push(v);
    });
    return vals;
  }

  function updateResults(root) {
    const vals = collectValues(root);
    const n = vals.length || 1;
    const avg = vals.reduce((a, b) => a + b, 0) / n;

    const avgEl = qs('#des2-avg', root);
    const lvlEl = qs('#des2-level', root);
    const bar = qs('#des2-bar', root);
    if (avgEl) avgEl.textContent = fmt(avg);
    if (lvlEl) lvlEl.textContent = levelText(avg);
    if (bar) {
      const v = Math.max(0, Math.min(100, avg));
      bar.style.width = v + '%';
      // 可访问性：进度条角色与实时值
      try {
        bar.setAttribute('role', 'progressbar');
        bar.setAttribute('aria-valuemin', '0');
        bar.setAttribute('aria-valuemax', '100');
        bar.setAttribute('aria-valuenow', String(Math.round(v)));
      } catch (_) {}
    }

    // 子量表（NovoPsych 公布的常用分组）
    const groups = {
      amn: [3, 4, 5, 8, 25, 26],          // 记忆缺失 Amnesia
      dpdr: [7, 11, 12, 13, 27, 28],      // 人格/现实解体 DP/DR
      abs: [2, 14, 15, 17, 18, 20],       // 沉浸吸收 Absorption
    };

    const valueOf = (idx) => {
      const inp = qs(`#item${idx}`, root);
      const v = inp ? Number(inp.value || 0) : 0;
      return Number.isFinite(v) ? v : 0;
    };

    const meanOf = (arr) => arr.reduce((s, i) => s + valueOf(i), 0) / (arr.length || 1);

    const amn = meanOf(groups.amn);
    const dpdr = meanOf(groups.dpdr);
    const abs = meanOf(groups.abs);

    const setSub = (idBase, val) => {
      const v = Math.max(0, Math.min(100, val));
      const out = qs(`#${idBase}-val`, root);
      const bar = qs(`#${idBase}-bar`, root);
      if (out) out.textContent = fmt(v);
      if (bar) {
        bar.style.width = v + '%';
        try {
          bar.setAttribute('role', 'progressbar');
          bar.setAttribute('aria-valuemin', '0');
          bar.setAttribute('aria-valuemax', '100');
          bar.setAttribute('aria-valuenow', String(Math.round(v)));
        } catch (_) {}
      }
    };

    setSub('des2-amn', amn);
    setSub('des2-dpdr', dpdr);
    setSub('des2-abs', abs);
  }

  function resetAll(root) {
    qsa('.des2-item input[type="range"]', root).forEach((inp) => {
      inp.value = inp.getAttribute('value') || '0';
      inp.dispatchEvent(new Event('input'));
    });
    updateResults(root);
  }

  function fillAll(root, val) {
    const v = String(Math.max(0, Math.min(100, val)));
    qsa('.des2-item input[type="range"]', root).forEach((inp) => {
      inp.value = v;
      inp.dispatchEvent(new Event('input'));
    });
    updateResults(root);
  }

  function init(root) {
    // 绑定每一项的数值显示
    qsa('.des2-item', root).forEach(bindItem);

    // 主按钮
    const calcBtn = qs('#des2-calc', root);
    const resetBtn = qs('#des2-reset', root);
    const lowBtn = qs('#des2-fill-10', root);
    const midBtn = qs('#des2-fill-20', root);
    const highBtn = qs('#des2-fill-30', root);

    if (calcBtn) calcBtn.addEventListener('click', () => updateResults(root));
    if (resetBtn) resetBtn.addEventListener('click', () => resetAll(root));
    if (lowBtn) lowBtn.addEventListener('click', () => fillAll(root, 10));
    if (midBtn) midBtn.addEventListener('click', () => fillAll(root, 20));
    if (highBtn) highBtn.addEventListener('click', () => fillAll(root, 30));

    // 实时更新：任意滑块变动即刷新结果
    root.addEventListener('input', (e) => {
      const t = e.target;
      if (t && t.matches('input[type="range"]')) updateResults(root);
    });

    // 初始计算一次
    updateResults(root);
  }

  function initIfPresent() {
    const app = document.getElementById('des2-app');
    if (!app) return;
    if (app.dataset.des2Inited === '1') return;
    app.dataset.des2Inited = '1';
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
