# from controller.MainWindow_Controller import Window_Main
from controller.Dialog_Ask_Experiment_Controller import Dialog_Ask_ID

from Data_Model import DataModel

import sys
import logging

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


def make_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_File_Handler = logging.FileHandler("log_data_memo_transfer.log")
    # log_File_Handler = logging.handlers.RotatingFileHandler(
    #     'C:/diamond/log_diamond.log', maxBytes=100_000_000, BackupCount=10)
    fh_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s -%(process)d - %(message)s"
    )
    log_File_Handler.setFormatter(fh_formatter)

    log_Stream_Handler = logging.StreamHandler()
    sh_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(process)d - %(message)s", "%Y/%m/%d %H:%M:%S"
    )
    log_Stream_Handler.setFormatter(sh_formatter)

    logger.addHandler(log_File_Handler)
    logger.addHandler(log_Stream_Handler)
    return logger


def main():
    logger = make_logger()

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
    data_Model.set_Dict_Data_Model(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    data_Model.set_logger(logger)
    data_Model.write_to_logger("Start Data Memo Transfer.")

    dialog_Ask_ID = Dialog_Ask_ID(data_Model=data_Model)
    dialog_Ask_ID.show()
    dialog_Ask_ID.activateWindow()
    app.exec_()


if __name__ == "__main__":
    main()
