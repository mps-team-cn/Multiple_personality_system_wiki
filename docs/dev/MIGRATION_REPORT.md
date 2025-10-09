# Plurality Wiki 迁移报告

## 迁移概述

**迁移时间** : 2025-10-05
**迁移人员** : Claude Code
**迁移类型** : 前端框架迁移 (Docsify → MkDocs Material)

本次迁移将 Plurality Wiki 从 Docsify 静态站点生成器迁移到 MkDocs Material 主题,以获得更好的功能性、可维护性和用户体验。

---

## 📊 迁移统计

### 文件变更

- **新增文件** : 156+ 个
- **修改文件** : 5 个
- **删除文件** : 0 个 (旧文件保留作为备份)

### 内容迁移

- **词条数量** : 142 个 Markdown 文件
- **文档文件** : 7 个 (README, CONTRIBUTING, tags, Glossary, changelog, etc.)
- **资源文件** : SVG 图标, JSON 数据文件

---

## 🔄 主要变更

### 1. 项目结构重组

#### 新增目录结构

```text
plurality_wiki/
├── docs/                    # 新增: MkDocs 文档目录
│   ├── index.md            # 新首页 (Material 风格)
│   ├── entries/            # 迁移: 所有词条
│   ├── assets/             # 自定义资源
│   │   ├── extra.css       # 自定义样式
│   │   ├── extra.js        # 自定义脚本
│   │   ├── favicon.svg     # 站点图标
│   │   └── last-updated.json
│   ├── README.md           # 关于本站
│   ├── CONTRIBUTING/index.md     # 贡献指南
│   ├── Preface.md          # 序言
│   ├── tags.md             # 标签索引
│   ├── Glossary.md         # 术语表
│   └── changelog.md        # 变更日志
├── mkdocs.yml              # MkDocs 配置文件
├── requirements.txt        # Python 依赖
├── .cfpages-build.sh       # Cloudflare Pages 构建脚本
├── CLOUDFLARE_PAGES.md     # 部署说明
└── MIGRATION_REPORT.md     # 本报告
```

#### 保留的旧文件

```text
├── index.html.old          # 旧版 Docsify 入口 (备份)
├── index.html.backup       # 旧版备份
├── index.html              # 当前仍为 Docsify (向后兼容)
├── assets/core/            # Docsify 模块化核心
└── entries/                # 原始词条目录 (保留)
```

### 2. 配置文件

#### mkdocs.yml (新增)

- 站点元信息配置
- Material 主题配置
- 导航结构定义
- 插件配置
- Markdown 扩展启用

**关键配置** :

```yaml
theme:
  name: material
  language: zh
  features:

    - navigation.instant
    - navigation.tracking
    - toc.follow
    - search.suggest
    - content.code.copy

plugins:

  - search
  - git-revision-date-localized
  - minify
  - glightbox
  - tags

```

#### requirements.txt (更新)

```text
mkdocs>=1.5.3
mkdocs-material>=9.5.0
mkdocs-git-revision-date-localized-plugin>=1.2.4
mkdocs-minify-plugin>=0.8.0
mkdocs-glightbox>=0.3.7
pymdown-extensions>=10.7
```

### 3. 首页重写

#### 旧版 (Docsify)

- HTML + 自定义卡片布局
- 手动编写的语录区块
- 自定义 CSS 样式

#### 新版 (MkDocs Material)

- **Grid Cards** : 使用 Material 原生卡片网格
- **Admonitions** : 使用告示框组件显示警告和提示
- **Tabs** : 使用标签页组织核心概念
- **响应式设计** : 自适应移动端和桌面端

**新特性** :

- ✅ 更现代的视觉设计
- ✅ 更好的移动端体验
- ✅ 内置图标系统 (Material Icons)
- ✅ 更清晰的信息层次

### 4. 样式定制

#### docs/assets/extra.css

- 中文字体优化 (Noto Sans SC)
- 代码字体 (JetBrains Mono)
- 卡片悬停效果
- 深色模式优化
- 表格美化
- 滚动条样式

#### 主题颜色

- **主色** : `#4FC08D` (青翠绿)
- **强调色** : `#8B9EFF` (冷紫)
- **支持深色/浅色模式切换**

### 5. JavaScript 增强

#### docs/assets/extra.js

- 外部链接自动添加图标和 `target="_blank"`
- 中英文混排优化
- 平滑滚动增强
- 复制代码提示

---

## 🎯 功能对比

| 功能             | Docsify  | MkDocs Material | 说明                   |
| ---------------- | -------- | --------------- | ---------------------- |
| **搜索** | ✅       | ✅ 增强         | 支持中文分词、搜索建议 |
| **即时加载** | ✅       | ✅              | 页面切换无刷新         |
| **深色模式** | ✅       | ✅ 增强         | 系统级切换支持         |
| **移动端适配** | ✅       | ✅ 更好         | 原生响应式设计         |
| **目录跟随** | ❌       | ✅              | 滚动时目录自动高亮     |
| **代码高亮** | ✅       | ✅ 更好         | 支持更多语言           |
| **代码复制** | ✅       | ✅              | 一键复制               |
| **图片缩放** | ✅       | ✅              | Lightbox 效果          |
| **最后更新时间** | ✅       | ✅ 自动         | Git 自动获取           |
| **标签系统** | 手动     | ✅ 自动         | 插件自动生成           |
| **导航面包屑** | ❌       | ✅              | 显示当前位置           |
| **版本控制** | ❌       | ✅              | 支持 mike 多版本       |
| **SEO 优化** | 一般     | ✅ 更好         | 自动生成 sitemap       |
| **构建速度** | 无需构建 | 快速            | 优化的构建流程         |
| **自定义主题** | 较难     | ✅ 容易         | CSS 变量系统           |

---

## ✅ 已完成的工作

### 结构迁移

- [x] 创建 `docs/` 目录结构
- [x] 复制所有 142 个词条到 `docs/entries/`
- [x] 复制文档文件 (README, CONTRIBUTING, tags, etc.)
- [x] 复制静态资源 (SVG, JSON)

### 配置文件

- [x] 创建 `mkdocs.yml` 主配置文件
- [x] 整理 `requirements.txt` 依赖清单
- [x] 创建 `.cfpages-build.sh` 构建脚本
- [x] 更新 `.gitignore` 忽略 `site/` 目录

### 内容创建

- [x] 重写首页 `docs/index.md` (Grid Cards + Admonitions + Tabs)
- [x] 创建自定义样式 `docs/assets/extra.css`
- [x] 创建自定义脚本 `docs/assets/extra.js`
- [x] 创建 Cloudflare Pages 部署文档

### 文档

- [x] 创建本迁移报告
- [x] 创建 Cloudflare Pages 配置说明
- [x] 更新前端架构文档

### 配置修复 (2025-10-05)

- [x] 修复 `mkdocs.yml` 配置问题:
  - 注释 `custom_dir: overrides` (目录不存在)
  - 注释 `tags_file: tags.md` (新版本不再需要)
  - 移除 nav 中的 README.md (与 index.md 冲突)
  - 移除重复的 index.md 引用
- [x] 创建 `docs/includes/abbreviations.md` 缩写定义文件
- [x] 成功构建: `mkdocs build --strict` ✅

### 文档更新 (2025-10-05)

- [x] 更新 `README.md`: 添加 MkDocs 构建说明
- [x] 更新 `AGENTS.md`: 更新文件路径和测试命令
- [x] 更新 `CONTRIBUTING/index.md`: 更新本地开发流程
- [x] 同步 `docs/CONTRIBUTING/index.md` 和 `docs/README.md`
- [x] 更新 `docs/tools/README.md`: 添加迁移说明
- [x] 更新 `docs/ADMIN_GUIDE.md`: 更新维护脚本说明

### 工具脚本更新 (2025-10-05)

- [x] `tools/generate_tags_index.py`: 支持 docs/entries/ 优先,entries/ 回退
- [x] `tools/check_links.py`: 支持 entries/, docs/entries/, ../entries/ 三种格式
- [x] `tools/retag_and_related.py`: 添加 get_entries_dir() 自动选择目录
- [x] `tools/fix_markdown.py`: 无需修改 (递归扫描)

---

## 🚧 待完成的工作

### 测试验证

- [x] 本地构建测试 (`mkdocs serve`) ✅ 2025-10-05 完成
- [x] 修复 mkdocs.yml 配置错误 (custom_dir, tags_file) ✅ 2025-10-05 完成
- [x] 创建缺失的 includes/abbreviations.md ✅ 2025-10-05 完成
- [x] 更新根目录文档 (README, AGENTS, CONTRIBUTING) ✅ 2025-10-05 完成
- [x] 更新工具脚本支持双目录 (docs/entries/ + entries/) ✅ 2025-10-05 完成
- [ ] 检查所有内部链接有效性
- [ ] 验证图片路径正确性
- [ ] 测试移动端显示
- [ ] 测试搜索功能
- [ ] 验证深色模式

### 部署

- [ ] 在 Cloudflare Pages 创建新项目
- [ ] 配置构建命令和环境变量
- [ ] 测试预览部署
- [ ] 配置自定义域名 (如需要)
- [ ] 设置 DNS 记录

### 优化

- [ ] 添加 Google Analytics (可选)
- [ ] 优化图片资源 (压缩)
- [ ] 添加更多导航快捷方式
- [ ] 完善标签分类
- [ ] 添加相关词条推荐

---

## 🔙 回滚方案

如果迁移后发现重大问题,可以通过以下方式回滚:

### 方案 A: Git 回滚

```bash

# 回滚到迁移前的提交

git revert <migration-commit-hash>

# 或者硬回滚 (谨慎使用)

git reset --hard <pre-migration-commit>
git push --force
```

### 方案 B: 保留双版本

- Docsify 版本: 继续使用 `index.html` + `assets/`
- MkDocs 版本: 部署到不同的子域名测试

### 方案 C: 分支切换

```bash

# 切换回未迁移的分支

git checkout main  # 或其他稳定分支
```

### 保留的备份文件

- `index.html.old` - 原始 Docsify 入口
- `index.html.backup` - 备份副本
- `entries/` - 原始词条目录 (未删除)

---

## 📝 注意事项

### 链接路径

- ✅ **相对路径** : 词条内部链接使用相对路径 (如 `entries/DID.md`)
- ✅ **锚点链接** : 支持页内锚点 (`#section-name`)
- ⚠️ **注意** : MkDocs 会自动处理 `.md` 扩展名

### Frontmatter

- MkDocs 支持 YAML Frontmatter
- 现有的 `title`, `tags`, `updated` 字段可以保留
- 额外字段会被忽略,不影响渲染

### 图片资源

- 确保所有图片路径使用相对于源文件的路径
- 从 `docs/entries/` 引用：`![alt](../assets/image.svg)`
- MkDocs 会根据生成的 HTML 位置自动调整路径

### 代码块

- 使用三个反引号 + 语言标识
- 支持行号、高亮特定行等高级功能

---

## 🎓 学习资源

### MkDocs Material 官方文档

- **主页** : [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
- **快速开始** : [https://squidfunk.github.io/mkdocs-material/getting-started/](https://squidfunk.github.io/mkdocs-material/getting-started/)
- **参考** : [https://squidfunk.github.io/mkdocs-material/reference/](https://squidfunk.github.io/mkdocs-material/reference/)

### 相关插件

- **搜索** : [https://squidfunk.github.io/mkdocs-material/plugins/search/](https://squidfunk.github.io/mkdocs-material/plugins/search/)
- **标签** : [https://squidfunk.github.io/mkdocs-material/plugins/tags/](https://squidfunk.github.io/mkdocs-material/plugins/tags/)
- **Git 修订日期** : [https://github.com/timvink/mkdocs-git-revision-date-localized-plugin](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin)

---

## 📊 后续建议

### 内容优化

1. **标签规范化** : 统一所有词条的标签命名
2. **交叉引用** : 增加词条之间的相关链接
3. **图片优化** : 压缩大图片,使用 WebP 格式
4. **多语言支持** : 考虑添加英文版本

### 功能增强

1. **评论系统** : 集成 Giscus 或类似服务
2. **版本管理** : 使用 mike 管理多个版本
3. **RSS 订阅** : 添加变更日志 RSS
4. **PWA 支持** : 添加离线访问功能

### 性能优化

1. **CDN 加速** : 使用 Cloudflare CDN
2. **资源压缩** : 启用 Brotli 压缩
3. **图片懒加载** : 已通过 glightbox 插件实现
4. **构建缓存** : 优化 CI/CD 流程

### 监控和分析

1. **访问统计** : 集成 Google Analytics
2. **错误追踪** : 集成 Sentry
3. **用户反馈** : 添加反馈表单
4. **性能监控** : 使用 Lighthouse CI

---

## 🤝 致谢

感谢以下工具和项目:

- **MkDocs** : [https://www.mkdocs.org/](https://www.mkdocs.org/)
- **Material for MkDocs** : [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
- **Cloudflare Pages** : [https://pages.cloudflare.com/](https://pages.cloudflare.com/)
- **原 Docsify 版本** : 为迁移提供了基础

---

## 📧 联系方式

如有问题或建议,请通过以下方式联系:

- **GitHub Issues** : [https://github.com/mps-team-cn/plurality_wiki/issues](https://github.com/mps-team-cn/plurality_wiki/issues)
- **邮件** : (如有)

---

**报告生成时间** : 2025-10-05
**报告版本** : 1.0
**最后更新** : 2025-10-05
