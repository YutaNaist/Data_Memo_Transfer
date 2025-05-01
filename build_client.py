import os
import shutil
import subprocess
import json
from pathlib import Path
from colorama import Fore, Style

# 設定
conda_env = "data-memo-transfer-PyQt5"
user_profile = os.environ.get("USERPROFILE")
conda_path = Path(user_profile) / "miniconda3" / "envs" / conda_env
conda_lib_path = conda_path / "Library" / "bin"
pyinstaller_path = conda_path / "Scripts" / "pyinstaller.exe"
python_path = conda_path / "python.exe"
os.environ["PATH"] = f"{conda_lib_path};{os.environ['PATH']}"

excluded_modules = [
    "tkinter",
    "unittest",
    "pydoc",
    "doctest",
    "test",
    "distutils",
    "setuptools",
    "pkg_resources",
    "turtle",
    "venv",
    "wsgiref",
    "pip",
    "wheel",
    "pytest",
    "colorama",
]

condition_file = Path("buildConfig/build_client_config.json")
is_debug_mode = False
base_dir = Path(__file__).resolve().parent
os.chdir(base_dir)


def run_pyinstaller(py_path, script_path, args):
    cmd = [str(py_path), "colorized_pyinstaller.py", str(script_path)] + args
    subprocess.run(cmd, check=True)


def print_color(text, color):
    print(color + text + Style.RESET_ALL)


if not condition_file.exists():
    print_color(f"Error: JSON file '{condition_file}' not found!", Fore.RED)
    exit(1)

with open(condition_file, encoding="utf-8") as f:
    build_conditions = json.load(f)

print_color(f"PyInstaller Path: {pyinstaller_path}", Fore.CYAN)
print_color("Start to build Data_Memo_Transfer.exe", Fore.CYAN)

# 古いBuildExeを削除
build_exe_dir = Path("BuildExe")
if build_exe_dir.exists():
    print_color("BuildExe folder already exists. Deleting it...", Fore.YELLOW)
    shutil.rmtree(build_exe_dir)

for condition in build_conditions:
    version_name = condition["version_name"]
    global_variable_file = Path(condition["global_variable_file"])

    print_color(f"Starting build: {version_name}", Fore.CYAN)

    if global_variable_file.exists():
        shutil.copy(global_variable_file, "global_variable.py")
    else:
        print_color(f"Error: Source file '{global_variable_file}' not found!", Fore.RED)
        continue

    pyinstaller_args = [
        "--paths",
        str(conda_lib_path),
        "Data_Memo_Transfer.py",
        "--onefile",
        # "--add-data",
        # "icons;icons",
        # "--add-data",
        # "forms;forms",
        # "--add-data",
        # "settings;settings",
    ]
    if not is_debug_mode:
        pyinstaller_args.append("--windowed")
    for module in excluded_modules:
        pyinstaller_args += ["--exclude-module", module]

    run_pyinstaller(python_path, pyinstaller_path, pyinstaller_args)

    # リソースのコピー
    for folder in ["settings", "icons", "forms"]:
        shutil.copytree(folder, Path("dist") / folder, dirs_exist_ok=True)
    (Path("dist") / "Logs").mkdir(exist_ok=True)

    Path("global_variable.py").unlink(missing_ok=True)
    Path("Data_Memo_Transfer.spec").unlink(missing_ok=True)

    output_dist_folder = f"Data_Memo_Transfer_{version_name}"
    output_build_folder = f"Build_Data_Memo_Transfer_{version_name}"

    build_exe_dir.mkdir(exist_ok=True)

    if Path("dist").exists():
        if (build_exe_dir / output_dist_folder).exists():
            shutil.rmtree(build_exe_dir / output_dist_folder)
        shutil.move("dist", build_exe_dir / output_dist_folder)
    else:
        print_color("Error: No 'dist' folder found after build!", Fore.RED)
        continue

    if Path("build").exists():
        if (build_exe_dir / output_build_folder).exists():
            shutil.rmtree(build_exe_dir / output_build_folder)
        shutil.move("build", build_exe_dir / output_build_folder)
    else:
        print_color("Error: No 'build' folder found after build!", Fore.RED)
        continue

    print_color(f"Build completed for: {version_name}", Fore.GREEN)

print_color("\nAll builds completed successfully!", Fore.CYAN)
