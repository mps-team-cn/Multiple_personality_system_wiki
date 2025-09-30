# plurality_wiki

本仓库按照主题将多重意识体系统与相关心理健康词条整理为 Markdown 页面。

## 目录结构

- `entries/诊断与临床/`：精神医学诊断、创伤与症状说明。
- `entries/系统角色与类型/`：系统内常见的身份类型与角色分工。
- `entries/系统体验与机制/`：系统运作体验、机制与状态变化。
- `entries/实践与支持/`：实践方法、互助工具与支持策略。

## 词条索引

### 诊断与临床

- [创伤](entries/诊断与临床/创伤.md)
- [创伤后应激障碍](entries/诊断与临床/创伤后应激障碍.md)
- [复杂性创伤后应激障碍](entries/诊断与临床/复杂性创伤后应激障碍.md)
- [孤独症谱系](entries/诊断与临床/孤独症谱系.md)
- [抑郁障碍](entries/诊断与临床/抑郁障碍.md)
- [解离性身份障碍](entries/诊断与临床/解离性身份障碍.md)
- [其他特定解离性障碍](entries/诊断与临床/其他特定解离性障碍.md)
- [躯体化障碍](entries/诊断与临床/躯体化障碍.md)
- [边缘性人格障碍](entries/诊断与临床/边缘性人格障碍.md)
- [部分解离性身份障碍](entries/诊断与临床/部分解离性身份障碍.md)
- [述情障碍](entries/诊断与临床/述情障碍.md)

### 系统角色与类型

- [主体](entries/系统角色与类型/主体.md)
- [仆从](entries/系统角色与类型/仆从.md)
- [内部自助者](entries/系统角色与类型/内部自助者.md)
- [核心](entries/系统角色与类型/核心.md)
- [特殊认同](entries/系统角色与类型/特殊认同.md)
- [管理者](entries/系统角色与类型/管理者.md)
- [人格面具](entries/系统角色与类型/人格面具.md)
- [伪主体](entries/系统角色与类型/伪主体.md)
- [医源型系统](entries/系统角色与类型/医源型系统.md)
- [混合](entries/系统角色与类型/混合.md)
- [碎片](entries/系统角色与类型/碎片.md)
- [系魂](entries/系统角色与类型/系魂.md)

### 系统体验与机制

- [偏重](entries/系统体验与机制/偏重.md)
- [存在感](entries/系统体验与机制/存在感.md)
- [封存](entries/系统体验与机制/封存.md)
- [应激反应](entries/系统体验与机制/应激反应.md)
- [意识修改](entries/系统体验与机制/意识修改.md)
- [意识共存](entries/系统体验与机制/意识共存.md)
- [权限](entries/系统体验与机制/权限.md)
- [独有记忆](entries/系统体验与机制/独有记忆.md)
- [独立性](entries/系统体验与机制/独立性.md)
- [融合](entries/系统体验与机制/融合.md)
- [记忆屏蔽](entries/系统体验与机制/记忆屏蔽.md)
- [迭代](entries/系统体验与机制/迭代.md)
- [整合](entries/系统体验与机制/整合.md)
- [重构](entries/系统体验与机制/重构.md)
- [躯体认同](entries/系统体验与机制/躯体认同.md)
- [非我感](entries/系统体验与机制/非我感.md)

### 实践与支持

- [冥想](entries/实践与支持/冥想.md)

## 导出为 PDF

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

