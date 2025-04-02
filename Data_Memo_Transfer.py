# from controller.MainWindow_Controller import Window_Main
import PyQt5.Qt
from TyDocDataMemoTransfer import TyDocDataMemoTransfer
import sys
import os
import portalocker
import subprocess
import platform
from PyQt5 import QtWidgets

def main():
    #* build_client.ps1から実行されたかどうかを判別。
    #* global_variable.pyが存在する場合はbuild_client.ps1から実行されたと判断。
    #* テストする場合はglobal_variable_Local.pyを使用。(global_variable.pyは削除する)
    if os.path.exists("global_variable.py"):
        import global_variable as global_variable
        isBuild = True
    else:
        import buildConfig.global_variable_Local as global_variable
        isBuild = False

    URL_DIAMOND = global_variable.URL_DIAMOND
    SAVE_DIRECTORY = global_variable.SAVE_DIRECTORY
    SHARE_DIRECTORY_IN_STORAGE = global_variable.SHARE_DIRECTORY_IN_STORAGE

    doc = TyDocDataMemoTransfer()
    doc.makeLogger("settings/logDataMemoTransfer.json", name=__name__)
    doc.isBuild = isBuild
    app = QtWidgets.QApplication(sys.argv)

    lock_file_path = "./test.lock"
    process_lock = portalocker.ProcessLock(lock_file_path)

    # 古いロックファイルのチェック
    if os.path.exists(lock_file_path):
        if not process_lock.check_and_remove_stale_lock():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Another Data_Memo_Transfer is running")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
            return False

    # 新しいロックファイルの作成
    lock_file = open(lock_file_path, mode="w")
    try:
        portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
        process_lock.write_lock_info()
    except IOError:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Another Data_Memo_Transfer is running")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
        return False

    doc.loadFromTemporary()
    # doc.setDiCtExperimentInformation("str_url_diamond", URL_DIAMOND)
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    # doc.setLogger(logger)
    doc.writeToLogger("Start Data Memo Transfer.")
    doc.changeView("log_in")

    # dialog_Ask_ID = TyDialogAskId(doc=data_Model)
    # dialog_Ask_ID.show()
    # dialog_Ask_ID.activateWindow()
    app.exec_()


if __name__ == "__main__":
    main()
