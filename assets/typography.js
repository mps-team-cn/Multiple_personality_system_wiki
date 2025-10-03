(function () {
  const CJK_RANGE = "\\u2E80-\\u2FFF\\u3000-\\u303F\\u3040-\\u30FF\\u3400-\\u4DBF\\u4E00-\\u9FFF\\uF900-\\uFAFF";
  const LATIN_SYMBOLS = "A-Za-z0-9@&=_\\$%\\^\\*\\+\\-\\\\/\\|:;\\?!~`";
  const OPEN_PUNCT = "\\(\\[\\{<\"'";
  const CLOSE_PUNCT = "\\)\\]\\}>\"'";

  const spacingRules = [
    new RegExp(`([${CJK_RANGE}])([${LATIN_SYMBOLS}])`, "g"),
    new RegExp(`([${LATIN_SYMBOLS}])([${CJK_RANGE}])`, "g"),
    new RegExp(`([${CJK_RANGE}])([${OPEN_PUNCT}])`, "g"),
    new RegExp(`([${CLOSE_PUNCT}])([${CJK_RANGE}])`, "g"),
  ];

  const IGNORED_TAGS = new Set([
    "CODE",
    "PRE",
    "KBD",
    "SAMP",
    "VAR",
    "SCRIPT",
    "STYLE",
    "TEXTAREA",
  ]);

  // 检测文本是否命中中西文混排模式，命中则需要插入空格
  function needsSpacing(value) {
    return spacingRules.some((rule) => {
      rule.lastIndex = 0;
      return rule.test(value);
    });
  }

  // 对文本按规则插入空格，保持原有顺序逐条替换
  function applySpacingToText(value) {
    let result = value;
    for (const rule of spacingRules) {
      result = result.replace(rule, "$1 $2");
    }
    return result;
  }

  // 跳过代码块等不应自动加空格的节点，支持通过 class 手动关闭
  function shouldSkipNode(node, root) {
    let current = node.parentNode;
    while (current && current !== root) {
      if (current.nodeType !== Node.ELEMENT_NODE) {
        current = current.parentNode;
        continue;
      }
      if (IGNORED_TAGS.has(current.tagName)) {
        return true;
      }
      if (current.classList && current.classList.contains("no-auto-spacing")) {
        return true;
      }
      current = current.parentNode;
    }
    return false;
  }

  // 遍历容器内所有文本节点并按需添加空格
  function processContainer(root) {
    if (!root) return;

    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          if (!node.nodeValue || !node.nodeValue.trim()) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        },
      },
    );

    const textNodes = [];
    while (walker.nextNode()) {
      textNodes.push(walker.currentNode);
    }

    for (const textNode of textNodes) {
      if (shouldSkipNode(textNode, root)) continue;

      const original = textNode.nodeValue;
      if (!needsSpacing(original)) continue;

      const spaced = applySpacingToText(original);
      if (spaced !== original) {
        textNode.nodeValue = spaced;
      }
    }
  }

  // 渲染完成后延迟执行，避免与 Docsify 更新冲突
  function scheduleSpacing() {
    const container = document.querySelector(".markdown-section");
    if (!container) return;

    requestAnimationFrame(() => {
      processContainer(container);
    });
  }

  const plugin = function (hook) {
    hook.doneEach(() => {
      scheduleSpacing();
    });
  };

  window.$docsify = window.$docsify || {};
  window.$docsify.plugins = (window.$docsify.plugins || []).concat(plugin);
})();
