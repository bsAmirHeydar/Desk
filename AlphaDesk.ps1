param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)
$ErrorActionPreference = "Stop"
$Repo = $PSScriptRoot
$Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT\tools\alpha_desk_v2.py"
if (-not (Test-Path -LiteralPath $Tool)) { throw "Alpha Desk V2 P13 canonical Gold Control Room is not installed." }
if (-not $AlphaArgs -or $AlphaArgs.Count -eq 0) {
    Write-Host "Alpha Desk V2 - Gold Control Room"
    Write-Host "Run Gold:          .\AlphaDesk.ps1 run Gold"
    Write-Host "Latest report:     .\AlphaDesk.ps1 report Gold"
    Write-Host "Open Control Room: .\AlphaDesk.ps1 open Gold"
    Write-Host "Output status:     .\AlphaDesk.ps1 output-status Gold"
    Write-Host "Cluster:           .\AlphaDesk.ps1 cluster Gold"
    Write-Host "Status:            .\AlphaDesk.ps1 status"
    Write-Host "Health:            .\AlphaDesk.ps1 health"
    Write-Host "True Forward:      .\AlphaDesk.ps1 tf-status"
    Write-Host "Learning:          .\AlphaDesk.ps1 learning-status"
    Write-Host "RC:                .\AlphaDesk.ps1 rc-status"
    exit 0
}
& python $Tool --repo-root $Repo @AlphaArgs
exit $LASTEXITCODE
