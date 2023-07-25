from forms.Widget_Equipment_Information_ui import Ui_Form as Ui_Widget_Equipment_Information

from Data_Model import DataModel
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Sub_Widget_Equipment_Information(QtWidgets.QWidget):

    def __init__(self, parent=None, data_Model=None):
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
            self.data_Model = DataModel()

    # def set_Data_Model(self, data_model):
    #     self.data_Model = data_model

    def set_All_From_Data_Model(self):
        self.ui.CMB_Method.setCurrentText(
            self.data_Model.get_Equipment_Contents("experiment_method"))
        # self.save_Previous_State()

    def get_All_To_Data_Model(self):
        self.data_Model.set_Equipment_Contents(
            "experiment_method", self.ui.CMB_Method.currentText())

    def set_All_From_Data_Model_File_Information(self, index):
        self.ui.CMB_Method.setCurrentText(
            self.data_Model.get_File_Data_Equipment_Contents_By_Index(
                index, "experiment_method"))
        # self.save_Previous_State()

    def get_All_To_Data_Model_File_Information(self, index):
        self.data_Model.set_File_Data_Equipment_Contents_By_Index(
            index, "experiment_method", self.ui.CMB_Method.currentText())

    def set_Data_Model(self, index):
        if index == -1:
            self.set_All_From_Data_Model()
        else:
            self.set_All_From_Data_Model_File_Information(index)

    def get_Data_Model(self, index):
        if index == -1:
            self.get_All_To_Data_Model()
        else:
            self.get_All_To_Data_Model_File_Information()

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
                self.ui.CMB_Method.setCurrentText(
                    saveSate["experiment_method"])
            except IndexError:
                pass
