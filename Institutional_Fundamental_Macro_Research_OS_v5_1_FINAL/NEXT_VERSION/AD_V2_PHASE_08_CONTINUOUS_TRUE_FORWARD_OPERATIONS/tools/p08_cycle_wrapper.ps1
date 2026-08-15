param(
    [Parameter(Mandatory=$true)][string]$RepoRoot,
    [Parameter(Mandatory=$true)][string]$DataRoot,
    [string]$PythonExe = "python"
)
$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"
$Tool = Join-Path $RepoRoot "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS\tools\p08_cycle.py"
& $PythonExe $Tool --data-root $DataRoot
exit $LASTEXITCODE
