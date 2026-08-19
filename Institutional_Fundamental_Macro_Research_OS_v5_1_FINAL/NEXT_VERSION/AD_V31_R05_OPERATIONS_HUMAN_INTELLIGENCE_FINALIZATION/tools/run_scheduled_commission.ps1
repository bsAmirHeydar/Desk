param([string]$RepoRoot)
$ErrorActionPreference = "Stop"
if (-not $RepoRoot) { throw "RepoRoot required" }
$PolicyPath = Join-Path $PSScriptRoot "..\config\operations_cadence_policy.json"
$Policy = Get-Content $PolicyPath -Raw | ConvertFrom-Json
$Now = Get-Date
$Allowed = $false
foreach ($Window in $Policy.active_windows) {
    $Start = [TimeSpan]::Parse($Window.start)
    $End = [TimeSpan]::Parse($Window.end)
    if ($End -ge $Start) { if ($Now.TimeOfDay -ge $Start -and $Now.TimeOfDay -le $End) { $Allowed = $true } }
    else { if ($Now.TimeOfDay -ge $Start -or $Now.TimeOfDay -le $End) { $Allowed = $true } }
}
if (-not $Allowed) { Write-Host "Outside configured Gold monitoring window; no backdated run created."; exit 0 }
Push-Location $RepoRoot
try { & .\AlphaDesk.ps1 commission Gold; exit $LASTEXITCODE }
finally { Pop-Location }
