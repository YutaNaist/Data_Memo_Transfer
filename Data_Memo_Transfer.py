# from controller.MainWindow_Controller import Window_Main
from controller.Dialog_Ask_Experiment_Controller import Dialog_Ask_ID

from Data_Model import DataModel

import sys
# import os
import portalocker

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets

import global_variable

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
    app = QtWidgets.QApplication(sys.argv)
    lock_file = open("./test.lock", mode="a+")
    try:
        portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    except IOError:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Another Data_Memo_Transfer is running")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
        return False

    data_Model = DataModel()
    data_Model.load_From_Temporary()
    data_Model.set_Dict_Data_Model("str_url_diamond", URL_DIAMOND)
    data_Model.set_Dict_Data_Model("str_save_directory", SAVE_DIRECTORY)
    data_Model.set_Dict_Data_Model("str_share_directory_in_storage",
                                   SHARE_DIRECTORY_IN_STORAGE)

    dialog_Ask_ID = Dialog_Ask_ID(data_Model=data_Model)
    dialog_Ask_ID.show()
    dialog_Ask_ID.activateWindow()
    app.exec_()


if __name__ == "__main__":
    main()
