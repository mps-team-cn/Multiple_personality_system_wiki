# 任务规划

## 目标
- 修复 frontmatter 解析对 updated 字段的校验，使 YAML 日期与字符串均可通过并输出一致的错误提示。

## 子任务
1. 审查 `_parse_frontmatter` 中 updated 字段处理逻辑，确认触发空字符串错误的原因。
2. 调整类型判断，允许 datetime/date 等可序列化对象并统一转换为字符串，同时保留对空值的明确报错。
3. 更新相关文档（docs/tools/README.md、tools/pdf_export/README_pdf_output.md、docs/pdf_export/README_pdf_output.md），同步说明 frontmatter 兼容策略。
4. 根据需要补充或调整内部注释，确保开发者理解 updated 字段的校验规则。
5. 运行 `python -m compileall tools/pdf_export/export_to_pdf.py` 验证语法通过。

## 验收标准
- PDF 导出工具在 frontmatter 中遇到 YAML 日期时不再抛出“updated 字段必须为非空字符串”的错误。
- 对缺失、null 或空字符串的 updated 字段仍会提供清晰错误提示。
- 文档明确 updated 字段可接受的写法与注意事项。
- 编译检查通过。
