# Giscus "Unable to create discussion" 错误排查

## 🔴 错误现象

用户在提交评论时,giscus.app 弹出提示:

```text
Unable to create discussion.
```

## 🔍 根本原因分析

这个错误表示 Giscus 无法在 GitHub Discussions 中创建新的讨论主题。通常有以下几种原因:

## ✅ 修复步骤

### 步骤 1: 检查 Giscus App 权限 ⭐ 最关键

1. **访问 Giscus App 配置页面**:

   ```
   [https://github.com/apps/giscus](https://github.com/apps/giscus)
   ```

2. **点击 "Configure"**,选择你的账号或组织

3. **确认仓库访问权限**:
    - 在 "Repository access" 部分
    - 确保选择了 "Only select repositories"
    - 确保列表中包含 `mps-team-cn/Multiple_personality_system_wiki`

   或者选择 "All repositories"(不推荐,安全性较低)

4. **确认权限范围**:

   必须包含以下权限:

    - ✅ **Discussions**: Read and write
    - ✅ **Metadata**: Read-only

5. **保存配置**

### 步骤 2: 验证 Discussion 分类配置

1. **访问仓库 Discussions**:

   ```
   [https://github.com/mps-team-cn/Multiple_personality_system_wiki/discussions](https://github.com/mps-team-cn/Multiple_personality_system_wiki/discussions)
   ```

2. **检查 "Comments" 分类**:
    - 点击右侧的 "Categories" 或 "管理分类"
    - 确认存在名为 "Comments" 的分类
    - **重要**: 该分类必须是 **Announcement** 类型

3. **如果分类不存在或类型错误**:
    - 点击 "New category"
    - 名称: `Comments`
    - 描述: `评论区讨论`
    - 格式: 选择 **Announcement** (公告)
    - 点击 "Create"

4. **获取正确的 category_id**:
    - 访问 [https://giscus.app/zh-CN](https://giscus.app/zh-CN)
    - 输入仓库: `mps-team-cn/Multiple_personality_system_wiki`
    - 在 "Discussion 分类" 下拉框中选择 "Comments"
    - 复制生成的 `data-category-id` 值

### 步骤 3: 验证环境变量配置

1. **登录 Cloudflare Pages 控制台**:
    - 进入项目设置
    - 找到 "Environment variables"

2. **确认以下环境变量已设置**:

   ```
   GISCUS_REPO_ID=<从 giscus.app 获取>
   GISCUS_CATEGORY_ID=<从 giscus.app 获取>
   ```

3. **获取正确的值**:

   访问 [https://giscus.app/zh-CN](https://giscus.app/zh-CN)

    - 输入仓库名
    - 选择 Comments 分类
    - 查看生成的配置中的 `data-repo-id` 和 `data-category-id`

4. **更新后重新部署**

### 步骤 4: 检查页面配置(已修复)

✅ **已修复**: 将 `data-giscus-mapping` 从硬编码的 "specific" 改为使用 mkdocs.yml 中的配置

**修复前** (错误):

```html
data-giscus-mapping="specific"
data-giscus-term="{{ page.title }}"
```

**修复后** (正确):

```html
data-giscus-mapping="{{ giscus.mapping | default('pathname') }}"
```

这确保了与 mkdocs.yml 中的 `mapping: pathname` 配置一致。

### 步骤 5: 验证页面源码

1. **打开有问题的页面**
2. **查看页面源码** (Ctrl+U 或 Cmd+U)
3. **搜索 "data-giscus"**
4. **检查以下属性值**:

   ```html
   data-giscus-repo="mps-team-cn/Multiple_personality_system_wiki"
   data-giscus-repo-id="R_..." (不应为空)
   data-giscus-category="Comments"
   data-giscus-category-id="DIC_..." (不应为空)
   data-giscus-mapping="pathname"
   ```

5. **如果 repo-id 或 category-id 为空**:
    - 说明环境变量未正确注入
    - 返回步骤 3 检查 Cloudflare Pages 配置

## 🧪 测试步骤

修复后,按以下步骤测试:

1. **清除浏览器缓存**
2. **访问启用了评论的页面** (如 `/entries/DID/`)
3. **等待 Giscus 加载**
4. **点击 "Sign in with GitHub"**
5. **授权后尝试发表评论**

如果仍然失败:

- 打开浏览器控制台 (F12)
- 查看 Console 和 Network 选项卡
- 记录错误信息并检查 API 响应

## 📋 完整检查清单

部署前,请确认:

- [ ] Giscus App 已安装并包含目标仓库
- [ ] Giscus App 拥有 Discussions "Read and write" 权限
- [ ] GitHub Discussions 已启用
- [ ] "Comments" 分类存在且为 Announcement 类型
- [ ] `GISCUS_REPO_ID` 环境变量已设置且正确
- [ ] `GISCUS_CATEGORY_ID` 环境变量已设置且正确
- [ ] comments.html 使用 `mapping: pathname`(不是 specific)
- [ ] 页面 Frontmatter 包含 `comments: true`

## 🔧 常见错误对照表

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| Unable to create discussion | Giscus App 权限不足 | 步骤 1 |
| Unable to create discussion | category_id 错误 | 步骤 2 |
| Discussion not found | 讨论不存在(正常) | 允许用户创建(已处理) |
| Bad credentials | 环境变量错误 | 步骤 3 |
| Error: Not Found | repo_id 错误 | 步骤 3 |

## 🆘 仍然无法解决?

1. **检查 GitHub 状态**:

   [https://www.githubstatus.com/](https://www.githubstatus.com/)

2. **查看 Giscus 仓库 Issues**:

   [https://github.com/giscus/giscus/issues](https://github.com/giscus/giscus/issues)

3. **在项目仓库提交 Issue**:

   [https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues](https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues)

4. **提供以下信息**:
    - 错误截图
    - 浏览器控制台错误
    - 页面 URL
    - 已完成的检查步骤

---

**文档版本**: v1.1
**最后更新**: 2025-10-11
**相关修复**: [comments.html mapping 配置修复]
