# README pdf 导出

> 本文亦同步发布于 [`docs/pdf_export/README_pdf_output.md`](../../docs/pdf_export/README_pdf_output.md)，更新内容时请保持两处文档一致。

要将整个 wiki 导出为带封面、目录的 PDF，请运行 `tools/pdf_export/export_to_pdf.py` 脚本，或进入模块目录后直接通过包入口执行：

```bash
python tools/pdf_export/export_to_pdf.py

# 或者

cd tools/pdf_export && python -m pdf_export
```

脚本会自动：

1. 优先读取 `index.md` 中的目录结构，确保 PDF 的目录页、章节顺序与索引保持一致；
2. 若索引缺失或未列出全部词条，缺失的文档会自动归入名为“未索引词条”的章节，避免导出内容遗漏；
3. 生成独立的封面页与目录页（目录中的词条名称可直接点击跳转至对应内容）；
4. 在合并内容前，会优先插入项目根目录下的 `Preface.md`（若存在且未被忽略），以确保 PDF 以《前言》开篇；
5. 收集索引及兜底章节列出的 Markdown 文件并按顺序合并，同时在 PDF 中为每个 Markdown 文件单独开启新页面，并在 PDF 大纲中按分类组织；在合并过程中会自动移除词条自身的一级标题，避免 PDF 中出现重复标题；
6. 自动识别 Markdown 中以 `entries/*.md` 形式书写的词条链接，并在合并时重写为指向 PDF 内部锚点的链接，确保离线文档中的交叉跳转仍可点击；
7. 如果 `assets/last-updated.json` 存在，则会读取索引并在每篇词条标题下插入“🕒 最后更新：2025/10/02 12:34:56（abc1234）”提示，使离线 PDF 与线上页面保持一致；
8. 调用 [Pandoc](https://pandoc.org/) 生成排好版的 `plurality_wiki.pdf`。

> ℹ️ 所有被导出的词条都必须在 Frontmatter 中声明 `title`、`tags`、`updated` 字段。`updated` 支持写成 `YYYY-MM-DD` 字符串或 YAML 自动识别的日期字面量，两种写法都会在导出时转换为同一格式。若将字段留空、显式写成 `null` 或填写布尔值/列表，脚本会提示“updated 字段必须为非空字符串或有效日期”。

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
