$targetPath = "C:\Users\81809\OneDrive\デスクトップ\事業\資料作成"

# 通信設定の最適化（巨大ファイルの送信エラー対策）
git config http.postBuffer 524288000
git config http.lowSpeedLimit 0
git config http.lowSpeedTime 999999

if (-not (Test-Path -LiteralPath $targetPath)) {
    Write-Host "Error: Target path not found." -ForegroundColor Red
    return
}
Set-Location -LiteralPath $targetPath -ErrorAction Stop

# 不要な巨大フォルダのインデックスを強制クリーンアップ
Write-Host "Cleaning index for heavy folders..." -ForegroundColor Gray
# APIキーが漏洩しやすい一時ファイル(work/)のみを除外対象に固定
git rm -r --cached work/ 2>$null

# 変更のコミット
git add .
$status = git status --porcelain
if ($status) {
    $commitMsg = "Sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m $commitMsg
    Write-Host "Committed: $commitMsg" -ForegroundColor Green
}

# リモートURLの確認と再設定
$remoteUrl = "https://github.com/yoshimurayusuke0922-design/-Materials.git"
if (-not (git remote)) {
    git remote add origin $remoteUrl
}

# 強制Push（履歴の書き換えを反映）
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "Sync successful!" -ForegroundColor Green
} else {
    Write-Host "Push failed. Check connection or authentication." -ForegroundColor Red
}
