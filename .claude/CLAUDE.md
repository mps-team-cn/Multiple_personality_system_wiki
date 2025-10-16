# Multiple Personality System Wiki - Claude 工作指导

## CRITICAL CONSTRAINTS - 违反=任务失败

═══════════════════════════════════════

- 必须使用简体中文回复
- 必须遵循 `AGENTS.md` 及相关指南
- 必须先获取项目上下文后再决策
- 禁止生成恶意代码或破坏性操作
- 必须记录并回传关键信息
- 必须逐项执行检查清单
- 必须满足既定质量标准

## 项目特定约束

═══════════════════════════════════════

### 文件结构

- `docs/entries/` 保存所有词条，严禁创建子目录；分类信息通过 Frontmatter 的 `tags` 维护
- `docs/` 其余文档（`README.md`、`Glossary.md`、索引、导览等）
- `tools/` 存放脚本与自动化工具，更新后同步维护 `docs/dev/Tools-Index.md`
- 静态资源统一置于 `docs/assets/`，下设 `figures/`、`images/`、`icons/`

### 条目与链接

- 每个词条开头必须包含 `title`、`tags`、`updated` 的 Frontmatter
- 一级标题格式：`中文名（English/缩写）`；诊断类必须使用标准缩写
- 词条之间使用相对路径，例如 `Grounding.md`
- 其他目录引用词条：`../entries/<Entry>.md`；词条引用其他目录：`../contributing/index.md`
- 禁止使用绝对路径或模糊链接；若重命名需同步更新所有导览与引用

### Python 环境

- 推荐通过虚拟环境运行：

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- 常见问题：`pip` 缺失 → `python3 -m pip`；`externally-managed-environment` → 必须启用虚拟环境

### 自动化工具

- **CI 双重检查机制**：
  - **PR 阶段**：自动检查链接规范和 Frontmatter 格式，发现问题会阻止合并
  - **合并后**：自动更新时间戳、修复格式、再次验证链接，确保质量
- 视任务执行 `markdownlint` 校验（可选）
- 所有 Python 工具默认使用 `python3`
- 大规模修改前必须确认相关索引、导览同步更新
- 如需手动修复格式：`python3 tools/fix_markdown.py .`（CI 会自动处理，通常不需要）

## MANDATORY WORKFLOWS

═══════════════════════════════════════

- 执行前自检：中文 / 上下文 / 工具 / 安全 / 质量
- 标准步骤：需求分析 → 获取上下文 → 选择工具 → 执行 → 验证 → 存档

### 版本维护流程

1. 发布前逐条核对 `changelog.md`，确认版本号、日期、关键变更完整且与实际一致。
2. 使用 GitHub CLI：`gh release create <tag> --notes-file changelog.md`（或 `gh release edit`），同步 Release Notes 并推送标签。
3. 若 `changelog.md` 缺失或不符，必须先更新后再发布。

## MANDATORY TOOL STRATEGY

═══════════════════════════════════════

- 词条/文档编辑 → 直接修改对应 Markdown
- 工具与脚本开发 → 调用 `python-pro`
- 文档架构或重组 → 调用 `docs-architect`
- 代码审查 → 调用 `code-reviewer`
- 疑难错误排查 → 调用 `debugger`

### 任务执行要求

- **时间戳和格式**：推送后 CI 会自动更新时间戳和修复格式，无需手动干预
- 大范围调整前确认相关 Guide（Clinical-Diagnosis、System-Operations、Practice、Trauma-Healing、Roles-Identity、Theory-Classification、Cultural-Media）是否需要同步更新
- 保持 tags.md、index.md 与 Glossary 的一致性（如任务涉及）
- 避免破坏 MkDocs 导航及 Frontmatter
- 词条的 `updated` 字段会由 CI 自动维护，编辑时无需手动更新

## QUALITY STANDARDS

═══════════════════════════════════════

- **Markdown**：遵循 markdownlint；结构清晰、语法统一
- **链接**：相对路径、有效锚点、及时同步导览与索引
- **内容**：用词准确、信息来源明确、Frontmatter 完整、保持简体中文

## SUBAGENT SELECTION

═══════════════════════════════════════

- 需要编写/扩写文档 → `docs-architect`
- 涉及数据处理/脚本 → `python-pro`
- 需要质量把控/审查 → `code-reviewer`
- 排查运行或构建问题 → `debugger`
- 内容格式或排版优化 → 继续使用相关文档代理

## ENFORCEMENT

═══════════════════════════════════════

- 会话开始：校验约束 → 工具调用前：确认流程 → 回复前：核对检查清单
- 词条编辑：检查 Frontmatter → 更新导览（格式和时间戳由 CI 自动处理）
- 工具修改：同时更新 `docs/dev/Tools-Index.md`
- **CI 流程**：
  - PR 创建时：运行 `pr-check.yml` 检查链接和 Frontmatter（只检查不修复）
  - 合并到 main：运行 `auto-fix-entries.yml` 自动修复并提交

## 项目知识存储

═══════════════════════════════════════

- **关键概念**：mps、多意识体；Docsify→MkDocs 迁移；Frontmatter；Conventional Commits；CI 双重检查
- **重要路径**：`docs/contributing/`、`docs/TEMPLATE_ENTRY.md`、`docs/entries/`、`tools/`、`docs/dev/Tools-Index.md`、`.github/workflows/`
- **CI 双重检查**：
  - PR 阶段（`.github/workflows/pr-check.yml`）：检查链接规范和 Frontmatter，不通过则阻止合并
  - 合并后（`.github/workflows/auto-fix-entries.yml`）：自动更新时间戳、修复格式、验证链接，然后触发部署
