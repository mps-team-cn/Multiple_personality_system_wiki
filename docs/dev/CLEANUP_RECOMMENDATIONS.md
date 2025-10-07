# Tools 清理建议报告

> **生成日期**：2025-10-07
> **背景**：Docsify → MkDocs Material 迁移后的工具审查

---

## 📊 审查概览

| 类别 | 数量 | 说明 |
|------|------|------|
| 可删除 | 2 | 功能已被 MkDocs Material 取代 |
| 需评估 | 7 | 标签管理工具组，需确认使用情况 |
| 保留 | 6 | 核心工具，仍然需要 |

---

## 🗑️ 建议删除的工具（2 个）

### 1. `docs_preview.py`

**功能**：本地预览服务器（支持 Docsify 和 Python http.server）

**删除理由**：
- 为 Docsify 设计，支持 `docsify-cli` 启动
- MkDocs Material 提供内置预览命令：`mkdocs serve`
- MkDocs 预览功能更强大（热重载、自动构建）

**替代方案**：
```bash
# 基本预览
mkdocs serve

# 自定义端口
mkdocs serve --dev-addr=127.0.0.1:4173

# 生产模式预览
mkdocs build && python -m http.server -d site/ 8080
```

**影响评估**：✅ 无影响，MkDocs 命令更简单

---

### 2. `generate_tags_index.py`

**功能**：根据 Frontmatter 自动生成 `docs/tags.md` 标签索引页面

**删除理由**：
- MkDocs Material 的 `tags` 插件自动生成标签页面
- 当前 `docs/tags.md` 已改为手动维护的导览页 + 自动标签列表
- 使用 `<!-- material/tags -->` 注释自动插入标签

**当前 tags.md 结构**：
```markdown
# 标签索引

浏览全部词条的分类标签...

## 主题导览
- 诊断与临床
- 系统运作
...

## 全部标签
<!-- material/tags -->  ← 自动生成部分
```

**替代方案**：
- 无需脚本，MkDocs Material tags 插件自动处理
- 手动维护导览部分即可

**影响评估**：✅ 无影响，功能已被插件取代

---

## ⚠️ 需要评估的工具（7 个）

### 标签管理工具组

这些工具用于批量管理和优化词条标签，需要确认是否仍在使用：

| 工具 | 功能描述 | 评估问题 |
|------|----------|----------|
| `add_top_level_tags.py` | 添加顶层标签 | 是否还需要批量添加标签？ |
| `add_topic_tags.py` | 添加主题标签 | MkDocs tags 是否足够？ |
| `analyze_current_tags.py` | 分析当前标签使用情况 | 是否需要标签统计？ |
| `analyze_tags.py` | 标签分析 | 功能是否重复？ |
| `optimize_tags.py` | 优化标签结构 | 是否还在优化标签？ |
| `update_entry_tags.py` | 更新词条标签 | 是否需要批量更新？ |
| `retag_and_related.py` | 重新标记和关联分析 | 27KB 大文件，功能复杂 |

**建议**：
1. 检查最近 3 个月的使用记录
2. 如果不再使用，移动到 `tools/deprecated/` 目录
3. 如果仍需要，考虑整合为统一的标签管理 CLI

---

## ✅ 建议保留的工具（6 个）

### 核心工具

| 工具 | 功能 | 保留理由 |
|------|------|----------|
| `fix_markdown.py` | Markdown 格式自动修复 | 核心工具，与 MkDocs 无关 |
| `check_links.py` | 链接有效性检查 | MkDocs 无内置链接检查 |
| `gen-validation-report.py` | 内容校验报告 | 质量控制必需 |
| `fix_bold_format.py` | 修复粗体格式 | 格式清理工具 |
| `fix_list_bold_colon.py` | 修复列表粗体冒号格式 | 格式清理工具 |
| `gen_changelog_by_tags.py` | 基于 Git 标签生成变更日志 | 发布管理需要 |

---

## 📋 执行计划

### 第一步：删除过时工具（立即执行）

```bash
# 创建备份目录
mkdir -p tools/deprecated

# 移动过时工具
git mv tools/docs_preview.py tools/deprecated/
git mv tools/generate_tags_index.py tools/deprecated/

# 提交
git commit -m "refactor: 移除 Docsify 时代的过时工具

- docs_preview.py → 使用 mkdocs serve 替代
- generate_tags_index.py → 使用 MkDocs Material tags 插件替代

相关文档：tools/CLEANUP_RECOMMENDATIONS.md"
```

### 第二步：评估标签工具（需调研）

**调研问题**：
1. 这些工具最后使用时间？
2. 是否在 CI/CD 中使用？
3. 是否有文档依赖？
4. 功能是否可被 MkDocs 插件替代？

**方法**：
```bash
# 查看最后修改时间
ls -lt tools/*.py

# 搜索使用引用
rg -g "*.{sh,bat,yml,yaml,md}" "add_top_level_tags|add_topic_tags|analyze_tags"

# 检查 Git 历史
git log --all --oneline --since="3 months ago" -- tools/add_*.py
```

### 第三步：更新文档（同步执行）

**需要更新的文档**：
1. `tools/REFACTORING_PLAN.md` - 反映 MkDocs 迁移影响
2. `docs/contributing/工具使用.md` - 更新工具列表
3. `CONTRIBUTING/index.md` - 更新快速参考
4. `.github/workflows/*.yml` - 检查 CI 中的工具调用

---

## 🎯 预期效果

**清理后的收益**：
- ✅ 减少维护负担（删除 2 个不再需要的脚本）
- ✅ 避免混淆（明确使用 MkDocs 原生功能）
- ✅ 简化工具链（减少依赖）
- ✅ 降低学习曲线（新贡献者只需学习必要工具）

**风险控制**：
- 🛡️ 移动到 `deprecated/` 而非直接删除
- 🛡️ 保留 Git 历史，随时可恢复
- 🛡️ 更新文档，避免误用

---

## 📝 附录：MkDocs Material 替代功能对照表

| 旧工具 | MkDocs Material 功能 | 配置位置 |
|--------|---------------------|---------|
| `docs_preview.py` | `mkdocs serve` | 内置命令 |
| `generate_tags_index.py` | tags 插件 | `mkdocs.yml` - `plugins.tags` |
| 搜索索引生成 | search 插件 | `mkdocs.yml` - `plugins.search` |
| 时间戳管理 | git-revision-date-localized 插件 | `mkdocs.yml` - `plugins.git-revision-date-localized` |
| 导航生成 | `nav` 配置 | `mkdocs.yml` - `nav` |
| HTML 压缩 | minify 插件 | `mkdocs.yml` - `plugins.minify` |
| 图片灯箱 | glightbox 插件 | `mkdocs.yml` - `plugins.glightbox` |

---

**维护者**：Plurality Wiki Team
**最后更新**：2025-10-07
