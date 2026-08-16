param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)
$ErrorActionPreference = "Stop"
$Repo = $PSScriptRoot
$Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION\tools\alpha_desk_v2.py"
if (-not (Test-Path -LiteralPath $Tool)) { throw "Alpha Desk V2 P11 launcher is not installed." }
if (-not $AlphaArgs -or $AlphaArgs.Count -eq 0) {
    Write-Host "Alpha Desk V2 unified front door"
    Write-Host "Run Gold:          .\AlphaDesk.ps1 run Gold"
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
