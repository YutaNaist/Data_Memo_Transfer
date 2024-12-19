@echo off
setlocal enabledelayedexpansion
@REM .\compileUiToPy.bat

REM Data_Memo_transfer.py -F
pyinstaller.exe Data_Memo_transfer.py -F -w
@REM pyinstaller.exe Data_Memo_transfer.py -F
mkdir .\dist\icons
copy /y .\icons\*.png .\dist\icons\
mkdir .\dist\forms
copy /y .\forms\*.ui .\dist\forms\
mkdir .\dist\settings
copy /y .\settings\*.json .\dist\settings\
echo "Succeed to build"
pause 60