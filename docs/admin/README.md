# Sveltia CMS 后台使用说明

## 访问地址

<https://wiki.mpsteam.cn/admin/>

## 首次登录

Sveltia CMS 使用 GitHub Personal Access Token 进行认证，首次访问时需要：

### 1. 创建 GitHub Token

1. 访问 [GitHub Token 创建页面](https://github.com/settings/tokens/new)
1. 填写 Token 描述（如 `Multiple Personality System Wiki CMS`）
1. 设置过期时间（建议 90 天或更长）
1. **必须勾选** `repo` 权限（完整仓库访问）
1. 点击 "Generate token" 生成 Token
1. **立即复制** Token（离开页面后无法再查看）

### 2. 登录 CMS

1. 访问 <https://wiki.mpsteam.cn/admin/>
1. 等待 Sveltia CMS 加载完成
1. 点击 "Log in with GitHub"
1. 粘贴您的 Personal Access Token
1. 点击 "Authenticate"

## 功能特性

### 词条管理

- ✅ 创建、编辑、删除词条
- ✅ 实时 Markdown 预览
- ✅ 主题分类和标签管理
- ✅ 同义词索引优化
- ✅ 视图过滤和分组

### 自动化

- 📝 自动生成符合 Conventional Commits 规范的提交信息
- 📅 自动更新 `updated` 字段
- 🔍 智能文件名建议（基于标题）

### 媒体文件

- 📷 上传图片到 `docs/assets/uploads/`
- 🖼️ 在词条中直接引用

## 常见问题

### Q: 页面显示空白/白屏？

**A:** 这通常是以下原因之一：

1. **Token 未配置或已过期**

   - 刷新页面重新登录
   - 创建新的 Personal Access Token

1. **CDN 加载失败**

   - 检查浏览器控制台是否有错误
   - 尝试切换网络（如使用移动热点）

1. **浏览器缓存问题**

   - 按 `Ctrl + Shift + R`（Windows/Linux）或 `Cmd + Shift + R`（macOS）强制刷新
   - 清除浏览器缓存后重试

### Q: 如何查看修改历史？

**A:** 所有修改都会直接提交到 GitHub 仓库，您可以：

- 在 [GitHub Commits](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commits/main) 查看完整历史
- 使用 Git 工具本地查看：`git log --oneline`

### Q: 可以离线使用吗？

**A:** 不可以。Sveltia CMS 需要：

- 网络连接（加载 CMS 资源）
- GitHub API 访问（读取和写入仓库）

## 技术架构

```text
用户浏览器
    ↓
Sveltia CMS (CDN)
    ↓
GitHub API (通过 Personal Access Token)
    ↓
mps-team-cn/Multiple_personality_system_wiki 仓库
    ↓
GitHub Pages / Cloudflare Pages 自动部署
    ↓
https://wiki.mpsteam.cn
```

## 安全提示

⚠️ **保护您的 Personal Access Token**：

- 不要分享给他人
- 不要提交到公开仓库
- 定期更换（建议 90 天）
- 如果泄露，立即在 [GitHub Settings - Tokens](https://github.com/settings/tokens) 删除

## 技术支持

如遇问题，请：

1. 检查 [GitHub Issues](https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues)
1. 查看 [Sveltia CMS 官方文档](https://github.com/sveltia/sveltia-cms)
1. 联系项目维护者

______________________________________________________________________

**最后更新：** 2025-10-11
**CMS 版本：** Sveltia CMS 0.112+
