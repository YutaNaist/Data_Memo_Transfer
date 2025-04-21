@echo off
echo "Start initialize for diamond system %0"
pause
if exist "%USERPROFILE%\miniconda3" (
    echo "Skip install miniconda"
) else (
    echo "Install the miniconda latest version on %USERPROFILE%"
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o "%USERPROFILE%\miniconda.exe"
    start /wait "" "%USERPROFILE%\miniconda.exe" /S
    del "%USERPROFILE%\miniconda.exe"
    "%USERPROFILE%\miniconda3\Scripts\conda.exe" init
    echo "Finish install ing miniconda. restart this bat file again"
    call %0
    exit
)

"%USERPROFILE%\miniconda3\Scripts\conda.exe" init

if exist "%USERPROFILE%\miniconda3\envs\diamond" (
    echo "Skip create conda environment diamond: already exist"
) else (
    echo "Create environment for diamond from yaml file."
    @REM "%USERPROFILE%\miniconda3\condabin\conda.bat" create -n diamond python=3.11 -y
    "%USERPROFILE%\miniconda3\condabin\conda.bat" env create -f "%CD%\environment_diamond.yml"
)


@REM REM To install with this script, MinGW and python with pip is required before running bat file.
@REM git clone https://github.com/pyinstaller/pyinstaller.git
@REM REM winget install MartinStorsjo.LLVM-MinGW.MSVCRT
@REM cd .\pyinstaller\bootloader\
@REM python .\waf distclean all
@REM cd ..
@REM @REM pip install wheel
@REM pip install .
@REM cd ..
@REM rm -rf .\pyinstaller
