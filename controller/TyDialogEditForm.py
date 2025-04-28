# from forms.Window_Edit_Form_ui import Ui_MainWindow as Ui_Window_Edit_Form
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer

# from forms.Dialog_Edit_Form_ui import Ui_Dialog as Ui_Dialog_Edit_Form

from controller.TySubWidgetExperimentInformation import (
    TySubWidgetExperimentInformation,
)
from controller.TySubWidgetSampleInformation import (
    TySubWidgetSampleInformation,
)
from controller.TySubWidgetEquipmentInformation import (
    TySubWidgetEquipmentInformation,
)

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic


class Dialog_Edit_Form(QtWidgets.QDialog):
    signal_update_to_metadata_clipboard = QtCore.pyqtSignal()

    def __init__(
        self, parent=None, doc=None, type_Form=None, isTemplate=True, index=-1
    ):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()

        if type_Form is not None:
            self.type_Form = type_Form
        else:
            self.type_Form = None

        self.list_Type_Form = [
            "experiment_information",
            "sample_information",
            "equipment_information",
        ]

        # self.ui = Ui_Dialog_Edit_Form()
        self.__loadUi()
        self.isTemplate = isTemplate
        if isTemplate is True:
            self.ui.PB_Copy_From_Clipboard.setVisible(False)
            self.ui.PB_Paste_To_Clipboard.setVisible(False)
            self.index = -1
        else:
            self.index = index

        # self.ui.setupUi(self)
        # if isTemplate is True:
        # self.ui.PB_OK.setVisible(False)

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
        self.ui.PB_Copy_From_Clipboard.clicked.connect(self.read_Current_Sample)
        self.ui.PB_Paste_To_Clipboard.clicked.connect(self.paste_To_Clipboard)
        # self.ui.PB_Undo.clicked.connect(self.Undo)

    def set_Signal_Update_To_Metadata_Clipboard(self, signal: QtCore.pyqtSignal):
        self.signal_update_to_metadata_clipboard = signal

    def set_Data_Model(self, data_model):
        self.doc = data_model

    def set_Type_Form(self, type_Form):
        self.type_Form = type_Form

    def set_Input_Form(self):
        self.index_Form_Type = self.list_Type_Form.index(self.type_Form)
        if self.index_Form_Type == 0:
            self.setWindowTitle("Edit Experiment")
            self.ui.LAB_Title.setText("Your Experiment")
            self.sub_Widget = TySubWidgetExperimentInformation(doc=self.doc)
            self.sub_Widget.get_From_Data_Model(
                index=self.index, is_Template=self.isTemplate
            )
        elif self.index_Form_Type == 1:
            self.setWindowTitle("Edit Current Sample")
            self.ui.LAB_Title.setText("Current Sample")
            self.sub_Widget = TySubWidgetSampleInformation(doc=self.doc)
            self.sub_Widget.get_From_Data_Model(
                index=self.index, is_Template=self.isTemplate
            )
        elif self.index_Form_Type == 2:
            self.setWindowTitle("Edit Current Equipment")
            self.ui.LAB_Title.setText("Current Equipment")
            self.sub_Widget = TySubWidgetEquipmentInformation(doc=self.doc)
            self.sub_Widget.get_From_Data_Model(
                index=self.index, is_Template=self.isTemplate
            )
        self.ui.HL_Add_Widget.addWidget(self.sub_Widget)

    def save_Update(self):
        self.index_Form_Type = self.list_Type_Form.index(self.type_Form)
        self.sub_Widget.set_To_Data_Model(self.index, self.isTemplate)
        """
            if self.index_Form_Type == 0:
                self.sub_Widget.set_All_To_Data_Model()
            elif self.index_Form_Type == 1:
                self.sub_Widget.set_All_To_Data_Model()
            elif self.index_Form_Type == 2:
                self.sub_Widget.set_All_To_Data_Model()
        else:
            if self.index_Form_Type == 0:
                self.sub_Widget.set_All_To_Data_Model_File_Information(
                    self.index)
            elif self.index_Form_Type == 1:
                self.sub_Widget.set_All_To_Data_Model_File_Information(
                    self.index)
            elif self.index_Form_Type == 2:
                self.sub_Widget.set_All_To_Data_Model_File_Information(
                    self.index)
        """
        self.doc.saveToTemporary()
        self.signal_update_to_metadata_clipboard.emit()
        self.close()

    def cancel_Update(self):
        self.close()

    def read_Current_Sample(self):
        self.sub_Widget.get_From_Data_Model(index=self.index, is_Template=True)
        # if self.index_Form_Type == 0:
        #     self.sub_Widget.get_All_From_Data_Model()
        # elif self.index_Form_Type == 1:
        #     self.sub_Widget.get_All_From_Data_Model()
        # elif self.index_Form_Type == 2:
        #     self.sub_Widget.get_All_From_Data_Model()

    def paste_To_Clipboard(self):
        self.index_Form_Type = self.list_Type_Form.index(self.type_Form)
        self.sub_Widget.set_To_Data_Model(self.index, is_Template=True)
        # if self.index_Form_Type == 0:
        #     self.sub_Widget.set_All_To_Data_Model()
        # elif self.index_Form_Type == 1:
        #     self.sub_Widget.set_All_To_Data_Model()
        # elif self.index_Form_Type == 2:
        #     self.sub_Widget.set_All_To_Data_Model()
        self.doc.saveToTemporary()
        self.signal_update_to_metadata_clipboard.emit()

    def Undo(self):
        self.sub_Widget.undo()
