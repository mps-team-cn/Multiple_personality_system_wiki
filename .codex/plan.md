# 任务规划

## 目标
- 让 PDF 导出结构（章节与书签）按照 index.md 的顺序组织词条。

## 子任务
1. 重新实现 collect_markdown_structure，使其优先解析 index.md。
2. 为未出现在 index.md 中的条目追加兜底分组，保持可访问性。
3. 确保 Preface.md 仍作为单独章节且不会重复。
4. 更新 docs/tools/README.md 说明结构调整。
5. 运行 python -m compileall tools/pdf_export/export_to_pdf.py 验证语法。

## 验收标准
- 结构顺序与 index.md 一致，包含 index 中出现的所有条目。
- 未在 index 中的条目汇总到独立章节。
- 目录与书签同步更新，无前置回归。
- 编译检查通过。
