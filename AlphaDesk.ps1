param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)

$ErrorActionPreference = "Stop"
$Repo = $PSScriptRoot

$V2Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT\tools\alpha_desk_v2.py"
$V3Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING\tools\alpha_desk_v3.py"
$P05Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION\tools\p05_status.py"
$P06Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE\tools\p06_status.py"
$P07Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL\tools\p07_status.py"
$script:AlphaDeskLastExitCode = 0

function Invoke-V2([string[]]$ArgsList) {
    if (-not (Test-Path -LiteralPath $V2Tool)) {
        throw "Alpha Desk V2 P13 canonical Gold Control Room is not installed."
    }

    # Stream native stdout/stderr to the operator. Exit status is kept
    # out-of-band so assigning a function result never swallows reports.
    & python $V2Tool @ArgsList
    $script:AlphaDeskLastExitCode = $LASTEXITCODE
}

function Invoke-V3([string[]]$ArgsList) {
    if (-not (Test-Path -LiteralPath $V3Tool)) {
        throw "Alpha Desk V3 P04 commissioning runtime is not installed."
    }

    # Windows PowerShell 5.1 commonly exposes a legacy cp1252 console to
    # native child processes. V3 reports may contain Persian/Unicode text.
    $OldPyIo = $env:PYTHONIOENCODING
    $OldPyUtf8 = $env:PYTHONUTF8
    $OldConsoleEncoding = [Console]::OutputEncoding

    try {
        $Utf8 = New-Object System.Text.UTF8Encoding($false)
        [Console]::OutputEncoding = $Utf8
        $env:PYTHONIOENCODING = "utf-8"
        $env:PYTHONUTF8 = "1"

        # Do not return native stdout as the function's return value.
        # The child output must stream live to the PowerShell host.
        & python $V3Tool @ArgsList
        $script:AlphaDeskLastExitCode = $LASTEXITCODE
    }
    finally {
        [Console]::OutputEncoding = $OldConsoleEncoding

        if ($null -eq $OldPyIo) {
            Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
        } else {
            $env:PYTHONIOENCODING = $OldPyIo
        }

        if ($null -eq $OldPyUtf8) {
            Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
        } else {
            $env:PYTHONUTF8 = $OldPyUtf8
        }
    }

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
    Write-Host "  V3 integrity status:   .\AlphaDesk.ps1 v3-integrity-status"
    Write-Host "  V3 semantic status:    .\AlphaDesk.ps1 v3-semantic-status"
    Write-Host "  V3 kernel status:      .\AlphaDesk.ps1 v3-kernel-status"
    Write-Host "  V3 full refresh:       .\AlphaDesk.ps1 commission Gold --full-refresh"
    Write-Host ""
    Write-Host "Promotion is fail-closed. Until PRODUCTION_V3, 'run Gold' remains on V2."
    exit 0
}

$Command = [string]$AlphaArgs[0]
$Rest = @()
if ($AlphaArgs.Count -gt 1) { $Rest = @($AlphaArgs[1..($AlphaArgs.Count-1)]) }

switch ($Command.ToLowerInvariant()) {
    "commission" {
        Invoke-V3 (@("run") + $Rest)
        exit $script:AlphaDeskLastExitCode
    }
    "commission-report" {
        Invoke-V3 (@("report") + $Rest)
        exit $script:AlphaDeskLastExitCode
    }
    "commission-open" {
        Invoke-V3 (@("open") + $Rest)
        exit $script:AlphaDeskLastExitCode
    }
    "v3-status" {
        Invoke-V3 @("status")
        exit $script:AlphaDeskLastExitCode
    }
    "v3-tf-status" {
        Invoke-V3 @("tf-status")
        exit $script:AlphaDeskLastExitCode
    }
    "v3-promotion-status" {
        Invoke-V3 @("promotion-status")
        exit $script:AlphaDeskLastExitCode
    }
    "v3-integrity-status" {
        if (-not (Test-Path -LiteralPath $P05Tool)) { throw "Alpha Desk V3 P05 integrity status tool is not installed." }
        & python $P05Tool
        exit $LASTEXITCODE
    }
    "v3-semantic-status" {
        if (-not (Test-Path -LiteralPath $P06Tool)) { throw "Alpha Desk V3 P06 semantic status tool is not installed." }
        & python $P06Tool
        exit $LASTEXITCODE
    }
    "v3-kernel-status" {
        if (-not (Test-Path -LiteralPath $P07Tool)) { throw "Alpha Desk V3 P07 kernel status tool is not installed." }
        & python $P07Tool
        exit $LASTEXITCODE
    }
    "v3-promote" {
        Invoke-V3 (@("promote") + $Rest)
        exit $script:AlphaDeskLastExitCode
    }
    "v3-rollback" {
        Invoke-V3 @("rollback")
        exit $script:AlphaDeskLastExitCode
    }
}

# Canonical commands remain on V2 until the explicit P04 promotion state
# becomes PRODUCTION_V3. This preserves the frozen V2 baseline and rollback.
if ($Command -in @("run","report","open")) {
    $IsGold = ($Rest.Count -gt 0 -and ([string]$Rest[0]).ToLowerInvariant() -in @("gold","xauusd"))
    if ($IsGold -and (Get-V3RouteMode) -eq "PRODUCTION_V3") {
        Invoke-V3 (@($Command) + $Rest)
        exit $script:AlphaDeskLastExitCode
    }
}

Invoke-V2 $AlphaArgs
exit $script:AlphaDeskLastExitCode
