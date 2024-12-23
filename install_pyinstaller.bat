REM To install with this script, MinGW and python with pip is required before running bat file.
git clone https://github.com/pyinstaller/pyinstaller.git
REM winget install MartinStorsjo.LLVM-MinGW.MSVCRT
cd .\pyinstaller\bootloader\
python .\waf distclean all
cd ..
pip install wheel
pip install .