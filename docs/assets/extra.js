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

  // 初始化 QQ 群二维码弹窗
  initQQGroupModal();
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

/**
 * QQ 群二维码弹窗功能
 */
function initQQGroupModal() {
  // 创建弹窗 HTML 结构
  const modalHTML = `
    <div class="qq-modal-overlay" id="qqModalOverlay">
      <div class="qq-modal">
        <button class="qq-modal-close" id="qqModalClose" aria-label="关闭">×</button>
        <div class="qq-modal-content">
          <h3>加入 MPS Wiki 交流群</h3>
          <p>扫描二维码或搜索群号加入</p>
          <img src="assets/935527821.png" alt="QQ群二维码" class="qq-modal-qrcode">
          <div class="qq-group-number">935527821</div>
          <p class="qq-modal-hint">点击群号可复制</p>
        </div>
      </div>
    </div>
  `;

  // 将弹窗添加到页面
  document.body.insertAdjacentHTML('beforeend', modalHTML);

  const overlay = document.getElementById('qqModalOverlay');
  const modal = overlay.querySelector('.qq-modal');
  const closeBtn = document.getElementById('qqModalClose');
  const groupNumber = overlay.querySelector('.qq-group-number');

  // 为所有 QQ 群链接添加点击事件
  function attachQQGroupLinks() {
    const qqLinks = document.querySelectorAll('.qq-group-link');
    qqLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        openModal();
      });
    });
  }

  // 打开弹窗
  function openModal() {
    overlay.classList.add('show');
    document.body.style.overflow = 'hidden'; // 防止背景滚动
  }

  // 关闭弹窗
  function closeModal() {
    overlay.classList.remove('show');
    document.body.style.overflow = ''; // 恢复滚动
  }

  // 点击关闭按钮
  closeBtn.addEventListener('click', closeModal);

  // 点击遮罩层关闭
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) {
      closeModal();
    }
  });

  // 点击弹窗内容区域不关闭
  modal.addEventListener('click', function(e) {
    e.stopPropagation();
  });

  // ESC 键关闭
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && overlay.classList.contains('show')) {
      closeModal();
    }
  });

  // 点击群号复制
  groupNumber.addEventListener('click', function() {
    const number = '935527821';

    // 尝试使用现代 API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(number).then(function() {
        showCopySuccess();
      }).catch(function() {
        // 降级到传统方法
        fallbackCopy(number);
      });
    } else {
      // 降级到传统方法
      fallbackCopy(number);
    }
  });

  // 传统复制方法
  function fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-9999px';
    document.body.appendChild(textArea);
    textArea.select();

    try {
      document.execCommand('copy');
      showCopySuccess();
    } catch (err) {
      console.error('复制失败:', err);
    }

    document.body.removeChild(textArea);
  }

  // 显示复制成功提示
  function showCopySuccess() {
    const hint = overlay.querySelector('.qq-modal-hint');
    const originalText = hint.textContent;
    hint.textContent = '✓ 已复制群号';
    hint.style.color = '#4FC08D';
    hint.style.opacity = '1';

    setTimeout(() => {
      hint.textContent = originalText;
      hint.style.color = '';
      hint.style.opacity = '';
    }, 2000);
  }

  // 初始化链接
  attachQQGroupLinks();

  // 监听页面内容变化,重新绑定链接
  if (typeof document$ !== 'undefined') {
    document$.subscribe(function() {
      attachQQGroupLinks();
    });
  }
}
