# from controller.MainWindow_Controller import Window_Main
from controller.Dialog_Ask_Experiment_Controller import Dialog_Ask_ID

from Data_Model import DataModel

import sys

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets

URL_DIAMOND = 'http://192.168.150.10:5462/request'
URL_DIAMOND = 'http://192.168.0.10:5462/request'
SAVE_DIRECTORY = "Z:/"
SHARE_DIRECTORY_IN_STORAGE = "D:/Share/NR-301/"
SHARE_DIRECTORY_IN_STORAGE = "C:/Share/SmartLab/"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    data_Model = DataModel()
    # dict_Data_Model = data_Model.get_Dict_Data_Model()
    # dict_Data_Model=
    data_Model.load_From_Temporary()
    data_Model.set_URL_Address_Diamond(URL_DIAMOND)
    data_Model.set_Share_Directory(SAVE_DIRECTORY)
    data_Model.set_Share_Directory_In_Storage(SHARE_DIRECTORY_IN_STORAGE)

    dialog_Ask_ID = Dialog_Ask_ID(data_Model=data_Model)
    dialog_Ask_ID.show()

    # window_Main = Window_Main()
    # signal_Update_ID = windowMain.signal_Update_ID
    # window_Main.show()

    dialog_Ask_ID.activateWindow()

    app.exec_()
