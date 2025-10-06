param(
    [string]$Prefix = "codex",                  # 要清理的前缀
    [string[]]$Protected = @("main","master","develop"),  # 保护分支，永不删除
    [switch]$DryRun,                            # 只显示将要删除的内容，不执行
    [switch]$Force                              # 跳过确认
)

function Test-RefExists($ref) {
    git show-ref --verify --quiet $ref
    return $LASTEXITCODE -eq 0
}

Write-Host "🔎 扫描并清理本地与远端分支，前缀 = '$Prefix' ..." -ForegroundColor Cyan

# 1) 同步远端 & 清理本地陈旧引用
git fetch origin --prune | Out-Null

# 2) 收集远端存在的匹配分支
$remoteRefs = git ls-remote --heads origin "refs/heads/$Prefix*" "refs/heads/$Prefix/*"
$remoteBranches = @()
if ($remoteRefs) {
    $remoteBranches = $remoteRefs | ForEach-Object {
        ($_ -split "`t")[1] -replace '^refs/heads/',''
    }
}

# 3) 收集本地存在的匹配分支（无论是否有上游）
$localBranches = git for-each-ref --format="%(refname:short)" "refs/heads/$Prefix*" "refs/heads/$Prefix/*" 2>$null

# 4) 需要处理的分支集合：远端 ∪ 本地
$allCandidates = @($remoteBranches + $localBranches) | Sort-Object -Unique

# 5) 过滤保护分支
$toDelete = $allCandidates | Where-Object { $Protected -notcontains $_ }

if (-not $toDelete -or $toDelete.Count -eq 0) {
    Write-Host "✅ 没有需要删除的分支（或都在保护名单中）。" -ForegroundColor Green
    exit 0
}

Write-Host "🗂️ 计划删除的分支（本地 & 远端，如存在）：" -ForegroundColor Yellow
$toDelete | ForEach-Object { Write-Host "  - $_" }

if ($DryRun) {
    Write-Host "`n🟦 DryRun 模式：仅展示将要删除的分支，不执行任何删除操作。" -ForegroundColor Cyan
    exit 0
}

if (-not $Force) {
    $confirm = Read-Host "⚠️ 确认删除以上分支？输入大写 YES 继续"
    if ($confirm -ne "YES") {
        Write-Host "已取消。" -ForegroundColor Yellow
        exit 0
    }
}

# 6) 若当前分支在删除清单中，则先切换到安全分支或分离HEAD
$currentBranch = (git rev-parse --abbrev-ref HEAD).Trim()
if ($toDelete -contains $currentBranch) {
    # 尝试安全分支顺序：main -> master -> develop
    $safe = $Protected | Where-Object { Test-RefExists "refs/heads/$_" } | Select-Object -First 1
    if ($safe) {
        Write-Host "🔀 当前在待删分支 '$currentBranch'，先切换到 '$safe' ..." -ForegroundColor Cyan
        git switch $safe | Out-Null
    } else {
        Write-Host "🔀 当前在待删分支 '$currentBranch'，找不到安全分支，改为分离 HEAD ..." -ForegroundColor Cyan
        git switch --detach | Out-Null
    }
}

# 7) 逐个删除：远端 -> 本地 -> 本地远端引用
foreach ($b in $toDelete) {
    # 7.1 远端分支
    if ($remoteBranches -contains $b) {
        Write-Host "🌐 删除远端分支 origin/$b ..." -ForegroundColor Magenta
        git push origin --delete "$b" 2>$null | Out-Null
    }

    # 7.2 本地分支
    if (Test-RefExists "refs/heads/$b") {
        Write-Host "💻 删除本地分支 $b ..." -ForegroundColor DarkCyan
        git branch -D "$b" 2>$null | Out-Null
    }

    # 7.3 本地的远端跟踪引用
    if (Test-RefExists "refs/remotes/origin/$b") {
        Write-Host "🧹 删除本地远端引用 origin/$b ..." -ForegroundColor DarkYellow
        git branch -dr "origin/$b" 2>$null | Out-Null
    }
}

# 8) 再次修剪远端引用缓存
git remote prune origin | Out-Null

Write-Host "✨ 清理完成！共处理分支：$($toDelete.Count)" -ForegroundColor Green
