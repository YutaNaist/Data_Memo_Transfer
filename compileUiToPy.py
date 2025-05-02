import os
import subprocess
import filecmp
import shutil

# 変換元・先・バックアップディレクトリ
source_dir = "./forms"
target_dir = "./views"
backup_dir = "./views_backup"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def check_pyuic5_installed():
    try:
        subprocess.run(
            ["pyuic5", "--version"],
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
    ensure_dir(target_dir)
    ensure_dir(backup_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".ui"):
            ui_file = os.path.join(source_dir, filename)
            base_name = os.path.splitext(filename)[0]
            py_file = os.path.join(target_dir, base_name + ".py")
            backup_file = os.path.join(target_dir, base_name + "_tmp.py")

            convert_ui_to_py(ui_file, backup_file)

            if os.path.exists(py_file):
                merge_files(backup_file, py_file, py_file)
            else:
                shutil.move(backup_file, py_file)
                print(f"生成完了: {py_file}")

    print("すべての .ui ファイルが変換され、マージされました。")


if __name__ == "__main__":
    compileUiToPy()
