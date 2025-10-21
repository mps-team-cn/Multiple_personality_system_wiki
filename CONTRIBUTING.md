# Multiple Personality System Wiki 贡献指南

欢迎参与 **Multiple Personality System Wiki** 的建设！

本文件是 GitHub 标准贡献指南的简要版本。 **详细规范请查阅 [完整贡献指南](docs/contributing/index.md)** 。

---

## 🚀 快速开始

### 1. 了解规范

- [编写规范](docs/contributing/writing-guidelines.md) - 语言、格式、Markdown 规范
- [学术引用](docs/contributing/academic-citation.md) - 引用格式与证据分级
- [诊断临床规范](docs/contributing/clinical-guidelines.md) - 病理学内容要求
- [技术约定](docs/contributing/technical-conventions.md) - 文件结构与链接管理
- [标签规范 v2.0](docs/contributing/tagging-standard.md) - 分面前缀与自动校验
- [PR 流程](docs/contributing/pr-workflow.md) - 提交流程与检查清单
- [贡献者墙](docs/contributing/contributors.md) - 查看所有贡献者

### 2. 本地开发

#### 方式 A：使用 Sveltia CMS（推荐）

**在线编辑**：

- 访问 <https://wiki.mpsteam.cn/admin/>
- 使用 GitHub 账号登录
- 需要有仓库协作者权限

**本地编辑**：

```bash

# 启动本地服务器

python -m http.server 8000 --directory docs

# 访问 http://localhost:8000/admin/

# 点击 "Work with Local Repository" 选择仓库目录

```

详见 [本地开发指南](docs/dev/LOCAL_DEV_SERVER.md)

#### 方式 B：手动编辑

```bash

# 安装依赖

pip install -r requirements.txt

# 编辑词条（在 docs/entries/ 目录）

# 自动修复格式

python tools/fix_markdown.py

# 本地预览

mkdocs serve
```

### 3. 提交 PR

详细流程请参考 [PR 流程](docs/contributing/pr-workflow.md)

---

## 📋 核心原则

本项目致力于提供 **一致性、严谨性、可验证性** 的知识内容：

1. **学术严谨** - 所有断言必须配备可靠引用
2. **格式统一** - 遵循项目的 Markdown 与命名规范
3. **内容质量** - 确保信息准确、表述清晰
4. **尊重边界** - 涉及敏感内容需添加触发警告

---

## 🎯 关键要求

### 文件结构

- **词条存放** ：统一在 `docs/entries/` 目录（禁止子目录）
- **Frontmatter** ：必须包含 `title`、`tags`、`updated` 字段
- **模板参考** ：[词条模板](docs/TEMPLATE_ENTRY.md)

### 引用规范

- **一级来源** （必选）：ICD-11、DSM-5-TR 官方资料
- **二级来源** （可补充）：StatPearls、UpToDate、权威期刊
- **引用格式** ：包含来源名称、版本、访问日期

### 诊断内容

- **双重对照** ：必须同时提供 ICD-11 与 DSM-5-TR 信息
- **原文摘录** ：包含英文原文（≤25 词）+ 中文翻译
- **差异说明** ：明确标注 ICD 与 DSM 的分类差异

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` - 新增条目/章节
- `fix:` - 错误修复
- `docs:` - 文档更新
- `refactor:` - 结构重构
- `chore:` - 工具维护
- `style:` - 格式变更

---

## ✅ PR 检查清单

提交前请确认：

- [ ] 所有断言均有就近引用
- [ ] 病理学内容包含 ICD-11 与 DSM-5-TR
- [ ] 内部链接与标签正确
- [ ] 图片/数据版权明确
- [ ] `python tools/fix_markdown.py` 已运行
- [ ] `mkdocs build --strict` 构建成功

---

## 💡 贡献方式

- 📝 **补充词条** - 新增或完善现有条目
- 🐛 **报告错误** - 在 Issues 中反馈问题
- 🌐 **翻译校对** - 改进术语翻译
- 📚 **分享经验** - 贡献实践技巧与资源

查看所有贡献者:访问 [贡献者墙](docs/contributing/contributors.md)

---

## 📚 参考资源

- [完整贡献指南](docs/contributing/index.md)
- [贡献者墙](docs/contributing/contributors.md)
- [词条模板](docs/TEMPLATE_ENTRY.md)
- [工具文档](docs/dev/Tools-Index.md)
- [前端架构](docs/dev/THEME_GUIDE.md)

---

## 📞 获取帮助

- 💬 在 GitHub Issues 中提问
- 📖 查阅 [详细规范文档](docs/contributing/)
- 🔍 参考现有词条的编写方式

---

**感谢你的贡献！** 让我们一起构建高质量的多意识体知识库。
