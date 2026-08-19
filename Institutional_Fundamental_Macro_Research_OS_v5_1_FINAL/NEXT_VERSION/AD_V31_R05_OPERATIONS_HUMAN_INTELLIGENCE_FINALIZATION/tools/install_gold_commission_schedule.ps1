param([string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path)
$ErrorActionPreference = "Stop"
$TaskName = "AlphaDesk_Gold_Commission"
$Runner = Join-Path $PSScriptRoot "run_scheduled_commission.ps1"
$Action = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Runner`" -RepoRoot `"$RepoRoot`""
& schtasks.exe /Create /TN $TaskName /TR $Action /SC MINUTE /MO 60 /F | Out-Host
if ($LASTEXITCODE -ne 0) { throw "FAILED TO INSTALL ALPHA DESK SCHEDULE" }
Write-Host "Installed optional hourly Alpha Desk schedule: $TaskName"
