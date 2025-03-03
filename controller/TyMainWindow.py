from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer

import forms.MainWindow_ui as MainWidow_ui

# from controller.Window_Edit_Form_Controller import Window_Edit_Form
from controller.Dialog_Edit_Form_Controller import Dialog_Edit_Form
from controller.SubWidget_Each_Files_Information_Controller import (
    Sub_Widget_Each_Files_Information,
)

from controller.SubWidget_Experiment_Information_Controller import (
    Sub_Widget_Experiment_Information,
)
from controller.SubWidget_Sample_Information_Controller import (
    Sub_Widget_Sample_Information,
)
from controller.SubWidget_Equipment_Information_Controller import (
    Sub_Widget_Equipment_Information,
)

from TyMessageSender import TyMessageSender

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic

import copy
import glob
import os


class TyMainWindow(QtWidgets.QMainWindow):
    # signal_Update_Data_Model = QtCore.pyqtSignal()
    # signal_Get_SampleInfo = QtCore.pyqtSignal()
    signal_update_to_metadata_clipboard = QtCore.pyqtSignal()

    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()

        self.current_Index_ToolBox = 0

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
    def __loadUi(self):
        uic.loadUi(r"forms\FromMainWindow.ui", self)
        self.ui = self

    def __setSignals(self):
        self.ui.PB_Refresh.clicked.connect(self.refreshFiles)
        self.ui.toolBox.currentChanged.connect(self.change_ToolBox_Index)
        self.ui.PB_Experiment_Title_Edit.clicked.connect(
            self.edit_Experiment_Information
        )
        self.ui.PB_Sample_ID_Edit.clicked.connect(self.edit_Sample_Information)
        self.ui.PB_Experiment_Method_Edit.clicked.connect(
            self.edit_Equipment_Information
        )
        # self.ui.PB_Upload_Data.clicked.connect(self.finish_Experiment)
        self.ui.PB_Upload_Data.clicked.connect(self.close)
        self.signal_update_to_metadata_clipboard.connect(
            self.set_Template_Form_By_Data_Model
        )

    def closeEvent(self, event):
        finish_Status = self.finishExperiment()
        if finish_Status:
            event.accept()
        else:
            event.ignore()

    def change_ToolBox_Index(self, index):
        self.current_Index_ToolBox = index

    def change_ToolBox_Title(self, index):
        pass

    def initializeForms(self):
        self.doc.writeToLogger("Start to initialize forms.")
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
        self.sub_Widget_Experiment = Sub_Widget_Experiment_Information(
            data_Model=self.doc, isEditable=False
        )
        self.sub_Widget_Sample = Sub_Widget_Sample_Information(
            data_Model=self.doc, isEditable=False
        )
        self.sub_Widget_Equipment = Sub_Widget_Equipment_Information(
            data_Model=self.doc, isEditable=False
        )
        self.ui.VL_Experiment.addWidget(self.sub_Widget_Experiment)
        self.ui.VL_Sample.addWidget(self.sub_Widget_Sample)
        self.ui.VL_Equipment.addWidget(self.sub_Widget_Equipment)

        self.set_Template_Form_By_Data_Model()
        self.doc.writeToLogger("finish initializing main window forms")
        # if self.data_Model.get_File_Names() != []:
        #     self.refresh_Files()

    def set_Template_Form_By_Data_Model(self):
        str_ID_Text = "Experiment ID : {}".format(
            self.doc.getDictExperimentInformation("str_experiment_id")
        )
        self.ui.LAB_Experiment_ID.setText(str_ID_Text)
        self.sub_Widget_Experiment.get_From_Data_Model()
        self.sub_Widget_Sample.get_From_Data_Model()
        self.sub_Widget_Equipment.get_From_Data_Model()

    def edit_Experiment_Information(self):
        self.window_Edit_Form = Dialog_Edit_Form(
            data_Model=self.doc,
            type_Form="experiment_information",
            isTemplate=True,
        )
        self.window_Edit_Form.set_Input_Form()
        self.window_Edit_Form.set_Signal_Update_To_Metadata_Clipboard(
            self.signal_update_to_metadata_clipboard
        )
        self.window_Edit_Form.show()

    def edit_Sample_Information(self):
        self.window_Edit_Form = Dialog_Edit_Form(
            data_Model=self.doc, type_Form="sample_information", isTemplate=True
        )
        self.window_Edit_Form.set_Input_Form()
        self.window_Edit_Form.set_Signal_Update_To_Metadata_Clipboard(
            self.signal_update_to_metadata_clipboard
        )
        self.window_Edit_Form.show()

    def edit_Equipment_Information(self):
        self.window_Edit_Form = Dialog_Edit_Form(
            data_Model=self.doc,
            type_Form="equipment_information",
            isTemplate=True,
        )
        self.window_Edit_Form.set_Input_Form()
        self.window_Edit_Form.set_Signal_Update_To_Metadata_Clipboard(
            self.signal_update_to_metadata_clipboard
        )
        self.window_Edit_Form.show()

    def refreshFiles(self):
        self.doc.writeToLogger("start refresh files")
        self.ui.LAB_File_List.setText("File List")
        # save_Directory = self.data_Model.get_Dict_Data_Model(
        #    "str_share_directory_in_storage")
        saveDirectory = self.doc.getDictExperimentInformation("str_save_directory")
        listFilesInSaveDirectoryOriginal = glob.glob(
            saveDirectory + "/**", recursive=True
        )
        self.doc.writeToLogger(f"Save directory: {saveDirectory}")
        self.doc.writeToLogger(
            f"List of files in save directory: {listFilesInSaveDirectoryOriginal}"
        )
        lenBaseDir = len(saveDirectory)
        listFilesInSaveDirectory = []
        xs = []
        # print("-----------------")
        # print(saveDirectory)
        # print(listFilesInSaveDirectoryOriginal)
        # print("-----------------")
        for file in listFilesInSaveDirectoryOriginal:
            if os.path.samefile(file, saveDirectory):
                continue
            path = os.path.join(saveDirectory, file)
            xs.append((os.path.getmtime(path), file))
        self.doc.writeToLogger(f"xs: {xs}")
        for _, file in sorted(xs):
            listFilesInSaveDirectory.append(file)
        new_List_File_Names = []
        new_List_File_Data = []
        # self.data_Model.reset_File_Data()
        focused_Index = self.current_Index_ToolBox
        focused_File_Name = self.ui.toolBox.itemText(focused_Index)

        for i in range(self.ui.toolBox.count()):
            self.ui.toolBox.removeItem(0)

        count = 0

        def check_Index(str_File_Name, list_File_Names):
            if str_File_Name in list_File_Names:
                return list_File_Names.index(str_File_Name)
            else:
                return -1

        list_filenames = self.doc.getFileNameList()
        old_list_File_Data = copy.copy(
            self.doc.getDictExperimentInformation("list_file_data")
        )
        self.doc.resetFileData()

        for i, file in enumerate(listFilesInSaveDirectory):
            file = file.replace("\\", "/")
            if file == saveDirectory:
                continue
            file = file[lenBaseDir + 1 :]
            # index = self.data_Model.check_Index_File_Name(file)
            index = check_Index(file, list_filenames)
            # if file not in self.data_Model.get_File_Names():
            if index == -1:
                new_List_File_Names.append(file)
                dict_File_Data = copy.copy(
                    self.doc.getDictExperimentInformation("dict_clipboard")
                )
                dict_File_Data["filename"] = file
                dict_File_Data["index"] = count
                dict_File_Data["classified"] = "not_classified"
                dict_File_Data["valid"] = False
                dict_File_Data["comment"] = ""
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
                self.doc.addFileInformation(dict_File_Data)
                new_List_File_Data.append(dict_File_Data)
            else:
                new_List_File_Names.append(file)
                dict_File_Data = copy.copy(old_list_File_Data[index])
                # self.data_Model.get_File_Data_By_Index(index))
                dict_File_Data["index"] = count
                self.doc.addFileInformation(dict_File_Data)
                new_List_File_Data.append(dict_File_Data)
            count += 1

        # self.data_Model.set_File_Names(copy.copy(new_List_File_Names))
        # self.data_Model.set_All_File_Data(copy.copy(new_List_File_Data))
        for i, file in enumerate(new_List_File_Names):
            sub_Widget_Each_Files_Information = Sub_Widget_Each_Files_Information(
                data_Model=self.doc
            )
            sub_Widget_Each_Files_Information.set_Signal_Update_To_Metadata_Clipboard(
                self.signal_update_to_metadata_clipboard
            )
            self.ui.toolBox.addItem(sub_Widget_Each_Files_Information, file)
            sub_Widget_Each_Files_Information.set_Parent_Widget(self.ui.toolBox, i)

            sub_Widget_Each_Files_Information.set_Index(i)
            sub_Widget_Each_Files_Information.set_File_Name(file)
            sub_Widget_Each_Files_Information.set_Text_From_Data_Model()
            sub_Widget_Each_Files_Information.update_Title()
            if new_List_File_Names[i] == focused_File_Name:
                self.ui.toolBox.setCurrentIndex(i)
        # self.ui.toolBox.currentWidget().setMinimumHeight(300)
        # self.ui.toolBox.widget(i).setMinimumHeight(500)
        self.doc.saveToTemporary()
        self.doc.writeToLogger("end refresh files")

    def finishExperiment(self):
        self.doc.writeToLogger("Finish experiment procedure starting.")
        # experiment_ID = self.data_Model.get_Dict_Data_Model(
        #     "str_experiment_id")
        self.messageSender = TyMessageSender(
            self.doc.getDictExperimentInformation("str_url_diamond"),
            self.doc,
        )
        if self.doc.getDictExperimentInformation("is_upload_arim") is True:
            list_file_data = self.doc.getAllFileInformation()
            flag_checked_arim = False
            for file_data in list_file_data:
                if file_data["arim_upload"] is True:
                    flag_checked_arim = True
                    break
            if flag_checked_arim is False:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(
                    "Your data should be uploaded to NIMS.\nPlease select at least one file to upload."
                )
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.exec_()
                return False

        msgBox = QtWidgets.QMessageBox()
        strSetText = ""
        strSetText += "実を終了しますか？\n"
        strSetText += (
            "OKボタンを押すと、共有フォルダのファイルはすべて保存領域に移動します！\n"
        )
        strSetText += "保存が必要な場合は、実験終了前に保存してください！\n\n"
        strSetText += "Are you sure to submit the experiment?\n"
        strSetText += "If OK button is clicked, files in the shared folder is moved and you can't access directory!\n"
        strSetText += "Before finish experiment, please check all files are saved!"
        msgBox.setText(strSetText)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        retval = msgBox.exec_()
        if retval == 1024:
            response = self.doc.messageSender.sendRequestFinishExperiment(
                self.doc, isAppendExisting=True
            )
            if response["status"] is True:
                msgBox.setText(
                    "Data upload have finished.\nThis program will be closed after click OK button."
                )
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retval = msgBox.exec_()
                os.remove("./temporary.json")
                self.doc.writeToLogger("Finish all procedure.")
                return True
            else:
                msgBox.setText(response["message"])
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retval = msgBox.exec_()
                self.doc.writeToLogger(
                    "any error occurs: {}.".format(response["message"])
                )
                return False
        else:
            self.doc.writeToLogger("canceled.")
