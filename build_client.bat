@echo off
@REM setlocal enabledelayedexpansion
@REM @REM .\compileUiToPy.bat

@REM pyinstaller.exe Data_Memo_transfer.py -F -w
@REM mkdir .\dist\icons
@REM copy /y .\icons\*.png .\dist\icons\
@REM mkdir .\dist\forms
@REM copy /y .\forms\*.ui .\dist\forms\
@REM mkdir .\dist\settings
@REM copy /y .\settings\*.json .\dist\settings\
@REM echo "Succeed to build"
@REM pause 60

powershell -ExecutionPolicy Bypass -File "build_client.ps1"

pause
