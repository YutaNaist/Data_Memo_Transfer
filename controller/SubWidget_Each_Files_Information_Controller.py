from forms.Widget_Each_Files_Information_ui import Ui_Form as Ui_Widget_Each_Files_Information

# from controller.SubWidget_Sample_Information_Controller import Sub_Widget_Sample_Information
# from controller.SubWidget_Equipment_Information_Controller import Sub_Widget_Equipment_Information
# from controller.Window_Edit_File_Information_Controller import Sub_Window_Edit_File_Information

from controller.Dialog_Edit_Form_Controller import Dialog_Edit_Form

from Data_Model import DataModel

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class Sub_Widget_Each_Files_Information(QtWidgets.QWidget):
    signal_Edit_Sample_Information = QtCore.pyqtSignal()

    def __init__(self, parent=None, data_Model=None):

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        # self.timer.start(600000)
        super().__init__(parent)
        self.ui = Ui_Widget_Each_Files_Information()
        self.ui.setupUi(self)
        self.file_Name = ""
        self.index = 0

        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()

        self.set_Signal()
        self.ui.PB_Edit_Equipment_Information.setIcon(
            QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Edit_Sample_Information.setIcon(
            QtGui.QIcon("./icons/edit.png"))

    def set_Signal(self):
        self.ui.RB_Valid.clicked.connect(self.set_Status_Classified)
        self.ui.RB_Not_Valid.clicked.connect(self.set_Status_Classified)
        self.ui.RB_No_Classified.clicked.connect(self.set_Status_Classified)
        # self.ui.TE_Free_Comment.cursorPosition.connect(
        #     self.set_File_Comment_To_Data_Model)
        self.ui.TE_Free_Comment.textChanged.connect(self.start_edit_Timer)
        self.timer.timeout.connect(self.set_File_Comment_To_Data_Model)
        self.ui.PB_Edit_Sample_Information.clicked.connect(
            self.edit_Sample_Information)
        self.ui.PB_Edit_Equipment_Information.clicked.connect(
            self.edit_Equipment_Information)
        self.signal_Edit_Sample_Information.connect(
            self.set_Text_From_Data_Model)

    def set_Parent_Widget(self, parent, parent_Index):
        self.parent_Widget = parent
        self.parent_Index = parent_Index

    def set_Data_Model(self, data_model):
        self.data_Model = data_model

    def set_File_Name(self, str_File_Name):
        self.file_Name = str_File_Name

    def set_Status_Classified(self):
        dict_File_Data = self.data_Model.get_File_Data_By_Index(self.index)
        status = self.get_Status_Classified()
        if status == "effective_data":
            dict_File_Data["file_status_classified"] = "effective_data"
            dict_File_Data["file_is_valid"] = True
        elif status == "not_effective_data":
            dict_File_Data["file_status_classified"] = "not_effective_data"
            dict_File_Data["file_is_valid"] = False
        else:
            dict_File_Data["file_status_classified"] = "not_classified"
            dict_File_Data["file_is_valid"] = False
        self.update_Title()
        self.data_Model.set_File_Data_By_Index(self.index, dict_File_Data)
        self.data_Model.save_To_Temporary()

    def get_Status_Classified(self):
        if self.ui.RB_Valid.isChecked():
            return "effective_data"
        elif self.ui.RB_Not_Valid.isChecked():
            return "not_effective_data"
        else:
            return "not_classified"

    def set_Index(self, index):
        self.index = index

    def set_classified(self, status_Classified):
        if status_Classified == "effective_data":
            self.ui.RB_Valid.setChecked(True)
            self.ui.RB_Not_Valid.setChecked(False)
            self.ui.RB_No_Classified.setChecked(False)
        elif status_Classified == "not_effective_data":
            self.ui.RB_Valid.setChecked(False)
            self.ui.RB_Not_Valid.setChecked(True)
            self.ui.RB_No_Classified.setChecked(False)
        else:
            self.ui.RB_Valid.setChecked(False)
            self.ui.RB_Not_Valid.setChecked(False)
            self.ui.RB_No_Classified.setChecked(True)

    def set_Text_From_Data_Model(self):
        # self.index = self.data_Model.check_Index_File_Name(self.file_Name)
        dict_File_Data = self.data_Model.get_File_Data_By_Index(self.index)

        self.ui.TE_Free_Comment.setPlainText(dict_File_Data["file_comment"])
        self.set_classified(dict_File_Data["file_status_classified"])

        self.set_Sample_And_Equipment_Information(self.index)
        self.update_Title()

    def update_Title(self):
        if self.get_Status_Classified() == "not_classified":
            self.parent_Widget.setItemText(self.parent_Index, self.file_Name)
            self.parent_Widget.setItemIcon(
                # self.parent_Index, QtGui.QIcon("./icons/NotClassified.png"))
                self.parent_Index,
                QtGui.QIcon("./icons/FileIcon_red.png"))
        else:
            self.parent_Widget.setItemText(self.parent_Index, self.file_Name)
            self.parent_Widget.setItemIcon(
                # self.parent_Index, QtGui.QIcon("./icons/Classified.png"))
                self.parent_Index,
                QtGui.QIcon("./icons/FileIcon.png"))

    def set_File_Comment_To_Data_Model(self):
        self.data_Model.set_File_Data_By_Index_And_Key(
            self.index, "file_comment", self.ui.TE_Free_Comment.toPlainText())
        self.data_Model.save_To_Temporary()

    def start_edit_Timer(self):
        self.timer.start(5000)

    def edit_Sample_Information(self):
        # self.sub_Window_Edit_Sample_Information = Sub_Window_Edit_File_Information(
        #     data_Model=self.data_Model, index_File_Information=self.index)
        # self.sub_Window_Edit_Sample_Information.set_Parent_Signal(
        #     self.signal_Edit_Sample_Information)
        # self.sub_Window_Edit_Sample_Information.show()
        self.dialog_Edit_Sample_Information = Dialog_Edit_Form(
            data_Model=self.data_Model,
            type_Form="sample_information",
            isTemplate=False,
            index=self.index)
        self.dialog_Edit_Sample_Information.set_Input_Form()
        self.dialog_Edit_Sample_Information.show()
        self.dialog_Edit_Sample_Information.signal_Update_Form.connect(
            self.update_Sample_And_Equipment_Information)
        # print("check sample")
        # self.set_Sample_And_Equipment_Information(self.index)
        # self.update_Title()

    def edit_Equipment_Information(self):
        # self.sub_Window_Edit_Sample_Information = Sub_Window_Edit_File_Information(
        #     data_Model=self.data_Model, index_File_Information=self.index)
        # self.sub_Window_Edit_Sample_Information.set_Parent_Signal(
        #     self.signal_Edit_Sample_Information)
        # self.sub_Window_Edit_Sample_Information.show()
        self.dialog_Edit_Sample_Information = Dialog_Edit_Form(
            data_Model=self.data_Model,
            type_Form="equipment_information",
            isTemplate=False,
            index=self.index)
        self.dialog_Edit_Sample_Information.set_Input_Form()
        self.dialog_Edit_Sample_Information.signal_Update_Form.connect(
            self.update_Sample_And_Equipment_Information)
        self.dialog_Edit_Sample_Information.show()
        # print("check equipment")
        # self.set_Sample_And_Equipment_Information(self.index)
        # self.update_Title()

    def set_Sample_And_Equipment_Information(self, index):
        dict_File_Data = self.data_Model.get_File_Data_By_Index(index)
        str_File_Information = ""
        str_File_Information += "Sample Name: {}\n".format(
            dict_File_Data["file_sample_name"])
        str_File_Information += "Sample ID: {}\n".format(
            dict_File_Data["file_sample_id"])
        str_File_Information += "Sample Comment: {}\n".format(
            dict_File_Data["file_sample_comment"])
        str_Equipment_Information = ""
        str_Equipment_Information += "Experiment Method: {}\n".format(
            dict_File_Data["file_equipment_contents"]["experiment_method"])
        if len(dict_File_Data["file_equipment_contents"]) > 1:
            for i in range(len(dict_File_Data["file_equipment_contents"]) - 1):
                key = dict_File_Data["file_equipment_contents"].keys()[i + 1]
                str_Equipment_Information += "{}: {}\n".format(
                    key, dict_File_Data["file_equipment_content"][key])
        self.ui.TE_SampleInfo.setPlainText(str_File_Information)
        self.ui.TE_EquipmentInfo.setPlainText(str_Equipment_Information)

    def update_Sample_And_Equipment_Information(self):
        self.set_Sample_And_Equipment_Information(self.index)
        self.update_Title()
