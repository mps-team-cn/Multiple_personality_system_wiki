# 静态资源使用指南

本目录（`docs/assets/`）用于存放 Multiple Personality System Wiki 的所有静态资源文件。

## 目录结构

```text
docs/assets/
├── figures/           # 图表、流程图、示意图、SVG 等
├── images/            # 一般图片（封面、截图等）
├── icons/             # 小图标、装饰性素材
├── extra.css          # 自定义样式表
├── extra.js           # 自定义脚本
├── extra-common.css   # 通用样式
└── extra-material.css # Material 主题样式
```

## 资源分类说明

### 1. figures/ - 图表与示意图

存放用于解释概念、展示流程的图表文件：

- 流程图（如：解离机制流程）
- 示意图（如：系统结构图）
- 数据可视化图表
- SVG 矢量图
- 复杂的技术图解

**命名建议** ：使用描述性名称，如 `dissociation-types.svg`、`therapy-phases.png`

### 2. images/ - 一般图片

存放通用图片资源：

- 词条封面图
- 屏幕截图
- 照片素材
- 背景图片

**命名建议** ：`cover-{词条名}.png`、`screenshot-{功能}.jpg`

### 3. icons/ - 图标素材

存放小图标和装饰性元素：

- 网站 favicon
- 功能图标
- 装饰性 SVG
- 提示图标（如 trigger-warning.svg）

**命名建议** ：简短清晰，如 `favicon.svg`、`warning.svg`

## 引用路径规范

### 从词条文件引用

词条文件位于 `docs/entries/`，引用资源时使用 **相对路径** （MkDocs 会自动处理）：

```markdown
<!-- ✅ 正确：使用相对于源文件的路径 -->
![解离类型示意图](../assets/figures/types.svg)
![封面图片](../assets/images/cover.png)
![提示图标](../assets/icons/warning.svg)

<!-- ⚠️ 说明：MkDocs 会根据生成的 HTML 位置自动调整路径 -->
<!-- 源文件: docs/entries/xxx.md 使用 ../assets/ -->
<!-- 生成为: site/entries/xxx/index.html 引用 ../../assets/ -->
```

### 从其他文档引用

根据文档位置使用 **相对路径** ：

```markdown
<!-- 从 docs/ 根目录的文档（如 index.md） -->
![图表](assets/figures/diagram.svg)

<!-- 从 docs/entries/ 子目录的文档 -->
![图表](../assets/figures/diagram.svg)

<!-- 从更深层级的文档，依次增加 ../ -->
![图表](../../assets/figures/diagram.svg)
```

**MkDocs 路径处理** ：

- MkDocs 自动根据源文件位置和目标文件位置计算路径
- 使用相对于 **源文件** 的路径，MkDocs 会在构建时自动调整

## 图片使用规范

### 1. 文件格式选择

- **SVG** : 优先用于图表、图标、流程图（矢量图，可缩放）
- **PNG** : 用于需要透明背景的图片、截图
- **JPG** : 用于照片、不需要透明背景的图片
- **GIF** : 仅用于必要的动画演示

### 2. 文件大小优化

- 图片上传前进行压缩优化
- SVG 文件移除不必要的元数据
- 推荐分辨率：
    - 图表/示意图：最大宽度 1200px
    - 图标：64px - 256px
    - 封面图：800px - 1600px

### 3. 图片说明与来源

每张图片应添加：

```markdown
![图片描述](../assets/figures/example.svg)

*图：图片详细说明（来源：作者/机构/许可证）*
```

### 4. 版权与许可

- 必须注明图片来源与许可协议
- 仅使用有合法使用权的图片
- 自制图片建议使用 CC BY-SA 4.0 许可

## 资源管理最佳实践

1. **命名规范**

    - 使用小写字母
    - 使用连字符 `-` 分隔单词
    - 使用描述性名称
    - 避免中文文件名

2. **目录整洁**

    - 定期清理未使用的资源
    - 避免重复文件
    - 保持目录结构清晰

3. **版本控制**

    - 图片修改时使用新文件名（如 `diagram-v2.svg`）
    - 或在提交信息中明确说明修改内容

## 常见问题

### Q: 图片显示不出来？

检查以下项：

1. ✅ 路径是否使用绝对路径（以 `/` 开头）：`/assets/figures/xxx.svg`
2. ✅ 文件扩展名大小写是否匹配
3. ✅ 文件是否已提交到仓库
4. ✅ 本地预览：刷新浏览器缓存（Ctrl+F5 或 Cmd+Shift+R）

### Q: 应该用什么路径格式？

**使用相对于源文件的路径** ：

| 路径格式 | 示例 | 适用场景 | 说明 |
|---------|------|---------|------|
| 相对路径 | `../assets/figures/types.svg` | ✅ 推荐 | 从 `docs/entries/` 引用 |
| 当前目录 | `assets/figures/types.svg` | ✅ 可用 | 从 `docs/` 根目录引用 |
| 绝对路径 | `/assets/figures/types.svg` | ⚠️ 避免 | 可能在某些环境下失效 |

### Q: SVG 图标颜色如何适配深色模式？

在 SVG 中使用 CSS 变量，或在 `extra.css` 中定义深色模式样式。

---

**相关文档** ：

- [贡献指南](../contributing/index.md) - 图表与数据要求
- [词条模板](../TEMPLATE_ENTRY.md) - 图片引用示例
- [开发规范](../../AGENTS.md) - 静态资源配置
