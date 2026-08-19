$ErrorActionPreference = "Stop"
$TaskName = "AlphaDesk_Gold_Commission"
& schtasks.exe /Delete /TN $TaskName /F | Out-Host
if ($LASTEXITCODE -ne 0) { throw "FAILED TO REMOVE ALPHA DESK SCHEDULE" }
Write-Host "Removed Alpha Desk schedule: $TaskName"
