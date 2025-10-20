#!/usr/bin/env bash
# 用于在本地一次性执行常用维护脚本，统一入口便于日常更新。
set -euo pipefail

# 切换到仓库根目录，避免相对路径引发执行失败。
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# 默认执行全部步骤，可通过参数跳过特定命令。
SKIP_CHANGELOG=false
SKIP_PDF=false
SKIP_FIX_MD=false
SKIP_MARKDOWNLINT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-changelog)
      SKIP_CHANGELOG=true
      ;;
    --skip-pdf)
      SKIP_PDF=true
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
  2. python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
  3. python tools/fix_markdown.py
  4. markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"

可选参数：
  --skip-changelog      跳过变更日志生成
  --skip-pdf            跳过 PDF 导出
  --skip-fix-md         跳过 Markdown 自动修复
  --skip-markdownlint   跳过 markdownlint 校验
  -h, --help            显示本帮助信息

注意：
  - MkDocs Material 使用内置搜索，不再需要单独生成搜索索引
  - 标签索引由 MkDocs Material tags 插件自动生成，无需手动维护
  - 页面修改时间由 git-revision-date-localized 插件自动获取，无需手动维护
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

if ! ${SKIP_PDF}; then
  run_step "导出 PDF" python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
else
  echo "已跳过：PDF 导出" >&2
fi

# 注意: 以下工具已废弃 (移至 tools/deprecated/),不再需要手动运行:
# - retag_and_related.py: 标签由 Frontmatter 直接管理
# - generate_tags_index.py: MkDocs Material tags 插件自动生成
# - build_search_index.py: MkDocs Material 内置搜索
# - gen-last-updated.mjs: MkDocs Material git-revision-date-localized 插件自动获取

if ! ${SKIP_FIX_MD}; then
  run_step "自动修复 Markdown" python tools/fix_markdown.py
else
  echo "已跳过：Markdown 自动修复" >&2
fi

run_step "检查标签规范 (Tagging Standard v2.0)" python tools/check_tags.py docs/entries/

if ! ${SKIP_MARKDOWNLINT}; then
  run_step "运行 markdownlint" markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
else
  echo "已跳过：markdownlint 校验" >&2
fi

echo "" >&2
echo "全部任务执行完毕。" >&2
