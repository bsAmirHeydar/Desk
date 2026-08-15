param(
    [ValidateSet("install","status","remove")][string]$Action = "status",
    [string]$RepoRoot,
    [string]$DataRoot,
    [string]$PythonExe = "python",
    [int]$IntervalMinutes = 5
)
$ErrorActionPreference = "Stop"
$TaskName = "AlphaDesk-V2-P08-ContinuousForward"
if ($Action -eq "status") {
    $t = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if (-not $t) { Write-Output '{"status":"NOT_INSTALLED","task_name":"AlphaDesk-V2-P08-ContinuousForward"}'; exit 0 }
    $i = Get-ScheduledTaskInfo -TaskName $TaskName
    [pscustomobject]@{status="PASS";task_name=$TaskName;state=$t.State.ToString();last_run_time=$i.LastRunTime;last_task_result=$i.LastTaskResult;next_run_time=$i.NextRunTime} | ConvertTo-Json -Compress
    exit 0
}
if ($Action -eq "remove") {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output '{"status":"PASS","action":"REMOVED","task_name":"AlphaDesk-V2-P08-ContinuousForward"}'
    exit 0
}
if ([string]::IsNullOrWhiteSpace($RepoRoot) -or [string]::IsNullOrWhiteSpace($DataRoot)) { throw "RepoRoot and DataRoot are required for install" }
if ($IntervalMinutes -lt 1) { throw "IntervalMinutes must be >= 1" }
$Wrapper = Join-Path $RepoRoot "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL\NEXT_VERSION\AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS\tools\p08_cycle_wrapper.ps1"
if (-not (Test-Path -LiteralPath $Wrapper)) { throw "P08 cycle wrapper not found: $Wrapper" }
$Arg = "-NoProfile -ExecutionPolicy Bypass -File `"$Wrapper`" -RepoRoot `"$RepoRoot`" -DataRoot `"$DataRoot`" -PythonExe `"$PythonExe`""
$act = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $Arg
$trg = New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(1)) -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) -RepetitionDuration (New-TimeSpan -Days 3650)
$set = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $TaskName -Action $act -Trigger $trg -Settings $set -Principal $principal -Force | Out-Null
Write-Output ([pscustomobject]@{status="PASS";action="INSTALLED_OR_REFRESHED";task_name=$TaskName;interval_minutes=$IntervalMinutes;repo_root=$RepoRoot;data_root=$DataRoot} | ConvertTo-Json -Compress)
