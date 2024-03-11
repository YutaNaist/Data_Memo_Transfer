@echo off
setlocal enabledelayedexpansion
@REM .\compileUiToPy.bat

pyinstaller.exe Data_Memo_transfer.py -F -w
@REM pyinstaller.exe Data_Memo_transfer.py -F
mkdir /y .\dist\icons
copy /y .\icons\*.png .\dist\icons\
