$isDebugMode = 0
# PowerShell script to build multiple versions using JSON configuration
$conditionFile = ".\buildConfig\build_client_config.json"
if (-Not (Test-Path $conditionFile)) {
    Write-Error "JSON file '$conditionFile' not found!"
    exit 1
}
$buildConditions = Get-Content -Path $conditionFile | ConvertFrom-Json
if ( -Not ( 0 -eq $isDebugMode ) ){
    Write-Host "`nDebug mode is: Activated" -ForegroundColor Cyan
}

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
    if ( 0 -eq $isDebugMode ){
        pyinstaller.exe .\Data_Memo_Transfer.py -F -w
    }
    else{pyinstaller.exe .\Data_Memo_Transfer.py -F
    }
    
    Copy-Item .\settings\ .\dist\settings\ -Recurse -Force
    Copy-Item .\icons\ .\dist\icons\ -Recurse -Force
    Copy-Item .\forms\ .\dist\forms\ -Recurse -Force
    Copy-Item C:\mingw64\bin\libmcfgthread-1.dll .\dist\libmcfgthread-1.dll -Force
    New-Item .\dist\Log -ItemType Directory -Force > $null

    if (-Not (Test-Path $outputFolder)) {
    $outputFolder = ".\BuildExe\"
        New-Item $outputFolder -ItemType Directory -Force > $null
    }

    $outputDistFolder = "Data_Memo_Transfer_$versionName"
    if (Test-Path ".\dist") {
        if (Test-Path $outputFolder$outputDistFolder) {
            Remove-Item -Recurse -Force $outputFolder$outputDistFolder
        }
        Rename-Item -Path ".\dist" -NewName $outputDistFolder
        Move-Item -Path $outputDistFolder -Destination $outputFolder$outputDistFolder -Force
    }
    else {
        Write-Error "No 'dist' folder found after build!"
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
        Write-Error "No 'build' folder found after build!"
        continue
    }
    Write-Host "Build completed for: $versionName" -ForegroundColor Green
}

Write-Host "`nAll builds completed successfully!" -ForegroundColor Magenta
