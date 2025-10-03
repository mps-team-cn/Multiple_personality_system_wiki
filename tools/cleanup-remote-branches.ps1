param(
    [string]$Prefix = "codex"   # 默认清理 codex 前缀的分支
)

Write-Host "🔎 正在清理远端分支，前缀 = '$Prefix' ..." -ForegroundColor Cyan

# 1) 同步远端 & 清理本地陈旧引用
git fetch origin --prune

# 2) 找出远端真正存在的分支
$remoteRefs = git ls-remote --heads origin "refs/heads/$Prefix*" "refs/heads/$Prefix/*"

if (-not $remoteRefs) {
    Write-Host "✅ 远端没有任何以 '$Prefix' 开头的分支，无需删除。" -ForegroundColor Green
    exit 0
}

# 3) 提取分支名
$branches = $remoteRefs | ForEach-Object {
    ($_ -split "`t")[1] -replace '^refs/heads/',''
} | Sort-Object -Unique

Write-Host "🗑️ 将删除这些远端分支：" -ForegroundColor Yellow
$branches | ForEach-Object { Write-Host "  - $_" }

# 4) 删除远端分支
foreach ($b in $branches) {
    git push origin --delete "$b"
}

# 5) 再次修剪本地远端分支缓存
git remote prune origin

Write-Host "✨ 清理完成！" -ForegroundColor Green
