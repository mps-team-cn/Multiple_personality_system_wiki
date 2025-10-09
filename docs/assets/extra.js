/**
 * Multiple Personality System Wiki 自定义脚本
 */

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
  // 为外部链接添加图标
  addExternalLinkIcons();

  // 优化中英文混排
  optimizeTypography();

  // 添加返回顶部功能增强
  enhanceBackToTop();
});

/**
 * 为外部链接添加图标
 */
function addExternalLinkIcons() {
  const links = document.querySelectorAll('.md-content a');
  links.forEach(link => {
    const href = link.getAttribute('href');
    if (href && (href.startsWith('http') || href.startsWith('//'))) {
      if (!link.hostname || link.hostname !== window.location.hostname) {
        link.classList.add('external-link');
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      }
    }
  });
}

/**
 * 优化中英文混排
 */
function optimizeTypography() {
  // 这里可以添加更多的排版优化逻辑
  // 例如自动在中英文之间添加间距等
}

/**
 * 增强返回顶部功能
 */
function enhanceBackToTop() {
  const backToTop = document.querySelector('.md-top');
  if (backToTop) {
    backToTop.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}

/**
 * 添加复制代码按钮的提示
 */
document$.subscribe(function() {
  const copyButtons = document.querySelectorAll('button[data-clipboard-target]');
  copyButtons.forEach(button => {
    button.addEventListener('click', function() {
      const original = this.textContent;
      this.textContent = '已复制!';
      setTimeout(() => {
        this.textContent = original;
      }, 2000);
    });
  });
});
