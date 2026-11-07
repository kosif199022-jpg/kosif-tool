# ASCII-only on purpose: Windows PowerShell 5.1 reads BOM-less scripts as ANSI, so any non-ASCII
# character (Arabic, em-dash, emoji) breaks parsing. Keep it that way (tests/test_dragon_montage_doctor.py).
# Dragon Montage - install the tools the protocol needs (Windows, PowerShell).
# The owner runs this; Claude never does. Idempotent: it asks dm_doctor.py what is
# MISSING and installs only that.
#
#   powershell -ExecutionPolicy Bypass -File .claude\skills\kosif-dragon-montage\scripts\install_tools.ps1 [-Tier required|recommended|all] [-Yes] [-DryRun]
#
# Model files (e.g. the YuNet face model) come as `dm_doctor.py fetch <id>` lines in the plan
# (sha256-checked, saved to the skill's git-ignored models/ folder).
# Python libraries go into <repo>\.venv (created if absent). Run the montage with
# <repo>\.venv\Scripts\python.exe afterwards.
param(
  [ValidateSet("required", "recommended", "all")][string]$Tier = "recommended",
  [switch]$Yes,
  [switch]$DryRun
)
$ErrorActionPreference = "Continue"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Here "..\..\..\..")).Path
Set-Location $Root

function Have($name) { return [bool](Get-Command $name -ErrorAction SilentlyContinue) }
function Refresh-Path {
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}

# 1) Python itself (needed to run the doctor).
if (-not (Have "py") -and -not (Have "python")) {
  Write-Host "== Python not found - installing it"
  if (-not $DryRun) {
    if (Have "winget") { winget install -e --id Python.Python.3.13 --accept-source-agreements --accept-package-agreements }
    elseif (Have "choco") { choco install -y python313 }
    else { Write-Host "Download Python from https://www.python.org/downloads/ and tick Add to PATH"; exit 1 }
    Refresh-Path
  }
}
$Boot = if (Have "py") { "py" } else { "python" }

# 2) A venv for the Python libraries.
$Venv = if ($env:KOSIF_VENV) { $env:KOSIF_VENV } else { Join-Path $Root ".venv" }
$Py = Join-Path $Venv "Scripts\python.exe"
if (-not (Test-Path $Py)) {
  Write-Host "== Creating venv in $Venv"
  if (-not $DryRun) { & $Boot -m venv $Venv }
}
if (-not (Test-Path $Py)) { $Py = (Get-Command $Boot).Source }

# 3) Ask the doctor for the exact plan (missing only) and run it line by line.
$Plan = & $Py (Join-Path $Here "dm_doctor.py") install-plan --os windows --tier $Tier --python $Py
$Plan | ForEach-Object { Write-Host $_ }
$Cmds = @($Plan | Where-Object { $_ -and -not $_.TrimStart().StartsWith("#") })
if ($Cmds.Count -eq 0) { Write-Host "[OK] Nothing is missing."; exit 0 }
if ($DryRun) { exit 0 }
if (-not $Yes) {
  $ans = Read-Host "Run these commands? [y/N]"
  if ($ans -notmatch '^(y|yes)$') { Write-Host "Cancelled."; exit 0 }
}
$HasWinget = Have "winget"
foreach ($line in $Cmds) {
  $cmd = $line
  if ($cmd -like "winget install*") {
    if (-not $HasWinget) { Write-Host "[WARN] winget not found: use the choco line from the plan"; continue }
    $cmd = "$cmd --accept-source-agreements --accept-package-agreements"
  }
  Write-Host "-> $cmd"
  try { Invoke-Expression $cmd } catch { Write-Host "[WARN] failed: $cmd (continuing with the rest)" }
  if ($cmd -like "winget install*") { Refresh-Path }
}

# 4) Verify.
& $Py (Join-Path $Here "dm_doctor.py") doctor --tier $Tier
