<#
.SYNOPSIS
    Build 贪吃蛇 v0.1.0 for Windows into dist\贪吃蛇 v0.1.0\

.DESCRIPTION
    Creates a local virtual environment, installs PyInstaller, bundles the PWA
    folder (page + manifest + icons) and the launcher, and produces a portable
    folder whose 贪吃蛇 v0.1.0.exe opens the game in an Edge/Chrome app window.
    No admin rights, no installer: unzip anywhere and double-click.

    A folder (--onedir) rather than a single file on purpose: a onefile build
    unpacks ~30 MB to %TEMP% on every start, which is slower and is blocked by
    locked-down machines.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File build.ps1
    powershell -ExecutionPolicy Bypass -File build.ps1 -SkipVenv
#>
[CmdletBinding()]
param(
    [string]$Python = 'python',
    [switch]$SkipVenv
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $here '..\..')).Path
$mobile = Join-Path $repo 'app\mobile'
$icon = Join-Path $repo 'app\icons\snake.ico'
$versionFile = Join-Path $here 'version.txt'
$finalName = '贪吃蛇 v0.1.0'

if (-not (Test-Path (Join-Path $mobile 'index.html'))) {
    throw "mobile app not built yet — run: python app\mobile\build.py"
}
if (-not (Test-Path $icon)) { throw "icon not found: $icon" }

# 1. environment
$py = $Python
if (-not $SkipVenv) {
    $venv = Join-Path $here '.venv'
    if (-not (Test-Path $venv)) { & $Python -m venv $venv }
    $py = Join-Path $venv 'Scripts\python.exe'
}
& $py -m pip install --disable-pip-version-check -q -r (Join-Path $here 'requirements.txt')
Write-Host "[1/3] environment ready ($py)"

# 2. freeze: the whole PWA folder travels inside the app
& $py -m PyInstaller --noconfirm --clean --onedir --windowed `
    --name 'Snake' `
    --icon $icon `
    --version-file $versionFile `
    --add-data "$mobile;mobile" `
    (Join-Path $here 'main.py')
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }
Write-Host '[2/3] frozen'

# 3. product name + a quick check of the bundle
$outDir = Join-Path $here "dist\$finalName"
if (Test-Path $outDir) { Remove-Item $outDir -Recurse -Force }
Move-Item (Join-Path $here 'dist\Snake') $outDir -Force
Rename-Item (Join-Path $outDir 'Snake.exe') "$finalName.exe" -Force
Write-Host "[3/3] built: $outDir\$finalName.exe"
& (Join-Path $outDir "$finalName.exe") --selftest
