# Sveltia CMS 本地开发指南

> Sveltia CMS 是 Decap CMS 的现代化替代品，提供更好的搜索和用户体验

## 技术栈组合

- **Sveltia CMS** - 前端内容管理系统
- **Cloudflare Functions** - OAuth 认证
- **MkDocs Material** - 静态站点生成
- **GitHub** - 内容存储

访问路径：`/admin`

---

## 🚀 特性

### ✨ 相比 Decap CMS 的优势

- **即时全文搜索** - 可搜索词条内容，而非仅集合名称
- **本地仓库工作流** - 使用浏览器 File System Access API，无需代理服务器
- **更快的性能** - 使用 GraphQL 批量加载，159 个词条瞬间加载
- **现代化 UI** - 深色模式、移动端优化、更直观的界面
- **更稳定** - 已解决 260+ Decap CMS 遗留问题

---

## 📝 在线使用（推荐）

### 访问后台

1. 打开 `[https://mpswiki.pages.dev/admin/`](https://mpswiki.pages.dev/admin/`)
2. 点击 **"Sign In with GitHub"** 使用 GitHub 账号登录
3. 授权后即可编辑词条

### 功能说明

- **搜索** - 顶部搜索框可搜索词条内容（例如搜索"多人"）
- **筛选** - 点击 "Filter" 按钮，选择主题分类或标签
- **分组** - 点击 "Group" 按钮，按主题或标签分组显示
- **排序** - 点击 "Sort" 按钮，选择排序方式

---

## 💻 本地开发

### 方法一：使用本地仓库（推荐）

Sveltia CMS 支持直接访问本地 Git 仓库，无需代理服务器。

#### 步骤：

1. **启动本地 Web 服务器**

   ```bash
   # 使用 Python
   python -m http.server 8000 --directory docs

   # 或使用 Node.js
   npx http-server docs -p 8000
   ```

2. **在浏览器中打开**

   访问 `[http://localhost:8000/admin/`](http://localhost:8000/admin/`)

3. **选择本地仓库模式**

   点击蓝色按钮 **"Work with Local Repository"**

4. **选择仓库目录**

   在弹出的文件选择器中，选择 `Multiple_personality_system_wiki` 仓库的根目录

5. **开始编辑**

   - 所有更改会实时写入本地文件
   - 更改后使用 Git 提交和推送

#### 浏览器要求：

- ✅ Chrome/Edge 86+
- ✅ Opera 72+
- ❌ Firefox (不支持 File System Access API)
- ❌ Safari (不支持 File System Access API)

---

### 方法二：使用 GitHub OAuth（在线模式）

如果需要直接推送到 GitHub：

1. 启动本地服务器（同上）
2. 访问 `[http://localhost:8000/admin/`](http://localhost:8000/admin/`)
3. 点击 **"Sign In with GitHub"**
4. 完成 OAuth 授权
5. 直接编辑和提交到 GitHub

**注意**：需要有仓库写入权限

> ⚠️ 提示：GitHub OAuth 的回调地址优先使用环境变量 `GITHUB_OAUTH_BASE_URL`。当未设置或值无效时，会回退为当前访问域名（如 `http://localhost:8000`）。请确保回调地址已在 GitHub OAuth App 中登记，否则会出现 “redirect_uri is not associated with this application” 报错。

---

## 🎯 使用技巧

### 快捷键

- `Ctrl+F` (Windows/Linux) 或 `Command+F` (macOS) - 打开搜索
- `Ctrl+E` 或 `Command+E` - 创建新词条
- `Ctrl+S` 或 `Command+S` - 保存词条
- `Escape` - 取消编辑

### 创建新词条

1. 点击右上角蓝色 **"New"** 按钮
2. 填写标题（格式：中文（English/缩写））
3. 选择主题分类（7 个选项之一）
4. 添加标签（用于筛选和交叉引用）
5. 编写正文内容（支持 Markdown）
6. 点击 **"Save"** 保存

### 编辑现有词条

1. 在列表中点击词条
2. 修改内容
3. 点击 **"Save"** 保存
4. 在提交时填写更新说明

---

## 🔧 配置文件

### 主配置：`docs/admin/config.yml`

```yaml
backend:
  name: github
  repo: mps-team-cn/Multiple_personality_system_wiki
  branch: main
  base_url: https://mpswiki.pages.dev
  auth_endpoint: /api/auth

collections:

  - name: "entries"

    label: "词条管理"
    folder: "docs/entries"

    # 7 个主题分类
    view_filters:

      - { label: "理论与分类", field: topic, pattern: "理论与分类" }
      - { label: "诊断与临床", field: topic, pattern: "诊断与临床" }
      - { label: "系统运作", field: topic, pattern: "系统运作" }
      - { label: "角色与身份", field: topic, pattern: "角色与身份" }
      - { label: "文化与表现", field: topic, pattern: "文化与表现" }
      - { label: "创伤与疗愈", field: topic, pattern: "创伤与疗愈" }
      - { label: "实践指南", field: topic, pattern: "实践指南" }

```

### 本地开发配置：`docs/admin/config.local.yml`

- 用于本地测试
- 不要提交到 Git
- 已在 `.gitignore` 中忽略

---

## 📊 主题分类

当前项目使用 7 个主题分类（共 158 个词条）：

| 分类 | 词条数 | 说明 |
|------|--------|------|
| 系统运作 | 48 | 切换、共意识等系统机制 |
| 诊断与临床 | 31 | DID、解离障碍等临床诊断 |
| 角色与身份 | 30 | Admin、Alter 等角色类型 |
| 理论与分类 | 22 | 结构性解离等理论模型 |
| 文化与表现 | 17 | 影视作品中的多重意识体 |
| 实践指南 | 5 | Tulpa 创造等实践方法 |
| 创伤与疗愈 | 5 | CPTSD、创伤治疗等 |

---

## ⚠️ 注意事项

1. **自动保存草稿** - Sveltia CMS 会自动保存草稿到浏览器
2. **提交前检查** - 确保 Markdown 格式正确
3. **标题格式** - 必须使用"中文（English/缩写）"格式
4. **主题分类** - 必须选择 7 个分类之一，保持一致性
5. **更新时间** - 修改词条时会自动更新 `updated` 字段

---

## 🆘 常见问题

### Q: 为什么搜索不到某个词条？

A: Sveltia CMS 使用即时搜索，确保：

- 搜索关键词存在于词条标题或正文中
- 已等待页面完全加载（159 个词条）

### Q: 本地仓库模式无法使用？

A: 检查：

- 浏览器是否为 Chrome/Edge
- 是否选择了正确的仓库根目录
- 是否有文件读写权限

### Q: 更改没有保存？

A: 确认：

- 点击了 "Save" 按钮
- 没有验证错误（红色提示）
- 本地仓库模式下，更改会立即写入文件

### Q: 如何回滚错误的提交？

A: 使用 Git 命令：

```bash
git log --oneline  # 查看提交历史
git revert <commit-hash>  # 回滚指定提交
git push origin main
```

---

## 📚 相关文档

- [Sveltia CMS 官方文档](https://github.com/sveltia/sveltia-cms)
- [Multiple personality system Wiki 贡献指南](docs/contributing/index.md)
- [词条编写规范](docs/contributing/编写规范.md)
- [管理员操作指南](docs/ADMIN_GUIDE.md)

---

## 🔄 从 Decap CMS 迁移

Sveltia CMS 完全兼容 Decap CMS 的配置文件，无需修改 `config.yml`。
只需将 `index.html` 中的脚本引用改为：

```html
<script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js" type="module"></script>
```

所有现有功能保持不变，并获得额外的搜索和性能提升。
