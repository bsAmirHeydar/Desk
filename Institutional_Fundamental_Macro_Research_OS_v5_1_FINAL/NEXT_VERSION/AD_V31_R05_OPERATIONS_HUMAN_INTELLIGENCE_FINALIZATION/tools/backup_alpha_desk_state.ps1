param([string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path,[string]$Destination)
$ErrorActionPreference = "Stop"
if (-not $Destination) { $Destination = Join-Path $env:USERPROFILE "Documents\AlphaDesk_Backups" }
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Temp = Join-Path $env:TEMP ("AlphaDeskBackup_" + $Stamp)
New-Item -ItemType Directory -Force -Path $Temp | Out-Null
$Paths = @(
 "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0\artifacts\state",
 "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE\artifacts\state",
 "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE\artifacts\state",
 "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE\certification"
)
foreach ($Rel in $Paths) {
 $Src = Join-Path $RepoRoot $Rel
 if (Test-Path $Src) { $Dst = Join-Path $Temp $Rel; New-Item -ItemType Directory -Force -Path (Split-Path $Dst -Parent) | Out-Null; Copy-Item -Recurse -Force $Src $Dst }
}
$Zip = Join-Path $Destination ("AlphaDesk_State_" + $Stamp + ".zip")
Compress-Archive -Path (Join-Path $Temp "*") -DestinationPath $Zip -Force
Remove-Item -Recurse -Force $Temp
Write-Host $Zip
