#!/usr/bin/env bash
# 用于在本地一次性执行常用维护脚本，统一入口便于日常更新。
set -euo pipefail

# 切换到仓库根目录，避免相对路径引发执行失败。
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# 默认执行全部步骤，可通过参数跳过特定命令。
SKIP_CHANGELOG=false
SKIP_RETAG=false
SKIP_LAST_UPDATED=false
SKIP_PDF=false
SKIP_TAG_INDEX=false
SKIP_SEARCH_INDEX=false
SKIP_FIX_MD=false
SKIP_MARKDOWNLINT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-changelog)
      SKIP_CHANGELOG=true
      ;;
    --skip-retag)
      SKIP_RETAG=true
      ;;
    --skip-last-updated)
      SKIP_LAST_UPDATED=true
      ;;
    --skip-pdf)
      SKIP_PDF=true
      ;;
    --skip-tag-index)
      SKIP_TAG_INDEX=true
      ;;
    --skip-search-index)
      SKIP_SEARCH_INDEX=true
      ;;
    --skip-fix-md)
      SKIP_FIX_MD=true
      ;;
    --skip-markdownlint)
      SKIP_MARKDOWNLINT=true
      ;;
    --help|-h)
      cat <<'USAGE'
用法：tools/run_local_updates.sh [选项]

默认执行以下步骤：
  1. python tools/gen_changelog_by_tags.py --latest-to-head
  2. python tools/retag_and_related.py
  3. node scripts/gen-last-updated.mjs
  4. python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
  5. python tools/generate_tags_index.py
  6. python tools/build_search_index.py
  7. python tools/fix_md.py
  8. markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"

可选参数：
  --skip-changelog      跳过变更日志生成
  --skip-retag          跳过标签与关联词条重建
  --skip-last-updated   跳过最后更新时间索引生成
  --skip-pdf            跳过 PDF 导出
  --skip-tag-index      跳过标签索引生成
  --skip-search-index   跳过搜索索引生成
  --skip-fix-md         跳过 Markdown 自动修复
  --skip-markdownlint   跳过 markdownlint 校验
  -h, --help            显示本帮助信息
USAGE
      exit 0
      ;;
    *)
      echo "未识别的参数：$1" >&2
      exit 1
      ;;
  esac
  shift
done

run_step() {
  local description="$1"
  shift
  echo "" >&2
  echo ">>> ${description}" >&2
  "$@"
}

if ! ${SKIP_CHANGELOG}; then
  run_step "生成变更日志" python tools/gen_changelog_by_tags.py --latest-to-head
else
  echo "已跳过：变更日志生成" >&2
fi

if ! ${SKIP_RETAG}; then
  run_step "刷新 Frontmatter 标签与相关词条" python tools/retag_and_related.py
else
  echo "已跳过：标签与相关词条重建" >&2
fi

if ! ${SKIP_LAST_UPDATED}; then
  run_step "生成最后更新时间索引" node scripts/gen-last-updated.mjs
else
  echo "已跳过：最后更新时间索引" >&2
fi

if ! ${SKIP_PDF}; then
  run_step "导出 PDF" python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
else
  echo "已跳过：PDF 导出" >&2
fi

if ! ${SKIP_TAG_INDEX}; then
  run_step "生成标签索引" python tools/generate_tags_index.py
else
  echo "已跳过：标签索引生成" >&2
fi

if ! ${SKIP_SEARCH_INDEX}; then
  run_step "生成 Docsify 搜索索引" python tools/build_search_index.py
else
  echo "已跳过：搜索索引生成" >&2
fi

if ! ${SKIP_FIX_MD}; then
  run_step "自动修复 Markdown" python tools/fix_md.py
else
  echo "已跳过：Markdown 自动修复" >&2
fi

if ! ${SKIP_MARKDOWNLINT}; then
  run_step "运行 markdownlint" markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
else
  echo "已跳过：markdownlint 校验" >&2
fi

echo "" >&2
echo "全部任务执行完毕。" >&2
