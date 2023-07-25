@echo off
setlocal enabledelayedexpansion
@REM .\compileUiToPy.bat

set url="http://192.168.150.10:5462/request"
set save="Z:/"
set share="D:/Share/NR-301/"

set fileContents=URL_DIAMOND=%url%
echo %fileContents% > global_variable.py
set fileContents=SAVE_DIRECTORY=%save%
echo %fileContents% >> global_variable.py
set fileContents=SHARE_DIRECTORY_IN_STORAGE=%share%
echo %fileContents% >> global_variable.py

pyinstaller.exe Data_Memo_transfer.py -F -w
@REM pyinstaller.exe Data_Memo_transfer.py -w
mkdir /y .\dist\icons
copy /y .\icons\*.png .\dist\icons\

@REM URL_DIAMOND = "http://192.168.0.10:5462/request"
@REM SAVE_DIRECTORY = "Z:/"
@REM SHARE_DIRECTORY_IN_STORAGE = "D:/Share/NR-301/"
