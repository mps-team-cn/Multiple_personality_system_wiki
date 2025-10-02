# 更新日志

## v1.2.4 (2025-10-02)

### ✨ 新增

- 优化 PDF 封面并提升暗黑模式对比度（[3b9b997](https://github.com/kuliantnt/plurality_wiki/commit/3b9b9978a36cef7a2fcdda6d55b6db9831842da7)）

### 🐛 修复（链接/引用/格式）

- 修复 README（[17e10f8](https://github.com/kuliantnt/plurality_wiki/commit/17e10f8c71902daac9afc8d3b73873c96d09e99f)）
- 修复链接问题（[b0d378c](https://github.com/kuliantnt/plurality_wiki/commit/b0d378c5a5e52172b7a0ad6f1b933b8b2462b4fa)）
- 本地化最后更新时间插件（[bff6afe](https://github.com/kuliantnt/plurality_wiki/commit/bff6afe9d97ac6fc011a949e4da841006eac9111)）
- 修复 Docsify 最后更新时间占位符（[7d86299](https://github.com/kuliantnt/plurality_wiki/commit/7d8629913b1c819ec084c4f7cb5ffc2d37fec715)）

### 📦 杂务（脚本/CI/批处理）

- 添加 changlog（[255fbff](https://github.com/kuliantnt/plurality_wiki/commit/255fbffde42896029c2e846349f391685ce1d475)）
- 新增 GitHub 社区配置（[44d6392](https://github.com/kuliantnt/plurality_wiki/commit/44d63921b2d553f219002a30468fd31ca2057720)）
- 修改 agents（[35a9f2a](https://github.com/kuliantnt/plurality_wiki/commit/35a9f2a8f25c33519da52178c53c0f3a10557e30)）

## v1.2.3 (2025-10-01)

### ✨ 新增

- 引入 Docsify 首页与在线浏览支持；补充“后台/里空间”等术语词条。

### 🐛 修复

- 修复 PDF 导出重复标题与若干导出异常。
- 修正首页与文档页 404、直链跳转、导航加载等问题。
- 调整暗黑模式下的侧边栏与配色一致性。
- 使用 SVG favicon 以规避 PR 限制；新增 404 跳转处理。

### 📝 文档 / 结构

- 修正 ANP-EP 模型、内部空间等词条的索引与互链。
- 调整多重意识体基础词条路径并配置映射。
- 更新 README 与站点文案。

### 📦 杂务

- 保留/清理 Docsify 相关辅助与站点文件。

---

## v1.2 (2025-09-30)

### 📝 文档

- 在 README 新增“系统语录”，并统一词条标题格式。
- 润色《前言》，修复 PDF 导出缺少“前言”的问题。
- 完善 ADHD、精神分裂症等诊断描述；调整抑郁障碍词条标题。
- 新增/完善：Tulpa（图帕）、宿主等词条与命名统一。

### 🐛 修复 / 改进

- 统一入口与导航，修复首页/导航加载及直达链接 404。

### 📚 术语与索引

- 补充并维护语录、索引与若干文档条目的一致性。

---

## v1.1 (2025-09-30)

### ✨ 新增

- 新增“解离”与“侵入性思维/强迫相关”词条，并纳入索引。

---

## v1.0 (2025-09-30)

### ✨ PDF 导出（新增/改进）

- 新增“一键导出 Wiki 为 PDF”的脚本与流程。
- 支持自定义封面与目录，目录与 README 索引对齐；条目间自动分页。
- 新增忽略清单与目录构建修复（即使 README 被忽略也能正确导出）。

### 🐛 PDF 导出（修复）

- 修复中文字体不显示、LaTeX 封面格式、封面特殊字符转义等问题。
- 修复 Windows 11 环境下的导出错误、目录结构/项目根路径解析等问题。

### 📝 文档

- 新增/维护：DID（含 DSM-5 诊断标准）、CPTSD、Meditation 等词条；
  将 OSDD、Partial DID 等条目纳入 `index`/README 索引；
  多处 README/条目内容与格式修正（含病理学相关内容维护）。

### 🗂️ 结构与规范

- 调整与归档：按主题重组 `entries/` 目录结构；
- 新增贡献指南（CONTRIBUTING/AGENTS 等），统一写作与提交流程。

---

— 由 Git 提交记录自动整理（合并同类项、去除纯合并/无信息提交）
