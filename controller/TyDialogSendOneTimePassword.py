# import forms.Dialog_Ask_Experiment_ID_ui as Dialog_Ask_Experiment_ID_ui
from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
    # from controller.TyDialogLogin import TyDialogLogin
    # from controller.TyDialogRegisterPassword import TyDialogRegisterPassword
from TyMessageSender import MessageSenderException

# from metaDataConverter import MetaDataConverter

# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic


class TyDialogSendOneTimePassword(QtWidgets.QDialog):
    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger("data_memo_transfer")
        self.loadUi()

        self.setSignal()
        self.setWindowTitle("Request One Time Password")
        self.experimentId = self.doc.getExperimentId()
        self.ui.LE_Experiment_ID.setText(self.experimentId)
        # self.window_Main = Window_Main(data_Model=data_Model)

    def loadUi(self):
        uic.loadUi(r"forms\FormSendOneTimePassword.ui", self)
        self.ui = self

    def setSignal(self):
        self.ui.PB_Send_One_Time_Password.clicked.connect(self.sendOneTimePassword)
        self.ui.PB_Cancel.clicked.connect(self.cancel)

    def sendOneTimePassword(self):
        experimentId = self.ui.LE_Experiment_ID.text()
        # isSendSupervisor = self.ui.CHB_Send_To_Supervisor.isChecked()
        isSendSupervisor = self.ui.RB_Send_To_Supervisor.isChecked()
        self.doc.setExperimentId(experimentId)
        try:
            response = self.doc.messageSender.sendRequestSendOneTimePassword(
                experimentId, isSendSupervisor
            )
            if response["status"] is True:
                mailAddress = response["mail_address"]
                self.doc.setMailAddress(mailAddress)
                self.doc.changeView("register_password")
            else:
                self.logger.error(response["message"])
                message = "Error!\n" + response["message"]
                self.doc.messageBox("Error", message)
        except MessageSenderException as e:
            message = f"MessageSenderException: {e.message}, {e.status_code}"
            self.logger.error(message)
            self.doc.messageBox("Error", message)

    def cancel(self):
        self.doc.setExperimentId(self.ui.LE_Experiment_ID.text())
        self.doc.changeView("log_in")
