# 本地开发 Decap CMS 指南

## 方案 1：使用 Test Backend（推荐）

### 步骤：

1. **备份生产配置**

   ```bash
   cd docs/admin
   cp config.yml config.production.yml
   ```

2. **使用本地配置**

   ```bash
   cp config.local.yml config.yml
   ```

3. **启动本地服务器**

   ```bash
   # Python 3
   python -m http.server 8000 --directory docs

   # 或者使用 Node.js 的 http-server
   npx http-server docs -p 8000
   ```

4. **访问 Admin 界面**

   - 打开浏览器访问：http://localhost:8000/admin/
   - 点击"Login"会直接进入（无需真实认证）

5. **使用完毕后恢复生产配置**

   ```bash
   cd docs/admin
   cp config.production.yml config.yml
   ```

### 注意事项：

- ⚠️ Test Backend 的数据不会真正保存到 GitHub
- ⚠️ 刷新页面会丢失所有更改
- ⚠️ 仅用于测试界面和样式
- ⚠️ 不要提交 `config.local.yml` 作为 `config.yml`

---

## 方案 2：使用 Netlify Dev（本地 OAuth）

如果需要完整的保存功能：

### 步骤：

1. **安装 Netlify CLI**

   ```bash
   npm install -g netlify-cli
   ```

2. **登录 Netlify**

   ```bash
   netlify login
   ```

3. **链接项目**

   ```bash
   netlify link
   ```

4. **启动开发服务器**

   ```bash
   netlify dev
   ```

5. **访问**
   - 打开：http://localhost:8888/admin/
   - OAuth 会通过 Netlify 的本地代理工作

---

## 推荐工作流

**日常开发**：

- 直接编辑 Markdown 文件（VS Code）
- 使用 MkDocs 预览：`mkdocs serve`

**测试 Admin 界面**：

- 方案 1（Test Backend）- 快速测试样式
- 线上预览分支 - 测试完整功能

**生产环境**：

- 使用 Cloudflare Pages 部署
- GitHub OAuth 认证
