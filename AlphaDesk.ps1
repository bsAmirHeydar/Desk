param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)

$ErrorActionPreference = "Stop"
$Repo = $PSScriptRoot

$V2Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT\tools\alpha_desk_v2.py"
$V3Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING\tools\alpha_desk_v3.py"

function Invoke-V2([string[]]$ArgsList) {
    if (-not (Test-Path -LiteralPath $V2Tool)) {
        throw "Alpha Desk V2 P13 canonical Gold Control Room is not installed."
    }
    & python $V2Tool @ArgsList
    return $LASTEXITCODE
}

function Invoke-V3([string[]]$ArgsList) {
    if (-not (Test-Path -LiteralPath $V3Tool)) {
        throw "Alpha Desk V3 P04 commissioning runtime is not installed."
    }
    & python $V3Tool @ArgsList
    return $LASTEXITCODE
}

function Get-V3RouteMode {
    if (-not (Test-Path -LiteralPath $V3Tool)) { return "V2_BASELINE" }
    $Mode = (& python $V3Tool route-mode | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { return "V2_BASELINE" }
    return $Mode
}

if (-not $AlphaArgs -or $AlphaArgs.Count -eq 0) {
    Write-Host "Alpha Desk - Gold"
    Write-Host ""
    Write-Host "Canonical baseline / production route:"
    Write-Host "  Run Gold:              .\AlphaDesk.ps1 run Gold"
    Write-Host "  Latest report:         .\AlphaDesk.ps1 report Gold"
    Write-Host "  Open Control Room:     .\AlphaDesk.ps1 open Gold"
    Write-Host ""
    Write-Host "V3 shadow commissioning:"
    Write-Host "  Commission Gold:       .\AlphaDesk.ps1 commission Gold"
    Write-Host "  V3 report:             .\AlphaDesk.ps1 commission-report Gold"
    Write-Host "  V3 open:               .\AlphaDesk.ps1 commission-open Gold"
    Write-Host "  V3 status:             .\AlphaDesk.ps1 v3-status"
    Write-Host "  V3 true-forward:       .\AlphaDesk.ps1 v3-tf-status"
    Write-Host "  V3 promotion status:   .\AlphaDesk.ps1 v3-promotion-status"
    Write-Host ""
    Write-Host "Promotion is fail-closed. Until PRODUCTION_V3, 'run Gold' remains on V2."
    exit 0
}

$Command = [string]$AlphaArgs[0]
$Rest = @()
if ($AlphaArgs.Count -gt 1) { $Rest = @($AlphaArgs[1..($AlphaArgs.Count-1)]) }

switch ($Command.ToLowerInvariant()) {
    "commission" {
        $Code = Invoke-V3 (@("run") + $Rest)
        exit $Code
    }
    "commission-report" {
        $Code = Invoke-V3 (@("report") + $Rest)
        exit $Code
    }
    "commission-open" {
        $Code = Invoke-V3 (@("open") + $Rest)
        exit $Code
    }
    "v3-status" {
        $Code = Invoke-V3 @("status")
        exit $Code
    }
    "v3-tf-status" {
        $Code = Invoke-V3 @("tf-status")
        exit $Code
    }
    "v3-promotion-status" {
        $Code = Invoke-V3 @("promotion-status")
        exit $Code
    }
    "v3-promote" {
        $Code = Invoke-V3 (@("promote") + $Rest)
        exit $Code
    }
    "v3-rollback" {
        $Code = Invoke-V3 @("rollback")
        exit $Code
    }
}

# Canonical commands remain on V2 until the explicit P04 promotion state
# becomes PRODUCTION_V3. This preserves the frozen V2 baseline and rollback.
if ($Command -in @("run","report","open")) {
    $IsGold = ($Rest.Count -gt 0 -and ([string]$Rest[0]).ToLowerInvariant() -in @("gold","xauusd"))
    if ($IsGold -and (Get-V3RouteMode) -eq "PRODUCTION_V3") {
        $Code = Invoke-V3 (@($Command) + $Rest)
        exit $Code
    }
}

$Code = Invoke-V2 $AlphaArgs
exit $Code
