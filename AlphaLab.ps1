param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)
$ErrorActionPreference = "Stop"
$Vault = Join-Path $PSScriptRoot "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL"
$Research = Join-Path $Vault "RUNTIME\Unified Research Interface\tools\alpha_research.py"

if (-not $AlphaArgs -or $AlphaArgs.Count -eq 0) {
    Write-Host "Alpha Lab canonical research interface"
    Write-Host "Usage: .\AlphaLab.ps1 run NASDAQ100"
    Write-Host "Advanced: .\AlphaLab.ps1 research --subject NASDAQ100 --request '...' [--mode LIVE|SHADOW|HISTORICAL] [--output EXPLORER]"
    Write-Host "Run memory: .\AlphaLab.ps1 run-status"
    Write-Host "Operations: .\AlphaLab_Commission.ps1 <command>"
    exit 0
}

if ($AlphaArgs[0].ToLowerInvariant() -eq "run") {
    if ($AlphaArgs.Count -lt 2) { throw "Usage: .\AlphaLab.ps1 run <SUBJECT>" }
    $Subject = $AlphaArgs[1]
    $Req = "Analyze the current market comprehensively. Determine the current fundamental direction, active force, consumption, remaining pressure, persistence, reversal conditions, dominant drivers, meaningful contradictions, key uncertainty, and next review."
    & python $Research --vault-root $Vault run --subject $Subject --request $Req --mode LIVE --horizon DAILY_OPEN_TO_CLOSE --depth DEEP --output EXPLORER --locale fa-IR
    exit $LASTEXITCODE
}


if ($AlphaArgs[0].ToLowerInvariant() -eq "run-status") {
    & python $Research --vault-root $Vault run-status
    exit $LASTEXITCODE
}

if ($AlphaArgs[0].ToLowerInvariant() -eq "research") {
    $Rest = @()
    if ($AlphaArgs.Count -gt 1) { $Rest = $AlphaArgs[1..($AlphaArgs.Count-1)] }
    & python $Research --vault-root $Vault run @Rest
    exit $LASTEXITCODE
}

if ($AlphaArgs[0].ToLowerInvariant() -eq "compile") {
    $Rest = @()
    if ($AlphaArgs.Count -gt 1) { $Rest = $AlphaArgs[1..($AlphaArgs.Count-1)] }
    & python $Research --vault-root $Vault compile @Rest
    exit $LASTEXITCODE
}

# Thin compatibility redirect for the old: AlphaLab.ps1 <INSTRUMENT> <LIVE|SHADOW|HISTORICAL> [timestamp]
$LegacySubject = $AlphaArgs[0]
$LegacyMode = if ($AlphaArgs.Count -gt 1) { $AlphaArgs[1].ToUpperInvariant() } else { "LIVE" }
if ($LegacyMode -in @("LIVE","SHADOW","HISTORICAL")) {
    Write-Warning "Deprecated AlphaLab.ps1 legacy syntax redirected through the canonical Unified Research Interface."
    if ($LegacySubject.ToUpperInvariant() -eq "DAILY6") {
        throw "Legacy DAILY6 human research syntax is retired. Use AlphaLab_Commission.ps1 tf3-cycle for scheduled universe operations, or issue explicit multi-market research through the canonical interface."
    }
    $Req = "Analyze the current market state, direction, remaining pressure, persistence, reversal conditions, and next review time."
    $Cmd = @('--vault-root',$Vault,'run','--subject',$LegacySubject,'--request',$Req,'--mode',$LegacyMode,'--output','EXPLORER')
    if ($LegacyMode -eq 'HISTORICAL') {
        if ($AlphaArgs.Count -lt 3) { throw "HISTORICAL requires an explicit timezone-aware timestamp." }
        $Cmd += @('--as-of',$AlphaArgs[2])
    }
    & python $Research @Cmd
    exit $LASTEXITCODE
}

throw "Unknown research command. Use '.\AlphaLab.ps1 research ...' or '.\AlphaLab_Commission.ps1 ...' for operations."
