param(
  [Parameter(Mandatory = $true)]
  [string]$Name,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$templatePath = Join-Path $root "projects\_template"

if (-not (Test-Path -LiteralPath $templatePath)) {
  throw "Template folder not found: $templatePath"
}

$safeName = ($Name.Trim() -replace "[^\p{L}\p{Nd}_-]+", "-").Trim("-")
if ([string]::IsNullOrWhiteSpace($safeName)) {
  throw "Project name is empty after normalization."
}

$date = Get-Date -Format "yyyy-MM-dd"
$projectPath = Join-Path $root "projects\$date-$safeName"

if (Test-Path -LiteralPath $projectPath) {
  throw "Project already exists: $projectPath"
}

if ($DryRun) {
  Write-Host "[DRY RUN] Would create: $projectPath"
  exit 0
}

Copy-Item -LiteralPath $templatePath -Destination $projectPath -Recurse
Write-Host "Created project: $projectPath"
Write-Host "Next: fill direction.md or requirements.md"
