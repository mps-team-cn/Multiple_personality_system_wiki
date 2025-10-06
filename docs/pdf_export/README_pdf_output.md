# README pdf 导出

要将整个 wiki 导出为带封面、目录的 PDF，请运行 `tools/pdf_export/export_to_pdf.py` 脚本，或进入模块目录后直接通过包入口执行：

```bash
python tools/pdf_export/export_to_pdf.py

# 或者

cd tools/pdf_export && python -m pdf_export
```

## 导出结构说明

PDF 导出采用**基于 topic 字段的自动分类**，根据每个词条 frontmatter 中的 `topic` 字段自动分组。

目前主要的 topic 分类包括:

1. **诊断与临床** - 解离、创伤、情绪与人格障碍等临床诊断
2. **系统运作** - 前台、切换、意识共存等多意识体系统运作机制
3. **创伤与疗愈** - 创伤类型、治疗方法、接地技巧等康复相关内容
4. **角色与身份** - 宿主、守门人、保护者等系统角色与职能
5. **理论与分类** - 埃蒙加德分类、结构性解离理论等理论框架
6. **文化与表现** - 影视作品、文学作品中的多意识体主题

词条通过 frontmatter 中的 `topic` 字段归类。每个词条会根据其 topic 值归入对应章节。topic 为空的词条会被归入"其他"分类。

## 导出流程

脚本会自动：

1. **前言章节**：如果项目根目录存在 `Preface.md` 且未被忽略，则在所有章节之前插入《前言》；
2. **按 topic 分类**：扫描 `docs/entries/` 和 `docs/` 下的所有词条文件，根据其 frontmatter 中的 `topic` 字段自动归入对应章节；
3. **自动生成章节**：根据所有词条的 topic 值自动生成章节，无需预定义；
4. **章节内排序**：同一章节内的词条按标题字母顺序排列；
5. **生成封面与目录**：生成独立的封面页与目录页（目录中的词条名称可直接点击跳转至对应内容）；
6. **格式化处理**：为每个章节中的词条单独开启新页面，并自动移除词条自身的一级标题，避免 PDF 中出现重复标题；
7. **链接重写**：自动识别 Markdown 中以 `entries/*.md` 形式书写的词条链接，并在合并时重写为指向 PDF 内部锚点的链接，确保离线文档中的交叉跳转仍可点击；
8. **时间戳插入**：如果 `assets/last-updated.json` 存在，则会读取索引并在每篇词条标题下插入"🕒 最后更新：2025/10/02 12:34:56（abc1234）"提示，使离线 PDF 与线上页面保持一致；
9. **生成 PDF**：调用 [Pandoc](https://pandoc.org/) 生成排好版的 `plurality_wiki.pdf`。

## Frontmatter 要求

所有被导出的词条都必须在 Frontmatter 中声明以下字段：

- `title`: 词条标题
- `tags`: 标签列表，至少包含一个标签
- `topic`: 主题分类，**用于 PDF 导出的章节分组**
- `updated`: 更新日期，支持 `YYYY-MM-DD` 字符串或 YAML 日期字面量

示例：

```yaml
---
tags:
- 诊断与临床
- DID
- 多重意识体
topic: 诊断与临床
title: 解离性身份障碍（DID）
updated: 2025-10-06
---
```

> ⚠️ 如果词条的 `topic` 字段为空，该词条会被归入"其他"分类。

运行脚本前，请确保：

1. 已安装 Pandoc 并可在命令行中直接执行 `pandoc`。
2. 系统中至少存在一个可用的 PDF 引擎，例如：
   - `xelatex` 或 `pdflatex`（可通过安装 TeX Live、MiKTeX 等 TeX 发行版获得）；
   - [Tectonic](https://tectonic-typesetting.github.io/)（一次安装即可自动下载所需宏包）。

脚本会尝试通过 `fontconfig` 自动检测常见的中文字体，并在使用 `xelatex`/`tectonic` 等引擎时自动启用，以避免导出后的 PDF 出现中文缺失或乱码。如果系统无法识别中文字体，可以通过 `--cjk-font` 参数显式指定，例如：

```bash
python tools/pdf_export/export_to_pdf.py --cjk-font "Noto Serif CJK SC"
python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei" # Windows
```

当指定了 `--cjk-font` 而未提供 `--main-font` 时，脚本会自动将主字体与中文字体保持一致，避免罗马数字（Ⅰ、Ⅱ 等）或数学符号在 `tectonic` 等引擎下回退为缺字方框。若需要分别为正文、无衬线与等宽文本配置不同字体，可使用下列参数：

```bash
python tools/pdf_export/export_to_pdf.py --main-font "Noto Serif" --cjk-font "Noto Serif CJK SC"
python tools/pdf_export/export_to_pdf.py --sans-font "Noto Sans" --mono-font "JetBrains Mono"
```

上述字体参数会分别映射到 Pandoc 的 `mainfont`、`sansfont`、`monofont` 变量，可灵活组合使用。

脚本会自动检测上述常见引擎，如果缺失会提示安装方式。也可以通过 `--pdf-engine` 参数显式指定要使用的引擎，例如：

```bash
python tools/pdf_export/export_to_pdf.py --pdf-engine xelatex
```

## 忽略指定文件

- 项目根目录下的 `ignore.md` 用于维护一个导出时需要排除的文件或目录列表，支持以 `#` 开头的注释与空行；
- 默认已经忽略了 `README.md`，这不会影响目录的生成；如果需要将其正文一并导出，只需从 `ignore.md` 中移除对应行，或运行脚本时添加 `--include-readme`；
- 也可以通过 `--ignore-file` 参数指定其他忽略列表文件。

## 封面与目录选项

- 若不需要封面，可以添加 `--no-cover`。
- `--cover-title`、`--cover-subtitle`、`--cover-date` 可覆盖封面的默认文字。
- 封面标题下方默认会展示可点击的“在线版本”链接，指向 <https://plurality-wiki.pages.dev/#/>，便于读者快速跳转至网页版内容。
- `--cover-footer` 用于自定义封面底部的“plurality_wiki 项目”字样（默认以更大字号斜体排版），传入空字符串即可移除该行。
- 目录页会根据 `index.md` 的分组与词条自动生成，默认不再展示各词条内部的小节标题。

如需进一步自定义输出文件名或其他设置，可执行 `python tools/pdf_export/export_to_pdf.py --help` 查看全部参数。
