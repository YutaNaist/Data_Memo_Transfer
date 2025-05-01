from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if TYPE_CHECKING:
    # from controller.TyDialogSetInitial import TyDialogSetInitial
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from TyMessageSender import MessageSenderException

from controller.TyDialogLogin import TyDialogLogin

# from metaDataConverter import MetaDataConverter

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
import logging


class TyDialogRegisterPassword(QtWidgets.QDialog):
    def __init__(
        self,
        doc: TyDocDataMemoTransfer = None,
    ):
        # self.experimentId = experimentId
        super().__init__()
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger("data_memo_transfer")

        self.experimentId = self.doc.getExperimentId()
        self.userMailAddress = self.doc.getMailAddress()
        print(f"experimentId: {self.experimentId}")
        self.loadUi()
        self.setSignal()
        self.setWindowTitle("Input new password")
        # self.LAB_Experiment_ID.setText(experimentId)
        # self.LAB_Email_Address.setText(userMailAddress)
        self.LAB_Experiment_ID.setText(self.experimentId)
        strMailAddressHide = (
            self.userMailAddress[:3]
            + "*" * 5
            + "@"
            + self.userMailAddress.split("@")[1]
        )
        self.LAB_Email_Address.setText(strMailAddressHide)
        # self.window_Main = Window_Main(data_Model=data_Model)

    def loadUi(self):
        uic.loadUi(r"forms\FormRegisterNewPassword.ui", self)
        self.ui = self

    def setSignal(self):
        self.ui.PB_OK.clicked.connect(self.registerPassword)
        self.ui.PB_Cancel.clicked.connect(self.cancel)

    def registerPassword(self):
        newPassword = self.ui.LE_New_Password.text()
        newPasswordVerify = self.ui.LE_New_Password_Verify.text()
        if newPassword != newPasswordVerify:
            self.logger.error("Verify password does not match")
            message = "Error!\n" + "Verified password does not match"
            self.doc.messageBox("Error", message)
            return False
        oneTimePassword = self.ui.LE_One_Time_Password.text()
        hashPassword = self.doc.makeHashFromString(newPassword)
        # print(str(hashPassword))
        self.doc.setHashPassword(hashPassword)
        try:
            response = self.doc.messageSender.sendRequestRegisterPassword(
                self.experimentId, hashPassword, oneTimePassword
            )
            if response["status"] is True:
                message = "Success!\n" + "Password has been registered"
                self.doc.messageBox("Success", message)
                response = self.doc.messageSender.sendRequestLogin(
                    self.experimentId, hashPassword
                )
                self.logger.info(f"responce: {response}")
                dictProposal = response["proposal"]
                login = TyDialogLogin(doc=self.doc)
                login.setProposal(dictProposal)
                login.startExperiment(self.experimentId)
                # self.doc.changeView("experiment_information")
            else:
                self.logger.error(response["message"])
                message = "Error!\n" + response["message"]
                self.doc.messageBox("Error", message)
        except MessageSenderException as e:
            message = f"Error in registering password: {e.message}: {e.status_code}"
            self.logger.error(message)
            self.doc.messageBox("Error", message)

    def cancel(self):
        self.doc.changeView("send_one_time_password")
