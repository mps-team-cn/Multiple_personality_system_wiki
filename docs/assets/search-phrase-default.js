(function () {
  // 认为是“高级语法”就不自动改写：已有引号、通配/模糊、字段、括号等
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

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[role="search"]').forEach((form) => {
      const input = form.querySelector('input[type="search"],input[type="text"]');
      if (!input) return;

      form.addEventListener('submit', () => {
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
          // 如需强制 AND，可改为：
          // input.value = parts.map(t => quoteToken(t.startsWith('+')||t.startsWith('-') ? t : '+'+t)).join(' ');
        }
      });
    });
  });
})();
