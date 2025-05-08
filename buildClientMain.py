import os
import shutil
import subprocess
import json

# from pathlib import Path
from colorama import Fore, Style
from TyMessageSender import TyMessageSender, MessageSenderException
from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from compileUiToPy import compileUiToPy
import zipfile

# 設定
isBuildLocalDebug = False  # True: ローカルデバッグ用、False: 本番ビルド用
isDisplayStd = False  # True: コンソール表示、False: GUIのみ

condaEnv = "data-memo-transfer-PyQt5"
userProfile = str(os.environ.get("USERPROFILE"))
condaPath = os.path.abspath(os.path.join(userProfile, f"miniconda3/envs/{condaEnv}"))
condaLibPath = os.path.abspath(os.path.join(condaPath, "Library/bin"))
pyinstallerPath = os.path.abspath(os.path.join(condaPath, "Scripts/pyinstaller.exe"))
pythonPath = os.path.abspath(os.path.join(condaPath, "python.exe"))
os.environ["PATH"] = f"{condaLibPath};{os.environ['PATH']}"

configFile = os.path.abspath("buildConfig/build_client_config.json")
urlProposalHandlerBase = "http://127.0.0.1:6427"
urlHttpsServerBase = "https://192.168.150.10:6426"

if isBuildLocalDebug:
    urlHttpsServerBase = "https://127.0.0.1:6426"
    configFile = os.path.abspath("buildConfig/build_client_config_dev.json")

doc = TyDocDataMemoTransfer()
doc.isBuild = True
messageSenderProposalHandler = TyMessageSender(urlProposalHandlerBase, doc)
messageSenderHttpsServer = TyMessageSender(urlHttpsServerBase, doc)

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
pyinstaller_args = [
    "--paths",
    str(condaLibPath),
    "Data_Memo_Transfer.py",
    "--onefile",
]
if not isDisplayStd:
    pyinstaller_args.append("--windowed")
for module in excluded_modules:
    pyinstaller_args += ["--exclude-module", module]


def registerProposal(experimentId: str, password: str):
    dummyProposal = createDummyProposal()
    dummyProposal["experiment_id"] = experimentId
    hashPassword = doc.makeHashFromString(password)
    dummyProposal["password"] = hashPassword
    url = urlProposalHandlerBase + f"/experiment_id/{experimentId}"
    jsonData = {
        "dict_proposal": dummyProposal,
    }
    try:
        response = messageSenderProposalHandler.sendMessage(url, jsonData, "POST")
        printColorized(
            f"Proposal registered successfully: {response['message']}", Fore.GREEN
        )
        return True
    except MessageSenderException as e:
        printColorized(f"Error: {e.message}: {e.status_code}", Fore.RED)
        return False


def upLoadFiles(
    version_name: str,
    experimentId: str,
    password: str,
    shareFolderInStorage: str,
    savedFolder: str,
    copyOriginal: str,
):
    doc.dictExperimentInformation["str_share_directory_in_storage"] = (
        shareFolderInStorage
    )
    doc.dictExperimentInformation["str_save_directory"] = savedFolder
    doc.dictExperimentInformation["dict_clipboard"]["experiment"][
        "title"
    ] = f"Data Memo Transfer {version_name}"
    doc.dictExperimentInformation["dict_clipboard"]["sample"][
        "name"
    ] = f"{version_name}"
    hashPassword = doc.makeHashFromString(password)
    try:
        messageSenderHttpsServer.sendRequestLogin(experimentId, hashPassword)
        messageSenderHttpsServer.sendRequestStartExperiment(experimentId, doc)
        # shutil.copytree(
        #     copyOriginal,
        #     os.path.join(shareFolderInStorage, os.path.basename(copyOriginal)),
        #     dirs_exist_ok=True,
        # )

        shutil.copy2(
            copyOriginal,
            os.path.join(shareFolderInStorage, os.path.basename(copyOriginal)),
        )
        messageSenderHttpsServer.sendRequestFinishExperiment(experimentId, doc)
        # messageSenderHttpsServer.sendRequestLogout(experimentId)
        return True
    except MessageSenderException as e:
        printColorized(f"Error: {e.message}: {e.status_code}", Fore.RED)
        return False
    except Exception as e:
        printColorized(f"Error: {e}", Fore.RED)
        return False


def createDummyProposal():
    return {
        "time_stamp": "2025/01/01 00:00:00",
        "user": {
            "address": "",
            "affiliation": "NAIST",
            "mail_address": "yuta.yamamoto@ms.naist.jp",
            "name": "Administrator",
            "phone_number": "",
        },
        "instrument": {"id": "NR-000", "name": "dummy"},
        "date": {"end": "2025/01/01 00:00:00", "start": "2025/01/01 00:00:00"},
        "arim": {
            "id": "",
            "is_arim": "0. アップロードなし",
            "is_uploaded": False,
        },
        "share": {
            "gmail": "",
            "is_share": "0. データ共有無し/USBで持ち帰り",
        },
        "is_remove": "",
        "supervisor": {"mail_address": "", "name": ""},
        "edit_url": "",
        "experiment_id": "",
        "is_enable": "Enable",
        "creators": [
            {
                "address": "",
                "affiliation": "NAIST",
                "mail_address": "yuta.yamamoto@ms.naist.jp",
                "name": "Administrator",
                "phone_number": "",
            }
        ],
        "password": "",
    }


def runPyinstaller(py_path, script_path, args):
    cmd = [str(py_path), "colorlizedPyinstaller.py", str(script_path)] + args
    subprocess.run(cmd, check=True)


def printColorized(text, color):
    print(color + text + Style.RESET_ALL)


def createGlobalVariableFile(configureJson):
    global_variable_file = os.path.abspath("global_variable.py")
    share_directory = configureJson["share_directory"]
    share_directory_folder_name = configureJson["folder_name"]
    share_directory_in_storage = os.path.abspath(
        os.path.join(share_directory, share_directory_folder_name)
    )
    url_diamond = configureJson["url_diamond"]
    save_directory = configureJson["save_directory"]
    listMeasurementMethods = configureJson["measurement_methods"]
    with open(global_variable_file, "w", encoding="utf-8") as f:
        f.write(f'SHARE_DIRECTORY_IN_STORAGE = "{share_directory_in_storage}"\n')
        f.write(f'URL_DIAMOND = "{url_diamond}"\n')
        f.write(f'SAVE_DIRECTORY = "{save_directory}"\n')
        f.write(f"LIST_MEASUREMENT_METHODS = {listMeasurementMethods}\n")


if __name__ == "__main__":
    printColorized("Start to build Data_Memo_Transfer.exe", Fore.CYAN)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    if not os.path.exists(configFile):
        printColorized(f"Error: JSON file '{configFile}' not found!", Fore.RED)
        exit(1)
    listBuildCondition = json.load(open(configFile, encoding="utf-8"))
    # print_color(f"PyInstaller Path: {pyinstallerPath}", Fore.CYAN)
    # 古いBuildExeを削除
    buildExeDir = os.path.abspath("BuildExe")
    if os.path.exists(buildExeDir):
        printColorized("BuildExe folder already exists. Deleting it...", Fore.YELLOW)
        shutil.rmtree(buildExeDir)
    printColorized("Compiling Ui files to Py files...", Fore.CYAN)
    compileUiToPy()

    for condition in listBuildCondition:
        version_name = condition["version_name"]
        printColorized(f"Starting build: {version_name}", Fore.CYAN)
        createGlobalVariableFile(condition)
        runPyinstaller(pythonPath, pyinstallerPath, pyinstaller_args)
        # リソースのコピー
        for folder in ["settings", "icons", "forms"]:
            shutil.copytree(
                folder,
                os.path.abspath(os.path.join("dist", folder)),
                dirs_exist_ok=True,
            )
        os.makedirs(os.path.abspath(os.path.join("dist", "Logs")), exist_ok=True)

        # Path("global_variable.py").unlink(missing_ok=True)
        # Path("Data_Memo_Transfer.spec").unlink(missing_ok=True)
        os.remove(os.path.abspath("global_variable.py"))
        os.remove(os.path.abspath("Data_Memo_Transfer.spec"))

        output_dist_folder = f"Data_Memo_Transfer_{version_name}"
        output_build_folder = f"Build_Data_Memo_Transfer_{version_name}"
        os.makedirs(buildExeDir, exist_ok=True)

        if os.path.exists("dist"):
            if os.path.exists(
                os.path.abspath(os.path.join(buildExeDir, output_dist_folder))
            ):
                shutil.rmtree(
                    os.path.abspath(os.path.join(buildExeDir, output_dist_folder))
                )
            shutil.move(
                os.path.abspath("dist"),
                os.path.abspath(os.path.join(buildExeDir, output_dist_folder)),
            )
        else:
            printColorized("Error: No 'dist' folder found after build!", Fore.RED)
            continue

        if os.path.exists("build"):
            if os.path.exists(
                os.path.abspath(os.path.join(buildExeDir, output_build_folder))
            ):
                shutil.rmtree(
                    os.path.abspath(os.path.join(buildExeDir, output_build_folder))
                )
            shutil.move(
                os.path.abspath("build"),
                os.path.abspath(os.path.join(buildExeDir, output_build_folder)),
            )
        else:
            printColorized("Error: No 'build' folder found after build!", Fore.RED)
            continue
        output_dist_folder_zip = os.path.abspath(
            os.path.join(buildExeDir, f"{output_dist_folder}.zip")
        )
        if os.path.exists(
            os.path.abspath(os.path.join(buildExeDir, output_dist_folder))
        ):
            if os.path.exists(output_dist_folder_zip):
                os.remove(output_dist_folder_zip)
            shutil.make_archive(
                os.path.abspath(os.path.join(buildExeDir, output_dist_folder)),
                "zip",
                os.path.abspath(os.path.join(buildExeDir, output_dist_folder)),
            )
        printColorized("Start to register to server", Fore.CYAN)
        experimentId = condition["experiment_id"]
        password = condition["password"]
        shareDirectory = condition["share_directory"]
        folderName = condition["folder_name"]
        shareFolderInStorage = os.path.abspath(os.path.join(shareDirectory, folderName))
        savedFolder = condition["save_directory"]
        # copyOriginal = os.path.abspath(os.path.join(buildExeDir, output_dist_folder))
        copyOriginal = os.path.abspath(output_dist_folder_zip)
        registerProposal(experimentId, password)
        upLoadFiles(
            version_name,
            experimentId,
            password,
            shareFolderInStorage,
            savedFolder,
            copyOriginal,
        )

        printColorized(f"Build completed for: {version_name}", Fore.GREEN)
        # exit(1)

    printColorized("\nAll builds completed successfully!", Fore.CYAN)
