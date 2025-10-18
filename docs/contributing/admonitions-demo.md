# 📘 Admonition 提示块效果对照表

本页展示 MkDocs Material 支持的所有 `!!!` 提示块语法及其视觉效果。

---

## 🧱 基本示例

```markdown
!!! note "标题"
    内容缩进四个空格
```

效果：

!!! note "标题"
    内容缩进四个空格

---

## 🎨 所有可用类型

### 🟦 note

!!! note "一般提示"
    这是一个普通的提示块，用于提供额外说明。

---

### 🟦 info

!!! info "信息"
    提供补充信息或背景说明。

---

### 🟩 tip

!!! tip "小技巧"
    可以用来强调实用建议或最佳实践。

---

### 🟩 success

!!! success "成功"
    操作成功、验证通过或任务完成。

---

### 🟧 warning

!!! warning "警告"
    注意！此操作可能导致数据丢失。

---

### 🟥 danger

!!! danger "危险"
    ⚠️ 此区域包含高风险操作。

---

### 🟥 failure

!!! failure "失败"
    操作未能成功执行，请检查配置。

---

### 🟥 bug

!!! bug "已知问题"
    目前存在一个渲染错误，将在下个版本修复。

---

### 🟪 example

!!! example "示例"
    展示功能、语法或结构示例。

---

### 🟪 abstract

!!! abstract "摘要"
    用于总结章节要点或概述内容。

---

### 🟦 question

!!! question "常见问题"
    **Q：** 如何启用站点搜索？
    **A：** 在 `mkdocs.yml` 中添加 `search` 插件。

---

### 🩶 quote

!!! quote "引用"
    “我们无法选择自己的过去，但能选择如何理解它。”

---

## ⚙️ 可折叠提示

```markdown
???+ tip "可折叠的提示"
    点击即可展开或折叠。
```

效果：

???+ tip "可折叠的提示"
    点击即可展开或折叠。

---

## 🧩 嵌套提示

!!! warning "组合示例"
    外层为警告块。
    !!! tip
        这是内层的提示块。

---

## 🎛️ 自定义样式（需要主题支持）

```markdown
!!! note "自定义类" +my-style
    你可以在 `extra.css` 中定义 `.my-style` 以调整外观。
```

---

## ✅ 小结

* 所有提示块语法以 `!!!` 开头
* 内容需 **缩进四个空格**
* 可通过 `collapsible`、`open` 等参数控制展开状态
* 可嵌套使用或自定义样式

---

* 以上内容基于 [MkDocs Material 官方文档](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)。*
