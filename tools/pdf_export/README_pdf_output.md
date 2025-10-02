# README pdf 导出

要将整个 wiki 导出为带封面、目录的 PDF，请运行 `tools/pdf_export/export_to_pdf.py` 脚本，或进入模块目录后直接通过包入口执行：

```bash
python tools/pdf_export/export_to_pdf.py
# 或者
cd tools/pdf_export && python -m pdf_export
```

脚本会自动：

1. 优先读取 `index.md` 中的目录结构，确保 PDF 的目录页与索引保持一致；
2. 若索引缺失或被忽略，脚本会回退至 `README.md`，如两者均不可用则按 `entries/` 目录实际文件构建后备目录结构；
3. 生成独立的封面页与目录页（目录中的词条名称可直接点击跳转至对应内容）；
4. 在合并内容前，会优先插入项目根目录下的 `前言.md`（若存在且未被忽略），以确保 PDF 以《前言》开篇；
5. 收集 README 或后备目录中列出的 Markdown 文件并按顺序合并，同时在 PDF 中为每个 Markdown 文件单独开启新页面，并在 PDF 大纲中按分类组织；在合并过程中会自动移除词条自身的一级标题，避免 PDF 中出现重复标题；
6. 调用 [Pandoc](https://pandoc.org/) 生成排好版的 `plurality_wiki.pdf`。

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
- 目录页会根据 README 的分组与词条自动生成，默认不再展示各词条内部的小节标题。

如需进一步自定义输出文件名或其他设置，可执行 `python tools/pdf_export/export_to_pdf.py --help` 查看全部参数。
