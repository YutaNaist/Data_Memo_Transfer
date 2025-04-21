from __future__ import annotations
from typing import TYPE_CHECKING

# from forms.Widget_Equipment_Information_ui import (
#     Ui_Form as Ui_Widget_Equipment_Information,
# )
if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic


class TySubWidgetEquipmentInformation(QtWidgets.QWidget):

    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None, isEditable=True):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        # self.ui = Ui_Widget_Equipment_Information()
        # self.ui.setupUi(self)
        self.__loadUi()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.ui.CMB_Method.currentIndexChanged.connect(self.start_edit_Timer)
        self.timer.timeout.connect(self.save_Previous_State)
        self.previousState = []

        if isEditable is False:
            self.ui.CMB_Method.setEditable(False)

    def __loadUi(self):
        if self.doc.isBuild:
            from views.FormSubWidgetEquipmentInformation import Ui_Form

            self.ui = Ui_Form()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormSubWidgetEquipmentInformation.ui", self)
            self.ui = self

    def get_From_Data_Model(self, index: int = -1, is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.doc.getDictExperimentInformation(
                "dict_clipboard"
            )
        else:
            dict_file_data = self.doc.getDictExperimentInformation(
                "list_file_data"
            )[index]
        try:
            self.ui.CMB_Method.setCurrentText(dict_file_data["equipment"]["method"])
        except KeyError:
            pass

    def set_To_Data_Model(self, index: int = -1, is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.doc.getDictExperimentInformation(
                "dict_clipboard"
            )
        else:
            dict_file_data = self.doc.getDictExperimentInformation(
                "list_file_data"
            )[index]
        dict_equipment = {}
        dict_equipment["method"] = self.ui.CMB_Method.currentText()
        dict_file_data["equipment"] = dict_equipment

        if is_Template is True:
            self.doc.setDiCtExperimentInformation(
                "dict_clipboard", dict_file_data
            )
        else:
            # self.data_Model.set_Dict_Data_Model("dict_clipboard",
            #                                     dict_file_data)
            self.doc.setFileInformation(index, dict_file_data)

    def start_edit_Timer(self):
        self.timer.start(1000)

    def save_Previous_State(self):
        saveState = {"experiment_method": self.ui.CMB_Method.currentText()}
        self.previousState.append(saveState)
        # print("Previous_State", self.previousState)

    def undo(self):
        # print("Undo", self.previousState)
        if len(self.previousState) != 0:
            try:
                saveSate = self.previousState[-2]
                self.previousState.pop()
                self.ui.CMB_Method.setCurrentText(saveSate["experiment_method"])
            except IndexError:
                pass
