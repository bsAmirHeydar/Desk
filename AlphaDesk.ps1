param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)
$ErrorActionPreference = "Stop"
$Repo = $PSScriptRoot
$P10Tool = Join-Path $Repo "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN\tools\alpha_desk.py"
if (-not (Test-Path -LiteralPath $P10Tool)) { throw "Alpha Desk V3 P10 canonical runtime is not installed." }
$OldPyIo=$env:PYTHONIOENCODING;$OldPyUtf8=$env:PYTHONUTF8;$OldConsoleEncoding=[Console]::OutputEncoding
try {
    $Utf8=New-Object System.Text.UTF8Encoding($false);[Console]::OutputEncoding=$Utf8;$env:PYTHONIOENCODING="utf-8";$env:PYTHONUTF8="1"
    if (-not $AlphaArgs -or $AlphaArgs.Count -eq 0) { & python $P10Tool --repo-root $Repo help }
    else { & python $P10Tool --repo-root $Repo @AlphaArgs }
    $Code=$LASTEXITCODE
} finally {
    [Console]::OutputEncoding=$OldConsoleEncoding
    if ($null -eq $OldPyIo) { Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue } else { $env:PYTHONIOENCODING=$OldPyIo }
    if ($null -eq $OldPyUtf8) { Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue } else { $env:PYTHONUTF8=$OldPyUtf8 }
}
exit $Code
