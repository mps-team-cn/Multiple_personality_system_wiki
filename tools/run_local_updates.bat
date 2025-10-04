@REM 更新日志
python tools/gen_changelog_by_tags.py --latest-to-head
@REM 批量维护词条标签与“相关条目”区块
python tools/retag_and_related.py
@REM 生成最后更新信息
node scripts/gen-last-updated.mjs
@REM 生成 PDF 和 目录索引
python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
@REM 生成标签索引
python tools/generate_tags_index.py
@REM 生成 Docsify 搜索索引
python tools/build_search_index.py
@REM 修正 Markdown 格式问题
python tools/fix_md.py
@REM 检查 Markdown 格式问题
markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
