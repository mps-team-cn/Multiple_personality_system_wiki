python tools/fix_md.py 
python tools/gen_changelog_by_tags.py  --latest-to-head
python tools/retag_and_related.py
node scripts/gen-last-updated.mjs
python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei" 
markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
python generate_tags_index