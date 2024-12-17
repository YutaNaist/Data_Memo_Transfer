from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # from controller.Dialog_Set_Initial_Controller import Dialog_Set_Initial
    # from controller.TyDialogSendOneTimePassword import TyDialogSendOneTimePassword
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer

# from metaDataConverter import MetaDataConverter

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic


class TyDialogLogin(QtWidgets.QDialog):
    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        # self.ui = Dialog_Ask_Experiment_ID_ui.Ui_Dialog()
        # self.ui.setupUi(self)

        # uic.loadUi(r"C:\Project\Data_Memo_Transfer_dev\forms\Dialog_Ask_Experiment_ID.ui", self)

        self.__loadUi()
        self.__setSignal()
        self.setWindowTitle("Log in")

        self.experimentId = self.doc.getExperimentId()
        self.ui.LE_Experiment_ID.setText(self.experimentId)
        # url = self.doc.getDictExperimentInformation("str_url_diamond")
        # self.window_Main = Window_Main(data_Model=data_Model)

    def __loadUi(self):
        uic.loadUi(r"forms\FormDialogLogin.ui", self)
        self.ui = self

    def __setSignal(self):
        self.ui.PB_Log_In.clicked.connect(self.logInToDiamond)
        self.ui.PB_Reset_Password.clicked.connect(self.resetPassword)

    def logInToDiamond(self):
        msgBox = QtWidgets.QMessageBox()
        message = ""
        try:
            self.doc.writeToLogger("Log in to diamond")
            strExperimentId = self.ui.LE_Experiment_ID.text()
            if strExperimentId == "":
                message = "Please input Experiment ID."
                self.doc.messageBox("Error", message)
                return False
            strPassword = self.ui.LE_Password.text()
            if strPassword == "":
                message = "Please input Password."
                self.doc.messageBox("Error", message)
                return False
            hashPassword = self.doc.makeHashFromString(strPassword)
            # self.doc.setHashPassword(hashPassword)
            # strExperimentId = self.CheckIdRequestToDiamond(strExperimentId)
            response = self.doc.messageSender.sendRequestLogin(
                strExperimentId, hashPassword
            )
            if response["status"] is True:
                self.proposal = response["args"]["dict_proposal"]
                strSetText = ""
                strSetText += response["message"] + "\n"
                strSetText += (
                    "Experiment ID : " + str(self.proposal["experiment_id"]) + "\n"
                )
                strSetText += "User Name : " + str(self.proposal["user"]["name"]) + "\n"
                strSetText += (
                    "Instrument : " + str(self.proposal["instrument"]["name"]) + "\n"
                )
                strSetText += (
                    "Start Date : " + str(self.proposal["date"]["start"]) + "\n"
                )
                strSetText += "Are you sure to start experiment?"

                # msgBox.setWindowTitle("Your Experiment ID")
                # msgBox.setText(strSetText)
                # msgBox.setStandardButtons(
                #     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
                # )
                # retval = msgBox.exec_()
                retval = self.doc.messageBox("Your Experiment ID", strSetText, 2)
                if retval == 1024:
                    self.startExperiment(strExperimentId, self.proposal)
            else:
                message = response["message"]
                msgBox.setWindowTitle("Warning")
                message = "Warning!\n" + message
                self.doc.messageBox("Warning", message)
                return False
        except BaseException as e:
            self.doc.writeToLogger(e, "warning")

    def resetPassword(self):
        experimentId = self.ui.LE_Experiment_ID.text()
        self.doc.setExperimentId(experimentId)
        self.doc.changeView("send_one_time_password")

    def startExperiment(self, strExperimentId: str, dictProposal: dict):
        self.doc.setExperimentId(strExperimentId)
        response = self.doc.messageSender.sendRequestStartExperiment(
            strExperimentId, self.doc
        )
        if dictProposal["arim"]["is_arim"][0] != "0":
            self.doc.setDiCtExperimentInformation("is_upload_arim", True)
        if dictProposal["share"]["is_share"][0] == "1":
            self.doc.setDiCtExperimentInformation("is_share_with_google", True)
        dictExperimentInformation = response["args"]["dict_experiment_information"]
        if self.doc.loadFromTemporary():
            self.doc.setExperimentId(strExperimentId)
            self.doc.setDiCtExperimentInformation("dict_user_information", dictProposal)
            # dictExperimentInformation = self.doc.getAllDictExperimentInformation()
            # dictExperimentInformation["dict_user_information"] = self.proposal
        else:
            if dictExperimentInformation != {}:
                oldExperimentId = self.doc.getDictExperimentInformation("str_experiment_id")
                if oldExperimentId != strExperimentId:
                    message = "Warning!\n"
                    message += f"Previous experiment ID : {oldExperimentId} is different from current experiment ID.\n"
                    message += "Are you sure to start experiment?\n"
                    retval = self.doc.messageBox("Warning", message, 2)
                    if retval == 1024:
                        dictExperimentInformation["dict_user_information"] = dictProposal
                        self.doc.setAllDictExperimentInformation(dictExperimentInformation)
                    else:
                        return False
                else:
                    dictExperimentInformation["dict_user_information"] = dictProposal
                    self.doc.setAllDictExperimentInformation(dictExperimentInformation)
            else:
                self.doc.setDiCtExperimentInformation(
                    "dict_user_information", dictProposal
                )
        self.doc.saveToTemporary()
        self.doc.writeToLogger("Start experiment")
        self.doc.changeView("set_initial")
        # self.dialogSetInitial = Dialog_Set_Initial(data_Model=self.doc)
        # self.dialogSetInitial.show()
        # self.close()

    # def CheckIdRequestToDiamond(self, experiment_ID: str) -> str:
    #     msgBox = QtWidgets.QMessageBox()
    #     flag_return_experiment_id = False
    #     if experiment_ID != "":
    #         self.doc.writeToLogger("Ask experiment ID to diamond")
    #         reply = self.messageSender.sendRequestCheckID(experiment_ID)
    #         if reply["status"] is True:
    #             if (
    #                 experiment_ID
    # != self.doc.getDictExperimentInformation("str_experiment_id")
    #                 and self.doc.getDictExperimentInformation("str_experiment_id") != ""
    #             ):
    #                 self.proposal = reply["args"]["database"]
    #                 strSetText = ""
    #                 strSetText += "Warning!\n"
    #                 strSetText += (
    #                     "Your Experiment ID : " + str(self.proposal["id"]) + "\n"
    #                 )
    #                 strSetText += "Different experiment ID is being used.\n"
    #                 strSetText += "Are you sure to start experiment?\n"
    #                 strSetText += "The previous experiment saved local is deleted.\n"
    #                 strSetText += "Please check the sheared folder empty!\n"
    #                 msgBox.setWindowTitle("Warning!")
    #                 msgBox.setText(strSetText)
    #                 msgBox.setStandardButtons(
    #                     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
    #                 )
    #                 retval = msgBox.exec_()
    #                 if retval == 1024:
    #                     flag_return_experiment_id = True
    #             else:
    #                 self.proposal = reply["args"]["database"]
    #                 strSetText = ""
    #                 strSetText += reply["message"] + "\n"
    #                 strSetText += "Experiment ID : " + str(self.proposal["id"]) + "\n"
    #                 strSetText += (
    #                     "User Name : "
    #                     + str(self.proposal["creators"][0]["name"])
    #                     + "\n"
    #                 )
    #                 strSetText += (
    #                     "Instrument : "
    #                     + str(self.proposal["instrument"]["name"])
    #                     + "\n"
    #                 )
    #                 strSetText += (
    #                     "Start Date : "
    #                     + str(self.proposal["experiment_date"]["start_date"])
    #                     + "\n"
    #                 )
    #                 strSetText += "Are you sure to start experiment?"

    #                 msgBox.setWindowTitle("Your Experiment ID")
    #                 msgBox.setText(strSetText)
    #                 msgBox.setStandardButtons(
    #                     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
    #                 )
    #                 retval = msgBox.exec_()
    #                 if retval == 1024:
    #                     flag_return_experiment_id = True
    #         elif "This Experiment ID is used" in reply["message"]:
    #             self.proposal = reply["args"]["database"]
    #             strSetText = ""
    #             strSetText += reply["message"] + "\n"
    #             strSetText += "Experiment ID : " + str(self.proposal["id"]) + "\n"
    #             strSetText += (
    #                 "User Name : " + str(self.proposal["creators"][0]["name"]) + "\n"
    #             )
    #             strSetText += "Are you continue to experiment?\n"
    #             strSetText += "Be careful of duplicated changes other requests!"

    #             msgBox.setWindowTitle("Warning")
    #             msgBox.setText(strSetText)
    #             msgBox.setStandardButtons(
    #                 QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
    #             )
    #             retval = msgBox.exec_()
    #             if retval == 1024:
    #                 flag_return_experiment_id = True
    #         else:
    #             msgBox.setWindowTitle("Error")
    #             strSetText = reply["message"]
    #             msgBox.setText(strSetText)
    #             msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #             retval = msgBox.exec_()
    #     if flag_return_experiment_id is True:
    #         return experiment_ID
    #     else:
    #         return None
