(function () {
  const DATA_ATTR = "data-label";

  function normalizeText(text) {
    return text.replace(/\s+/g, " ").trim();
  }

  function collectHeaders(table) {
    const headers = [];
    const thead = table.tHead;

    if (thead && thead.rows.length) {
      Array.from(thead.rows).forEach((row) => {
        Array.from(row.cells).forEach((cell, index) => {
          const text = normalizeText(cell.textContent || "");
          if (!text) return;
          headers[index] = headers[index]
            ? `${headers[index]} / ${text}`
            : text;
        });
      });
    }

    if (!headers.length) {
      const firstRow = table.rows[0];
      if (firstRow) {
        Array.from(firstRow.cells).forEach((cell, index) => {
          headers[index] = normalizeText(cell.textContent || "");
        });
      }
    }

    return headers;
  }

  function collectBodyRows(table, usedHeaderFromFirstRow) {
    if (table.tBodies && table.tBodies.length) {
      const rows = [];
      Array.from(table.tBodies).forEach((tbody) => {
        rows.push(...Array.from(tbody.rows));
      });
      return rows;
    }

    const rows = Array.from(table.rows);
    return usedHeaderFromFirstRow ? rows.slice(1) : rows;
  }

  function enhanceTable(table) {
    const headers = collectHeaders(table);
    const usedHeaderFromFirstRow =
      (!table.tHead || !table.tHead.rows.length) && headers.length > 0;
    const bodyRows = collectBodyRows(table, usedHeaderFromFirstRow);

    bodyRows.forEach((row) => {
      Array.from(row.cells).forEach((cell, index) => {
        if (cell.tagName && cell.tagName.toLowerCase() === "th") return;
        const label = headers[index] || "";
        if (label) {
          cell.setAttribute(DATA_ATTR, label);
        } else {
          cell.removeAttribute(DATA_ATTR);
        }
      });
    });
  }

  function enhanceAllTables() {
    const container =
      (window.Docsify && window.Docsify.dom.getNode(".markdown-section")) ||
      document.querySelector(".markdown-section");
    if (!container) return;
    const tables = container.querySelectorAll("table");
    tables.forEach((table) => enhanceTable(table));
  }

  window.$docsify = window.$docsify || {};
  const userPlugins = window.$docsify.plugins || [];

  window.$docsify.plugins = [].concat(
    function (hook) {
      hook.doneEach(function () {
        try {
          enhanceAllTables();
        } catch (error) {
          console.error("表格响应式增强失败", error);
        }
      });
    },
    userPlugins
  );
})();
