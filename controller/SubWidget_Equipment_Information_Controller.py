from __future__ import annotations
from typing import TYPE_CHECKING

from forms.Widget_Equipment_Information_ui import (
    Ui_Form as Ui_Widget_Equipment_Information,
)
if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Sub_Widget_Equipment_Information(QtWidgets.QWidget):

    def __init__(
        self, parent=None, data_Model: TyDocDataMemoTransfer = None, isEditable=True
    ):
        super().__init__(parent)
        self.ui = Ui_Widget_Equipment_Information()
        self.ui.setupUi(self)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.ui.CMB_Method.currentIndexChanged.connect(self.start_edit_Timer)
        self.timer.timeout.connect(self.save_Previous_State)
        self.previousState = []

        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = TyDocDataMemoTransfer()
        if isEditable is False:
            self.ui.CMB_Method.setEditable(False)

    def get_From_Data_Model(self, index: int = -1, is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.data_Model.getDictExperimentInformation(
                "dict_clipboard"
            )
        else:
            dict_file_data = self.data_Model.getDictExperimentInformation(
                "list_file_data"
            )[index]
        try:
            self.ui.CMB_Method.setCurrentText(dict_file_data["equipment"]["method"])
        except KeyError:
            pass

    def set_To_Data_Model(self, index: int = -1, is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.data_Model.getDictExperimentInformation(
                "dict_clipboard"
            )
        else:
            dict_file_data = self.data_Model.getDictExperimentInformation(
                "list_file_data"
            )[index]
        dict_equipment = {}
        dict_equipment["method"] = self.ui.CMB_Method.currentText()
        dict_file_data["equipment"] = dict_equipment

        if is_Template is True:
            self.data_Model.setDiCtExperimentInformation(
                "dict_clipboard", dict_file_data
            )
        else:
            # self.data_Model.set_Dict_Data_Model("dict_clipboard",
            #                                     dict_file_data)
            self.data_Model.setFileInformation(index, dict_file_data)

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
