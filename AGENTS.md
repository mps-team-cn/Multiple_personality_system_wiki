# Multiple Personality System Wiki 贡献与开发约定

> **适用范围**：本文档定义了项目的贡献规则与开发约定，适用于人工贡献者与自动化工具（代理/脚本）。

!!! warning "强制要求"
    所有贡献必须严格遵循以下规范，以保持条目结构与站点一致性。

---

## 📑 目录导览

1. [通用约定](#1-通用约定)
    - [语言规范](#11-语言规范)
    - [文件与目录规范](#12-文件与目录规范)
    - [索引与链接规范](#13-索引与链接规范)
2. [站点配置与前端规则](#2-站点配置与前端规则)
    - [提示块语法](#21-提示块语法)
3. [工具与脚本](#3-工具与脚本)
4. [提交与版本管理](#4-提交与版本管理)
    - [提交规范](#41-提交规范)
    - [Pull Request 要求](#42-pull-request-要求)
    - [版本发布流程](#44-版本发布流程)
5. [Python 环境配置](#5-python-环境配置)
6. [测试与检查](#6-测试与检查)
7. [自动化维护规则](#7-自动化维护规则代理脚本必须遵循)
8. [Markdown 自动修复与校验](#8-markdown-自动修复与校验)

---

## 1. 通用约定

### 1.1 语言规范

!!! info "语言要求"

    - ✅ **统一使用简体中文**：所有条目、文档与提交信息
    - ✅ **一级标题格式**：`中文名（English/缩写）`
    - ⚠️ **诊断/疾病条目**：括号内必须使用标准缩写（如 `解离性身份障碍（DID）`）

### 1.2 文件与目录规范

!!! warning "重要变更：Docsify → MkDocs Material"
    本项目已从 Docsify 迁移至 MkDocs Material，目录结构与引用方式已更新。

#### 📂 目录结构概览

| 目录/文件 | 用途 | 说明 |
|----------|------|------|
| `docs/entries/` | **词条存放** | ❌ 不得创建子目录，分类通过 Frontmatter `tags` 声明 |
| `docs/` | **核心文档** | `index.md`, `README.md`, `Glossary.md` 等 |
| `docs/contributing/` | **贡献指南** | 拆分为多个专题文档 |
| `docs/dev/Tools-Index.md` | **工具文档** | 脚本说明与使用指南 |
| `tools/` | **脚本与工具** | 所有自动化工具 |
| `docs/assets/` | **静态资源** | CSS, JS, 图片等 |
| `docs/assets/figures/` | **图表资源** | 流程图、示意图、SVG |
| `docs/assets/images/` | **图片资源** | 封面、截图 |
| `docs/assets/icons/` | **图标资源** | 小图标、装饰性素材 |

#### 📝 词条 Frontmatter 要求

!!! danger "必须包含的字段"
    每篇词条文件开头必须声明 YAML 格式的 Frontmatter：

```yaml
---
title: 词条标题
topic: 词条主题
tags:

  - 标签1
  - 标签2

updated: YYYY-MM-DD
---
```

!!! info "特殊文件例外"
    以下类型的文件 **无需** `updated` 字段（检查工具会自动跳过）：

    - 📚 导览文件：`*-Guide.md`（如 `Clinical-Diagnosis-Guide.md`）
    - 📑 索引文件：`*-Index.md`（如 `Tools-Index.md`）

#### 🔍 搜索权重配置（可选）

!!! tip "提升重要词条的搜索排名"
    对于核心词条，可在 Frontmatter 中添加 `search.boost` 字段来提高搜索结果中的权重。

**推荐的权重分级**：

| 优先级 | 权重值 | 适用词条类型 | 示例 |
|--------|--------|-------------|------|
| **最高** | `2.0` | 诊断类疾病 | DID、OSDD、PTSD、CPTSD |
| **高** | `1.8` | 核心概念与操作 | Alter、Tulpa、System、Switch、Grounding、Host、Dissociation、Trauma |
| **中高** | `1.5` | 重要概念 | Multiple_Personality_System、Protector、Front/Fronting |
| **默认** | `1.0`（无需设置） | 普通词条 | 其他所有词条 |

**配置示例**：

```yaml
---
title: 解离性身份障碍（DID）
topic: 诊断与临床
tags:
  - 诊断与临床
  - DID
  - 多重意识体
updated: 2025-01-15
search:
  boost: 2.0  # 最高优先级
---
```

```yaml
---
title: 系统（System）
topic: 系统运作
tags:
  - 系统运作
  - 多重意识体
updated: 2025-01-15
search:
  boost: 1.8  # 高优先级
---
```

!!! warning "注意事项"
    - ✅ 仅为**真正重要**的核心词条设置权重，避免滥用
    - ✅ 权重值通常在 `1.0` - `2.0` 之间，不建议超过 `2.0`
    - ✅ 大多数词条无需设置权重（默认 `1.0`）
    - ⚠️ 修改权重后需重新构建站点才能生效

#### ✨ 词条格式规范

!!! tip "加粗内容格式"
    加粗内容前后都需要加空格：` **加粗内容** `（空格 + 星号 + 内容 + 星号 + 空格）

### 1.3 索引与链接规范

#### 🔗 必须同步维护的文档

创建或修改词条时，**必须同步更新** 以下相关文档：

| 文档 | 更新时机 | 说明 |
|------|---------|------|
| 主题总览页面 | 新增词条 | 更新对应主题索引 |
| **对应的 Guide** | 创建/更新/删除词条 | 见下方主题映射表 |

#### 📚 词条主题与 Guide 映射表

| 词条主题 | 对应 Guide 文件 | 示例内容 |
|---------|----------------|---------|
| **诊断与临床** | `Clinical-Diagnosis-Guide.md` | DID, OSDD, CPTSD, 焦虑障碍, 情绪障碍 |
| **系统运作** | `System-Operations-Guide.md` | 前台切换, 共同意识, 记忆管理, 内部空间 |
| **实践指南** | `Practice-Guide.md` | Tulpa三阶段, 冥想, 可视化, 接地技巧 |
| **创伤与疗愈** | `Trauma-Healing-Guide.md` | 创伤机理, PTSD症状, 三阶段治疗模型 |
| **角色与身份** | `Roles-Identity-Guide.md` | 宿主, 守门人, 保护者, 照护者 |
| **理论与分类** | `Theory-Classification-Guide.md` | 结构性解离, 依恋理论, 自我决定理论 |
| **文化与表现** | `Cultural-Media-Guide.md` | 影视, 文学, 动画, 游戏主题 |

!!! warning "Guide 维护要求"

    - ✅ **创建新词条**：在对应 Guide 中添加链接和简短描述
    - ✅ **更新词条**：检查 Guide 中的描述是否需要同步更新
    - ✅ **跨主题词条**：同时更新所有相关 Guide
    - ✅ **删除/重命名**：同步更新所有引用该词条的 Guide

#### 🔗 链接路径规范

| 链接场景 | 正确格式 | 错误示例 |
|---------|---------|---------|
| 词条间链接（同目录） | `Admin.md` | `/docs/entries/Admin.md` |
| 词条→其他目录 | `../contributing/index.md` | `/contributing/index.md` |
| 其他目录→词条 | `../entries/Admin.md` | `Admin.md` |

!!! danger "禁止事项"

    - ❌ 绝对路径（如 `/docs/entries/DID.md`）
    - ❌ 模糊链接或锚点不明确
    - ❌ 不存在的文件引用

---

## 2. 站点配置与前端规则

!!! info "当前框架"
    **MkDocs Material** - 静态站点生成器

### 🛠 配置文件一览

| 文件 | 用途 |
|------|------|
| `mkdocs.yml` | 站点元信息、主题、插件、导航结构 |
| `requirements.txt` | Python 依赖清单 |
| `.cfpages-build.sh` | Cloudflare Pages 构建脚本 |
| `docs/assets/extra.css` | 自定义样式 |
| `docs/assets/extra.js` | 自定义脚本 |

### 2.1 提示块语法

!!! tip "Material for MkDocs 提示块"
    使用提示块强调重要信息时，注意 **缩进使用四个空格**。

#### 常用提示块类型

```markdown
!!! note "笔记标题（可选）"
    这是一个笔记块。

!!! tip "提示"
    这是一个提示块，用于分享有用建议。

!!! warning "警告"
    这是一个警告块，用于提醒注意事项。

!!! danger "危险"
    这是一个危险块，用于严重警告。

!!! success "成功"
    这是一个成功块，用于展示正面结果。

!!! info "信息"
    这是一个信息块，用于补充说明。

!!! quote "引用"
    这是一个引用块。

??? question "可折叠问题块"
    这是一个可折叠的问答块。
    点击标题可展开/收起内容。
```

---

## 3. 工具与脚本

!!! info "工具位置"

    - **代码**：`tools/` 目录
    - **文档**：`docs/dev/Tools-Index.md`（必须同步维护）

### 📦 PDF 导出工具规范

**位置**：`tools/pdf_export/`

| 要求类别 | 具体规范 |
|---------|---------|
| **环境** | Python ≥ 3.10 |
| **代码风格** | 使用 `pathlib.Path`，禁止字符串拼接路径 |
| **编程规范** | 函数化/`dataclass`/类型注解 |
| **兼容性** | 注意 LaTeX/Markdown 转换的跨平台兼容与转义 |

!!! warning "文档同步要求"
    修改导出逻辑后，**必须同步更新** `docs/dev/Tools-Index.md`。

---

## 4. 提交与版本管理

### 4.1 提交规范

!!! info "Conventional Commits"
    使用标准化的提交信息前缀：

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat:` | 新增条目或功能 | `feat: 新增 Grounding 词条` |
| `fix:` | 修复错误或错别字 | `fix: 修正 DID 定义中的错误` |
| `docs:` | 文档说明调整 | `docs: 更新贡献指南` |
| `refactor:` | 代码重构或结构调整 | `refactor: 重组词条分类` |
| `chore:` | 构建/配置/依赖更新 | `chore: 更新 MkDocs 版本` |
| `style:` | 格式化（非语义变更） | `style: 统一缩进格式` |

### 4.2 Pull Request 要求

!!! warning "PR 说明必须包含"

    - ✅ 变更动机
    - ✅ 主要改动点
    - ✅ 潜在风险
    - ✅ 关联词条或文档
    - ⚠️ 若涉及自动生成/重写，需列出所用方法（正则/脚本名/范围等）

### 4.3 忽略文件

!!! tip "提交前检查"
    确认 `ignore.md` 与项目实际状态一致。

### 4.4 版本发布流程

!!! danger "发布前必须执行"

    1. **核对 `changelog.md`**：
        - 版本号正确
        - 日期准确
        - 关键变更完整
        - 与实际改动一致

    2. **检查 `docs/index.md` 页面**，确保版本信息正确。

    3. **使用 GitHub CLI 发布**：

       ```bash
       # 创建新 Release
       gh release create <tag> --notes-file changelog.md

       # 或编辑现有 Release
       gh release edit <tag> --notes-file changelog.md
       ```

    4. **推送标签**：

       ```bash
       git push origin <tag>
       ```

!!! warning "重要提醒"
    若 `changelog.md` 未更新或与实际不符，**先补全记录再创建 Release**。

---

## 5. Python 环境配置

### 5.1 系统要求

| 要求 | 版本 |
|------|------|
| Python | ≥ 3.8 |
| pip | 最新版本 |

### 5.2 推荐配置方式

=== "方式一：虚拟环境（推荐）"

    !!! success "适用场景"
        Debian/Ubuntu 等外部管理 Python 环境的系统

    ```bash
    # 1. 安装 venv 支持（如需要）
    sudo apt install python3.12-venv  # 或对应的 Python 版本

    # 2. 创建虚拟环境
    python3 -m venv venv

    # 3. 激活虚拟环境
    source venv/bin/activate

    # 4. 安装依赖
    pip install -r requirements.txt
    ```

    !!! tip "后续使用"
        每次使用项目工具前，需先激活虚拟环境：
        ```bash
        source venv/bin/activate
        ```

=== "方式二：系统级安装"

    !!! info "适用场景"
        非托管 Python 环境（如 macOS、Windows）

    ```bash
    # 直接安装依赖
    pip install -r requirements.txt
    ```

### 5.3 常见问题解决

??? question "`pip: command not found` 错误"

    ```bash
    # 方法 1：使用 python3 -m pip
    python3 -m pip install -r requirements.txt

    # 方法 2：安装 pip
    python3 -m ensurepip --default-pip

    # 方法 3：系统包管理器安装
    sudo apt install python3-pip
    ```

??? question "`externally-managed-environment` 错误"

    !!! danger "这是 Debian/Ubuntu 系统的安全特性"

        - ✅ **推荐**：使用虚拟环境（见 5.2 方式一）
        - ❌ **不推荐**：使用 `--break-system-packages`（可能破坏系统 Python 环境）

---

## 6. 测试与检查

### 🔍 MkDocs 本地预览（推荐）

```bash

# 1. 安装依赖（在虚拟环境中）

pip install -r requirements.txt

# 2. 启动本地服务器（支持热重载）

mkdocs serve

# 3. 访问 http://127.0.0.1:8000

```

### 🏗 构建测试

```bash

# 构建静态站点

mkdocs build

# 严格模式构建（有警告则失败）

mkdocs build --strict
```

### 🔗 链接规范检查

!!! info "链接检查工具"
    检查 Markdown 文件中的内部链接是否符合项目规范。支持检查整个项目、指定目录或单个文件。

```bash

# 检查词条目录的所有链接

python3 tools/check_links.py docs/entries/

# 检查整个项目的所有链接

python3 tools/check_links.py

# 检查单个文件

python3 tools/check_links.py docs/entries/DID.md

# 显示详细检查信息（包含通过的文件）

python3 tools/check_links.py --verbose docs/entries/

# 指定仓库根目录（当不在项目根目录时）

python3 tools/check_links.py --root /path/to/repo docs/entries/
```

!!! tip "链接规范快速参考"

    - ✅ **词条间链接**：直接使用文件名（如 `DID.md`）
    - ✅ **词条→其他目录**：使用 `../` 相对路径（如 `../contributing/index.md`）
    - ✅ **其他目录→词条**：使用 `../entries/` 路径（如 `../entries/DID.md`）
    - ❌ **禁止**：绝对路径（如 `/docs/entries/DID.md`）

    详见：[链接路径规范](#13-索引与链接规范)

### 🐍 Python 语法检查

```bash

# 检查特定脚本

python -m compileall tools/pdf_export/export_to_pdf.py

# 检查整个工具目录

python -m compileall tools/
```

---

## 7. 自动化维护规则（代理/脚本必须遵循）

!!! danger "强制要求"

    | 符号 | 规则 | 说明 |
    |------|------|------|
    | ✅ | 遵循贡献指南与模板 | `docs/contributing/` + `docs/TEMPLATE_ENTRY.md` |
    | ✅ | 保持小步提交 | 最小可审查单位 |
    | ✅ | 遵守 markdownlint | 格式规范 |
    | ✅ | 提交前运行检查 | `fix_markdown.py` + `check_links.py` + `markdownlint` |
    | ✅ | PR 说明方法来源 | 正则/脚本名/范围等 |
    | ✅ | 同步维护工具文档 | `docs/dev/Tools-Index.md` |
    | ❌ | 禁止无法追溯的证据 | 需可验证来源 |
    | ❌ | 禁止破坏索引/链接 | 保持引用完整性 |
    | ⚠️ | 大规模操作附回滚指引 | 格式化/重构等 |

---

## 8. Markdown 自动修复与校验

!!! info "执行优先级"
    自动执行优先；手动修改后需手动执行。

### 8.1 自动执行（CI 双重检查）

!!! success "PR 阶段检查（`.github/workflows/pr-check.yml`）"
    当创建或更新 PR 时，CI 会自动检查：

    1. 🔍 **检查链接规范**
        - 检查所有修改的 Markdown 文件
        - 不符合规范时显示详细错误并阻止合并
        - 只检查不修复，确保提交前质量

    2. 📋 **检查 Frontmatter 格式**
        - 验证词条必需字段（title, topic, tags）
        - 格式错误时提供修复指引和 Guide 映射表链接

    3. ✅ **通过后才可合并**
        - 所有检查通过才能合并到 main
        - 时间戳会在合并后自动更新

    详见 `.github/workflows/pr-check.yml`

!!! success "合并后自动修复（`.github/workflows/auto-fix-entries.yml`）"
    当词条文件（`docs/entries/*.md`）被推送到 main 分支时，CI 会自动执行：

    1. ✅ 运行 `python3 tools/update_git_timestamps.py` 更新时间戳
    2. 🔍 检查链接规范（修复前）
    3. ✅ 运行 `python3 tools/fix_markdown.py docs/entries/` 自动修复格式
    4. 🔍 **检查链接规范（修复后）** - 如不通过则 CI 失败，不会提交
    5. ✅ 自动提交修复后的文件（仅当所有检查通过且有更改时）

    详见 `.github/workflows/auto-fix-entries.yml`

!!! tip "CI 双重保障机制"
    - **第一道防线（PR 阶段）**：提前发现问题，避免将问题合并到 main
    - **第二道防线（合并后）**：自动修复格式，最终验证质量
    - **结果**：确保 main 分支始终保持高质量

!!! info "手动触发"
    也可以通过 GitHub Actions 页面手动触发工作流

### 8.2 手动执行（本地）

```bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 自动修复

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 处理当前目录及子目录所有 Markdown 文件

python3 tools/fix_markdown.py .

# 可选：仅查看将修改哪些文件（不实际修改）

python3 tools/fix_markdown.py --dry-run .

# 可选：仅修复特定文件

python3 tools/fix_markdown.py docs/entries/DID.md

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Markdownlint 校验

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# MkDocs 项目检查

markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"

# 或检查所有 Markdown

markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor" --ignore "site"
```

### 8.3 规则说明与例外

#### ✅ 脚本自动修复的规则

- `MD012` - 多余空行
- `MD022` - 标题前后空行
- `MD040` - 代码块语言标识
- `MD009` - 行尾空格
- `MD034` - 裸露 URL
- `MD047` - 文件末尾空行
- `MD028` - 连续空白引用块

#### ⚠️ 需人工处理的规则

| 规则 | 说明 | 解决方法 |
|------|------|---------|
| `MD024` | 重复标题 | 调整为唯一标题或降级层级 |
| `MD052` | 参考式链接缺失定义 | 补充 `[n]: [https://...`](https://...`) |
| `MD042` | 徽章空链接 | 修正为有效 URL |
| `MD051` | 无效锚点 | 检查并修正锚点引用 |

---

## 📖 附录：快速参考

### 关键命令速查

```bash

# 环境配置

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 本地预览

mkdocs serve

# 格式检查

python3 tools/fix_markdown.py .
markdownlint "docs/**/*.md" --ignore "node_modules"

# 链接检查

python3 tools/check_links.py docs/entries/

# 构建测试

mkdocs build --strict
```

### 关键文档路径

| 文档 | 路径 |
|------|------|
| 词条模板 | `docs/TEMPLATE_ENTRY.md` |
| 贡献指南 | `docs/contributing/` |
| 工具说明 | `docs/dev/Tools-Index.md` |
| 管理员指南 | `docs/ADMIN_GUIDE.md` |
| GitHub 工作流 | `docs/GITHUB_WORKFLOW.md` |

---

!!! success "文档版本"
    最后更新：2025-01-XX
    如有疑问，请查阅项目 Wiki 或提交 Issue。
