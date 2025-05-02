import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from forms.Window_Edit_Form_ui import Ui_MainWindow as Ui_Window_Edit_Form

from controller.TySubWidgetExperimentInformation import (
    TySubWidgetExperimentInformation,
)
from controller.TySubWidgetSampleInformation import (
    TySubWidgetSampleInformation,
)
from controller.TySubWidgetEquipmentInformation import (
    TySubWidgetEquipmentInformation,
)

# from TyMessageSender import MessageSenderException

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
import logging

from TyDocDataMemoTransfer import TyDocDataMemoTransfer


class TyWindowEditForm(QtWidgets.QMainWindow):
    signal_Update_Form = QtCore.pyqtSignal()

    def __init__(self, parent=None, doc=None, type_Form=None):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger(self.doc.loggerName)
        self.__loadUi()
        self.listTypeForm = [
            "experiment_information",
            "sample_information",
            "equipment_information",
        ]
        if type_Form is not None:
            self.type_Form = type_Form
        else:
            self.type_Form = None
        self.set_Signals()

    def __loadUi(self):
        if self.doc.isBuild:
            from views.FormDialogEditInformation import Ui_Dialog

            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormDialogEditInformation.ui", self)
            self.ui = self

    def set_Signals(self):
        self.ui.PB_OK.clicked.connect(self.save_Update)
        self.ui.PB_Cancel.clicked.connect(self.cancel_Update)
        self.ui.PB_Undo(self.Undo)

    def set_Data_Model(self, data_model):
        self.doc = data_model

    def set_Type_Form(self, type_Form):
        self.type_Form = type_Form

    def set_Input_Form(self):
        self.index_Form_Type = self.listTypeForm.index(self.type_Form)
        if self.index_Form_Type == 0:
            self.setWindowTitle("Edit Experiment")
            self.ui.LAB_Title.setText("Your Experiment")
            self.sub_Widget = TySubWidgetExperimentInformation(doc=self.doc)
            self.sub_Widget.set_All_From_Data_Model()
        elif self.index_Form_Type == 1:
            self.setWindowTitle("Edit Current Sample")
            self.ui.LAB_Title.setText("Current Sample")
            self.sub_Widget = TySubWidgetSampleInformation(doc=self.doc)
            self.sub_Widget.set_All_From_Data_Model()
        elif self.index_Form_Type == 2:
            self.setWindowTitle("Edit Current Equipment")
            self.ui.LAB_Title.setText("Current Equipment")
            self.sub_Widget = TySubWidgetEquipmentInformation(doc=self.doc)
            self.sub_Widget.set_All_From_Data_Model()
        self.ui.HL_Add_Widget.addWidget(self.sub_Widget)

    def save_Update(self):
        self.index_Form_Type = self.listTypeForm.index(self.type_Form)
        if self.index_Form_Type == 0:
            self.sub_Widget.get_All_To_Data_Model()
        elif self.index_Form_Type == 1:
            self.sub_Widget.get_All_To_Data_Model()
        elif self.index_Form_Type == 2:
            self.sub_Widget.get_All_To_Data_Model()

        self.doc.saveToTemporary()
        self.signal_Update_Form.emit()
        self.close()

    def cancel_Update(self):
        self.close()

    def Undo(self):
        self.close()
