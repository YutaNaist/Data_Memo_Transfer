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

@REM powershell -ExecutionPolicy Bypass -File "%~dp0build_client.ps1"
@REM %USERPROFILE%\miniconda3\envs\data-memo-transfer-PyQt5\python.exe -m PyInstaller Data_Memo_transfer.py -F -w --add-data "icons;icons" --add-data "forms;forms" --add-data "settings;settings" --distpath dist --workpath build --specpath .
%USERPROFILE%\miniconda3\envs\data-memo-transfer-PyQt5\python.exe build_client.py

pause
