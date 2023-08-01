from forms.Widget_Experiment_Information_ui import Ui_Form as Ui_Widget_Experiment_Information
from Data_Model import DataModel

from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Sub_Widget_Experiment_Information(QtWidgets.QWidget):

    def __init__(self, parent=None, data_Model: DataModel = None, isEditable=True):
        super().__init__(parent)
        self.ui = Ui_Widget_Experiment_Information()
        self.ui.setupUi(self)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.ui.LE_Title.textChanged.connect(self.start_edit_Timer)
        self.ui.TE_Experiment_Comment.textChanged.connect(
            self.start_edit_Timer)
        self.timer.timeout.connect(self.save_Previous_State)
        self.previousState = []

        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()
        if isEditable is False:
            self.ui.LE_Title.setReadOnly(True)
            self.ui.TE_Experiment_Comment.setReadOnly(True)

    # def set_Data_Model(self, data_model):
    #     self.data_Model = data_model

    def get_From_Data_Model(self,
                            index: int = -1,
                            is_Template: bool = True) -> None:
        self.ui.LE_Title.setText(
            self.data_Model.get_Dict_Data_Model("dict_clipboard")["experiment"]
            ["title"])
        self.ui.TE_Experiment_Comment.setPlainText(
            self.data_Model.get_Dict_Data_Model("dict_clipboard")["experiment"]
            ["comment"])

    def set_To_Data_Model(self,
                          index: int = -1,
                          is_Template: bool = True) -> None:
        dict_file_data = self.data_Model.get_Dict_Data_Model("dict_clipboard")
        dict_experiment = {}
        dict_experiment["title"] = self.ui.LE_Title.text()
        dict_experiment["comment"] = self.ui.TE_Experiment_Comment.toPlainText(
        )
        dict_file_data["experiment"] = dict_experiment
        self.data_Model.set_Dict_Data_Model("dict_clipboard", dict_file_data)

    def start_edit_Timer(self):
        self.timer.start(1000)

    def save_Previous_State(self):
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
