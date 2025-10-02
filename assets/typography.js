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

  function needsSpacing(value) {
    return spacingRules.some((rule) => {
      rule.lastIndex = 0;
      return rule.test(value);
    });
  }

  function applySpacingToText(value) {
    let result = value;
    for (const rule of spacingRules) {
      result = result.replace(rule, "$1 $2");
    }
    return result;
  }

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
