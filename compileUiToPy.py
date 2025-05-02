import os
import subprocess
import filecmp
import shutil

# 変換元・先・バックアップディレクトリ
sourceDir = "./forms"
targetDir = "./views"
backupDir = "./views_backup"
condaEnv = "data-memo-transfer-PyQt5"

userProfile = str(os.environ.get("USERPROFILE"))
condaPath = os.path.abspath(os.path.join(userProfile, f"miniconda3/envs/{condaEnv}"))
# condaLibPath = os.path.abspath(os.path.join(condaPath, "Library/bin"))
pyuicPath = os.path.abspath(os.path.join(condaPath, "Scripts/pyuic5.exe"))
# pythonPath = os.path.abspath(os.path.join(condaPath, "python.exe"))
# os.environ["PATH"] = f"{condaLibPath};{os.environ['PATH']}"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def check_pyuic5_installed():
    try:
        subprocess.run(
            [pyuicPath, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print(
            "pyuic5 がインストールされていません。Python 環境にインストールしてください。"
        )
        exit(1)


def convert_ui_to_py(ui_path, py_path_tmp):
    print(f"変換中: {ui_path} -> {py_path_tmp}")
    subprocess.run(["pyuic5", "-x", ui_path, "-o", py_path_tmp], check=True)


def merge_files(original, new, output):
    with open(original, encoding="utf-8") as f1, open(new, encoding="utf-8") as f2:
        original_lines = f1.readlines()
        new_lines = f2.readlines()

    merged_lines = []
    for line in new_lines:
        if line in original_lines:
            merged_lines.append(line)
        else:
            merged_lines.append(line)  # 必要ならここでマージルールを変更

    with open(output, "w", encoding="utf-8") as fout:
        fout.writelines(merged_lines)

    print(f"マージ完了: {output}")
    os.remove(original)


def compileUiToPy():
    check_pyuic5_installed()
    ensure_dir(targetDir)
    ensure_dir(backupDir)

    for filename in os.listdir(sourceDir):
        if filename.endswith(".ui"):
            ui_file = os.path.join(sourceDir, filename)
            base_name = os.path.splitext(filename)[0]
            py_file = os.path.join(targetDir, base_name + ".py")
            backup_file = os.path.join(targetDir, base_name + "_tmp.py")

            convert_ui_to_py(ui_file, backup_file)

            if os.path.exists(py_file):
                merge_files(backup_file, py_file, py_file)
            else:
                shutil.move(backup_file, py_file)
                print(f"生成完了: {py_file}")

    print("すべての .ui ファイルが変換され、マージされました。")


if __name__ == "__main__":
    compileUiToPy()
