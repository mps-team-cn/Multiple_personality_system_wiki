(function () {
  "use strict";

  /**
   * 侧边栏开关增强：为按钮增加图标容器与中文标签
   * 便于移动端用户理解该控件负责打开目录
   */
  function enhanceSidebarToggle(button) {
    if (!button || button.dataset.enhanced === "1") return;

    button.dataset.enhanced = "1";
    button.setAttribute("aria-label", "切换目录");
    button.setAttribute("title", "切换目录");

    const iconWrapper = document.createElement("span");
    iconWrapper.className = "sidebar-toggle__icon";

    while (button.firstChild) {
      iconWrapper.appendChild(button.firstChild);
    }

    const label = document.createElement("span");
    label.className = "sidebar-toggle__label";
    label.textContent = "目录";

    button.appendChild(iconWrapper);
    button.appendChild(label);
  }

  /**
   * 监听按钮插入，确保 Docsify 初始化后也能完成增强
   */
  function observeToggle() {
    const existing = document.querySelector(".sidebar-toggle");
    if (existing) {
      enhanceSidebarToggle(existing);
      return;
    }

    const observer = new MutationObserver(function () {
      const target = document.querySelector(".sidebar-toggle");
      if (target) {
        enhanceSidebarToggle(target);
        observer.disconnect();
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", observeToggle);
  } else {
    observeToggle();
  }
})();
