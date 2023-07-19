# from forms.Window_Edit_Form_ui import Ui_MainWindow as Ui_Window_Edit_Form
from forms.Dialog_Edit_Form_ui import Ui_Dialog as Ui_Dialog_Edit_Form

from controller.SubWidget_Experiment_Information_Controller import Sub_Widget_Experiment_Information
from controller.SubWidget_Sample_Information_Controller import Sub_Widget_Sample_Information
from controller.SubWidget_Equipment_Information_Controller import Sub_Widget_Equipment_Information

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from Data_Model import DataModel


class Dialog_Edit_Form(QtWidgets.QDialog):
    signal_Update_Form = QtCore.pyqtSignal()

    def __init__(self,
                 parent=None,
                 data_Model=None,
                 type_Form=None,
                 isTemplate=True,
                 index=-1):
        super().__init__(parent)
        self.ui = Ui_Dialog_Edit_Form()
        self.ui.setupUi(self)
        # if isTemplate is True:
        # self.ui.PB_OK.setVisible(False)

        self.list_Type_Form = [
            "experiment_information", "sample_information",
            "equipment_information"
        ]

        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()

        if type_Form is not None:
            self.type_Form = type_Form
        else:
            self.type_Form = None

        self.isTemplate = isTemplate
        if isTemplate is True:
            self.ui.PB_Current_Sample.setVisible(False)
        else:
            self.index = index

        self.set_Signals()

    def set_Signals(self):
        self.ui.PB_OK.clicked.connect(self.save_Update)
        self.ui.PB_Cancel.clicked.connect(self.cancel_Update)
        self.ui.PB_Current_Sample.clicked.connect(self.read_Current_Sample)

    def set_Data_Model(self, data_model):
        self.data_Model = data_model

    def set_Type_Form(self, type_Form):
        self.type_Form = type_Form

    def set_Input_Form(self):
        self.index_Form_Type = self.list_Type_Form.index(self.type_Form)
        if self.isTemplate is True:
            if self.index_Form_Type == 0:
                self.setWindowTitle("Edit Experiment")
                self.ui.LAB_Title.setText("Your Experiment")
                self.sub_Widget = Sub_Widget_Experiment_Information(
                    data_Model=self.data_Model)
                self.sub_Widget.set_All_From_Data_Model()
            elif self.index_Form_Type == 1:
                self.setWindowTitle("Edit Current Sample")
                self.ui.LAB_Title.setText("Current Sample")
                self.sub_Widget = Sub_Widget_Sample_Information(
                    data_Model=self.data_Model)
                self.sub_Widget.set_All_From_Data_Model()
            elif self.index_Form_Type == 2:
                self.setWindowTitle("Edit Current Equipment")
                self.ui.LAB_Title.setText("Current Equipment")
                self.sub_Widget = Sub_Widget_Equipment_Information(
                    data_Model=self.data_Model)
                self.sub_Widget.set_All_From_Data_Model()
        else:
            if self.index_Form_Type == 0:
                self.setWindowTitle("Edit Experiment")
                self.ui.LAB_Title.setText("Your Experiment")
                self.sub_Widget = Sub_Widget_Experiment_Information(
                    data_Model=self.data_Model)
                self.sub_Widget.set_All_From_Data_Model()
            elif self.index_Form_Type == 1:
                self.setWindowTitle("Edit Current Sample")
                self.ui.LAB_Title.setText("Current Sample")
                self.sub_Widget = Sub_Widget_Sample_Information(
                    data_Model=self.data_Model)
                self.sub_Widget.set_All_From_Data_Model_File_Information(
                    self.index)
            elif self.index_Form_Type == 2:
                self.setWindowTitle("Edit Current Equipment")
                self.ui.LAB_Title.setText("Current Equipment")
                self.sub_Widget = Sub_Widget_Equipment_Information(
                    data_Model=self.data_Model)
                self.sub_Widget.set_All_From_Data_Model_File_Information(
                    self.index)
        self.ui.HL_Add_Widget.addWidget(self.sub_Widget)

    def save_Update(self):
        self.index_Form_Type = self.list_Type_Form.index(self.type_Form)
        if self.isTemplate is True:
            if self.index_Form_Type == 0:
                self.sub_Widget.get_All_To_Data_Model()
            elif self.index_Form_Type == 1:
                self.sub_Widget.get_All_To_Data_Model()
            elif self.index_Form_Type == 2:
                self.sub_Widget.get_All_To_Data_Model()
        else:
            if self.index_Form_Type == 0:
                self.sub_Widget.get_All_To_Data_Model_File_Information(
                    self.index)
            elif self.index_Form_Type == 1:
                self.sub_Widget.get_All_To_Data_Model_File_Information(
                    self.index)
            elif self.index_Form_Type == 2:
                self.sub_Widget.get_All_To_Data_Model_File_Information(
                    self.index)

        self.data_Model.save_To_Temporary()
        self.signal_Update_Form.emit()
        self.close()

    def cancel_Update(self):
        self.close()

    def read_Current_Sample(self):
        if self.index_Form_Type == 0:
            self.sub_Widget.set_All_From_Data_Model()
        elif self.index_Form_Type == 1:
            self.sub_Widget.set_All_From_Data_Model()
        elif self.index_Form_Type == 2:
            self.sub_Widget.set_All_From_Data_Model()
