from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer

# from forms.Widget_Each_Files_Information_ui import (
#     Ui_Form as Ui_Widget_Each_Files_Information,
# )
from controller.TyDialogEditForm import Dialog_Edit_Form
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import uic


class TySubWidgetEachFiles(QtWidgets.QWidget):
    signal_Edit_Sample_Information = QtCore.pyqtSignal()
    signalUpdataToMetadataClipboard = QtCore.pyqtSignal()

    # signal_update_text_box

    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        super().__init__(parent)

        # self.ui = Ui_Widget_Each_Files_Information()
        # self.ui.setupUi(self)
        self.__loadUi()
        self.fileName = ""
        self.index = 0

        # print()
        # print(self.data_Model.get_All_Dict_Data_Model())
        # print()

        if self.doc.getDictExperimentInformation("is_upload_arim") is False:
            # self.ui.GB_ARIM_Upload.setVisible(False)
            self.ui.RB_ARIM_Upload.setVisible(False)
            self.ui.RB_ARIM_Not_Upload.setVisible(False)

        self.setSignal()
        self.ui.PB_Edit_Equipment_Information.setIcon(QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Edit_Sample_Information.setIcon(QtGui.QIcon("./icons/edit.png"))

    def __loadUi(self):
        if self.doc.isBuild:
            from views.FormSubWidgetEachFile import Ui_Form

            self.ui = Ui_Form()
            self.ui.setupUi(self)
            self.setWindowTitle("File Information")
        else:
            uic.loadUi(r"forms/FormSubWidgetEachFile.ui", self)
            self.ui = self

    def setSignal(self) -> None:
        self.ui.RB_Valid.clicked.connect(self.updateFileClassification)
        self.ui.RB_Not_Valid.clicked.connect(self.updateFileClassification)
        self.ui.RB_No_Classified.clicked.connect(self.updateFileClassification)
        self.ui.RB_ARIM_Upload.clicked.connect(self.setStatusArimUpload)
        self.ui.RB_ARIM_Not_Upload.clicked.connect(self.setStatusArimUpload)
        # self.ui.TE_Free_Comment.cursorPosition.connect(
        #     self.set_File_Comment_To_Data_Model)
        self.ui.TE_Free_Comment.textChanged.connect(self.startEditTimer)
        self.timer.timeout.connect(self.setFileCommentToDoc)
        self.ui.PB_Edit_Sample_Information.clicked.connect(self.editSampleInformation)
        self.ui.PB_Edit_Equipment_Information.clicked.connect(
            self.editEquipmentInformation
        )
        self.signal_Edit_Sample_Information.connect(self.setTextFromDoc)

    def setSignalUpdateToMetadataClipboard(self, signal: QtCore.pyqtSignal) -> None:
        self.signalUpdataToMetadataClipboard = signal
        self.signalUpdataToMetadataClipboard.connect(
            self.updateSampleAndEquipmentInformation
        )

        # self.dialog_Edit_Sample_Information.signal_Update_Form.connect(
        #     self.update_Sample_And_Equipment_Information)

    def setParentWidget(self, parent, parentIndex) -> None:
        self.parentWidget = parent
        self.parentIndex = parentIndex

    def setDoc(self, doc: TyDocDataMemoTransfer) -> None:
        self.doc = doc

    def setFileName(self, strFileName) -> None:
        self.fileName = strFileName

    def updateFileClassification(self) -> None:
        dictFileData = self.doc.getFileInformation(self.index)
        status = self.getStatusClassification()
        if status == "effective_data":
            dictFileData["classified"] = "effective_data"
            dictFileData["valid"] = True
        elif status == "not_effective_data":
            dictFileData["classified"] = "not_effective_data"
            dictFileData["valid"] = False
        else:
            dictFileData["classified"] = "not_classified"
            dictFileData["valid"] = False
        self.updateTitle()
        self.doc.setFileInformation(self.index, dictFileData)
        self.doc.saveToTemporary()

    def getStatusClassification(self):
        if self.ui.RB_Valid.isChecked():
            return "effective_data"
        elif self.ui.RB_Not_Valid.isChecked():
            return "not_effective_data"
        else:
            return "not_classified"

    def setStatusArimUpload(self) -> None:
        dictFileData = self.doc.getFileInformation(self.index)
        if self.ui.RB_ARIM_Upload.isChecked():
            dictFileData["arim_upload"] = True
        else:
            dictFileData["arim_upload"] = False
        self.doc.setFileInformation(self.index, dictFileData)
        self.doc.saveToTemporary()

    def getStatusArimUpload(self) -> bool:
        if self.ui.RB_ARIM_Upload.isChecked():
            return True
        else:
            return False

    def setIndex(self, index: int) -> None:
        self.index = index

    def setClassification(self, statusClassification: str) -> None:
        if statusClassification == "effective_data":
            self.ui.RB_Valid.setChecked(True)
            self.ui.RB_Not_Valid.setChecked(False)
            self.ui.RB_No_Classified.setChecked(False)
        elif statusClassification == "not_effective_data":
            self.ui.RB_Valid.setChecked(False)
            self.ui.RB_Not_Valid.setChecked(True)
            self.ui.RB_No_Classified.setChecked(False)
        else:
            self.ui.RB_Valid.setChecked(False)
            self.ui.RB_Not_Valid.setChecked(False)
            self.ui.RB_No_Classified.setChecked(True)

    def setArimUpload(self, statusArimUpload: bool) -> None:
        if statusArimUpload:
            self.ui.RB_ARIM_Upload.setChecked(True)
            self.ui.RB_ARIM_Not_Upload.setChecked(False)
        else:
            self.ui.RB_ARIM_Upload.setChecked(False)
            self.ui.RB_ARIM_Not_Upload.setChecked(True)

    def setTextFromDoc(self) -> None:
        # self.index = self.data_Model.check_Index_File_Name(self.file_Name)
        dict_File_Data = self.doc.getFileInformation(self.index)
        self.ui.TE_Free_Comment.setPlainText(dict_File_Data["comment"])
        self.setClassification(dict_File_Data["classified"])
        self.setArimUpload(dict_File_Data["arim_upload"])
        self.setSampleAndEquipmentInformation(self.index)
        self.updateTitle()

    def updateTitle(self) -> None:
        if self.getStatusClassification() == "not_classified":
            self.parentWidget.setItemText(self.parentIndex, self.fileName)
            self.parentWidget.setItemIcon(
                # self.parent_Index, QtGui.QIcon("./icons/NotClassified.png"))
                self.parentIndex,
                QtGui.QIcon("./icons/FileIcon_red.png"),
            )
        else:
            self.parentWidget.setItemText(self.parentIndex, self.fileName)
            self.parentWidget.setItemIcon(
                # self.parent_Index, QtGui.QIcon("./icons/Classified.png"))
                self.parentIndex,
                QtGui.QIcon("./icons/FileIcon.png"),
            )

    def setFileCommentToDoc(self) -> None:
        dictFileData = self.doc.getFileInformation(self.index)
        dictFileData["comment"] = self.ui.TE_Free_Comment.toPlainText()
        self.doc.setFileInformation(self.index, dictFileData)
        self.doc.saveToTemporary()

    def startEditTimer(self):
        self.timer.start(5000)

    def editSampleInformation(self) -> None:
        # self.sub_Window_Edit_Sample_Information = Sub_Window_Edit_File_Information(
        #     data_Model=self.data_Model, index_File_Information=self.index)
        # self.sub_Window_Edit_Sample_Information.set_Parent_Signal(
        #     self.signal_Edit_Sample_Information)
        # self.sub_Window_Edit_Sample_Information.show()
        self.dialogEditSampleInformation = Dialog_Edit_Form(
            doc=self.doc,
            type_Form="sample_information",
            isTemplate=False,
            index=self.index,
        )
        self.dialogEditSampleInformation.setInputForm()
        self.dialogEditSampleInformation.setSignalUpdateToMetadataClipboard(
            self.signalUpdataToMetadataClipboard
        )
        self.dialogEditSampleInformation.show()
        # self.dialog_Edit_Sample_Information.signal_Update_Form.connect(
        #     self.update_Sample_And_Equipment_Information)

        # print("check sample")
        # self.set_Sample_And_Equipment_Information(self.index)
        # self.update_Title()

    def editEquipmentInformation(self):
        # self.sub_Window_Edit_Sample_Information = Sub_Window_Edit_File_Information(
        #     data_Model=self.data_Model, index_File_Information=self.index)
        # self.sub_Window_Edit_Sample_Information.set_Parent_Signal(
        #     self.signal_Edit_Sample_Information)
        # self.sub_Window_Edit_Sample_Information.show()
        self.dialogEditEquipmentInformation = Dialog_Edit_Form(
            doc=self.doc,
            type_Form="equipment_information",
            isTemplate=False,
            index=self.index,
        )
        self.dialogEditEquipmentInformation.setInputForm()
        self.dialogEditEquipmentInformation.setSignalUpdateToMetadataClipboard(
            self.signalUpdataToMetadataClipboard
        )
        # self.dialog_Edit_Equipment_Information.signal_Update_Form.connect(
        #     self.update_Sample_And_Equipment_Information)
        self.dialogEditEquipmentInformation.show()
        # print("check equipment")
        # self.set_Sample_And_Equipment_Information(self.index)
        # self.update_Title()

    def setSampleAndEquipmentInformation(self, index: int) -> None:
        dictFileData = self.doc.getFileInformation(index)
        strFileInformation = ""
        strFileInformation += "Sample Name: {}\n".format(
            dictFileData["sample"]["name"]
        )
        strFileInformation += "Sample ID: {}\n".format(dictFileData["sample"]["id"])
        strFileInformation += "Sample Comment: {}\n".format(
            dictFileData["sample"]["comment"]
        )
        strEquipmentInformation = ""
        strEquipmentInformation += "Experiment Method: {}\n".format(
            dictFileData["equipment"]["method"]
        )
        if len(dictFileData["equipment"].keys()) > 1:
            for i in range(len(dictFileData["equipment"].keys) - 1):
                key = dictFileData["equipment"].keys()[i + 1]
                strEquipmentInformation += "{}: {}\n".format(
                    key, dictFileData["equipment"][key]
                )
        self.ui.TE_SampleInfo.setPlainText(strFileInformation)
        self.ui.TE_EquipmentInfo.setPlainText(strEquipmentInformation)

    def updateSampleAndEquipmentInformation(self):
        self.setSampleAndEquipmentInformation(self.index)
        self.updateTitle()
