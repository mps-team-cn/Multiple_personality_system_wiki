# Cloudflare Pages 部署配置

本文档说明如何在 Cloudflare Pages 上部署 Plurality Wiki (MkDocs Material 版本)。

## 配置步骤

### 1. 在 Cloudflare Pages 创建项目

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **Pages** 部分
3. 点击 **Create a project**
4. 连接你的 GitHub 仓库 `kuliantnt/plurality_wiki`

### 2. 构建配置

在 Cloudflare Pages 的项目设置中，配置以下参数:

#### 框架预设
- **Framework preset**: `None` (不使用预设)

#### 构建配置
- **Build command**: `bash .cfpages-build.sh`
- **Build output directory**: `site`

#### 环境变量

可选的环境变量:

```
PYTHON_VERSION=3.11
```

### 3. 高级设置

#### 构建超时
- 推荐设置为 **15 分钟** (如果构建较慢)

#### 部署分支
- **Production branch**: `main`
- **Preview branches**: `dev`, `refactor/*`

### 4. 自定义域名 (可选)

如果要使用自定义域名 `wiki.pluralitycn.com`:

1. 在 Cloudflare Pages 项目中，进入 **Custom domains**
2. 点击 **Set up a custom domain**
3. 输入 `wiki.pluralitycn.com`
4. 按照提示配置 DNS 记录

## 构建脚本说明

`.cfpages-build.sh` 脚本执行以下步骤:

1. 安装 Python 依赖 (`requirements-mkdocs.txt`)
2. 运行 `mkdocs build --strict` 构建站点
3. 生成的静态文件输出到 `site/` 目录

## 本地构建测试

在推送到 GitHub 之前，可以本地测试构建:

```bash
# 安装依赖
pip install -r requirements-mkdocs.txt

# 本地预览
mkdocs serve

# 构建站点
mkdocs build --strict
```

## 常见问题

### Q: 构建失败,提示缺少依赖

**A**: 检查 `requirements-mkdocs.txt` 是否包含所有必要的包。

### Q: 构建成功但页面显示不正常

**A**: 检查 `mkdocs.yml` 中的 `site_url` 是否正确配置。

### Q: 如何查看构建日志?

**A**: 在 Cloudflare Pages 项目中，进入 **Deployments**，点击具体的部署查看详细日志。

## 迁移注意事项

从 Docsify 迁移到 MkDocs Material 后:

1. ✅ 所有词条路径保持不变 (`entries/*.md`)
2. ✅ 静态资源路径已适配
3. ✅ 内部链接已更新
4. ⚠️ 确保 DNS 记录指向正确的 Cloudflare Pages 项目

## 回滚方案

如需回滚到 Docsify 版本:

1. 在 GitHub 切换到旧的提交或分支
2. Cloudflare Pages 会自动重新构建
3. 或者手动切换部署版本

## 性能优化

MkDocs Material 已启用以下优化:

- ✅ HTML/CSS/JS 压缩 (`minify` 插件)
- ✅ 图片懒加载 (`glightbox` 插件)
- ✅ 即时加载 (`navigation.instant`)
- ✅ 搜索索引优化

## 监控和分析

可以在 `mkdocs.yml` 中配置 Google Analytics:

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

环境变量方式 (推荐):

```bash
GOOGLE_ANALYTICS_KEY=G-XXXXXXXXXX
```

## 技术支持

如有问题,请在 [GitHub Issues](https://github.com/kuliantnt/plurality_wiki/issues) 提出。
