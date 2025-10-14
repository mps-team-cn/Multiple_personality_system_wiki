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

  // 添加 JSON-LD 结构化数据
  addStructuredData();
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
    "description": "专业的多重人格系统（MPS）、解离障碍（DID/OSDD）与创伤疗愈中文知识库",
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
