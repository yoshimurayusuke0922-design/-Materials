param(
  [Parameter(Mandatory = $true)]
  [string]$Name,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$templatePath = Join-Path $root "workflow\templates\reference_metadata.md"

if (-not (Test-Path -LiteralPath $templatePath)) {
  throw "Reference metadata template not found: $templatePath"
}

$safeName = ($Name.Trim() -replace "[^\p{L}\p{Nd}_-]+", "-").Trim("-")
if ([string]::IsNullOrWhiteSpace($safeName)) {
  throw "Reference set name is empty after normalization."
}

$setPath = Join-Path $root "reference_slides\library\$safeName"
$slidesPath = Join-Path $setPath "slides"
$sourcePath = Join-Path $setPath "source"
$metadataPath = Join-Path $setPath "metadata.md"

if (Test-Path -LiteralPath $setPath) {
  throw "Reference set already exists: $setPath"
}

if ($DryRun) {
  Write-Host "[DRY RUN] Would create: $setPath"
  Write-Host "[DRY RUN] Would create: $slidesPath"
  Write-Host "[DRY RUN] Would create: $sourcePath"
  Write-Host "[DRY RUN] Would copy metadata template to: $metadataPath"
  exit 0
}

New-Item -ItemType Directory -Path $slidesPath -Force | Out-Null
New-Item -ItemType Directory -Path $sourcePath -Force | Out-Null
Copy-Item -LiteralPath $templatePath -Destination $metadataPath

Write-Host "Created reference set: $setPath"
Write-Host "Next: put source PDFs in source\ or PNG slide images in slides\, then fill metadata.md"
