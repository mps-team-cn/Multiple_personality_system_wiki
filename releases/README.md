# Releases - PDF 输出与历史版本

本目录是 `make pdf` 的**默认输出目录**（本地构建产物，通常不提交）。历史 PDF 归档在 GitHub Releases，按 tag 下载。

## 📦 最新版本

当前最新：**v4.4.0**（2026-08-26）

- 下载：[Multiple_Personality_System_wiki.pdf](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/download/v4.4.0/Multiple_Personality_System_wiki.pdf)
- 全部版本：<https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases>
- 版本变更：见 [更新日志](../docs/changelog.md)

## 🛠 生成方式

PDF 由 `tools/pdf_export/export_to_pdf.py` 生成（Pandoc 排版 + `tectonic`/`xelatex` 编译），不是 `mkdocs-pdf-export-plugin`。

```bash
make pdf                    # 输出到 releases/Multiple_Personality_System_wiki.pdf
make pdf PDF_OUTPUT=dist/wiki.pdf           # 改输出路径
make pdf PDF_ENGINE=xelatex CJK_FONT="Noto Serif CJK SC"   # 换引擎/字体
```

文件名由 `Makefile` 的 `PDF_OUTPUT` 决定，默认 `Multiple_Personality_System_wiki.pdf`；发布到 Releases 时沿用该文件名。

## 🔗 在线版本

- 主站：<https://wiki.mpsteam.cn/>
- Cloudflare Pages：<https://mpswiki.pages.dev/>（备用）

在线版本始终最新，包含所有词条更新。

## 📌 使用说明

PDF 适合离线阅读、打印成册、存档引用与版本对比；需要最新内容请访问在线版本。

---

**工具文档**：`docs/dev/Tools-Index.md` · **代码**：`tools/pdf_export/`
