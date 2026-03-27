#!/usr/bin/env bash

set -u

PREFIX="codex"
DRY_RUN=0
FORCE=0
PROTECTED=("main" "master" "develop")

usage() {
    cat <<'EOF'
用法:
  bash tools/cleanup-remote-branches.sh [选项]

选项:
  -p, --prefix <前缀>         指定要清理的分支前缀，默认: codex
      --protected <分支名>    添加保护分支，可重复使用
      --replace-protected     清空默认保护分支后，再配合 --protected 自定义
  -n, --dry-run               仅展示将要删除的分支，不执行删除
  -f, --force                 跳过确认
  -h, --help                  显示帮助

示例:
  bash tools/cleanup-remote-branches.sh --dry-run
  bash tools/cleanup-remote-branches.sh --prefix codex --force
  bash tools/cleanup-remote-branches.sh --replace-protected --protected main --protected release
EOF
}

test_ref_exists() {
    git show-ref --verify --quiet "$1"
}

contains_branch() {
    local branch="$1"
    shift
    local item
    for item in "$@"; do
        if [[ "$item" == "$branch" ]]; then
            return 0
        fi
    done
    return 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -p|--prefix)
            if [[ $# -lt 2 ]]; then
                echo "错误: $1 需要一个参数。" >&2
                usage
                exit 1
            fi
            PREFIX="$2"
            shift 2
            ;;
        --protected)
            if [[ $# -lt 2 ]]; then
                echo "错误: $1 需要一个参数。" >&2
                usage
                exit 1
            fi
            PROTECTED+=("$2")
            shift 2
            ;;
        --replace-protected)
            PROTECTED=()
            shift
            ;;
        -n|--dry-run)
            DRY_RUN=1
            shift
            ;;
        -f|--force)
            FORCE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "错误: 不支持的参数 $1" >&2
            usage
            exit 1
            ;;
    esac
done

echo "扫描并清理本地与远端分支，前缀 = '$PREFIX' ..."

git fetch origin --prune >/dev/null

remote_branches=()
while IFS=$'\t' read -r _ ref; do
    [[ -n "${ref:-}" ]] || continue
    remote_branches+=("${ref#refs/heads/}")
done < <(git ls-remote --heads origin "refs/heads/${PREFIX}*" "refs/heads/${PREFIX}/*")

local_branches=()
while IFS= read -r branch; do
    [[ -n "$branch" ]] || continue
    local_branches+=("$branch")
done < <(git for-each-ref --format='%(refname:short)' "refs/heads/${PREFIX}*" "refs/heads/${PREFIX}/*" 2>/dev/null)

mapfile -t all_candidates < <(
    printf '%s\n' "${remote_branches[@]:-}" "${local_branches[@]:-}" \
        | awk 'NF' \
        | sort -u
)

to_delete=()
for branch in "${all_candidates[@]:-}"; do
    [[ -n "$branch" ]] || continue
    if ! contains_branch "$branch" "${PROTECTED[@]:-}"; then
        to_delete+=("$branch")
    fi
done

if [[ ${#to_delete[@]} -eq 0 ]]; then
    echo "没有需要删除的分支，或它们都在保护名单中。"
    exit 0
fi

echo "计划删除的分支（本地与远端，如存在）："
for branch in "${to_delete[@]}"; do
    echo "  - $branch"
done

if [[ $DRY_RUN -eq 1 ]]; then
    echo
    echo "DryRun 模式：仅展示将要删除的分支，不执行任何删除操作。"
    exit 0
fi

if [[ $FORCE -ne 1 ]]; then
    read -r -p "确认删除以上分支？输入大写 YES 继续: " confirm
    if [[ "$confirm" != "YES" ]]; then
        echo "已取消。"
        exit 0
    fi
fi

current_branch="$(git rev-parse --abbrev-ref HEAD | tr -d '\n')"
if contains_branch "$current_branch" "${to_delete[@]}"; then
    safe_branch=""
    for candidate in "${PROTECTED[@]:-}"; do
        if test_ref_exists "refs/heads/$candidate"; then
            safe_branch="$candidate"
            break
        fi
    done

    if [[ -n "$safe_branch" ]]; then
        echo "当前位于待删分支 '$current_branch'，先切换到 '$safe_branch' ..."
        git switch "$safe_branch" >/dev/null
    else
        echo "当前位于待删分支 '$current_branch'，未找到安全分支，切换到分离 HEAD ..."
        git switch --detach >/dev/null
    fi
fi

for branch in "${to_delete[@]}"; do
    if contains_branch "$branch" "${remote_branches[@]:-}"; then
        echo "删除远端分支 origin/$branch ..."
        git push origin --delete "$branch" >/dev/null 2>&1 || true
    fi

    if test_ref_exists "refs/heads/$branch"; then
        echo "删除本地分支 $branch ..."
        git branch -D "$branch" >/dev/null 2>&1 || true
    fi

    if test_ref_exists "refs/remotes/origin/$branch"; then
        echo "删除本地远端引用 origin/$branch ..."
        git branch -dr "origin/$branch" >/dev/null 2>&1 || true
    fi
done

git remote prune origin >/dev/null

echo "清理完成！共处理分支：${#to_delete[@]}"
