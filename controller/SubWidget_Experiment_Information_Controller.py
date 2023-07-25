from forms.Widget_Experiment_Information_ui import Ui_Form as Ui_Widget_Experiment_Information
from Data_Model import DataModel

from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Sub_Widget_Experiment_Information(QtWidgets.QWidget):

    def __init__(self, parent=None, data_Model=None):
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

    # def set_Data_Model(self, data_model):
    #     self.data_Model = data_model

    def set_All_From_Data_Model(self):
        self.ui.LE_Title.setText(
            self.data_Model.get_Template_Data_By_Key("title"))
        self.ui.TE_Experiment_Comment.setPlainText(
            self.data_Model.get_Template_Data_By_Key("experiment_comment"))
        # self.save_Previous_State()

    def get_All_To_Data_Model(self):
        self.data_Model.set_Template_Data_By_Key("title",
                                                 self.ui.LE_Title.text())
        self.data_Model.set_Template_Data_By_Key(
            "experiment_comment", self.ui.TE_Experiment_Comment.toPlainText())

    def set_Data_Model(self, index=-1):
        self.set_All_From_Data_Model()

    def get_Data_Model(self, index=-1):
        self.get_All_To_Data_Model()

    def start_edit_Timer(self):
        self.timer.start(1000)

    def save_Previous_State(self):
        saveState = {}
        saveState["experiment_title"] = self.ui.LE_Title.text()
        saveState[
            "experiment_comment"] = self.ui.TE_Experiment_Comment.toPlainText(
            )
        self.previousState.append(saveState)

    def undo(self):
        if len(self.previousState) != 0:
            try:
                saveSate = self.previousState[-2]
                self.previousState.pop()
                self.ui.LE_Title.setText(saveSate["experiment_title"])
                self.ui.TE_Experiment_Comment.setPlainText(
                    saveSate["experiment_comment"])
            except IndexError:
                pass
