# 操作日志

- 更新结构：重写 `collect_markdown_structure`，改为读取 `index.md` 并提供未索引兜底分组。
- 文档维护：同步修改 `docs/tools/README.md`、`tools/pdf_export/README_pdf_output.md` 与 `docs/pdf_export/README_pdf_output.md` 说明新的导出顺序。
- 工具尝试：执行 `sequential-thinking` 指令失败（命令不存在），记录后改用手动推理。
- 依赖限制：尝试通过 `pip install pyyaml` 安装依赖失败（代理 403），后续调试转为静态代码分析。
- 计划工具：尝试运行 `shrimp-task-manager plan_task` 未找到命令，改为手动编制任务计划。
