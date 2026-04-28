param(
  [Parameter(Mandatory = $false)]
  [string]$Name,

  [Parameter(Mandatory = $true)]
  [string]$Direction,

  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$templatePath = Join-Path $root "projects\_template"

if (-not (Test-Path -LiteralPath $templatePath)) {
  throw "Template folder not found: $templatePath"
}

if ([string]::IsNullOrWhiteSpace($Name)) {
  $Name = "deck-from-direction-$(Get-Date -Format 'HHmmss')"
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
  Write-Host "[DRY RUN] Would write direction.md"
  exit 0
}

Copy-Item -LiteralPath $templatePath -Destination $projectPath -Recurse

$directionPath = Join-Path $projectPath "direction.md"
$createdAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$directionDocument = @(
  "# Direction Brief"
  ""
  "Created: $createdAt"
  "Project name: $safeName"
  ""
  "## Direction"
  ""
  $Direction
  ""
  "## Next Codex Prompt"
  ""
  "Use projects/$date-$safeName/direction.md as input and create requirements.md in the DECK_REQUIREMENTS_TEMPLATE.md format."
  "Put assumptions, open questions, and final-check items in intake/assumptions.md."
) -join [Environment]::NewLine

Set-Content -LiteralPath $directionPath -Value $directionDocument -Encoding UTF8

Write-Host "Created project: $projectPath"
Write-Host "Wrote direction: $directionPath"
Write-Host "Next: ask Codex to create requirements.md from this direction.md"
