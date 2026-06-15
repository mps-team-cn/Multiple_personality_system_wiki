/*
 * ECR 中文版教育性评分页逻辑
 * - 纯前端，不存储数据
 * - 反向计分：8 - 原始分
 */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function setText(root, id, text) {
    const node = qs(`#${id}`, root);
    if (node) node.textContent = text;
  }

  function average(values) {
    if (!values.length) return null;
    return values.reduce((sum, value) => sum + value, 0) / values.length;
  }

  function level(value) {
    if (value === null) return { text: "未完成", className: "mid" };
    if (value < 3.5) return { text: "较低", className: "low" };
    if (value < 4.5) return { text: "中间", className: "mid" };
    return { text: "较高", className: "high" };
  }

  function pattern(anxiety, avoidance) {
    if (anxiety === null || avoidance === null) return "完成全部题目后显示二维参考。";
    const highAnxiety = anxiety >= 4;
    const highAvoidance = avoidance >= 4;
    if (!highAnxiety && !highAvoidance) return "低焦虑、低回避：更接近安全型关系策略。";
    if (highAnxiety && !highAvoidance) return "高焦虑、低回避：更接近焦虑-沉溺型关系策略。";
    if (!highAnxiety && highAvoidance) return "低焦虑、高回避：更接近疏离-回避型关系策略。";
    return "高焦虑、高回避：更接近恐惧-回避型关系策略。";
  }

  function progressWidth(value) {
    if (value === null) return "0%";
    return `${Math.max(0, Math.min(100, ((value - 1) / 6) * 100))}%`;
  }

  function itemNumberFromId(id) {
    const match = String(id || "").match(/(\d+)$/);
    return match ? match[1] : "";
  }

  function valueLabel(value) {
    const labels = {
      1: "非常不同意",
      4: "中间",
      7: "非常同意"
    };
    return labels[value] ? `${value} ${labels[value]}` : String(value);
  }

  function setRangeAria(input) {
    if (!input) return;
    if (input.dataset.empty === "true") {
      input.setAttribute("aria-valuetext", "未作答，初始位置为 4 中间");
    } else {
      input.setAttribute("aria-valuetext", valueLabel(Number(input.value || 4)));
    }
  }

  function selectToRange(select) {
    const input = document.createElement("input");
    input.id = select.id;
    input.type = "range";
    input.min = "1";
    input.max = "7";
    input.step = "1";
    input.value = select.value || "4";
    input.dataset.empty = select.value ? "false" : "true";
    input.setAttribute("tabindex", "0");
    select.replaceWith(input);
    return input;
  }

  function collect(root) {
    const rows = qsa(".ecr-item", root);
    const scores = [];
    const anxiety = [];
    const avoidance = [];

    rows.forEach((row) => {
      const control = qs('input[type="range"], select', row);
      const badge = qs(".ecr-badge", row);
      const isEmptyRange = control && control.matches('input[type="range"]') && control.dataset.empty === "true";
      const raw = control && control.value && !isEmptyRange ? Number(control.value) : null;
      const reverse = row.dataset.reverse === "true";
      const scored = raw === null ? null : reverse ? 8 - raw : raw;

      if (badge) badge.textContent = scored === null ? "-" : String(scored);
      if (control && control.matches('input[type="range"]')) setRangeAria(control);
      if (scored !== null) {
        scores.push(scored);
        if (row.dataset.subscale === "anxiety") anxiety.push(scored);
        if (row.dataset.subscale === "avoidance") avoidance.push(scored);
      }
    });

    return {
      count: scores.length,
      total: rows.length,
      anxiety: anxiety.length === 18 ? average(anxiety) : null,
      avoidance: avoidance.length === 18 ? average(avoidance) : null
    };
  }

  function update(root) {
    const result = collect(root);
    const anxietyLevel = level(result.anxiety);
    const avoidanceLevel = level(result.avoidance);

    setText(root, "ecr-completion", `${result.count}/${result.total}`);
    setText(root, "ecr-anxiety-score", result.anxiety === null ? "-" : result.anxiety.toFixed(2));
    setText(root, "ecr-avoidance-score", result.avoidance === null ? "-" : result.avoidance.toFixed(2));
    setText(root, "ecr-pattern", pattern(result.anxiety, result.avoidance));

    const anxietyStatus = qs("#ecr-anxiety-level", root);
    if (anxietyStatus) {
      anxietyStatus.textContent = anxietyLevel.text;
      anxietyStatus.className = `ecr-status ${anxietyLevel.className}`;
    }

    const avoidanceStatus = qs("#ecr-avoidance-level", root);
    if (avoidanceStatus) {
      avoidanceStatus.textContent = avoidanceLevel.text;
      avoidanceStatus.className = `ecr-status ${avoidanceLevel.className}`;
    }

    const anxietyBar = qs("#ecr-anxiety-bar", root);
    if (anxietyBar) anxietyBar.style.width = progressWidth(result.anxiety);

    const avoidanceBar = qs("#ecr-avoidance-bar", root);
    if (avoidanceBar) avoidanceBar.style.width = progressWidth(result.avoidance);
  }

  function reset(root) {
    qsa('.ecr-item input[type="range"], .ecr-item select', root).forEach((control) => {
      if (control.matches('input[type="range"]')) {
        control.value = "4";
        control.dataset.empty = "true";
        setRangeAria(control);
      } else {
        control.value = "";
      }
    });
    update(root);
  }

  function bindItem(root, row) {
    let control = qs('input[type="range"], select', row);
    if (!control) return;

    if (control.matches("select")) {
      control = selectToRange(control);
    }

    const prompt = row.querySelector("td:nth-child(2)")?.textContent?.trim() || "";
    const itemNumber = row.dataset.item || itemNumberFromId(control.id);
    control.setAttribute("aria-label", `ECR 题目 ${itemNumber}: ${prompt.slice(0, 42)} - 评分 1 到 7`);
    setRangeAria(control);

    const markAnswered = () => {
      if (control.matches('input[type="range"]')) {
        control.dataset.empty = "false";
      }
      update(root);
    };

    control.addEventListener("input", markAnswered);
    control.addEventListener("change", markAnswered);
  }

  function init() {
    const root = document.getElementById("ecr-app");
    if (!root || root.dataset.inited === "1") return;
    root.dataset.inited = "1";

    qsa(".ecr-item", root).forEach((row) => bindItem(root, row));

    const resetBtn = qs("#ecr-reset", root);
    if (resetBtn) resetBtn.addEventListener("click", () => reset(root));

    update(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  if (typeof window !== "undefined" && window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(() => setTimeout(init, 0));
  }
})();
