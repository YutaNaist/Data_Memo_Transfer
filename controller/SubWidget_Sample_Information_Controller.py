from forms.Widget_Sample_Information_ui import Ui_Form as Ui_Widget_Sample_Information

from Data_Model import DataModel
from PyQt5 import QtWidgets


class Sub_Widget_Sample_Information(QtWidgets.QWidget):
    def __init__(self, parent=None, data_Model=None):
        super().__init__(parent)
        self.ui = Ui_Widget_Sample_Information()
        self.ui.setupUi(self)
        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()

    # def set_Data_Model(self, data_model):
    #     self.data_Model = data_model

    def set_All_From_Data_Model(self):
        self.ui.LE_Sample_ID.setText(
            self.data_Model.get_Template_Data_By_Key("sample_id"))
        self.ui.LE_Sample_Name.setText(
            self.data_Model.get_Template_Data_By_Key("sample_name"))
        self.ui.TE_Sample_Comment.setPlainText(
            self.data_Model.get_Template_Data_By_Key("sample_comment"))

    def get_All_To_Data_Model(self):
        self.data_Model.set_Template_Data_By_Key("sample_id",
                                                 self.ui.LE_Sample_ID.text())
        self.data_Model.set_Template_Data_By_Key("sample_name",
                                                 self.ui.LE_Sample_Name.text())
        self.data_Model.set_Template_Data_By_Key(
            "sample_comment", self.ui.TE_Sample_Comment.toPlainText())

    def set_All_From_Data_Model_File_Information(self, index):
        self.ui.LE_Sample_ID.setText(
            self.data_Model.get_File_Data_By_Index_And_Key(
                index, "file_sample_id"))
        self.ui.LE_Sample_Name.setText(
            self.data_Model.get_File_Data_By_Index_And_Key(
                index, "file_sample_name"))
        self.ui.TE_Sample_Comment.setPlainText(
            self.data_Model.get_File_Data_By_Index_And_Key(
                index, "file_sample_comment"))

    def get_All_To_Data_Model_File_Information(self, index):
        self.data_Model.set_File_Data_By_Index_And_Key(
            index, "file_sample_id", self.ui.LE_Sample_ID.text())
        self.data_Model.set_File_Data_By_Index_And_Key(
            index, "file_sample_name", self.ui.LE_Sample_Name.text())
        self.data_Model.set_File_Data_By_Index_And_Key(
            index, "file_sample_comment",
            self.ui.TE_Sample_Comment.toPlainText())

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
