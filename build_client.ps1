
# PowerShell script to build multiple versions using JSON configuration
$conditionFile = ".\buildConfig\build_client_config.json"
if (-Not (Test-Path $conditionFile)) {
    Write-Error "JSON file '$conditionFile' not found!"
    exit 1
}
$buildConditions = Get-Content -Path $conditionFile | ConvertFrom-Json

# Loop through each build condition
foreach ($condition in $buildConditions) {
    $versionName = $condition.version_name
    $globalVariableFile = $condition.global_variable_file

    Write-Host "`nStarting build for: $versionName" -ForegroundColor Cyan
    if (Test-Path $globalVariableFile) {
        Copy-Item $globalVariableFile global_variable.py -Force
    }
    else {
        Write-Error "Source file '$globalVariableFile' not found!"
        continue
    }
    pyinstaller.exe .\Data_Memo_Transfer.py -F -w
    Copy-Item .\settings\ .\dist\settings\ -Recurse -Force
    Copy-Item .\icons\ .\dist\icons\ -Recurse -Force
    Copy-Item .\forms\ .\dist\forms\ -Recurse -Force

    $outputDistFolder = ".\Data_Memo_Transfer_$versionName"
    if (Test-Path ".\dist") {
        if (Test-Path $outputDistFolder) {
            Remove-Item -Recurse -Force $outputDistFolder
        }
        Rename-Item -Path ".\dist" -NewName $outputDistFolder
    }
    else {
        Write-Error "No 'dist' folder found after build!"
        continue
    }
    $outputBuildFolder = ".\Build_Data_Memo_Transfer_$versionName"
    if (Test-Path ".\build") {
        if (Test-Path $outputBuildFolder) {
            Remove-Item -Recurse -Force $outputBuildFolder
        }
        Rename-Item -Path ".\build" -NewName $outputBuildFolder
    }
    else {
        Write-Error "No 'build' folder found after build!"
        continue
    }
    Write-Host "Build completed for: $versionName" -ForegroundColor Green
}

Write-Host "`nAll builds completed successfully!" -ForegroundColor Magenta