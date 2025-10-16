(function () {
  'use strict';

  // 认为是"高级语法"就不自动改写：已有引号、通配/模糊、字段、括号等
  const hasAdvancedSyntax = s => /["*~:()]/.test(s);

  // 包一层引号（若前缀有 + 或 -，保留在前）
  const quoteToken = (tok) => {
    // 已有引号则不处理
    if (/^["].*["]$/.test(tok)) return tok;

    // 分离前缀操作符
    const m = tok.match(/^([+\-]?)(.+)$/);
    const prefix = m ? m[1] : '';
    const body   = m ? m[2] : tok;

    // 空串直接返回
    if (!body) return tok;

    return `${prefix}"${body}"`;
  };

  // 处理搜索表单提交
  function handleSearchSubmit(e) {
    const form = e.target;
    const input = form.querySelector('input[type="search"], input[type="text"]');
    if (!input) return;

    const raw = (input.value || '').trim();
    if (!raw) return;

    // 检测高级语法，尊重用户原始输入
    if (hasAdvancedSyntax(raw)) return;

    // 以空白分词（含全角空格）
    const parts = raw.split(/\s+/u).filter(Boolean);

    if (parts.length <= 1) {
      // 无空格 → 整体短语
      input.value = `"${raw}"`;
    } else {
      // 有空格 → 每个词作为短语（保留 + / - 前缀）
      input.value = parts.map(quoteToken).join(' ');
    }
  }

  // 使用事件委托优化性能
  function initSearchOptimization() {
    // 使用事件委托监听所有搜索表单
    document.addEventListener('submit', function(e) {
      const form = e.target.closest('form[role="search"]');

      // 更精确的检测：确保是 MkDocs Material 的搜索表单
      if (form) {
        const input = form.querySelector('input[type="search"], input[type="text"]');
        // 检查是否是 MkDocs Material 搜索表单（通常包含特定的 class 或 data 属性）
        const isMkDocsSearch = input && (
          input.classList.contains('md-search__input') ||
          form.closest('.md-search') ||
          input.name === 'query'
        );

        if (isMkDocsSearch) {
          handleSearchSubmit(e);
        }
      }
    }, { capture: true, passive: true });
  }

  // 延迟初始化，避免阻塞页面加载
  if ('requestIdleCallback' in window) {
    requestIdleCallback(initSearchOptimization, { timeout: 1000 });
  } else {
    // 降级方案：使用 setTimeout
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        setTimeout(initSearchOptimization, 100);
      });
    } else {
      setTimeout(initSearchOptimization, 100);
    }
  }
})();
