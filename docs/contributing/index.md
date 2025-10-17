# 贡献指南

欢迎参与 Multiple Personality System Wiki 的建设！本页提供一站式的贡献导航、快速开始与检查清单，全面使用 MkDocs Material 语法与组件，避免额外 CSS。

______________________________________________________________________

## 📌 快速导航

<div class="grid cards" markdown>

- :material-pencil-outline: **编写规范**\
  语言与格式、标题与 Frontmatter、段落与代码块\
  [:octicons-arrow-right-24: 前往](writing-guidelines.md)

- :material-book-cog-outline: **学术引用**\
  引用格式、证据分级、来源可追溯性\
  [:octicons-arrow-right-24: 前往](academic-citation.md)

- :material-hospital-box-outline: **诊断临床规范**\
  临床条目强制要求、缩写、专业表述\
  [:octicons-arrow-right-24: 前往](clinical-guidelines.md)

- :material-cog-outline: **技术约定**\
  目录结构、链接规则、图片与静态资源\
  [:octicons-arrow-right-24: 前往](technical-conventions.md)

- :material-source-pull: **PR 流程**\
  提交流程、检查清单、CI 与自动修复\
  [:octicons-arrow-right-24: 前往](pr-workflow.md)

- :material-account-group-outline: **贡献者墙**\
  致谢所有贡献者与贡献记录\
  [:octicons-arrow-right-24: 前往](contributors.md)

- :material-shield-crown-outline: **管理员操作指南**\
  维护流程、分支管理、发布与回滚\
  [:octicons-arrow-right-24: 前往](../ADMIN_GUIDE.md)

</div>

______________________________________________________________________

## 🎯 核心原则

!!! tip "一致性 · 严谨性 · 可验证性"
\- ✅ 统一使用简体中文，遵守命名与标题规范
\- ✅ 所有断言提供可靠引用，来源可追溯
\- ✅ 严格遵守链接与目录规则，避免绝对路径
\- ✅ 敏感话题添加触发警告与必要背景

______________________________________________________________________

## 🚀 快速开始

=== "方式一：虚拟环境（推荐）"

````
```bash
# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```
````

=== "方式二：系统级安装"

````
```bash
# 直接安装依赖（macOS/Windows 等）
pip install -r requirements.txt
```
````

=== "本地编辑与预览"

````
```bash
# 编辑词条（位于 docs/entries/）
# 运行自动修复
python3 tools/fix_markdown.py docs/entries/

# 本地预览（热重载）
mkdocs serve
# 访问： http://127.0.0.1:8000
```
````

!!! info "时间戳自动维护"
词条 Frontmatter 中的 `updated` 字段由 CI 自动更新，无需手动修改。详见「技术约定 → Frontmatter 规范」。

______________________________________________________________________

## ✅ 提交前检查清单

!!! success "PR 自检（建议逐项确认）"
\- [ ] 词条位于 `docs/entries/`，不创建子目录
\- [ ] Frontmatter 含 `title / topic / tags` 且格式正确
\- [ ] 链接使用相对路径，符合项目规范
\- [ ] 已运行：`python3 tools/fix_markdown.py docs/entries/`
\- [ ] 已运行：`python3 tools/check_links.py docs/entries/`
\- [ ] 构建通过：`mkdocs build --strict`
\- [ ] PR 说明包含动机、改动点、潜在风险与方法来源

______________________________________________________________________

## 💡 贡献方式

<div class="grid" markdown>

- 📝 **补充词条** — 新增或完善条目，保持学术与格式一致性
- 🐛 **报告错误** — 通过 Issues 反馈错别字、断链与事实性问题
- 🌐 **翻译校对** — 统一术语、改进表达、补充参考
- 📚 **分享实践** — 贡献实操技巧与资源汇编

</div>

______________________________________________________________________

## 📚 参考资源

- :material-file-document-edit-outline: [词条模板](https://github.com/mps-team-cn/Multiple_personality_system_wiki/blob/main/docs/TEMPLATE_ENTRY.md)
- :material-shield-crown-outline: [管理员操作指南](https://github.com/mps-team-cn/Multiple_personality_system_wiki/blob/main/docs/ADMIN_GUIDE.md)
- :material-hammer-wrench: [工具文档](https://github.com/mps-team-cn/Multiple_personality_system_wiki/blob/main/docs/dev/Tools-Index.md)
- :material-palette-swatch-outline: [前端架构](https://github.com/mps-team-cn/Multiple_personality_system_wiki/blob/main/docs/dev/THEME_GUIDE.md)
- :material-alert-box-outline: [Admonition 提示块效果对照](admonitions-demo.md)
- :material-folder-information-outline: [开发文档目录](https://github.com/mps-team-cn/Multiple_personality_system_wiki/tree/main/docs/dev)

______________________________________________________________________

## ❓ 常见问题（FAQ）

???+ question "如何选择合适的标签？"
参考现有词条的标签使用，确保标签准确反映主题；避免创建同义重复标签。

???+ question "引用格式有什么要求？"
必须包含来源名称、版本/年份与访问日期，学术类内容优先引用学术数据库或权威指南。详见「学术引用」。

???+ question "图片应该放在哪里？"
\- 图表/示意图：`docs/assets/figures/`
\- 一般图片：`docs/assets/images/`
\- 小图标：`docs/assets/icons/`
详见「技术约定 → 图片资源组织」。

______________________________________________________________________

## 📞 获取帮助

- :material-email: **信息反馈**：[support@mpsteam.cn](mailto:support@mpsteam.cn)
- :material-email-outline: **官方联系**：[contact@mpsteam.cn](mailto:contact@mpsteam.cn)
- :material-github: **GitHub Issues**：[提交问题或建议](https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues)
- :material-qqchat: **QQ 群**：935527821
