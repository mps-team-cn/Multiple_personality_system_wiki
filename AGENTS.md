# Plurality Wiki 贡献指南

## 通用约定

- 所有条目、说明文档与提交信息优先使用简体中文。
- 词条一级标题统一采用 `中文名（English）` 格式，若为诊断或疾病则在括号内使用标准缩写（如“重度抑郁障碍（MDD）”）。
- 更新或新增词条时，强制同步维护 `README.md` 中的目录索引与分类结构。
- Markdown 文档采用一级标题表示词条名称，二级及以下标题依内容层级递增；若存在触发警示，请置于文首。
- 提交前请检查 `ignore.md`，确保需要排除的文件已正确维护。

## PDF 导出脚本 (`tools/pdf_export/`)

- 脚本使用 Python 3.10+ 语法与类型标注，保持现有的函数拆分与 dataclass 结构。
- 处理路径时使用 `pathlib.Path`，避免直接拼接字符串。
- 在解析/生成 LaTeX 与 Markdown 时需考虑跨平台兼容性，并对用户输入做必要的转义。
- 如修改导出逻辑，请同步更新 `tools/pdf_export/README_pdf_output.md` 说明文档。

## 测试与检查

- 修改 Python 代码后至少运行 `python -m compileall tools/pdf_export/export_to_pdf.py` 确认无语法错误。
- 若引入额外依赖或命令行选项，请在 README 或相关文档中注明使用方法与必备前置条件。
