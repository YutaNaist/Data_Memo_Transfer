# from controller.MainWindow_Controller import Window_Main
# import PyQt5.Qt
from TyDocDataMemoTransfer import TyDocDataMemoTransfer
import sys
import os
import portalocker
import logging
from PyQt5 import QtWidgets



def main():
    # * build_client.ps1から実行されたかどうかを判別。
    # * global_variable.pyが存在する場合はbuild_client.ps1から実行されたと判断。
    # * テストする場合はglobal_variable_Local.pyを使用。(global_variable.pyは削除する)
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
    # for handler in doc.logger.handlers:
    #     # print(handler.name)
    #     if handler.get_name() == "console_log" or handler.get_name() == "console_error":
    #         handler.setLevel(logging.DEBUG)
    # doc.makeLogger("settings/logDataMemoTransfer.json", name=__name__)
    # doc.setLogger(logger)
    doc.setIsBuild(isBuild)
    if doc.isBuild:
        logger = logging.getLogger("data_memo_transfer")
    else:
        logger = logging.getLogger("data_memo_transfer_debug")
        logger.setLevel(logging.DEBUG)
    logger.info("Start Data Memo Transfer.")
    app = QtWidgets.QApplication(sys.argv)

    lockFilePath = "./lock_file.lock"
    processLock = portalocker.ProcessLock(lockFilePath)
    logger.info(f"Lock file path: {lockFilePath}")
    logger.info(f"Process ID: {processLock.pid}")
    # if os.path.exists(lockFilePath):
    if processLock.checkAndRemoveStateLock():
        logger.error("Another Data_Memo_Transfer is running.")
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Another Data_Memo_Transfer is running")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
        exit(1)
    processLock.writeLockInfo()
    doc.loadFromTemporary()

    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    # doc.setLogger(logger)
    logger.info("Start Data Memo Transfer.")
    doc.changeView("log_in")
    app.exec_()
    if os.path.exists(lockFilePath):
        os.remove(lockFilePath)
    logger.info("End Data Memo Transfer.")


if __name__ == "__main__":
    main()
