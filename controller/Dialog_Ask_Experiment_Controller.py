import forms.Dialog_Ask_Experiment_ID_ui as Dialog_Ask_Experiment_ID_ui

# from controller.MainWindow_Controller import Window_Main
from controller.Dialog_Set_Initial_Controller import Dialog_Set_Initial

from sendMessageToDiamond import senderMessageToDiamond
from Data_Model import DataModel
# from metaDataConverter import MetaDataConverter

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Dialog_Ask_ID(QtWidgets.QDialog):
    def __init__(self, parent=None, data_Model=None):

        super().__init__(parent)
        self.ui = Dialog_Ask_Experiment_ID_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.set_Signal()
        self.setWindowTitle("Log in")

        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()
        url = self.data_Model.get_URL_Address_Diamond()
        self.messageSender = senderMessageToDiamond(url)
        # self.window_Main = Window_Main(data_Model=data_Model)

    def set_Signal(self):
        self.ui.PB_Log_In.clicked.connect(self.log_In_To_Diamond)

    def set_Data_Model(self, data_model):
        self.data_Model = data_model
        url = self.data_Model.get_URL_Address_Diamond()
        self.messageSender = senderMessageToDiamond(url)

    def log_In_To_Diamond(self):
        str_Experiment_ID = self.ui.LE_Experiment_ID.text()
        str_Experiment_ID = self.check_ID_Request_To_Diamond(str_Experiment_ID)
        if str_Experiment_ID is not None:
            message_MetaData = self.messageSender.sendRequestCopyOriginal(
                str_Experiment_ID, self.data_Model)
            self.messageSender.sendRequestStartExperiment(str_Experiment_ID)
            print(message_MetaData)
            experiment_Information = message_MetaData["args"][
                "experiment_information"]
            self.data_Model.save_Initial_Temporary_From_Dict(
                experiment_Information)
            self.data_Model.set_Experiment_ID(str_Experiment_ID)
            self.data_Model.set_User_Information(self.userData)
            self.dialog_Set_Initial = Dialog_Set_Initial(
                data_Model=self.data_Model)
            self.dialog_Set_Initial.show()
            self.close()

    def check_ID_Request_To_Diamond(self, experiment_ID):
        msgBox = QtWidgets.QMessageBox()
        if experiment_ID != "":
            print(experiment_ID)
            reply = self.messageSender.sendRequestCheckID(experiment_ID)
            if reply["status"] is True:
                self.userData = reply["args"]["database"]
                strSetText = ""
                strSetText += reply["message"] + "\n"
                strSetText += "Experiment ID : " + str(
                    self.userData["id"]) + "\n"
                strSetText += "User Name : " + str(
                    self.userData["creators"][0]["name"]) + "\n"
                strSetText += "Instrument : " + str(
                    self.userData["instrument"]["name"]) + "\n"
                strSetText += "Start Date : " + str(
                    self.userData["experiment_date"]["start_date"]) + "\n"
                strSetText += "Are you sure to start experiment?"

                msgBox.setWindowTitle("Your Experiment ID")
                msgBox.setText(strSetText)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok
                                          | QtWidgets.QMessageBox.Cancel)
                retval = msgBox.exec_()
                if retval == 1024:
                    return experiment_ID
            elif "This Experiment ID is used" in reply["message"]:
                self.userData = reply["args"]["database"]
                strSetText = ""
                strSetText += reply["message"] + "\n"
                strSetText += "Experiment ID : " + str(
                    self.userData["id"]) + "\n"
                strSetText += "User Name : " + str(
                    self.userData["creators"][0]["name"]) + "\n"
                strSetText += "Are you continue to experiment?\n"
                strSetText += "Be careful of duplicated changes other requests!"

                msgBox.setWindowTitle("Warning")
                msgBox.setText(strSetText)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok
                                          | QtWidgets.QMessageBox.Cancel)
                retval = msgBox.exec_()
                if retval == 1024:
                    return experiment_ID
            else:
                msgBox.setWindowTitle("Error")
                strSetText = reply["message"]
                msgBox.setText(strSetText)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retval = msgBox.exec_()
        return None
