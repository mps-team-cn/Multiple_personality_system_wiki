/*
 * PHQ-9 / GAD-7 简式量表共享前端逻辑
 * - 纯前端，不存储数据
 * - 仅在对应页面存在时激活
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function nextFrame() {
    return new Promise((resolve) => requestAnimationFrame(resolve));
  }

  const IMPAIRMENT_TEXT = {
    "": "未选择",
    none: "完全不困难",
    somewhat: "有点困难",
    very: "非常困难",
    extremely: "极度困难"
  };

  const CONFIGS = {
    phq9: {
      title: "PHQ-9 抑郁筛查结果",
      fileName: "PHQ-9-结果",
      totalItems: 9,
      maxScore: 27,
      cutoffLabel: "进一步评估阈值：总分 ≥ 10",
      severity(score) {
        if (score >= 20) return { text: "重度抑郁", class: "severe" };
        if (score >= 15) return { text: "中重度抑郁", class: "moderate" };
        if (score >= 10) return { text: "中度抑郁", class: "mild" };
        if (score >= 5) return { text: "轻度抑郁", class: "mild" };
        return { text: "无或极轻", class: "none" };
      },
      progressColor(score) {
        if (score >= 20) return "linear-gradient(90deg, #f44336, #d32f2f)";
        if (score >= 15) return "linear-gradient(90deg, #ff9800, #f57c00)";
        if (score >= 10) return "linear-gradient(90deg, #9c27b0, #7b1fa2)";
        if (score >= 5) return "linear-gradient(90deg, #81c784, #4caf50)";
        return "linear-gradient(90deg, #4fc08d, #3fb489)";
      },
      secondary(root, scores) {
        const phq2 = (scores[0] || 0) + (scores[1] || 0);
        const algorithmCount = scores.reduce((acc, value, index) => {
          if (index === 8) return acc + (value >= 1 ? 1 : 0);
          return acc + (value >= 2 ? 1 : 0);
        }, 0);
        const corePositive = (scores[0] || 0) >= 2 || (scores[1] || 0) >= 2;
        let hint = "当前未达到 PHQ 抑郁模块的常见阳性筛查阈值。";
        if (corePositive && algorithmCount >= 5) {
          hint = "达到 PHQ 抑郁模块中“重性抑郁综合征”常见筛查阈值，建议尽快结合专业访谈进一步评估。";
        } else if (corePositive && algorithmCount >= 2) {
          hint = "达到 PHQ 抑郁模块中“其他抑郁综合征”常见筛查阈值，建议继续观察并考虑专业评估。";
        } else if ((scores[8] || 0) >= 1) {
          hint = "虽然总分未必很高，但第 9 题出现阳性反应，仍建议尽快与专业人员讨论当前风险。";
        }

        const positiveCount = scores.reduce((acc, value, index) => {
          if (index === 8) return acc + (value >= 1 ? 1 : 0);
          return acc + (value >= 2 ? 1 : 0);
        }, 0);

        const item9 = scores[8] || 0;
        setText(root, "phq9-phq2", `${phq2}/6`);
        setText(root, "phq9-positive-count", `${positiveCount}/9`);
        setText(root, "phq9-screening-hint", hint);
        setText(root, "phq9-item9", item9 >= 1 ? "有阳性反应" : "未见阳性反应");

        const safety = qs("#phq9-safety-alert", root);
        if (safety) {
          safety.style.display = item9 >= 1 || total(scores) >= 15 ? "block" : "none";
        }
      }
    },
    gad7: {
      title: "GAD-7 焦虑筛查结果",
      fileName: "GAD-7-结果",
      totalItems: 7,
      maxScore: 21,
      cutoffLabel: "进一步评估阈值：总分 ≥ 10",
      severity(score) {
        if (score >= 15) return { text: "重度焦虑", class: "severe" };
        if (score >= 10) return { text: "中度焦虑", class: "moderate" };
        if (score >= 5) return { text: "轻度焦虑", class: "mild" };
        return { text: "无或极轻", class: "minimal" };
      },
      progressColor(score) {
        if (score >= 15) return "linear-gradient(90deg, #f44336, #d32f2f)";
        if (score >= 10) return "linear-gradient(90deg, #9c27b0, #7b1fa2)";
        if (score >= 5) return "linear-gradient(90deg, #ff9800, #f57c00)";
        return "linear-gradient(90deg, #4fc08d, #3fb489)";
      },
      secondary(root, scores) {
        const gad2 = (scores[0] || 0) + (scores[1] || 0);
        const highFreqCount = scores.filter((value) => value >= 2).length;
        let hint = "当前未达到 GAD-7 的常见进一步评估阈值。";
        const sum = total(scores);
        if (sum >= 10) {
          hint = "达到 GAD-7 常见进一步评估阈值，建议结合访谈区分广泛性焦虑、惊恐、社交焦虑或创伤相关焦虑。";
        } else if (gad2 >= 3) {
          hint = "GAD-2 子分达到常见阳性筛查阈值，即使总分未满 10，也值得继续观察或补充评估。";
        }

        setText(root, "gad7-gad2", `${gad2}/6`);
        setText(root, "gad7-positive-count", `${highFreqCount}/7`);
        setText(root, "gad7-screening-hint", hint);

        const safety = qs("#gad7-safety-alert", root);
        if (safety) {
          safety.style.display = sum >= 15 ? "block" : "none";
        }
      }
    }
  };

  function total(scores) {
    return scores.reduce((acc, value) => acc + value, 0);
  }

  function setText(root, id, text) {
    const node = qs(`#${id}`, root);
    if (node) node.textContent = text;
  }

  async function ensureHtmlToImage() {
    if (window.htmlToImage) return window.htmlToImage;
    const src = "https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.min.js";
    await new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = () => reject(new Error("无法加载导出库"));
      document.head.appendChild(s);
    });
    return window.htmlToImage;
  }

  async function exportResultsImage(prefix, root, title, fileName) {
    const node = qs(`#${prefix}-results`, root);
    if (!node) return;
    let wm = null;
    try {
      const h2i = await ensureHtmlToImage();
      const bg = getComputedStyle(document.body).backgroundColor || "#ffffff";

      wm = document.createElement("div");
      wm.className = "brief-scale-watermark";
      wm.textContent = "wiki.mpsteam.cn";
      node.appendChild(wm);

      try { if (document.fonts && document.fonts.ready) await document.fonts.ready; } catch (_) {}
      await nextFrame();
      await nextFrame();

      const dataUrl = await h2i.toJpeg(node, {
        width: Math.ceil(node.scrollWidth + 2),
        height: Math.ceil(node.scrollHeight + 2),
        cacheBust: true,
        pixelRatio: Math.min(2, window.devicePixelRatio || 1.5),
        backgroundColor: bg,
        style: {
          padding: "20px",
          boxSizing: "border-box",
          backgroundColor: bg
        }
      });

      const blob = await (await fetch(dataUrl)).blob();
      let file = null;
      try {
        file = new File([blob], `${fileName}.jpg`, { type: blob.type || "image/jpeg" });
      } catch (_) {}

      if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title,
          text: "来自 wiki.mpsteam.cn"
        });
        return;
      }

      if (navigator.clipboard && window.ClipboardItem) {
        try {
          await navigator.clipboard.write([new ClipboardItem({ [blob.type]: blob })]);
          alert("图片已复制，可直接粘贴到聊天");
          return;
        } catch (_) {}
      }

      const a = document.createElement("a");
      a.href = dataUrl;
      a.download = `${fileName}.jpg`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error(err);
      alert("导出失败，请重试");
    } finally {
      if (wm && wm.parentNode) {
        wm.remove();
      }
    }
  }

  function bindSelect(prefix, item) {
    const select = qs("select", item);
    const badge = qs(".brief-scale-badge", item);
    if (!select || !badge) return;

    const questionText = item.querySelector("td:nth-child(2)")?.textContent?.trim() || "";
    if (!select.hasAttribute("aria-label")) {
      select.setAttribute(
        "aria-label",
        `${prefix.toUpperCase()} 题目 ${select.id.replace("item", "")}: ${questionText.substring(0, 40)}`
      );
    }

    const update = () => {
      const value = Number(select.value || 0);
      badge.textContent = String(value);
    };

    select.addEventListener("change", update);
    update();
  }

  function collectScores(prefix, root) {
    return qsa(`.${prefix}-item select`, root).map((select) => Number(select.value || 0));
  }

  function updateResults(prefix, root, config) {
    const scores = collectScores(prefix, root);
    const sum = total(scores);
    const severity = config.severity(sum);

    setText(root, `${prefix}-raw-score`, String(sum));

    const severityNode = qs(`#${prefix}-severity`, root);
    if (severityNode) {
      severityNode.textContent = severity.text;
      severityNode.className = `brief-scale-status ${severity.class}`;
    }

    const progressBar = qs(`#${prefix}-progress-bar`, root);
    if (progressBar) {
      progressBar.style.width = `${Math.max(0, Math.min(100, (sum / config.maxScore) * 100))}%`;
      progressBar.style.background = config.progressColor(sum);
    }

    const progress = qs(`#${prefix}-progress`, root);
    if (progress) progress.setAttribute("aria-valuenow", String(sum));

    setText(root, `${prefix}-completion`, `${scores.length}/${config.totalItems} (100%)`);
    setText(root, `${prefix}-cutoff`, sum >= 10 ? "达到常见进一步评估阈值" : "未达到常见进一步评估阈值");
    setText(root, `${prefix}-impairment-text`, IMPAIRMENT_TEXT[qs(`#${prefix}-impairment`, root)?.value || ""]);

    config.secondary(root, scores);
  }

  function resetAll(prefix, root, config) {
    qsa(`.${prefix}-item select`, root).forEach((select) => {
      select.value = "0";
      select.dispatchEvent(new Event("change"));
    });
    const impairment = qs(`#${prefix}-impairment`, root);
    if (impairment) impairment.value = "";
    updateResults(prefix, root, config);
  }

  function initScale(prefix) {
    const config = CONFIGS[prefix];
    const root = document.getElementById(`${prefix}-app`);
    if (!config || !root || root.dataset.inited === "1") return;
    root.dataset.inited = "1";

    qsa(`.${prefix}-item`, root).forEach((item) => bindSelect(prefix, item));

    const resetBtn = qs(`#${prefix}-reset`, root);
    if (resetBtn) {
      resetBtn.addEventListener("click", () => resetAll(prefix, root, config));
    }

    const actions = qs(".brief-scale-actions", root) || root;
    let exportBtn = qs(`#${prefix}-export`, actions);
    if (!exportBtn) {
      exportBtn = document.createElement("button");
      exportBtn.id = `${prefix}-export`;
      exportBtn.className = "md-button md-button--primary";
      exportBtn.type = "button";
      exportBtn.textContent = "导出图片";
      actions.appendChild(exportBtn);
    }
    exportBtn.addEventListener("click", () => exportResultsImage(prefix, root, config.title, config.fileName));

    root.addEventListener("change", (event) => {
      const target = event.target;
      if (target && target.matches("select")) updateResults(prefix, root, config);
    });

    const cutoffLabel = qs(`#${prefix}-cutoff-label`, root);
    if (cutoffLabel) cutoffLabel.textContent = config.cutoffLabel;

    updateResults(prefix, root, config);
  }

  function initAll() {
    initScale("phq9");
    initScale("gad7");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }

  if (typeof window !== "undefined" && window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(() => {
      setTimeout(initAll, 0);
    });
  }
})();
