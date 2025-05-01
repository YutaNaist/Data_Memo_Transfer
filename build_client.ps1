$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
Set-Location $CurrentDir

$condaPath = Join-Path $env:USERPROFILE "miniconda3\envs\data-memo-transfer-PyQt5"
$condaLibPath = Join-Path $condaPath "Library\bin"
$pyinstallerPath = Join-Path $condaPath "Scripts\pyinstaller.exe"
$pythonPath = Join-Path $condaPath "python.exe"
$env:PATH = "$condaLibPath;$env:PATH"
$pyinstallerExcludedModules = @(
    "tkinter",
    "unittest",
    "pydoc",
    "doctest",
    "test",
    "distutils",
    "setuptools",
    "pkg_resources",
    "turtle",
    "venv",
    "wsgiref",
    "pip",
    "wheel",
    "pytest",
    "colorama"
)

$conditionFile = "buildConfig\build_client_config.json"

$isDebugMode = 0
# PowerShell script to build multiple versions using JSON configuration

if (-Not (Test-Path $conditionFile)) {
    Write-Host "Error: JSON file '$conditionFile' not found!" -ForegroundColor Red
    exit 1
}
$buildConditions = Get-Content -Path $conditionFile | ConvertFrom-Json
if ( -Not ( 0 -eq $isDebugMode ) ) {
    Write-Host "Debug mode is: Activated" -ForegroundColor Cyan
}

# Loop through each build condition

Write-Host "PyInstaller Path: $pyinstallerPath" -ForegroundColor Cyan

Write-Host "Start to build Data_Memo_Transfer.exe" -ForegroundColor Cyan
if (Test-Path .\BuildExe) {
    Write-Host "BuildExe folder already exists. Deleting it..." -ForegroundColor Yellow
    Remove-Item .\BuildExe -Recurse -Force
}
foreach ($condition in $buildConditions) {
    $versionName = $condition.version_name
    $globalVariableFile = $condition.global_variable_file

    Write-Host "Starting build: $versionName" -ForegroundColor Cyan
    if (Test-Path $globalVariableFile) {
        Copy-Item $globalVariableFile global_variable.py -Force
    }
    else {
        Write-Host "Error: Source file '$globalVariableFile' not found!" -ForegroundColor Red
        continue
    }
    $pyinstallerArgs = @(
        "--paths", $condaLibPath,
        "Data_Memo_Transfer.py",
        "--onefile"
    )
    if ( 0 -eq $isDebugMode ) {
        $pyinstallerArgs += "--windowed"
    }
    foreach ($module in $pyinstallerExcludedModules) {
        $pyinstallerArgs += "--exclude-module"
        $pyinstallerArgs += $module
    }
    & $pythonPath "colorized_pyinstaller.py" $pyinstallerPath @pyinstallerArgs

    Copy-Item .\settings\ .\dist\settings\ -Recurse -Force
    Copy-Item .\icons\ .\dist\icons\ -Recurse -Force
    Copy-Item .\forms\ .\dist\forms\ -Recurse -Force
    # Copy-Item C:\mingw64\bin\libmcfgthread-1.dll .\dist\libmcfgthread-1.dll -Force
    New-Item .\dist\Logs -ItemType Directory -Force > $null
    Remove-Item global_variable.py -Force
    Remove-Item Data_Memo_Transfer.spec -Force
    Write-Host "Finish Build: $versionName" -ForegroundColor Cyan

    $outputFolder = "BuildExe\"
    if (-Not (Test-Path $outputFolder)) {
        Write-Host "Create Build Folder" -ForegroundColor Cyan
        New-Item $outputFolder -ItemType Directory -Force > $null
    }
    Write-Host "Move Build and Dist Folder: $versionName" -ForegroundColor Cyan

    $outputDistFolder = "Data_Memo_Transfer_$versionName"
    if (Test-Path "dist") {
        if (Test-Path $outputFolder$outputDistFolder) {
            Remove-Item -Recurse -Force $outputFolder$outputDistFolder
        }
        Rename-Item -Path "dist" -NewName $outputDistFolder
        Move-Item -Path $outputDistFolder -Destination $outputFolder$outputDistFolder -Force
    }
    else {
        Write-Host "Error: No 'dist' folder found after build!" -ForegroundColor Red
        continue
    }
    $outputBuildFolder = "Build_Data_Memo_Transfer_$versionName"
    if (Test-Path ".\build") {
        if (Test-Path $outputFolder$outputBuildFolder) {
            Remove-Item -Recurse -Force $outputFolder$outputBuildFolder
        }
        Rename-Item -Path ".\build" -NewName $outputBuildFolder
        Move-Item -Path $outputBuildFolder -Destination $outputFolder$outputBuildFolder -Force
    }
    else {
        Write-Host "Error: No 'build' folder found after build!" -ForegroundColor Red
        continue
    }
    Write-Host "Build completed for: $versionName" -ForegroundColor Green
}
# Remove-Item -Force global_variable.py
Write-Host "`nAll builds completed successfully!" -ForegroundColor Cyan
