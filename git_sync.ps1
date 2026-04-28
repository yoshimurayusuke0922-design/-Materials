$targetPath = "C:\Users\81809\OneDrive\デスクトップ\事業\資料作成"

# フォルダの存在確認
if (-not (Test-Path -LiteralPath $targetPath)) {
    Write-Host "Error: Target path not found: $targetPath" -ForegroundColor Red
    return
}

# フォルダへ移動
Set-Location -LiteralPath $targetPath -ErrorAction Stop

# Gitリポジトリの初期化
if (-not (Test-Path ".git")) {
    git init
    git branch -M main
    Write-Host "Initialized Git repository in target folder." -ForegroundColor Cyan
}

# 全ファイルのステージングと変更の確認
git add .
$status = git status --porcelain
if ($status) {
    $commitMsg = "Sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m $commitMsg
    Write-Host "Committed changes: $commitMsg" -ForegroundColor Green
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

# リモートリポジトリのURL設定（未設定の場合のみ入力を求める）
if (-not (git remote)) {
    $url = Read-Host "Enter Remote URL (e.g., https://github.com/user/repo.git)"
    if ($url) {
        git remote add origin $url
    } else {
        Write-Host "Push cancelled: Remote URL is required." -ForegroundColor Yellow
        return
    }
}

# Pushの実行
Write-Host "Pushing to remote..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "Sync successful!" -ForegroundColor Green
} else {
    Write-Host "Push failed. Check authentication or remote URL." -ForegroundColor Red
}
