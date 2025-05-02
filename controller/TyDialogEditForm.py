# from forms.Window_Edit_Form_ui import Ui_MainWindow as Ui_Window_Edit_Form
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

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
    signaUpdateToMetadataClipboard = QtCore.pyqtSignal()

    def __init__(
        self,
        parent=None,
        doc: TyDocDataMemoTransfer = None,
        typeForm: str = None,
        isTemplate: bool = True,
        index: int = -1,
    ):
        super().__init__(parent)
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger(self.doc.getLoggerName())

        if typeForm is not None:
            self.typeForm = typeForm
        else:
            self.typeForm = None

        self.listTypeForm = [
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

        self.setSignals()

    def __loadUi(self):
        if self.doc.getIsBuild():
            from views.FormDialogEditInformation import Ui_Dialog

            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormDialogEditInformation.ui", self)
            self.ui = self

    def setSignals(self):
        self.ui.PB_OK.clicked.connect(self.saveUpdate)
        self.ui.PB_Cancel.clicked.connect(self.cancelUpdate)
        self.ui.PB_Copy_From_Clipboard.clicked.connect(self.readCurrentSample)
        self.ui.PB_Paste_To_Clipboard.clicked.connect(self.pasteToClipboard)
        # self.ui.PB_Undo.clicked.connect(self.Undo)

    def setSignalUpdateToMetadataClipboard(self, signal: QtCore.pyqtSignal):
        self.signaUpdateToMetadataClipboard = signal

    def setDoc(self, doc):
        self.doc = doc

    def setTypeForm(self, typeForm):
        self.typeForm = typeForm

    def setInputForm(self):
        self.indexFormType = self.listTypeForm.index(self.typeForm)
        if self.indexFormType == 0:
            self.logger.info(f"Input Form Experiment, {self.indexFormType}")
            self.setWindowTitle("Edit Experiment")
            self.ui.LAB_Title.setText("Your Experiment")
            self.subWidget = TySubWidgetExperimentInformation(doc=self.doc)
            self.subWidget.getFromDoc(index=self.index, is_Template=self.isTemplate)
        elif self.indexFormType == 1:
            self.logger.info(f"Input Form Sample, {self.indexFormType}")
            self.setWindowTitle("Edit Current Sample")
            self.ui.LAB_Title.setText("Current Sample")
            self.subWidget = TySubWidgetSampleInformation(doc=self.doc)
            self.subWidget.getFromDoc(index=self.index, is_Template=self.isTemplate)
        elif self.indexFormType == 2:
            self.logger.info(f"Input Form Equipment, {self.indexFormType}")
            self.setWindowTitle("Edit Current Equipment")
            self.ui.LAB_Title.setText("Current Equipment")
            self.subWidget = TySubWidgetEquipmentInformation(doc=self.doc)
            self.subWidget.getFromDoc(index=self.index, is_Template=self.isTemplate)
        self.ui.HL_Add_Widget.addWidget(self.subWidget)

    def saveUpdate(self):
        self.indexFormType = self.listTypeForm.index(self.typeForm)
        self.subWidget.setToDoc(self.index, self.isTemplate)
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
        self.logger.info(f"Save update {self.typeForm} and Emit signal.")
        self.signaUpdateToMetadataClipboard.emit()
        self.close()

    def cancelUpdate(self):
        self.close()

    def readCurrentSample(self):
        self.subWidget.getFromDoc(index=self.index, is_Template=True)
        # if self.index_Form_Type == 0:
        #     self.sub_Widget.get_All_From_Data_Model()
        # elif self.index_Form_Type == 1:
        #     self.sub_Widget.get_All_From_Data_Model()
        # elif self.index_Form_Type == 2:
        #     self.sub_Widget.get_All_From_Data_Model()

    def pasteToClipboard(self):
        self.indexFormType = self.listTypeForm.index(self.typeForm)
        self.subWidget.setToDoc(self.index, is_Template=True)
        # if self.index_Form_Type == 0:
        #     self.sub_Widget.set_All_To_Data_Model()
        # elif self.index_Form_Type == 1:
        #     self.sub_Widget.set_All_To_Data_Model()
        # elif self.index_Form_Type == 2:
        #     self.sub_Widget.set_All_To_Data_Model()
        self.logger.debug(f"Paste to clipboard {self.typeForm}")
        self.doc.saveToTemporary()
        self.signaUpdateToMetadataClipboard.emit()

    def Undo(self):
        self.subWidget.undo()
