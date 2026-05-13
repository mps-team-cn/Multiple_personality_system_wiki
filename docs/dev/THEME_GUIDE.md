# MkDocs 主题切换指南

本文档说明如何在不同 MkDocs 主题之间切换。

## 📦 可用主题

### 1. Material for MkDocs（当前使用）

**特点** ：

- ✅ 最流行，功能最强大（25K+ stars）
- ✅ 现代化设计，Material Design 风格
- ✅ 强大的搜索功能（中文分词、拼音支持）
- ✅ 丰富的插件生态（标签、图片缩放、Git 日期等）
- ✅ 完善的深色模式
- ✅ 移动端优化

**依赖** ：

```bash
uv add mkdocs-material
uv add mkdocs-git-revision-date-localized-plugin
uv add mkdocs-minify-plugin
uv add mkdocs-glightbox
```

**配置文件** ：`mkdocs.yml`（当前）或 `mkdocs.yml.material-backup`（备份）

---

### 2. ReadTheDocs 主题

**特点** ：

- ✅ 内置主题，无需安装
- ✅ 经典文档风格
- ✅ 简洁清晰
- ⚠️ 功能较少
- ⚠️ 移动端体验一般

**依赖** ：

```bash

# 无需额外依赖，MkDocs 内置

```

**配置文件** ：`mkdocs.yml.readthedocs`

**切换方式** ：

```bash

# 备份当前配置

cp mkdocs.yml mkdocs.yml.backup

# 切换到 ReadTheDocs 主题

cp mkdocs.yml.readthedocs mkdocs.yml

# 测试预览

uv run mkdocs serve
```

---

### 3. MkDocs 默认主题

**特点** ：

- ✅ 内置主题，无需安装
- ✅ 轻量简洁
- ✅ 加载快速
- ⚠️ 设计较为朴素
- ⚠️ 功能基础

**依赖** ：

```bash

# 无需额外依赖，MkDocs 内置

```

**配置文件** ：`mkdocs.yml.mkdocs`

**切换方式** ：

```bash

# 备份当前配置

cp mkdocs.yml mkdocs.yml.backup

# 切换到默认主题

cp mkdocs.yml.mkdocs mkdocs.yml

# 测试预览

uv run mkdocs serve
```

---

## 🎨 CSS 样式管理

### 样式文件说明

项目中包含三个 CSS 文件：

1. **extra-material.css** - Material 主题专用增强样式

    - 使用 Material CSS 变量
    - 卡片网格、告示框增强
    - 深色模式优化
    - 仅在 Material 主题下生效

2. **extra.css** - 通用样式（当前使用）

    - 适用于所有 MkDocs 主题
    - 中文字体优化
    - 基础表格、代码块美化
    - 打印样式

3. **extra-common.css** - 通用样式源文件

    - 与 extra.css 相同
    - 作为备份保留

### 主题与 CSS 对应关系

| 主题 | 使用的 CSS | 说明 |
|------|-----------|------|
| Material | extra-material.css | Material 专用增强 |
| ReadTheDocs | extra.css | 通用样式 |
| MkDocs 默认 | extra.css | 通用样式 |
| 第三方主题 | extra.css | 通用样式 |

### 切换主题时的 CSS 处理

主题配置文件已自动配置好对应的 CSS：

- `mkdocs.yml` → 使用 `extra-material.css`
- `mkdocs.yml.readthedocs` → 使用 `extra.css`
- `mkdocs.yml.mkdocs` → 使用 `extra.css`

**无需手动调整 CSS 引用** ，切换主题时会自动使用对应的样式文件。

---

## 🔧 第三方主题安装

如果想尝试其他第三方主题，可以按以下方式安装：

### Cinder 主题

```bash
uv add mkdocs-cinder
```

修改 `mkdocs.yml`：

```yaml
theme:
  name: cinder
```

### Windmill 主题

```bash
uv add mkdocs-windmill
```

修改 `mkdocs.yml`：

```yaml
theme:
  name: windmill
```

### Bootswatch 主题包

```bash
uv add mkdocs-bootswatch
```

修改 `mkdocs.yml`（20+ 种配色可选）：

```yaml
theme:
  name: cosmo  # 或 flatly, darkly, slate, superhero 等
```

可用配色：cerulean, cosmo, cyborg, darkly, flatly, journal, litera, lumen, lux, materia, minty, pulse, sandstone, simplex, slate, solar, spacelab, superhero, united, yeti

---

## 📊 主题对比

| 特性               | Material | ReadTheDocs | MkDocs 默认 | Cinder | Windmill |
| ------------------ | -------- | ----------- | ----------- | ------ | -------- |
| **安装难度** | 中等     | 无需        | 无需        | 简单   | 简单     |
| **功能丰富度** | ⭐⭐⭐⭐⭐ | ⭐⭐        | ⭐⭐        | ⭐⭐⭐  | ⭐⭐⭐    |
| **视觉效果** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐      | ⭐⭐        | ⭐⭐⭐⭐ | ⭐⭐⭐⭐   |
| **中文支持** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐      | ⭐⭐⭐      | ⭐⭐⭐  | ⭐⭐⭐    |
| **搜索功能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐      | ⭐⭐⭐      | ⭐⭐⭐  | ⭐⭐⭐    |
| **移动端优化** | ⭐⭐⭐⭐⭐ | ⭐⭐        | ⭐⭐⭐      | ⭐⭐⭐⭐ | ⭐⭐⭐⭐   |
| **插件生态** | ⭐⭐⭐⭐⭐ | ⭐⭐        | ⭐⭐⭐      | ⭐⭐⭐  | ⭐⭐⭐    |
| **社区活跃度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐      | ⭐⭐⭐      | ⭐⭐    | ⭐⭐     |
| **加载速度** | ⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐ | ⭐⭐⭐⭐   |

---

## 🎯 推荐选择

### 推荐使用 Material（当前）

**适用场景** ：

- ✅ 需要现代化的视觉效果
- ✅ 重视移动端体验
- ✅ 需要强大的搜索功能
- ✅ 希望使用丰富的插件
- ✅ 中文内容为主

**不适合** ：

- ❌ 需要极致的加载速度
- ❌ 服务器资源有限
- ❌ 不需要复杂功能

### 备选：ReadTheDocs

**适用场景** ：

- ✅ 喜欢经典文档风格
- ✅ 无需安装额外依赖
- ✅ 简单直接的文档

### 备选：MkDocs 默认

**适用场景** ：

- ✅ 追求简洁
- ✅ 加载速度优先
- ✅ 基础功能足够

---

## 🔄 快速切换命令

```bash

# 切换到 Material（推荐）

cp mkdocs.yml.material-backup mkdocs.yml
uv run mkdocs serve

# 切换到 ReadTheDocs

cp mkdocs.yml.readthedocs mkdocs.yml
uv run mkdocs serve

# 切换到 MkDocs 默认

cp mkdocs.yml.mkdocs mkdocs.yml
uv run mkdocs serve

# 恢复到最近的备份

cp mkdocs.yml.backup mkdocs.yml
uv run mkdocs serve
```

---

## 🧩 Markdown 扩展配置

- **统一锚点规则** : `toc.slugify` 与 `pymdownx.tabbed.slugify` 均改用 `pymdownx.slugs.slugify(case="lower-ascii")`，确保在 MkDocs、GitHub 预览与本地编辑器之间生成一致的标题锚点。
- **按钮/卡片兼容性** : 继续保留 `attr_list`、`pymdownx.superfences` 等扩展，Material 专用语法在站点渲染，而 GitHub 端会回退为可阅读的纯文本。
- **维护建议** : 新增或调整 Markdown 扩展时，请同步验证 `uv run mkdocs serve`、GitHub 网页预览与常用 Markdown 编辑器三端的表现，并在本节记录差异说明。

---

## ⚠️ 注意事项

### 主题特定功能

某些功能只在特定主题下可用：

- **Material 独有** :

    - Grid Cards（卡片网格）
    - Admonitions 高级样式
    - 标签系统
    - Git 修订日期
    - 图片缩放（glightbox）
    - 内容标签页

- **切换主题后需要调整** :

    - 首页 `index.md` 可能需要简化（去除 Material 特定语法）
    - 某些 Markdown 扩展可能不支持
    - 插件配置需要相应调整

### 构建兼容性

- 内置主题（readthedocs, mkdocs）可以直接在 Cloudflare Pages 构建
- Material 和其他第三方主题需要在 `pyproject.toml` 中声明依赖

---

## 📝 自定义主题

如果想深度自定义主题，可以：

1. **创建 overrides 目录** ：

```bash
mkdir -p overrides
```

2. **修改 mkdocs.yml** ：

```yaml
theme:
  name: material
  custom_dir: overrides
```

3. **添加自定义模板/样式** ：

```text
overrides/
├── main.html           # 覆盖主模板
├── partials/           # 部分模板
│   ├── header.html
│   └── footer.html
└── assets/
    └── stylesheets/
        └── extra.css
```

---

## 📚 参考资源

- **MkDocs 官方文档** : [https://www.mkdocs.org/](https://www.mkdocs.org/)
- **Material 主题文档** : [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
- **MkDocs 主题目录** : [https://github.com/mkdocs/catalog](https://github.com/mkdocs/catalog)
- **主题选择指南** : [https://www.mkdocs.org/user-guide/choosing-your-theme/](https://www.mkdocs.org/user-guide/choosing-your-theme/)

---

**最后更新** : 2025-10-05
