from forms.Widget_Experiment_Information_ui import Ui_Form as Ui_Widget_Experiment_Information
from Data_Model import DataModel

from PyQt5 import QtWidgets


class Sub_Widget_Experiment_Information(QtWidgets.QWidget):
    def __init__(self, parent=None, data_Model=None):
        super().__init__(parent)
        self.ui = Ui_Widget_Experiment_Information()
        self.ui.setupUi(self)
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

    def get_All_To_Data_Model(self):
        self.data_Model.set_Template_Data_By_Key("title",
                                                 self.ui.LE_Title.text())
        self.data_Model.set_Template_Data_By_Key(
            "experiment_comment", self.ui.TE_Experiment_Comment.toPlainText())

    def set_Data_Model(self, index=-1):
        self.set_All_From_Data_Model()

    def get_Data_Model(self, index=-1):
        self.get_All_To_Data_Model()
