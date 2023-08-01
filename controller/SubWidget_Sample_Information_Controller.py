from forms.Widget_Sample_Information_ui import Ui_Form as Ui_Widget_Sample_Information

from Data_Model import DataModel
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Sub_Widget_Sample_Information(QtWidgets.QWidget):

    def __init__(self,
                 parent=None,
                 data_Model: DataModel = None,
                 isEditable=True):
        super().__init__(parent)
        self.ui = Ui_Widget_Sample_Information()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.ui.LE_Sample_ID.textChanged.connect(self.start_edit_Timer)
        self.ui.LE_Sample_Name.textChanged.connect(self.start_edit_Timer)
        self.ui.TE_Sample_Comment.textChanged.connect(self.start_edit_Timer)
        self.timer.timeout.connect(self.save_Previous_State)
        self.previousState = []

        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()

        if isEditable is False:
            self.ui.LE_Sample_ID.setReadOnly(True)
            self.ui.LE_Sample_Name.setReadOnly(True)
            self.ui.TE_Sample_Comment.setReadOnly(True)

    def get_From_Data_Model(self,
                            index: int = -1,
                            is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.data_Model.get_Dict_Data_Model(
                "dict_clipboard")
        else:
            dict_file_data = self.data_Model.get_Dict_Data_Model(
                "list_file_data")[index]
        try:
            self.ui.LE_Sample_ID.setText(dict_file_data["sample"]["id"])
            self.ui.LE_Sample_Name.setText(dict_file_data["sample"]["name"])
            self.ui.TE_Sample_Comment.setPlainText(
                dict_file_data["sample"]["comment"])
        except KeyError:
            pass

    def set_To_Data_Model(self,
                          index: int = -1,
                          is_Template: bool = True) -> None:
        dict_file_data = {}
        if is_Template is True:
            dict_file_data = self.data_Model.get_Dict_Data_Model(
                "dict_clipboard")
        else:
            dict_file_data = self.data_Model.get_Dict_Data_Model(
                "list_file_data")[index]
        dict_sample = {}
        dict_sample["name"] = self.ui.LE_Sample_Name.text()
        dict_sample["id"] = self.ui.LE_Sample_ID.text()
        dict_sample["comment"] = self.ui.TE_Sample_Comment.toPlainText()
        dict_file_data["sample"] = dict_sample
        if is_Template is True:
            self.data_Model.set_Dict_Data_Model("dict_clipboard",
                                                dict_file_data)
        else:
            # self.data_Model.set_Dict_Data_Model("dict_clipboard",
            #                                     dict_file_data)
            self.data_Model.set_File_Information(index, dict_file_data)

    def start_edit_Timer(self):
        self.timer.start(1000)

    def save_Previous_State(self):
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
                self.ui.TE_Sample_Comment.setPlainText(
                    saveSate["sample_comment"])
            except IndexError:
                pass
