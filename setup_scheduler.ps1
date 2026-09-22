# ==========================================================
# Windows Task Scheduler Setup for Earthitects Lead Engine
# Schedules run_engine.py to run daily at 8:00 AM IST at zero cost
# ==========================================================

$TaskName = "EarthitectsLeadEngine"
$ScriptDir = $PSScriptRoot
$PythonPath = "$ScriptDir\.venv\Scripts\python.exe"
$RunnerPath = "$ScriptDir\run_engine.py"

Write-Host "Setting up automated daily schedule for Earthitects Lead Engine..." -ForegroundColor Cyan

# Check if python exists in venv
if (-not (Test-Path $PythonPath)) {
    Write-Host "Error: Virtual environment python not found at $PythonPath" -ForegroundColor Red
    exit 1
}

# Action to execute
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$RunnerPath`" --send" -WorkingDirectory $ScriptDir

# Trigger daily at 08:00 AM
$Trigger = New-ScheduledTaskTrigger -Daily -At "08:00AM"

# Settings: run only when network is available
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RunOnlyIfNetworkAvailable -StartWhenAvailable

# Register or update task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Daily Earthitects UHNW Liquidity & ICP Lead Prospecting Engine" -Force

Write-Host "[OK] Task '$TaskName' registered successfully!" -ForegroundColor Green
Write-Host "[i] It will run every morning at 8:00 AM IST and email faraz.z@earthitects.com" -ForegroundColor Yellow
