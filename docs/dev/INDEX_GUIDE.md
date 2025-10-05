# 首页文件管理指南

## 📁 首页文件结构

```
docs/
├── index.md              # 通用版首页（当前默认，所有主题适用）
├── index-material.md     # Material 主题增强版（含卡片、图标等）
├── index-simple.md       # 简化版备份（与 index.md 相同）
└── README.md             # 开发者文档（与 index.md 冲突）
```

## ⚠️ README.md 冲突问题

### 问题说明

MkDocs 会将 `index.md` 和 `README.md` 都视为首页文件，导致冲突：

```
WARNING - Excluding 'README.md' from the site because it conflicts with 'index.md'.
```

### 解决方案

**方案 A：保留 README.md 作为开发文档（推荐）**

将 README.md 移到根目录，仅用于 GitHub 项目说明：

```bash
# 已经在根目录，无需移动
# 根目录的 README.md 不会被 MkDocs 处理
```

**方案 B：删除 docs/README.md**

如果不需要在文档站点中显示：

```bash
rm docs/README.md
```

**方案 C：重命名 docs/README.md**

```bash
mv docs/README.md docs/ABOUT.md
```

然后在 nav 中引用：
```yaml
nav:
  - 关于本站: ABOUT.md
```

## 🎨 主题与首页对应关系

| 主题 | 首页文件 | 特性 |
|------|---------|------|
| Material（当前） | index-material.md | Material 图标、卡片网格、内容标签页、告示框增强 |
| ReadTheDocs | index.md | 纯 Markdown，基础引用块，无特殊组件 |
| MkDocs 默认 | index.md | 纯 Markdown，基础引用块，无特殊组件 |
| 其他主题 | index.md | 纯 Markdown，基础引用块，无特殊组件 |

## 🔄 切换主题时的首页处理

### Material 主题

**mkdocs.yml 配置**：
```yaml
nav:
  - 首页: index-material.md
```

**包含的 Material 专用语法**：
- `:material-*:` 图标
- `<div class="grid cards">` 卡片网格
- `=== "标签"` 内容标签页
- `!!! quote/warning/info/tip` 增强告示框

### ReadTheDocs / MkDocs 默认 / 其他主题

**mkdocs.yml.readthedocs 配置**：
```yaml
nav:
  - 首页: index.md
```

**使用纯 Markdown 语法**：
- 普通列表
- 基础引用块 `>`
- 标准标题和链接
- 无特殊图标和组件

## 📝 首页内容对比

### index-material.md（Material 专用）

```markdown
<div class="grid cards" markdown>

- :material-book-open-variant:{ .lg .middle } **关于本站**

  ***

  我们专注于整理...

  [:octicons-arrow-right-24: 开始阅读](README.md)

</div>

=== "核心概念"
    卡片内容...
```

**优点**：
- ✅ 视觉效果现代化
- ✅ 卡片式布局
- ✅ Material 图标
- ✅ 响应式设计

**缺点**：
- ❌ 只在 Material 主题下正确显示
- ❌ 其他主题会显示原始 HTML

### index.md（通用版）

```markdown
## 关于本站

我们专注于整理...

**快速开始**：
- [标签索引](tags.md)
- [术语表](Glossary.md)

## 核心概念

- **[多元性（Plurality）](entries/Plurality.md)** - 简介
- **[系统（System）](entries/System.md)** - 简介

> **脸脸系统**
>
> "社区语录内容..."

### ⚠️ 触发警告

本Wiki内容涉及...
```

**优点**：
- ✅ 适用所有 MkDocs 主题
- ✅ 纯 Markdown，兼容性好
- ✅ 降级优雅

**缺点**：
- ❌ 视觉效果较简单
- ❌ 无卡片和图标

## 🔧 手动切换首页

### 切换到 Material 增强版

```bash
# 方式 1：修改 nav 配置
# 编辑 mkdocs.yml，将 index.md 改为 index-material.md

# 方式 2：替换文件
cp docs/index-material.md docs/index.md
mkdocs serve
```

### 切换到通用版

```bash
# 方式 1：修改 nav 配置
# 编辑 mkdocs.yml，将 index-material.md 改为 index.md

# 方式 2：替换文件
cp docs/index-simple.md docs/index.md
mkdocs serve
```

## 🎯 推荐配置

### 当前配置（推荐）

```
Material 主题：
- nav 引用: index-material.md
- index.md: 通用版（备用）
- README.md: 仍然冲突（建议删除或移到根目录）

其他主题：
- nav 引用: index.md
- index.md: 通用版
```

### 优化后配置（最佳）

```bash
# 1. 删除 docs/README.md（开发文档已在根目录）
rm docs/README.md

# 2. Material 主题使用增强版
# mkdocs.yml 保持 index-material.md

# 3. 其他主题使用通用版
# mkdocs.yml.readthedocs 和 mkdocs.yml.mkdocs 使用 index.md
```

## ⚠️ 注意事项

### README.md 的处理

1. **根目录的 README.md**
   - 用于 GitHub 项目说明
   - 不会被 MkDocs 处理
   - ✅ 保留

2. **docs/README.md**
   - 与 index.md 冲突
   - MkDocs 会自动排除
   - ❌ 建议删除或重命名

### 首页链接问题

index-material.md 中有一行：
```markdown
[:octicons-arrow-right-24: 开始阅读](README.md)
```

由于 README.md 被排除，这个链接会失效。建议：

**方案 1：链接到通用首页**
```markdown
[:octicons-arrow-right-24: 开始阅读](index.md)
```

**方案 2：创建独立的"关于"页面**
```bash
mv docs/README.md docs/ABOUT.md
```
```markdown
[:octicons-arrow-right-24: 开始阅读](ABOUT.md)
```

## 📊 建议操作

```bash
# 1. 删除冲突的 README.md
rm docs/README.md

# 2. 修复 Material 首页的链接
# 将 index-material.md 中的 README.md 链接改为其他页面

# 3. 测试构建
mkdocs build --strict

# 4. 预览效果
mkdocs serve
```

---

**最后更新**: 2025-10-05
