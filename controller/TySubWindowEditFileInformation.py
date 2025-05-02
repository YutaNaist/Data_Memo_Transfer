# from forms.Window_Edit_File_Information_ui import (
#     Ui_MainWindow as Ui_Window_Edit_File_Information,
# )

from controller.TySubWidgetSampleInformation import (
    TySubWidgetSampleInformation,
)
from controller.TySubWidgetEquipmentInformation import (
    TySubWidgetEquipmentInformation,
)

from TyDocDataMemoTransfer import TyDocDataMemoTransfer

from PyQt5 import QtWidgets
from PyQt5 import uic
import logging


class TySubWindowEditFileInformation(QtWidgets.QMainWindow):
    def __init__(self, parent=None, doc=None, indexFileInformation: int = 0):
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        super().__init__(parent)
        self.logger = logging.getLogger(self.doc.getLoggerName())
        self.__LoadUI()
        self.indexFileInformation = indexFileInformation
        self.setFileInformation()

        self.set_Signal()

    def __LoadUI(self):
        if self.doc.getIsBuild():
            from views.FormSubWidgetEachFile import Ui_Form

            self.ui = Ui_Form()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormSubWidgetEachFile.ui", self)
            self.ui = self

    def setFileInformation(self) -> None:
        """Set the file information index."""
        self.sub_Widget_Equipment_Information = TySubWidgetEquipmentInformation(
            doc=self.doc
        )
        self.sub_Widget_Sample_Information = TySubWidgetSampleInformation(doc=self.doc)
        self.file_Name = self.doc.get_File_Data_By_Index_And_Key(
            self.indexFileInformation, "file_name"
        )
        self.setWindowTitle(self.file_Name)
        self.ui.LAB_Sample.setText("Sample of " + self.file_Name)
        self.ui.LAB_Equipment.setText("Equipment of " + self.file_Name)

        self.sub_Widget_Sample_Information.set_All_From_Data_Model_File_Information(
            self.indexFileInformation
        )
        self.sub_Widget_Equipment_Information.set_All_From_Data_Model_File_Information(
            self.indexFileInformation
        )

        self.ui.VL_Sample_Information.addWidget(self.sub_Widget_Sample_Information)
        self.ui.VL_Instrument_Information.addWidget(
            self.sub_Widget_Equipment_Information
        )

    def set_Signal(self):
        self.ui.PB_OK.clicked.connect(self.set_To_Parent_File_Information)
        self.ui.PB_Cancel.clicked.connect(self.close)
        self.ui.PB_Read_Current_Information_2.clicked.connect(
            self.read_Current_Template
        )

    def set_Parent_Signal(self, parent_Signal):
        self.signal_Edit_Sample_Information = parent_Signal

    def set_To_Parent_File_Information(self):
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation,
            "file_sample_id",
            self.sub_Widget_Sample_Information.ui.LE_Sample_ID.text(),
        )
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation,
            "file_sample_name",
            self.sub_Widget_Sample_Information.ui.LE_Sample_Name.text(),
        )
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation,
            "file_sample_comment",
            self.sub_Widget_Sample_Information.ui.TE_Sample_Comment.toPlainText(),
        )
        self.signal_Edit_Sample_Information.emit()
        self.close()

    def read_Current_Template(self):
        current_Template = self.doc.get_All_Template_Data()
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation, "file_sample_id", current_Template["sample_id"]
        )
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation,
            "file_sample_name",
            current_Template["sample_name"],
        )
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation,
            "file_sample_comment",
            current_Template["sample_comment"],
        )
        self.doc.set_File_Data_By_Index_And_Key(
            self.indexFileInformation,
            "file_equipment_contents",
            current_Template["equipment_contents"],
        )

        self.sub_Widget_Sample_Information.set_All_From_Data_Model_File_Information(
            self.indexFileInformation
        )
        self.sub_Widget_Equipment_Information.set_All_From_Data_Model_File_Information(
            self.indexFileInformation
        )
