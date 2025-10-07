# PR 提交流程

本文档介绍本地开发流程、PR 提交步骤与质量检查清单。

---

## 1. 本地开发流程

### 1.1 环境准备

#### 安装依赖

```bash

# Python 依赖（MkDocs）

pip install -r requirements-mkdocs.txt

# Node.js 依赖（可选，用于时间戳更新）

npm install
```

#### 验证安装

```bash

# 验证 MkDocs

mkdocs --version

# 验证 Python 工具

python tools/fix_markdown.py --help
```

### 1.2 创建/编辑词条

#### 新增词条

1. 在 `docs/entries/` 创建新文件
2. **使用标准模板** `docs/TEMPLATE_ENTRY.md`
3. 填写 Frontmatter（title、tags、updated、topic 等）

!!! tip "使用模板"
    模板文件位置：`docs/TEMPLATE_ENTRY.md`

模板包含：

- 标准 Frontmatter 结构
- 常用章节框架
- 引用格式示例

**示例** ：

```bash

# 使用模板创建新词条

cp docs/TEMPLATE_ENTRY.md docs/entries/新词条名.md

# 编辑内容

code docs/entries/新词条名.md
```

#### 编辑现有词条

```bash

# 直接编辑

code docs/entries/DID.md
```

---

## 2. 本地验证

### 2.1 自动修复格式

```bash

# 修复所有文件

python tools/fix_markdown.py

# 修复特定文件

python tools/fix_markdown.py docs/entries/某词条.md
```

**修复内容** ：

- 加粗链接格式
- 列表加粗文本空格
- 链接括号格式
- 冒号格式

### 2.2 Markdown Lint 检查

```bash

# 检查所有文件

markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "site"

# 检查特定文件

markdownlint docs/entries/某词条.md
```

### 2.3 本地预览

```bash

# 启动开发服务器

mkdocs serve

# 访问 http://127.0.0.1:8000

```

**检查项** ：

- [ ] 页面正常显示
- [ ] 链接跳转正确
- [ ] 图片加载正常
- [ ] Frontmatter 信息正确
- [ ] 标签显示正确

### 2.4 构建测试

```bash

# 严格模式构建

mkdocs build --strict
```

**说明** ：`--strict` 会将所有警告视为错误，确保构建质量。

---

## 3. PR 提交步骤

### 3.1 提交前检查

运行以下命令确保质量：

```bash

# 1. 格式修复

python tools/fix_markdown.py

# 2. Lint 检查

markdownlint "docs/**/*.md" --ignore "node_modules" --ignore "site"

# 3. 构建测试

mkdocs build --strict
```

### 3.2 Git 提交

#### 提交类型

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat:` | 新增条目/章节 | `feat: 添加 OSDD 词条` |
| `fix:` | 错误修复 | `fix: 修复 DID 词条引用链接` |
| `docs:` | 文档更新 | `docs: 更新贡献指南` |
| `refactor:` | 结构重构 | `refactor: 重组创伤相关词条` |
| `chore:` | 工具维护 | `chore: 更新构建脚本` |
| `style:` | 格式变更 | `style: 统一 Markdown 格式` |

#### 提交命令

```bash

# 添加修改的文件

git add docs/entries/某词条.md

# 提交（使用规范格式）

git commit -m "feat: 添加解离性遗忘症词条"

# 推送到远程

git push origin 你的分支名
```

### 3.3 创建 Pull Request

1. 访问 GitHub 仓库
2. 点击"New Pull Request"
3. 填写 PR 信息（见下文模板）
4. 提交 PR

---

## 4. PR 检查清单

### 4.1 内容质量

每个 PR 必须包含以下信息：

#### 基本信息

- [ ] 变更类型（feat/fix/docs/...）
- [ ] 影响范围（词条/工具/文档）
- [ ] 变更说明

#### 引用与来源

- [ ] 所有断言均有就近引用
- [ ] 引用包含版本与访问日期
- [ ] 【病理学】同时给出 ICD-11 与 DSM-5-TR 锚点
- [ ] 【病理学】含原文摘录（≤25 词）+ 中文翻译 + 链接/页码
- [ ] 翻译注明译者/校对

#### 格式与技术

- [ ] 内部链接正确（相对路径）
- [ ] 标签正确填写在 Frontmatter
- [ ] 图片/数据版权与许可明确
- [ ] 最后更新时间已更新（`updated` 字段）

#### 本地验证

- [ ] `python tools/fix_markdown.py` 已运行
- [ ] `markdownlint` 检查通过
- [ ] `mkdocs serve` 本地预览无误
- [ ] `mkdocs build --strict` 构建成功

#### CI/CD

- [ ] GitHub Actions CI 通过
- [ ] Cloudflare Pages 预览部署成功

---

## 5. PR 模板

### 5.1 标题格式

```text
<type>(<scope>): <subject>
```

**示例** ：

```text
feat(entries): 添加解离性遗忘症词条
fix(entries): 修复 DID 词条引用格式
docs(contributing): 更新贡献指南
```

### 5.2 PR 描述模板

```markdown

## 变更类型

- [ ] feat - 新增条目/功能
- [ ] fix - 错误修复
- [ ] docs - 文档更新
- [ ] refactor - 结构重构
- [ ] chore - 工具维护
- [ ] style - 格式变更

## 变更说明

<!-- 简要描述本次变更的内容 -->

## 主要变更

<!-- 列出主要的修改项 -->

- 添加了 XXX 词条
- 修复了 XXX 问题
- 更新了 XXX 引用

## 引用来源

<!-- 列出主要引用来源 -->

- ICD-11 Browser, 6BXX（MMS 2025-01）
- DSM-5-TR, XXX

## 检查清单

- [ ] 所有断言均有引用
- [ ] 病理学内容包含 ICD-11 与 DSM-5-TR
- [ ] 内部链接与标签正确
- [ ] 本地构建通过（`mkdocs build --strict`）
- [ ] Lint 检查通过
- [ ] 已更新最后修改时间

## 相关 Issue

<!-- 如果有相关 Issue，请引用 -->
Closes #XXX

## 附加说明

<!-- 其他需要说明的内容 -->
```

---

## 6. 常见问题

### 6.1 格式问题

**问题** ：加粗链接渲染错误

```markdown
❌ **[文本](链接)**
✅ **文本（[链接](url)）**
```

**解决** ：运行 `python tools/fix_markdown.py` 自动修复

### 6.2 链接问题

**问题** ：链接失效或 404

- 检查是否使用相对路径
- 确认目标文件存在
- 使用 `mkdocs serve` 本地验证

### 6.3 构建问题

**问题** ：`mkdocs build --strict` 失败

- 查看错误信息
- 检查 Frontmatter 格式
- 确认所有链接有效
- 验证图片路径正确

### 6.4 标签问题

**问题** ：标签索引未更新

- 确认 Frontmatter 中标签格式正确（数组格式）
- MkDocs Material tags 插件会自动生成索引
- 无需手动维护 `tags.md`

---

## 7. 自动化工具

### 7.1 格式修复

```bash

# 修复单个文件

python tools/fix_markdown.py docs/entries/某词条.md

# 修复所有词条

python tools/fix_markdown.py
```

### 7.2 时间戳自动更新

MkDocs Material 的 `git-revision-date-localized` 插件会自动从 Git 历史获取页面的创建时间和最后更新时间，无需手动维护。

### 7.3 校验报告

```bash

# 生成校验报告

python tools/gen-validation-report.py

# 查看报告

cat docs/VALIDATION_REPORT.md
```

---

## 8. 权威资源入口

提交时建议固定引用以下权威入口：

### 8.1 一级来源

- **ICD-11 Browser** ：[https://icd.who.int/browse11](https://icd.who.int/browse11)（使用 MMS 2025-01）
- **WHO CDDR** ：Clinical Descriptions and Diagnostic Requirements（2024 PDF）
- **APA DSM-5-TR** ：[https://www.psychiatry.org/](https://www.psychiatry.org/)

### 8.2 二级来源

- **StatPearls** ：[https://www.ncbi.nlm.nih.gov/books/NBK](https://www.ncbi.nlm.nih.gov/books/NBK)
- **UpToDate** ：[https://www.uptodate.com/](https://www.uptodate.com/)

---

## 9. 获取帮助

### 9.1 文档资源

- [编写规范](编写规范.md)
- [学术引用](学术引用.md)
- [诊断临床规范](诊断临床规范.md)
- [技术约定](技术约定.md)

### 9.2 问题反馈

- 💬 在 GitHub Issues 中提问
- 📖 查阅项目文档
- 🔍 参考现有词条的编写方式

---

## 10. 最终检查清单

提交 PR 前，请完成以下所有检查：

### 内容检查

- [ ] 所有断言均有引用
- [ ] 病理学内容包含 ICD-11 与 DSM-5-TR
- [ ] 原文摘录（≤25 词）+ 中文翻译
- [ ] 译者/校对已标注
- [ ] 图片/数据版权明确

### 格式检查

- [ ] Frontmatter 完整（title、tags、updated）
- [ ] 内部链接使用相对路径
- [ ] 标签正确填写
- [ ] 图片路径正确

### 技术检查

- [ ] `python tools/fix_markdown.py` 已运行
- [ ] `markdownlint` 检查通过
- [ ] `mkdocs serve` 预览正常
- [ ] `mkdocs build --strict` 构建成功

### 提交检查

- [ ] 提交信息符合 Conventional Commits
- [ ] PR 描述完整
- [ ] CI/CD 通过

---

## 相关文档

- [编写规范](编写规范.md)
- [学术引用](学术引用.md)
- [诊断临床规范](诊断临床规范.md)
- [技术约定](技术约定.md)
- [贡献指南总览](index.md)
