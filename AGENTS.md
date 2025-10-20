# Multiple Personality System Wiki - AI 代理工作规范

> **文档定位**:本文档是 **AI 代码助手(Codex/Claude/GitHub Copilot)** 的操作手册,定义了自动化贡献的强制规则与质量标准。人工贡献者请参考 [docs/contributing/](docs/contributing/)。

!!! danger "AI 代理必读 - 违反 = 任务失败"
    本文档优先级 **高于** AI 默认行为。所有自动化操作必须严格遵循以下规范。

---

## 🎯 快速开始(AI 代理 30 秒速查)

### 核心原则

```yaml
✅ 必须遵守:
  - 语言: 简体中文(代码/命令除外)
  - 路径: 相对路径(禁止绝对路径)
  - 提交: 小步提交 + Conventional Commits
  - 时间戳: 让 CI 自动更新(勿手动修改)
  - Guide 同步: 修改词条必须更新对应 Guide

❌ 严禁操作:
  - 使用绝对路径链接(如 /docs/entries/DID.md)
  - 手动修改 updated 时间戳(CI 自动处理)
  - 破坏 Frontmatter 结构
  - 跳过链接检查
  - 在 docs/entries/ 创建子目录
```

### 决策树(任务开始前必查)

```text
┌─ 修改词条?
│  ├─ 读取 docs/TEMPLATE_ENTRY.md
│  ├─ 检查 Frontmatter(title/topic/tags,勿碰 updated)
│  ├─ 更新对应 Guide(见 §5 映射表)
│  └─ 使用相对路径(词条间直接 DID.md,跨目录 ../entries/DID.md)
│
┌─ 开发/修改工具?
│  ├─ 修改 tools/*.py
│  ├─ 同步更新 docs/dev/Tools-Index.md
│  └─ 命令使用 python3(不是 python)
│
┌─ 大规模重构?
│  ├─ 先列影响范围
│  ├─ 检查 7 个 Guide 是否需更新
│  ├─ 小步提交 + 回滚指引
│  └─ PR 说明自动化方法(正则/脚本/范围)
│
└─ 提交前检查
   ├─ python3 tools/check_links.py docs/entries/
   ├─ python3 tools/check_tags.py docs/entries/
   └─ mkdocs build --strict(可选)
```

---

## 📑 目录导览

### 🔴 强制阅读(执行前必看)

- [§2 AI 代理强制规则](#2-ai-代理强制规则) ⚠️ 最高优先级
- [§3 文件结构与路径](#3-文件结构与路径)
- [§4 Frontmatter 规范](#4-frontmatter-规范)
- [§5 链接规范与 Guide 映射](#5-链接规范与-guide-映射)
- [§6 提交与 CI 流程](#6-提交与-ci-流程)

### 🟡 按需查阅

- [§7 站点配置](#7-站点配置)
- [§8 工具开发](#8-工具开发)
- [§9 Python 环境](#9-python-环境)
- [§10 标签规范](#10-标签规范-v20)
- [§11 常见问题](#11-常见问题)

---

## 2. AI 代理强制规则

!!! danger "违反以下任一规则 = 任务失败"

### 2.1 语言规范

| 规则 | 说明 | 示例 |
|------|------|------|
| ✅ 简体中文 | 所有文本内容、提交信息 | `feat: 新增 Grounding 词条` |
| ✅ 一级标题 | `中文名(English/缩写)` | `# 解离性身份障碍(DID)` |
| ⚠️ 诊断类词条 | 括号内必须用标准缩写 | `解离性身份障碍(DID)` 不是 `解离性身份障碍` |

### 2.2 路径规范(高频错误)

| 场景 | ✅ 正确 | ❌ 错误 |
|------|---------|---------|
| 词条间链接 | `[DID](DID.md)` | `[DID](/docs/entries/DID.md)` |
| 词条→其他目录 | `[贡献指南](../contributing/index.md)` | `[贡献指南](/contributing/index.md)` |
| 其他目录→词条 | `[DID](../entries/DID.md)` | `[DID](DID.md)` |

### 2.3 提交规范

```text
<type>: <description>

type 必须是:
  feat     新增词条/功能
  fix      修复错误/错别字
  docs     文档说明调整
  refactor 结构调整/重构
  chore    构建/配置/依赖
  style    格式化(非语义)

示例:
  feat: 新增 Grounding 技巧词条
  fix: 修正 DID 诊断标准引用
  docs: 更新贡献指南链接规范
```

### 2.4 自动化操作规范

| 操作 | 规范 |
|------|------|
| ✅ 小步提交 | 每次提交最小可审查单位 |
| ✅ 提交前检查 | 必须运行 `check_links.py` + `check_tags.py` |
| ✅ PR 说明 | 大规模自动化需注明方法(正则/脚本名/范围) |
| ✅ 工具同步 | 修改 `tools/` 必须更新 `docs/dev/Tools-Index.md` |
| ❌ 无迹可查 | 禁止无法验证来源的批量修改 |
| ❌ 破坏索引 | 禁止破坏导航/引用完整性 |
| ⚠️ 大规模重构 | 必须附回滚指引 |

---

## 3. 文件结构与路径

### 3.1 目录结构(只读规则)

```text
docs/
├── entries/              # 词条存放(禁止子目录)
│   ├── DID.md
│   └── Grounding.md
├── contributing/         # 贡献指南(拆分多文件)
├── dev/
│   └── Tools-Index.md   # 工具文档(修改 tools/ 必须同步)
├── assets/
│   ├── figures/         # 流程图/示意图
│   ├── images/          # 封面/截图
│   └── icons/           # 图标
├── index.md             # 首页
├── README.md
├── Glossary.md
└── TEMPLATE_ENTRY.md    # 词条模板(必读)

tools/                    # 脚本与工具
├── check_links.py       # 链接检查(提交前必跑)
├── check_tags.py        # 标签验证(提交前必跑)
├── fix_markdown.py      # 格式修复(CI 自动)
└── update_git_timestamps.py  # 时间戳(CI 自动)
```

### 3.2 关键约束

!!! danger "严格遵守"

    - ❌ **禁止**在 `docs/entries/` 创建子目录(分类通过 Frontmatter tags 管理)
    - ✅ **必须**将静态资源放在 `docs/assets/` 对应子目录
    - ✅ **必须**修改 `tools/` 后同步更新 `docs/dev/Tools-Index.md`

---

## 4. Frontmatter 规范

### 4.1 必需字段

```yaml
---
title: 词条标题              # 必需
topic: 所属主题              # 必需,见下方主题列表
tags:                       # 必需,至少 1 个,最多 5 个
  - dx:DID                  # 格式: prefix:名称
  - sx:切换(Switch)
updated: YYYY-MM-DD        # 必需,但 CI 自动维护,勿手动改
---
```

### 4.2 可选字段

```yaml
search:
  boost: 1.8               # 搜索权重(仅核心词条使用)
```

**权重分级参考**:

| 优先级 | 值 | 适用 | 示例 |
|--------|-----|------|------|
| 最高 | 2.0 | 诊断类 | DID/OSDD/PTSD/CPTSD |
| 高 | 1.8 | 核心概念 | Alter/System/Switch/Grounding |
| 中高 | 1.5 | 重要概念 | Protector/Host/Dissociation |
| 默认 | 1.0 | 普通词条 | 无需设置 |

### 4.3 主题列表(topic 必须从此选择)

```text
诊断与临床      # DID/OSDD/CPTSD/焦虑障碍/情绪障碍
系统运作        # 前台切换/共同意识/记忆管理/内部空间
实践指南        # Tulpa 三阶段/冥想/可视化/接地技巧
创伤与疗愈      # 创伤机理/PTSD 症状/三阶段治疗模型
角色与身份      # 宿主/守门人/保护者/照护者
理论与分类      # 结构性解离/依恋理论/自我决定理论
文化与表现      # 影视/文学/动画/游戏主题
```

### 4.4 例外文件(无需 updated 字段)

- `*-Guide.md`(如 `Clinical-Diagnosis-Guide.md`)
- `*-Index.md`(如 `Tools-Index.md`)

---

## 5. 链接规范与 Guide 映射

### 5.1 链接路径速查表

| 链接场景 | 格式 | 示例 |
|---------|------|------|
| **词条间** | `文件名.md` | `[DID](DID.md)` |
| **词条→Guide** | `../contributing/XX-Guide.md` | `[诊断指南](../contributing/Clinical-Diagnosis-Guide.md)` |
| **Guide→词条** | `../entries/XX.md` | `[DID](../entries/DID.md)` |
| **词条→首页** | `../index.md` | `[首页](../index.md)` |

### 5.2 Guide 映射表(修改词条必须同步更新对应 Guide)

| 词条主题(topic) | 对应 Guide 文件 | 操作 |
|----------------|----------------|------|
| **诊断与临床** | `Clinical-Diagnosis-Guide.md` | 新增/修改/删除词条时更新链接和描述 |
| **系统运作** | `System-Operations-Guide.md` | 同上 |
| **实践指南** | `Practice-Guide.md` | 同上 |
| **创伤与疗愈** | `Trauma-Healing-Guide.md` | 同上 |
| **角色与身份** | `Roles-Identity-Guide.md` | 同上 |
| **理论与分类** | `Theory-Classification-Guide.md` | 同上 |
| **文化与表现** | `Cultural-Media-Guide.md` | 同上 |

!!! warning "Guide 更新要求"

    - ✅ 创建新词条 → 在对应 Guide 添加链接和简短描述
    - ✅ 更新词条 → 检查 Guide 描述是否需同步
    - ✅ 跨主题词条 → 同时更新所有相关 Guide
    - ✅ 删除/重命名 → 更新所有引用该词条的 Guide

---

## 6. 提交与 CI 流程

### 6.1 本地检查(提交前必做)

```bash
# 1. 检查链接规范
python3 tools/check_links.py docs/entries/

# 2. 检查标签规范
python3 tools/check_tags.py docs/entries/

# 3. (可选)构建测试
mkdocs build --strict
```

### 6.2 CI 双重检查机制

!!! success "自动化质量保障"

    **第一道防线:PR 阶段(`.github/workflows/pr-check.yml`)**

    - 🔍 检查所有修改文件的链接规范
    - 📋 验证 Frontmatter 必需字段
    - ❌ 不通过 → 阻止合并,显示详细错误
    - ✅ 只检查不修复(确保提交前质量)

    **第二道防线:合并后(`.github/workflows/auto-fix-entries.yml`)**

    - ✅ 更新 `updated` 时间戳
    - ✅ 修复 Markdown 格式
    - 🔍 再次验证链接规范
    - ✅ 自动提交修复(仅当所有检查通过)
    - 🚀 触发站点部署

### 6.3 版本发布流程

!!! danger "发布前检查清单"

    ```bash
    # 1. 核对 changelog.md
    #    - 版本号正确
    #    - 日期准确
    #    - 变更完整

    # 2. 检查 docs/index.md 版本信息

    # 3. 创建 Release
    gh release create v1.2.0 --notes-file changelog.md

    # 4. 推送标签
    git push origin v1.2.0
    ```

---

## 7. 站点配置

### 7.1 配置文件一览

| 文件 | 用途 | 修改权限 |
|------|------|---------|
| `mkdocs.yml` | 站点元信息/主题/插件/导航 | ⚠️ 谨慎修改 |
| `requirements.txt` | Python 依赖 | ✅ 可修改 |
| `.cfpages-build.sh` | Cloudflare Pages 构建 | ⚠️ 谨慎修改 |
| `docs/assets/extra.css` | 自定义样式 | ✅ 可修改 |
| `docs/assets/extra.js` | 自定义脚本 | ✅ 可修改 |

### 7.2 提示块语法(Material for MkDocs)

```markdown
!!! note "笔记"
    缩进使用 4 个空格

!!! tip "提示"
    用于分享建议

!!! warning "警告"
    用于注意事项

!!! danger "危险"
    用于严重警告

!!! success "成功"
    用于正面结果

!!! info "信息"
    用于补充说明

??? question "可折叠问答"
    点击标题展开/收起
```

---

## 8. 工具开发

### 8.1 PDF 导出工具规范

**位置**:`tools/pdf_export/`

| 规范 | 要求 |
|------|------|
| Python 版本 | ≥ 3.10 |
| 代码风格 | 使用 `pathlib.Path`,禁止字符串拼接路径 |
| 编程规范 | 函数化/`dataclass`/类型注解 |
| 兼容性 | 注意 LaTeX/Markdown 转换的跨平台兼容 |

### 8.2 工具文档同步(强制)

!!! danger "修改 `tools/` 必须同步更新 `docs/dev/Tools-Index.md`"

    包括:
    - 工具用途说明
    - 使用方法
    - 参数说明
    - 示例命令

---

## 9. Python 环境

### 9.1 推荐配置(虚拟环境)

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 9.2 常见问题

??? question "`pip: command not found`"

    ```bash
    # 方法 1: 使用 python3 -m pip
    python3 -m pip install -r requirements.txt

    # 方法 2: 安装 pip
    python3 -m ensurepip --default-pip
    ```

??? question "`externally-managed-environment`"

    !!! danger "Debian/Ubuntu 系统安全特性"
        - ✅ 推荐: 使用虚拟环境
        - ❌ 不推荐: `--break-system-packages`(可能破坏系统)

---

## 10. 标签规范 v2.0

!!! danger "MPS Wiki Tagging Standard v2.0"

### 10.1 强制规则

```yaml
格式: prefix:名称
  - 前缀小写,中文为主,必要英文置于全角括号
  - 示例: dx:DID | sx:切换(Switch) | tx:EMDR

数量: 每篇词条 1-5 个标签

来源: 必须来自以下分面前缀
  - dx(诊断) | sx(系统运作) | tx(治疗)
  - scale(量表) | theory(理论) | ops(操作)
  - role(角色) | community(社区) | guide(指南)
  - history(历史) | misuse(误用) | bio(生理)
  - sleep(睡眠) | dev(工具) | culture(文化)
  - meta(元数据)

禁止:
  - 无前缀标签
  - 页面标题型标签(标签名 = title)
  - 空格/句号/英文半角括号
  - 别名(通过 data/tags_alias.yaml 映射)
```

### 10.2 验证命令

```bash
# 检查单个文件
python3 tools/check_tags.py docs/entries/DID.md

# 检查整个目录
python3 tools/check_tags.py docs/entries/

# 正则校验: ^[a-z]+:[^\s()]+$
```

!!! info "完整规范"
    详见:`docs/contributing/tagging-standard.md`

---

## 11. 常见问题

### 11.1 错误场景与解决

| 错误 | 原因 | 解决 |
|------|------|------|
| `check_links.py` 报错 | 使用了绝对路径或错误相对路径 | 查看 [§5.1 链接路径速查表](#51-链接路径速查表) |
| CI `pr-check` 失败 | Frontmatter 缺失字段或链接不规范 | 查看 CI 日志具体错误,修复后重新推送 |
| `mkdocs build` 失败 | 导航配置或链接损坏 | 运行 `mkdocs build --strict` 查看详细错误 |
| 标签验证失败 | 标签格式不符或使用了别名 | 运行 `check_tags.py` 查看具体问题 |

### 11.2 快速命令参考

```bash
# 环境配置
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 本地预览
mkdocs serve  # 访问 http://127.0.0.1:8000

# 提交前检查
python3 tools/check_links.py docs/entries/
python3 tools/check_tags.py docs/entries/
mkdocs build --strict

# 格式修复(CI 会自动执行,通常无需手动)
python3 tools/fix_markdown.py docs/entries/
```

---

## 📖 附录:关键文档路径

| 文档 | 路径 | 用途 |
|------|------|------|
| 词条模板 | `docs/TEMPLATE_ENTRY.md` | 新建词条必读 |
| 贡献指南 | `docs/contributing/` | 人工贡献参考 |
| 工具说明 | `docs/dev/Tools-Index.md` | 脚本使用指南 |
| 管理员指南 | `docs/ADMIN_GUIDE.md` | 管理员操作 |
| GitHub 工作流 | `docs/GITHUB_WORKFLOW.md` | CI/CD 说明 |
| 标签规范 | `docs/contributing/tagging-standard.md` | 标签详细规范 |

---

## 🔄 文档更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2025-01-XX | 2.0 | 重构为 AI 代理优化版本,增加决策树和快速开始 |
| 2024-XX-XX | 1.0 | 原贡献与开发约定文档 |

---

**文档维护**: 本文档随项目演进持续更新。AI 代理在执行任务前应检查最新版本。
