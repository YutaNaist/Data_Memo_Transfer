from __future__ import annotations
from typing import TYPE_CHECKING

# from forms.Widget_Experiment_Information_ui import (
#     Ui_Form as Ui_Widget_Experiment_Information,
# )
if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
import logging


class TySubWidgetExperimentInformation(QtWidgets.QWidget):

    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None, isEditable=True):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger(self.doc.loggerName)
        self.__loadUi()
        # self.ui = Ui_Widget_Experiment_Information()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.savePreviousStatus)
        self.ui.LE_Title.textChanged.connect(self.startEditTimer)
        self.ui.TE_Experiment_Comment.textChanged.connect(self.startEditTimer)
        self.previousState = []

        if isEditable is False:
            self.ui.LE_Title.setReadOnly(True)
            self.ui.TE_Experiment_Comment.setReadOnly(True)

    # def set_Data_Model(self, data_model):
    #     self.data_Model = data_model
    # def loadUi(self):
    def __loadUi(self):
        if self.doc.getIsBuild():
            from views.FormSubWidgetExperimentInformation import Ui_Form

            self.ui = Ui_Form()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormSubWidgetExperimentInformation.ui", self)
            self.ui = self
        # pass

    def getFromDoc(self, index: int = -1, is_Template: bool = True) -> None:
        self.ui.LE_Title.setText(
            self.doc.getDictExperimentInformation("dict_clipboard")["experiment"][
                "title"
            ]
        )
        self.ui.TE_Experiment_Comment.setPlainText(
            self.doc.getDictExperimentInformation("dict_clipboard")["experiment"][
                "comment"
            ]
        )

    def setToDoc(self, index: int = -1, is_Template: bool = True) -> None:
        dictFileData = self.doc.getDictExperimentInformation("dict_clipboard")
        dictExperiment = {}
        dictExperiment["title"] = self.ui.LE_Title.text()
        dictExperiment["comment"] = self.ui.TE_Experiment_Comment.toPlainText()
        dictFileData["experiment"] = dictExperiment
        self.doc.setDiCtExperimentInformation("dict_clipboard", dictFileData)

    def startEditTimer(self):
        self.timer.start(1000)

    def savePreviousStatus(self):
        saveState = {}
        saveState["title"] = self.ui.LE_Title.text()
        saveState["comment"] = self.ui.TE_Experiment_Comment.toPlainText()
        self.previousState.append(saveState)

    def undo(self):
        if len(self.previousState) != 0:
            try:
                saveSate = self.previousState[-2]
                self.previousState.pop()
                self.ui.LE_Title.setText(saveSate["title"])
                self.ui.TE_Experiment_Comment.setPlainText(saveSate["comment"])
            except IndexError:
                pass
