# Multiple Personality System Wiki - Claude 工作指导

## CRITICAL CONSTRAINTS - 违反=任务失败

═══════════════════════════════════════

- 必须使用简体中文回复
- 必须遵循 AGENTS.md 所有规范
- 必须先获取项目上下文
- 禁止生成恶意代码
- 必须存储重要知识
- 必须执行检查清单
- 必须遵循质量标准

## 项目特定约束

═══════════════════════════════════════

### 文件结构规范

- 词条：`docs/entries/` 目录，禁止子目录
- 工具：`tools/` 目录
- 文档：`docs/` 目录
- 贡献指南：`docs/contributing/`（拆分为多个专题文档）
- 静态资源：`docs/assets/` 目录
  - `docs/assets/figures/` - 图表、流程图、示意图、SVG 等
  - `docs/assets/images/` - 一般图片（封面、截图等）
  - `docs/assets/icons/` - 小图标、装饰性素材

### 条目编写规范

- 一级标题：`中文名（English/缩写）`
- Frontmatter 必须包含：`title`、`tags`、`updated`
- 内部链接规范：
  - 词条间链接（同目录）：`Admin.md`（相对路径）
  - 跨目录到词条：`../entries/Admin.md`
  - 词条到其他目录：`../contributing/index.md`
  - MkDocs 会自动处理 `.md` 扩展名转换为 HTML
  - **禁止** 使用绝对路径（如 `/docs/entries/DID.md`）
- 提交信息：Conventional Commits 格式

### Python 环境配置

- **推荐方式**：使用虚拟环境
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- **常见问题**：
  - `pip: command not found` → 使用 `python3 -m pip`
  - `externally-managed-environment` → 必须使用虚拟环境
  - 详见 `AGENTS.md` 第 5 章节或 `docs/contributing/技术约定.md` 第 7 章节

### 自动化工具要求

- `python tools/fix_markdown.py` - Markdown 自动修复
- 所有 Python 工具必须在虚拟环境中运行（推荐）

## MANDATORY WORKFLOWS

═══════════════════════════════════════

执行前检查清单：
[ ] 中文 [ ] 上下文 [ ] 工具 [ ] 安全 [ ] 质量

标准工作流：

1. 分析需求 → 2. 获取上下文 → 3. 选择工具 → 4. 执行任务 → 5. 验证质量 → 6. 存储知识

## MANDATORY TOOL STRATEGY

═══════════════════════════════════════

### 优先调用策略

- 词条编辑 → 直接编辑相关文件
- 工具开发 → python-pro
- 文档维护 → docs-architect
- 代码审查 → code-reviewer
- 错误调试 → debugger

### 任务执行要求

- 提交前必须运行：`python tools/fix_markdown.py`
- 大规模修改前必须：检查相关索引和链接
- 标签索引由 MkDocs Material tags 插件自动生成，无需手动维护
- **创建或更新条目时必须同步维护对应的 Guide 条目**：
  - 治疗方法 → `Mental-Health-Guide.md`、`Three-Phase-Trauma-Treatment.md`
  - 核心概念 → `Core-Concepts-Guide.md`
  - 诊断标准 → `Clinical-Diagnosis-Guide.md`
  - 确保引用链接和描述的一致性

## QUALITY STANDARDS

═══════════════════════════════════════

### Markdown 规范

- 遵循 markdownlint 规则
- 使用项目自动修复工具
- 保持一致的格式和结构

### 链接管理

- 内部链接使用完整路径
- 定期检查链接有效性
- 同步维护 tags.md 和 index.md

### 内容质量

- 简体中文优先
- 准确的术语使用
- 完整的元数据信息

## SUBAGENT SELECTION

═══════════════════════════════════════

必须主动调用合适子代理：

- Python 工具开发 → python-pro
- 文档编写维护 → docs-architect
- 代码质量审查 → code-reviewer
- 错误问题调试 → debugger
- 内容格式优化 → 文档相关代理

## ENFORCEMENT

═══════════════════════════════════════

强制触发器：会话开始 → 检查约束，工具调用前 → 检查流程，回复前 → 验证清单

项目特有触发器：

- 词条编辑 → 检查 Frontmatter → 运行索引工具 → **更新对应 Guide 条目**
- 工具修改 → 更新 docs/tools/README.md
- 提交前 → 运行 fix_markdown 和 markdownlint

## 项目知识存储

═══════════════════════════════════════

### 关键概念

- Plurality（多重意识体）
- Docsify 静态站点
- Frontmatter 元数据
- Conventional Commits

### 重要文件路径

- `AGENTS.md` - 完整开发规范
- `CONTRIBUTING.md` - 贡献指南简化版（详细版在 `docs/contributing/`）
- `docs/contributing/` - 贡献指南详细文档目录
- `docs/TEMPLATE_ENTRY.md` - 词条模板
- `docs/entries/` - 词条目录
- `tools/` - 工具目录
- `docs/tools/README.md` - 工具使用说明
