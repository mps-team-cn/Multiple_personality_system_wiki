python tools/fix_md.py 
python tools/gen_changelog_by_tags.py  --latest-to-head
node scripts/gen-last-updated.mjs
@REM python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei" # Windows 
markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"