param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AlphaArgs
)
$ErrorActionPreference = "Stop"
$Vault = Join-Path $PSScriptRoot "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL"
$Tool = Join-Path $Vault "RUNTIME\Production Commissioning\tools\alpha_launch.py"
& python $Tool --vault-root $Vault @AlphaArgs
exit $LASTEXITCODE
