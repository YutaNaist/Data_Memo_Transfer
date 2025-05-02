import subprocess
import sys
import os

try:
    import colorama
    from colorama import Fore, Style
except ImportError:
    print("colorama をインストールしてください: pip install colorama")
    sys.exit(1)

colorama.init()


def colorize(line: str) -> str:
    if "ERROR" in line or "failed" in line.lower():
        return Fore.RED + line + Style.RESET_ALL
    elif "WARNING" in line:
        return Fore.YELLOW + line + Style.RESET_ALL
    elif "INFO" in line:
        return Fore.WHITE + line + Style.RESET_ALL
    elif "DEBUG" in line:
        return Fore.CYAN + line + Style.RESET_ALL
    return line


def main():
    if "pyinstaller" in sys.argv[1]:
        pyinstallerPath = sys.argv[1]
        pyinstallerArgs = sys.argv[2:]
    else:
        pyinstallerPath = "pyinstaller"
        pyinstallerArgs = sys.argv[1:]

    if not os.path.isfile(pyinstallerPath):
        print(f"指定された PyInstaller のパスが見つかりません: {pyinstallerPath}")
        sys.exit(1)

    cmd = [pyinstallerPath] + pyinstallerArgs
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    for line in proc.stdout:
        print(colorize(line.strip()))

    proc.wait()
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
