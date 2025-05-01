from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import os

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from TyMessageSender import MessageSenderException

# from metaDataConverter import MetaDataConverter

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
import logging
import traceback  # tracebackモジュールをインポート


class TyDialogLogin(QtWidgets.QDialog):
    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        self.isTest = False
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        if self.doc.isBuild:
            self.logger = logging.getLogger("data_memo_transfer")
        else:
            self.logger = logging.getLogger("data_memo_transfer_debug")
            self.logger.setLevel(logging.DEBUG)
        self.logger.info("----------Dialog Log in----------")
        # self.ui = Dialog_Ask_Experiment_ID_ui.Ui_Dialog()
        # self.ui.setupUi(self)
        # uic.loadUi(r"C:\Project\Data_Memo_Transfer_dev\forms\Dialog_Ask_Experiment_ID.ui", self)

        self.__loadUi()
        self.__setSignal()

        self.experimentId = self.doc.getExperimentId()
        self.ui.LE_Experiment_ID.setText(self.experimentId)
        # url = self.doc.getDictExperimentInformation("str_url_diamond")
        # self.window_Main = Window_Main(data_Model=data_Model)

    def __loadUi(self):
        if self.doc.isBuild:
            # if True:
            from views.FormDiamondLogin import Ui_Dialog

            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
            self.setWindowTitle("Log in")
        else:
            uic.loadUi(r"forms\FormDialogLogin.ui", self)
            self.ui = self
            self.ui.setWindowTitle("Log in")

    def __setSignal(self):
        self.ui.PB_Log_In.clicked.connect(self.logInToDiamond)
        self.ui.PB_Reset_Password.clicked.connect(self.resetPassword)

    def logInToDiamond(self) -> tuple[bool, str]:
        try:
            self.logger.info("Log in to diamond")
            strExperimentId = self.ui.LE_Experiment_ID.text()
            self.doc.setExperimentId(strExperimentId)
            if strExperimentId == "":
                message = "Please input Experiment ID."
                self.doc.messageBox("Error", message)
                return (False, "Please input Experiment ID.")
            strPassword = self.ui.LE_Password.text()
            if strPassword == "":
                message = "Please input Password."
                self.doc.messageBox("Error", message)
                return (False, "Please input Password.")
            hashPassword = self.doc.makeHashFromString(strPassword)
            try:
                response = self.doc.messageSender.sendRequestLogin(
                    strExperimentId, hashPassword
                )
                if response["status"] is True:
                    self.proposal = response["proposal"]
                    if self.isTest:
                        self.doc.setExperimentId(strExperimentId)
                        return (True, "Success")
                    strSetText = self.createLoginMessage(response["message"])
                    retval = self.doc.messageBox("Your Experiment ID", strSetText, 2)
                    if retval == 1024:
                        self.doc.setHashPassword(hashPassword)
                        self.doc.setExperimentId(strExperimentId)
                        self.startExperiment(strExperimentId)
                        return (True, "Success")
                    else:
                        return (True, "Cancel")
                else:
                    message = response["message"]
                    message = "Warning!\n" + message
                    self.doc.messageBox("Warning", message)
                    return (False, message)
            except MessageSenderException as e:
                errorMessage = f"Log in Error! : {e} : {e.status_code}"
                self.logger.error(errorMessage)
                self.doc.messageBox("Error", errorMessage)
                return (False, errorMessage)
        except Exception as e:
            errorMessage = f"Error: {e}"
            self.logger.error(errorMessage)
            stackTrace = traceback.format_exc()  # スタックトレースを取得
            self.logger.debug(f"Stack Trace:\n{stackTrace}")
            return (False, errorMessage)

    def resetPassword(self) -> tuple[bool, str]:
        experimentId = self.ui.LE_Experiment_ID.text()
        self.doc.setExperimentId(experimentId)
        self.doc.changeView("send_one_time_password", isTest=self.isTest)
        return (True, "Success")

    def startExperiment(self, strExperimentId: str) -> tuple[bool, str]:
        self.doc.setExperimentId(strExperimentId)
        try:
            response = self.doc.messageSender.sendRequestStartExperiment(
                strExperimentId, self.doc
            )
            if response["status"] is False:
                message = "Failed to start experiment.\n"
                message += "Please contact to administrator.\n"
                message += "--------------------\n"
                message += response["message"]
                message += "--------------------\n"
                self.doc.messageBox("Error", message)
                return (False, "Status is False")
            if self.proposal["arim"]["is_arim"][0] != "0":
                self.doc.setDiCtExperimentInformation("is_upload_arim", True)
            if self.proposal["share"]["is_share"][0] == "1":
                self.doc.setDiCtExperimentInformation("is_share_with_google", True)
            dictExperimentInformation = response["experiment_information"]
            if self.doc.loadFromTemporary():
                self.doc.setExperimentId(strExperimentId)
                self.doc.setDiCtExperimentInformation(
                    "dict_user_information", self.proposal
                )
            else:
                if dictExperimentInformation != {}:
                    oldExperimentId = self.doc.getDictExperimentInformation(
                        "str_experiment_id"
                    )
                    if oldExperimentId != strExperimentId:
                        message = "Warning!\n"
                        message += (
                            "There is confliction compared with temporally saved file."
                        )
                        message += f"Previous experiment ID : {oldExperimentId}.\n"
                        message += f"Current experiment ID : {strExperimentId}.\n"
                        message += "Are you sure to start experiment?\n"
                        retval = self.doc.messageBox("Warning", message, 2)
                        if retval == 1024:
                            dictExperimentInformation["dict_user_information"] = (
                                self.proposal
                            )
                            dictExperimentInformation[
                                "str_share_directory_in_storage"
                            ] = self.doc.getDictExperimentInformation(
                                "str_share_directory_in_storage"
                            )
                            self.doc.setAllDictExperimentInformation(
                                dictExperimentInformation
                            )
                        else:
                            return (False, "Status is False")
                    else:
                        dictExperimentInformation["dict_user_information"] = (
                            self.proposal
                        )
                        dictExperimentInformation["str_share_directory_in_storage"] = (
                            self.doc.getDictExperimentInformation(
                                "str_share_directory_in_storage"
                            )
                        )
                        self.doc.setAllDictExperimentInformation(
                            dictExperimentInformation
                        )
                else:
                    self.doc.setDiCtExperimentInformation(
                        "dict_user_information", self.proposal
                    )
            self.doc.saveToTemporary()
            self.logger.info("Start experiment")
            self.doc.changeView("set_initial", isTest=self.isTest)
            return (True, "Success")
        except MessageSenderException as e:
            errorMessage = f"Error in Starting Experiment! : {e} : {e.status_code}"
            self.logger.error(errorMessage)
            self.doc.messageBox("Error", errorMessage)
            return (False, errorMessage)

    def setProposal(self, proposal: dict) -> None:
        self.proposal = proposal

    def createLoginMessage(self, message: str) -> str:
        strSetText = ""
        strSetText += message + "\n"
        strSetText += "Experiment ID : " + str(self.proposal["experiment_id"]) + "\n"
        strSetText += "User Name : " + str(self.proposal["user"]["name"]) + "\n"
        strSetText += "Instrument : " + str(self.proposal["instrument"]["name"]) + "\n"
        strSetText += "Start Date : " + str(self.proposal["date"]["start"]) + "\n"
        strSetText += "Are you sure to start experiment?"
        return strSetText


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    )
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
    import buildConfig.global_variable_Local as global_variable

    URL_DIAMOND = global_variable.URL_DIAMOND
    SAVE_DIRECTORY = global_variable.SAVE_DIRECTORY
    SHARE_DIRECTORY_IN_STORAGE = global_variable.SHARE_DIRECTORY_IN_STORAGE

    doc = TyDocDataMemoTransfer()
    doc.isBuild = False
    logger = logging.getLogger("data_memo_transfer_debug")
    logger.setLevel(logging.DEBUG)

    app = QtWidgets.QApplication(sys.argv)

    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    # doc.setLogger(logger)
    logger.info("Start Data Memo Transfer.")
    dialogLogin = TyDialogLogin(doc=doc)
    dialogLogin.isTest = True
    dialogLogin.ui.LE_Experiment_ID.setText("0000-0000-0000")
    dialogLogin.show()
    app.exec_()
