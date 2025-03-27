# from controller.MainWindow_Controller import Window_Main
import PyQt5.Qt
from TyDocDataMemoTransfer import TyDocDataMemoTransfer
import sys
import portalocker
from PyQt5 import QtWidgets

import global_variable as global_variable

URL_DIAMOND = global_variable.URL_DIAMOND
SAVE_DIRECTORY = global_variable.SAVE_DIRECTORY
SHARE_DIRECTORY_IN_STORAGE = global_variable.SHARE_DIRECTORY_IN_STORAGE
# URL_DIAMOND = 'http://192.168.0.10:5462/request'
# SAVE_DIRECTORY = "Z:/"
# SHARE_DIRECTORY_IN_STORAGE = "C:/Share/SmartLab/"
# URL_DIAMOND = 'http://localhost:5462/request'
# SAVE_DIRECTORY = "C:/Test/Share/"
# SHARE_DIRECTORY_IN_STORAGE = "C:/Test/Share/"

def main():
    doc = TyDocDataMemoTransfer()
    doc.makeLogger("settings/logDataMemoTransfer.json", name=__name__)

    app = QtWidgets.QApplication(sys.argv)
    lock_file = open("./test.lock", mode="a+")
    # try:
    #     portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    # except IOError:
    #     msgBox = QtWidgets.QMessageBox()
    #     msgBox.setText("Another Data_Memo_Transfer is running")
    #     msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #     msgBox.exec_()
    #     return False

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
