from forms.Widget_Equipment_Information_ui import Ui_Form as Ui_Widget_Equipment_Information

from Data_Model import DataModel
from PyQt5 import QtWidgets


class Sub_Widget_Equipment_Information(QtWidgets.QWidget):
    def __init__(self, parent=None, data_Model=None):
        super().__init__(parent)
        self.ui = Ui_Widget_Equipment_Information()
        self.ui.setupUi(self)
        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()

    # def set_Data_Model(self, data_model):
    #     self.data_Model = data_model

    def set_All_From_Data_Model(self):
        self.ui.CMB_Method.setCurrentText(
            self.data_Model.get_Equipment_Contents("experiment_method"))

    def get_All_To_Data_Model(self):
        self.data_Model.set_Equipment_Contents(
            "experiment_method", self.ui.CMB_Method.currentText())

    def set_All_From_Data_Model_File_Information(self, index):
        self.ui.CMB_Method.setCurrentText(
            self.data_Model.get_File_Data_Equipment_Contents_By_Index(
                index, "experiment_method"))

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
