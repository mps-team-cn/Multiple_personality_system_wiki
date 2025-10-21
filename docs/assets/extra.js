/**
 * Multiple Personality System Wiki 自定义脚本
 * 性能优化版本 - 使用事件委托和 requestIdleCallback
 */

// 使用 requestIdleCallback 延迟非关键任务
function scheduleIdleTask(callback) {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(callback, { timeout: 2000 });
  } else {
    setTimeout(callback, 1);
  }
}

// 暴露到全局，供其他脚本按需使用（如延迟加载第三方脚本）
if (typeof window !== 'undefined') {
  window.scheduleIdleTask = scheduleIdleTask;
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
  // 关键任务：立即执行
  addStructuredData();

  // 非关键任务：使用 requestIdleCallback 延迟执行
  scheduleIdleTask(() => {
    addExternalLinkIcons();
    enhanceBackToTop();
    optimizeTypography();
    addBreadcrumbStructuredData();
  });
});

/**
 * 为外部链接添加图标（使用事件委托优化性能）
 */
function addExternalLinkIcons() {
  // 使用事件委托，避免遍历所有链接
  const content = document.querySelector('.md-content');
  if (!content) return;

  // 处理外部链接的通用函数
  const processExternalLink = (link) => {
    // 检查是否已处理，避免重复操作
    if (link.dataset.extHandled) return;

    const href = link.getAttribute('href');
    if (href && (href.startsWith('http') || href.startsWith('//'))) {
      if (!link.hostname || link.hostname !== window.location.hostname) {
        link.classList.add('external-link');
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
        // 标记为已处理
        link.dataset.extHandled = '1';
      }
    }
  };

  // 使用事件委托处理点击
  content.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link) return;
    processExternalLink(link);
  }, { capture: true });

  // 使用 IntersectionObserver 批量处理可见的链接（带降级方案）
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          processExternalLink(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '50px'
    });

    // 批量观察链接，避免一次性处理所有链接
    requestAnimationFrame(() => {
      const links = content.querySelectorAll('a[href^="http"], a[href^="//"]');
      links.forEach(link => observer.observe(link));
    });
  } else {
    // 降级方案：IntersectionObserver 不支持时，一次性处理所有链接
    requestAnimationFrame(() => {
      const links = content.querySelectorAll('a[href^="http"], a[href^="//"]');
      links.forEach(link => processExternalLink(link));
    });
  }
}

/**
 * 优化中英文混排
 */
function optimizeTypography() {
  // 这里可以添加更多的排版优化逻辑
  // 例如自动在中英文之间添加间距等
}

/**
 * 增强返回顶部功能（优化版本）
 */
function enhanceBackToTop() {
  const backToTop = document.querySelector('.md-top');
  if (backToTop) {
    // 使用 passive 监听器优化滚动性能
    backToTop.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }, { passive: false });
  }
}

/**
 * 添加复制代码按钮的提示（使用事件委托优化）
 */
if (typeof document$ !== 'undefined' && document$.subscribe) {
  document$.subscribe(function() {
    // 使用事件委托，避免为每个按钮添加监听器
    const content = document.querySelector('.md-content');
    if (!content) return;

    // 移除旧的监听器（如果存在）
    if (content._copyListenerAdded) return;
    content._copyListenerAdded = true;

    content.addEventListener('click', function(e) {
      const button = e.target.closest('button[data-clipboard-target]');
      if (!button) return;

      const original = button.textContent;
      button.textContent = '已复制!';
      setTimeout(() => {
        button.textContent = original;
      }, 2000);
    });
  });
}

/**
 * 添加 JSON-LD 结构化数据用于 SEO
 */
function addStructuredData() {
  const script = document.createElement('script');
  script.type = 'application/ld+json';

  const title = document.title;
  const description = document.querySelector('meta[name="description"]')?.content;
  const url = window.location.href;
  const canonical = document.querySelector('link[rel="canonical"]')?.href || url;

  // 网站基础信息
  const websiteData = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Multiple Personality System Wiki - 多意识体系统百科",
    "alternateName": "多意识体系统百科",
    "url": "https://wiki.mpsteam.cn",
    "description": "专业的多意识体系统（MPS）、解离障碍（DID/OSDD）与创伤疗愈中文知识库",
    "inLanguage": "zh-CN",
    "publisher": {
      "@type": "Organization",
      "name": "MPS Team",
      "url": "https://mpsteam.cn"
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://wiki.mpsteam.cn/search/?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  };

  // 如果是词条页面，添加 Article 数据
  if (window.location.pathname.includes('/entries/')) {
    const articleData = {
      "@context": "https://schema.org",
      "@type": ["Article", "MedicalWebPage"],
      "headline": title,
      "description": description,
      "url": canonical,
      "inLanguage": "zh-CN",
      "isPartOf": {
        "@type": "WebSite",
        "name": "Multiple Personality System Wiki",
        "url": "https://wiki.mpsteam.cn"
      },
      "author": {
        "@type": "Organization",
        "name": "MPS Team 社区贡献者"
      },
      "publisher": {
        "@type": "Organization",
        "name": "MPS Team",
        "url": "https://mpsteam.cn"
      },
      "dateModified": document.lastModified,
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": canonical
      }
    };

    // 创建包含两个结构的数组
    script.textContent = JSON.stringify([websiteData, articleData]);
  } else {
    // 非词条页面只添加网站信息
    script.textContent = JSON.stringify(websiteData);
  }

  document.head.appendChild(script);
}

/**
 * 面包屑导航结构化数据
 */
function addBreadcrumbStructuredData() {
  const breadcrumbLinks = document.querySelectorAll('.md-path');
  if (breadcrumbLinks.length > 0) {
    const breadcrumbList = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": []
    };

    breadcrumbLinks.forEach((link, index) => {
      breadcrumbList.itemListElement.push({
        "@type": "ListItem",
        "position": index + 1,
        "name": link.textContent.trim(),
        "item": link.href
      });
    });

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(breadcrumbList);
    document.head.appendChild(script);
  }
}
