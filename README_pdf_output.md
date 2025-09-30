# 导出为 PDF

要将整个 wiki 导出为带目录的 PDF，可以使用仓库根目录提供的 `export_to_pdf.py` 脚本：

```bash
python export_to_pdf.py
```

脚本会自动收集 `entries/` 目录下的所有 Markdown 文件并按照 README 中的分类顺序合并，然后调用 [Pandoc](https://pandoc.org/) 生成包含目录的 `plurality_wiki.pdf`。

运行脚本前，请确保：

1. 已安装 Pandoc 并可在命令行中直接执行 `pandoc`。
2. 系统中至少存在一个可用的 PDF 引擎，例如：
   - `xelatex` 或 `pdflatex`（可通过安装 TeX Live、MiKTeX 等 TeX 发行版获得）；
   - [Tectonic](https://tectonic-typesetting.github.io/)（一次安装即可自动下载所需宏包）。

脚本会尝试通过 `fontconfig` 自动检测常见的中文字体，并在使用 `xelatex`/`tectonic` 等引擎时自动启用，以避免导出后的 PDF 出现中文缺失或乱码。如果系统无法识别中文字体，可以通过 `--cjk-font` 参数显式指定，例如：

```bash
python export_to_pdf.py --cjk-font "Noto Serif CJK SC"
python export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei" # windows
```

脚本会自动检测上述常见引擎，如果缺失会提示安装方式。也可以通过 `--pdf-engine` 参数显式指定要使用的引擎，例如：

```bash
python export_to_pdf.py --pdf-engine xelatex
```

如需进一步自定义输出文件名或目录深度，可执行 `python export_to_pdf.py --help` 查看全部参数。