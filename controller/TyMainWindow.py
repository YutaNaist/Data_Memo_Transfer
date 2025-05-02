from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer


# import forms.MainWindow_ui as MainWidow_ui

# from controller.Window_Edit_Form_Controller import Window_Edit_Form
from controller.TyDialogEditForm import Dialog_Edit_Form
from controller.TySubWidgetEachFiles import (
    TySubWidgetEachFiles,
)

from controller.TySubWidgetExperimentInformation import (
    TySubWidgetExperimentInformation,
)
from controller.TySubWidgetSampleInformation import (
    TySubWidgetSampleInformation,
)
from controller.TySubWidgetEquipmentInformation import (
    TySubWidgetEquipmentInformation,
)

# from TyMessageSender import TyMessageSender
from TyMessageSender import MessageSenderException

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic

import copy
import glob
import os
import logging
from typing import List


class TyMainWindow(QtWidgets.QMainWindow):
    # signal_Update_Data_Model = QtCore.pyqtSignal()
    # signal_Get_SampleInfo = QtCore.pyqtSignal()
    signalUpdateToMetadataClipboard = QtCore.pyqtSignal()

    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        self.logger = logging.getLogger(self.doc.getLoggerName())
        self.isForceCloseWindow = False

        self.currentIndexToolBox = 0

        super().__init__(parent)
        # self.ui = MainWidow_ui.Ui_MainWindow()
        # self.ui.setupUi(self)
        self.__loadUi()
        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint
        #                     | QtCore.Qt.WindowMinimizeButtonHint
        #                     | QtCore.Qt.WindowMaximizeButtonHint
        #                     | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Data Memo Transfer")
        self.ui.toolBox.removeItem(0)
        self.__setSignals()
        self.initializeForms()
        self.refreshFiles()
        # self.ui.HL_AddSampleInformation.addWidget(self.subWidSampleInfo)
        # self.ui.PB_Upload_Data.isEnabled = False
        # self.load_Information_Temporals()

    # def __del__(self):
    #     self.finish_Experiment()
    def __loadUi(self) -> None:
        if self.doc.getIsBuild():
            from views.FormMainWindow import Ui_MainWindow

            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms\FormMainWindow.ui", self)
            self.ui = self

    def __setSignals(self) -> None:
        self.ui.PB_Refresh.clicked.connect(self.refreshFiles)
        self.ui.toolBox.currentChanged.connect(self.changeToolboxIndex)
        self.ui.PB_Experiment_Title_Edit.clicked.connect(self.editExperimentInformation)
        self.ui.PB_Sample_ID_Edit.clicked.connect(self.editSampleInformation)
        self.ui.PB_Experiment_Method_Edit.clicked.connect(self.editEquipmentInformation)
        # self.ui.PB_Upload_Data.clicked.connect(self.finish_Experiment)
        self.ui.PB_Upload_Data.clicked.connect(self.close)
        self.signalUpdateToMetadataClipboard.connect(self.setTemplateFormByDoc)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.isForceCloseWindow:
            self.logger.debug("Force close window.")
            event.accept()
        else:
            finishStatus = self.finishExperiment()
            if finishStatus:
                event.accept()
            else:
                event.ignore()

    def changeToolboxIndex(self, index: int) -> None:
        self.currentIndexToolBox = index

    # def change_ToolBox_Title(self, index):
    #     pass

    def initializeForms(self) -> None:
        self.logger.info("Start to initialize forms.")
        self.ui.PB_Experiment_Title_Edit.setIcon(QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Sample_ID_Edit.setIcon(QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Experiment_Method_Edit.setIcon(QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Refresh.setIcon(QtGui.QIcon("./icons/reflesh.png"))
        self.ui.PB_Upload_Data.setIcon(QtGui.QIcon("./icons/Exit2.png"))
        pixmap = QtGui.QPixmap("./icons/FileIcon.png")
        pixmap = pixmap.scaled(
            25, 25, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        self.ui.LAB_Confirmed.setPixmap(pixmap)

        pixmap_red = QtGui.QPixmap("./icons/FileIcon_red.png")
        pixmap_red = pixmap_red.scaled(
            25, 25, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        self.ui.LAB_UnConfirmed.setPixmap(pixmap_red)
        self.subWidgetExperiment = TySubWidgetExperimentInformation(
            doc=self.doc, isEditable=False
        )
        self.subWidgetSample = TySubWidgetSampleInformation(
            doc=self.doc, isEditable=False
        )
        self.subWidgetEquipment = TySubWidgetEquipmentInformation(
            doc=self.doc, isEditable=False
        )
        self.ui.VL_Experiment.addWidget(self.subWidgetExperiment)
        self.ui.VL_Sample.addWidget(self.subWidgetSample)
        self.ui.VL_Equipment.addWidget(self.subWidgetEquipment)

        self.setTemplateFormByDoc()
        self.logger.info("finish initializing main window forms")
        # if self.data_Model.get_File_Names() != []:
        #     self.refresh_Files()

    def setTemplateFormByDoc(self) -> None:
        strExperimentIdText = "Experiment ID : {}".format(
            self.doc.getDictExperimentInformation("str_experiment_id")
        )
        self.ui.LAB_Experiment_ID.setText(strExperimentIdText)
        self.subWidgetExperiment.getFromDoc()
        self.subWidgetSample.getFromDoc()
        self.subWidgetEquipment.getFromDoc()

    def editExperimentInformation(self) -> None:
        self.windowEditForm = Dialog_Edit_Form(
            doc=self.doc,
            typeForm="experiment_information",
            isTemplate=True,
        )
        self.windowEditForm.setInputForm()
        self.windowEditForm.setSignalUpdateToMetadataClipboard(
            self.signalUpdateToMetadataClipboard
        )
        self.windowEditForm.show()

    def editSampleInformation(self) -> None:
        self.windowEditForm = Dialog_Edit_Form(
            doc=self.doc, typeForm="sample_information", isTemplate=True
        )
        self.windowEditForm.setInputForm()
        self.windowEditForm.setSignalUpdateToMetadataClipboard(
            self.signalUpdateToMetadataClipboard
        )
        self.windowEditForm.show()

    def editEquipmentInformation(self) -> None:
        self.windowEditForm = Dialog_Edit_Form(
            doc=self.doc,
            typeForm="equipment_information",
            isTemplate=True,
        )
        self.windowEditForm.setInputForm()
        self.windowEditForm.setSignalUpdateToMetadataClipboard(
            self.signalUpdateToMetadataClipboard
        )
        self.windowEditForm.show()

    def refreshFiles(self) -> None:
        self.logger.info("start refreshing files")

        def checkIndex(strFileName: str, listFileNames: List[str]) -> int:
            if strFileName in listFileNames:
                return listFileNames.index(strFileName)
            else:
                return -1

        self.ui.LAB_File_List.setText("File List")
        # save_Directory = self.data_Model.get_Dict_Data_Model(
        #    "str_share_directory_in_storage")
        saveDirectory = self.doc.getDictExperimentInformation("str_save_directory")
        listFilesInSaveDirectoryOriginal = glob.glob(
            saveDirectory + "/**", recursive=True
        )
        self.logger.info(f"Save directory: {saveDirectory}")
        self.logger.info(
            f"List of files in save directory: {listFilesInSaveDirectoryOriginal}"
        )
        lenBaseDir = len(saveDirectory)
        listFilesInSaveDirectory = []
        xs = []
        for file in listFilesInSaveDirectoryOriginal:
            if os.path.samefile(file, saveDirectory):
                continue
            path = os.path.join(saveDirectory, file)
            xs.append((os.path.getmtime(path), file))
        self.logger.debug(f"xs: {xs}")

        for _, file in sorted(xs):
            listFilesInSaveDirectory.append(file)
        newListFileNames = []
        newListFileData = []
        # self.data_Model.reset_File_Data()
        focusedIndex = self.currentIndexToolBox
        focusedFileName = self.ui.toolBox.itemText(focusedIndex)

        for i in range(self.ui.toolBox.count()):
            self.ui.toolBox.removeItem(0)

        count = 0

        listFIlenames = self.doc.getFileNameList()
        oldListFileData = copy.copy(
            self.doc.getDictExperimentInformation("list_file_data")
        )
        self.doc.resetFileData()

        for i, file in enumerate(listFilesInSaveDirectory):
            file = file.replace("\\", "/")
            if file == saveDirectory:
                continue
            file = file[lenBaseDir + 1 :]
            # index = self.data_Model.check_Index_File_Name(file)
            index = checkIndex(file, listFIlenames)
            # if file not in self.data_Model.get_File_Names():
            if index == -1:
                newListFileNames.append(file)
                dictFileData = copy.copy(
                    self.doc.getDictExperimentInformation("dict_clipboard")
                )
                dictFileData["filename"] = file
                dictFileData["index"] = count
                dictFileData["classified"] = "not_classified"
                dictFileData["valid"] = False
                dictFileData["comment"] = ""
                # dict_File_Data[
                #     "file_sample_id"] = self.data_Model.get_Template_Data_By_Key(
                #         "sample_id")
                # dict_File_Data[
                #     "file_sample_name"] = self.data_Model.get_Template_Data_By_Key(
                #         "sample_name")
                # dict_File_Data[
                #     "file_sample_comment"] = self.data_Model.get_Template_Data_By_Key(
                #         "sample_comment")
                # dict_File_Data[
                #     "file_equipment_contents"] = self.data_Model.get_Template_Data_By_Key(
                #         "equipment_contents")
                self.doc.addFileInformation(dictFileData)
                newListFileData.append(dictFileData)
            else:
                newListFileNames.append(file)
                dictFileData = copy.copy(oldListFileData[index])
                # self.data_Model.get_File_Data_By_Index(index))
                dictFileData["index"] = count
                self.doc.addFileInformation(dictFileData)
                newListFileData.append(dictFileData)
            count += 1

        # self.data_Model.set_File_Names(copy.copy(new_List_File_Names))
        # self.data_Model.set_All_File_Data(copy.copy(new_List_File_Data))
        for i, file in enumerate(newListFileNames):
            subWidgetEachFilesInformation = TySubWidgetEachFiles(doc=self.doc)
            subWidgetEachFilesInformation.setSignalUpdateToMetadataClipboard(
                self.signalUpdateToMetadataClipboard
            )
            self.ui.toolBox.addItem(subWidgetEachFilesInformation, file)
            subWidgetEachFilesInformation.setParentWidget(self.ui.toolBox, i)

            subWidgetEachFilesInformation.setIndex(i)
            subWidgetEachFilesInformation.setFileName(file)
            subWidgetEachFilesInformation.readTextFromDoc()
            subWidgetEachFilesInformation.updateTitle()
            if newListFileNames[i] == focusedFileName:
                self.ui.toolBox.setCurrentIndex(i)
        # self.ui.toolBox.currentWidget().setMinimumHeight(300)
        # self.ui.toolBox.widget(i).setMinimumHeight(500)
        self.doc.saveToTemporary()
        self.logger.info("end refresh files")

    def finishExperiment(self):
        self.logger.info("Finish experiment procedure starting.")
        # experiment_ID = self.data_Model.get_Dict_Data_Model(
        #     "str_experiment_id")
        # self.messageSender = TyMessageSender(
        #     self.doc.getDictExperimentInformation("str_url_diamond"),
        #     self.doc,
        # )
        if self.doc.getDictExperimentInformation("is_upload_arim") is True:
            listFileData = self.doc.getAllFileInformation()
            flagCheckedArim = False
            for fileData in listFileData:
                if fileData["arim_upload"] is True:
                    flagCheckedArim = True
                    break
            if flagCheckedArim is False:
                message = "Your data should be uploaded to NIMS.\nPlease select at least one file to upload."
                # msgBox = QtWidgets.QMessageBox()
                # msgBox.setText(

                # )
                # msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                # msgBox.exec_()
                self.doc.messageBox("Error", message, 1)
                return False

        # msgBox = QtWidgets.QMessageBox()
        strSetText = ""
        strSetText += "実を終了しますか？\n"
        strSetText += (
            "OKボタンを押すと、共有フォルダのファイルはすべて保存領域に移動します！\n"
        )
        strSetText += "保存が必要な場合は、実験終了前に保存してください！\n\n"
        strSetText += "Are you sure to submit the experiment?\n"
        strSetText += "If OK button is clicked, files in the shared folder is moved and you can't access directory!\n"
        strSetText += "Before finish experiment, please check all files are saved!"
        # msgBox.setText(strSetText)
        # msgBox.setStandardButtons(
        #     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        # )
        # retval = msgBox.exec_()
        retval = self.doc.messageBox("Finish Experiment", strSetText, 2)
        if retval == 1024:
            try:
                response = self.doc.messageSender.sendRequestFinishExperiment(
                    self.doc.getExperimentId(), self.doc
                )
                if response["status"] is True:
                    message = "Data upload have finished.\nThis program will be closed after click OK button."
                    # msgBox.setText(
                    #     "Data upload have finished.\nThis program will be closed after click OK button."
                    # )
                    # msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    # retval = msgBox.exec_()
                    retval = self.doc.messageBox("Finish Experiment", message, 1)
                    os.remove("./temporary.json")
                    self.logger.info("Finish all procedure.")
                    return True
                # elif response["status_code"] == 401:
                #     message = "Your session has expired.\nPlease log in again."
                #     retval = self.doc.messageBox("Finish Experiment", message, 1)
                #     self.logger.error("Session expired. Log in again.")
                #     self.isForceCloseWindow = True
                #     self.doc.changeView("log_in")
                #     return True
                else:
                    # msgBox.setText(response["message"])
                    # msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    # retval = msgBox.exec_()
                    retval = self.doc.messageBox(
                        "Finish Experiment", response["message"], 1
                    )
                    self.logger.error("Finish experiment procedure canceled.")
                    self.logger.error(f"Message: {response['message']}")
                    return False
            except MessageSenderException as e:
                if e.status_code == 401:
                    message = "Your session has expired.\nPlease log in again."
                    retval = self.doc.messageBox("Finish Experiment", message, 1)
                    self.logger.error("Session expired. Log in again.")
                    self.isForceCloseWindow = True
                    self.doc.changeView("log_in")
                    return True
                message = f"Error in Finishing Experiment: {e.message}, {e.status_code}"
                retval = self.doc.messageBox("Error", message, 1)
                self.logger.error(message)
                return False
        else:
            self.logger.info("Finish experiment procedure canceled.")
