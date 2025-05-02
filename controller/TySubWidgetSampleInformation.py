from __future__ import annotations
from typing import TYPE_CHECKING

# from forms.Widget_Sample_Information_ui import Ui_Form as Ui_Widget_Sample_Information
if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
import logging


class TySubWidgetSampleInformation(QtWidgets.QWidget):

    def __init__(
        self, parent=None, doc: TyDocDataMemoTransfer = None, isEditable: bool = True
    ):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger(self.doc.getLoggerName())
        self.__loadUi()
        # self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.ui.LE_Sample_ID.textChanged.connect(self.startEditTimer)
        self.ui.LE_Sample_Name.textChanged.connect(self.startEditTimer)
        self.ui.TE_Sample_Comment.textChanged.connect(self.startEditTimer)
        self.timer.timeout.connect(self.savePreviousStatus)
        self.previousState = []

        if isEditable is False:
            self.ui.LE_Sample_ID.setReadOnly(True)
            self.ui.LE_Sample_Name.setReadOnly(True)
            self.ui.TE_Sample_Comment.setReadOnly(True)

    def __loadUi(self):
        if self.doc.getIsBuild():
            from views.FormSubWidgetSampleInformation import Ui_Form

            self.ui = Ui_Form()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormSubWidgetSampleInformation.ui", self)
            self.ui = self

    def getFromDoc(self, index: int = -1, is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.doc.getDictExperimentInformation("dict_clipboard")
        else:
            dict_file_data = self.doc.getDictExperimentInformation("list_file_data")[
                index
            ]
        try:
            self.ui.LE_Sample_ID.setText(dict_file_data["sample"]["id"])
            self.ui.LE_Sample_Name.setText(dict_file_data["sample"]["name"])
            self.ui.TE_Sample_Comment.setPlainText(dict_file_data["sample"]["comment"])
        except KeyError:
            pass

    def setToDoc(self, index: int = -1, is_Template: bool = True) -> None:
        dictFileData = {}
        if is_Template is True:
            dictFileData = self.doc.getDictExperimentInformation("dict_clipboard")
        else:
            dictFileData = self.doc.getDictExperimentInformation("list_file_data")[
                index
            ]
        dictSample = {}
        dictSample["name"] = self.ui.LE_Sample_Name.text()
        dictSample["id"] = self.ui.LE_Sample_ID.text()
        dictSample["comment"] = self.ui.TE_Sample_Comment.toPlainText()
        dictFileData["sample"] = dictSample
        if is_Template is True:
            self.doc.setDiCtExperimentInformation("dict_clipboard", dictFileData)
        else:
            # self.data_Model.set_Dict_Data_Model("dict_clipboard",
            #                                     dict_file_data)
            self.doc.setFileInformation(index, dictFileData)

    def startEditTimer(self):
        self.timer.start(1000)

    def savePreviousStatus(self):
        saveState = {}
        saveState["sample_id"] = self.ui.LE_Sample_ID.text()
        saveState["sample_name"] = self.ui.LE_Sample_Name.text()
        saveState["sample_comment"] = self.ui.TE_Sample_Comment.toPlainText()
        self.previousState.append(saveState)
        # print("Previous_State", self.previousState)

    def undo(self):
        # print("Undo", self.previousState)
        if len(self.previousState) != 0:
            try:
                saveSate = self.previousState[-2]
                self.previousState.pop()
                self.ui.LE_Sample_ID.setText(saveSate["sample_id"])
                self.ui.LE_Sample_Name.setText(saveSate["sample_name"])
                self.ui.TE_Sample_Comment.setPlainText(saveSate["sample_comment"])
            except IndexError:
                pass
