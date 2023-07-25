import forms.MainWindow_ui as MainWidow_ui

# from controller.Window_Edit_Form_Controller import Window_Edit_Form
from controller.Dialog_Edit_Form_Controller import Dialog_Edit_Form
from controller.SubWidget_Each_Files_Information_Controller import Sub_Widget_Each_Files_Information

from Data_Model import DataModel
from sendMessageToDiamond import senderMessageToDiamond

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import copy
import glob
import os


class Window_Main(QtWidgets.QMainWindow):
    # signal_Update_Data_Model = QtCore.pyqtSignal()
    # signal_Get_SampleInfo = QtCore.pyqtSignal()

    def __init__(self, parent=None, data_Model=None):
        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()
        # print(self.data_Model.get_File_Names())

        # self.timer = QtCore.QTimer()
        # self.timer.start(600000)
        self.current_Index_ToolBox = 0

        super().__init__(parent)
        self.ui = MainWidow_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint
        #                     | QtCore.Qt.WindowMinimizeButtonHint
        #                     | QtCore.Qt.WindowMaximizeButtonHint
        #                     | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Data Memo Transfer")
        self.ui.toolBox.removeItem(0)
        self.set_Signals()
        self.initialize_Forms()

        # self.ui.HL_AddSampleInformation.addWidget(self.subWidSampleInfo)
        # self.ui.PB_Upload_Data.isEnabled = False
        # self.load_Information_Temporals()

    def set_Signals(self):
        self.ui.PB_Refresh.clicked.connect(self.refresh_Files)
        self.ui.toolBox.currentChanged.connect(self.change_ToolBox_Index)

        self.ui.PB_Experiment_Title_Edit.clicked.connect(
            self.edit_Experiment_Information)

        self.ui.PB_Sample_ID_Edit.clicked.connect(self.edit_Sample_Information)

        self.ui.PB_Experiment_Method_Edit.clicked.connect(
            self.edit_Equipment_Information)

        self.ui.PB_Upload_Data.clicked.connect(self.finish_Experiment)

    def change_ToolBox_Index(self, index):
        self.current_Index_ToolBox = index

    def change_ToolBox_Title(self, index):
        pass

    def initialize_Forms(self):
        self.ui.PB_Experiment_Title_Edit.setIcon(
            QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Sample_ID_Edit.setIcon(QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Experiment_Method_Edit.setIcon(
            QtGui.QIcon("./icons/edit.png"))
        self.ui.PB_Refresh.setIcon(QtGui.QIcon("./icons/reflesh.png"))
        self.ui.PB_Upload_Data.setIcon(QtGui.QIcon("./icons/Exit2.png"))
        pixmap = QtGui.QPixmap("./icons/FileIcon.png")
        pixmap = pixmap.scaled(25, 25, QtCore.Qt.KeepAspectRatio,
                               QtCore.Qt.FastTransformation)
        self.ui.LAB_Confirmed.setPixmap(pixmap)

        pixmap_red = QtGui.QPixmap("./icons/FileIcon_red.png")
        pixmap_red = pixmap_red.scaled(25, 25, QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.FastTransformation)
        self.ui.LAB_UnConfirmed.setPixmap(pixmap_red)
        self.set_Template_Form_By_Data_Model()
        # if self.data_Model.get_File_Names() != []:
        #     self.refresh_Files()

    def set_Template_Form_By_Data_Model(self):
        str_ID_Text = "Experiment ID : {}".format(
            self.data_Model.get_Experiment_ID())
        self.ui.LAB_Experiment_ID.setText(str_ID_Text)
        self.ui.LE_Title.setText(
            self.data_Model.get_Template_Data_By_Key("title"))
        self.ui.TE_Experiment_Comment.setPlainText(
            self.data_Model.get_Template_Data_By_Key("experiment_comment"))

        self.ui.LE_Sample_ID.setText(
            self.data_Model.get_Template_Data_By_Key("sample_id"))
        self.ui.LE_Sample_Name.setText(
            self.data_Model.get_Template_Data_By_Key("sample_name"))
        self.ui.TE_Sample_Comment.setPlainText(
            self.data_Model.get_Template_Data_By_Key("sample_comment"))

        self.ui.LE_Experiment_Method.setText(
            self.data_Model.get_Equipment_Contents("experiment_method"))
        equipment_Key = self.data_Model.get_Equipment_Contents_Keys()
        if len(equipment_Key) > 1:
            str_Equipment_Contents = ""
            for i in range(len(equipment_Key) - 1):
                str_Equipment_Contents += "{}: {}\n".format(
                    equipment_Key[i],
                    self.data_Model.get_Equipment_Contents(equipment_Key[i]))

    def edit_Experiment_Information(self):
        self.window_Edit_Form = Dialog_Edit_Form(
            data_Model=self.data_Model,
            type_Form="experiment_information",
            isTemplate=True)
        self.window_Edit_Form.set_Input_Form()
        self.window_Edit_Form.signal_Update_Form.connect(
            self.set_Template_Form_By_Data_Model)
        self.window_Edit_Form.show()

    def edit_Sample_Information(self):
        self.window_Edit_Form = Dialog_Edit_Form(
            data_Model=self.data_Model,
            type_Form="sample_information",
            isTemplate=True)
        self.window_Edit_Form.set_Input_Form()
        self.window_Edit_Form.signal_Update_Form.connect(
            self.set_Template_Form_By_Data_Model)
        self.window_Edit_Form.show()

    def edit_Equipment_Information(self):
        self.window_Edit_Form = Dialog_Edit_Form(
            data_Model=self.data_Model,
            type_Form="equipment_information",
            isTemplate=True)
        self.window_Edit_Form.set_Input_Form()
        self.window_Edit_Form.signal_Update_Form.connect(
            self.set_Template_Form_By_Data_Model)
        self.window_Edit_Form.show()

    def refresh_Files(self):
        self.ui.LAB_File_List.setText("File List")
        save_Directory = self.data_Model.get_Share_Directory()
        list_Files_In_Save_Directory_Original = glob.glob(save_Directory +
                                                          "**",
                                                          recursive=True)

        lenBaseDir = len(save_Directory)

        list_Files_In_Save_Directory = []
        xs = []

        for file in list_Files_In_Save_Directory_Original:
            path = os.path.join(save_Directory, file)
            xs.append((os.path.getmtime(path), file))
        for _, file in sorted(xs):
            list_Files_In_Save_Directory.append(file)

        new_List_File_Names = []
        new_List_File_Data = []
        # self.data_Model.reset_File_Data()

        focused_Index = self.current_Index_ToolBox
        focused_File_Name = self.ui.toolBox.itemText(focused_Index)

        for i in range(self.ui.toolBox.count()):
            self.ui.toolBox.removeItem(0)

        count = 0
        for i, file in enumerate(list_Files_In_Save_Directory):
            if file == save_Directory:
                continue
            file = file[lenBaseDir:]
            file = file.replace("\\", "/")
            index = self.data_Model.check_Index_File_Name(file)
            # if file not in self.data_Model.get_File_Names():
            if index == -1:
                new_List_File_Names.append(file)
                dict_File_Data = copy.copy(
                    self.data_Model.get_File_Data_Template())
                dict_File_Data["file_name"] = file
                dict_File_Data["file_index"] = count
                dict_File_Data["file_status_classified"] = "not_classified"
                dict_File_Data["file_is_valid"] = False
                dict_File_Data["file_comment"] = ""
                dict_File_Data[
                    "file_sample_id"] = self.data_Model.get_Template_Data_By_Key(
                        "sample_id")
                dict_File_Data[
                    "file_sample_name"] = self.data_Model.get_Template_Data_By_Key(
                        "sample_name")
                dict_File_Data[
                    "file_sample_comment"] = self.data_Model.get_Template_Data_By_Key(
                        "sample_comment")
                dict_File_Data[
                    "file_equipment_contents"] = self.data_Model.get_Template_Data_By_Key(
                        "equipment_contents")
                new_List_File_Data.append(dict_File_Data)
            else:
                new_List_File_Names.append(file)
                dict_File_Data = copy.copy(
                    self.data_Model.get_File_Data_By_Index(index))
                dict_File_Data["file_index"] = count
                new_List_File_Data.append(dict_File_Data)
            count += 1

        self.data_Model.set_File_Names(copy.copy(new_List_File_Names))
        self.data_Model.set_All_File_Data(copy.copy(new_List_File_Data))
        for i, file in enumerate(new_List_File_Names):
            sub_Widget_Each_Files_Information = Sub_Widget_Each_Files_Information(
                data_Model=self.data_Model)
            self.ui.toolBox.addItem(sub_Widget_Each_Files_Information, file)
            sub_Widget_Each_Files_Information.set_Parent_Widget(
                self.ui.toolBox, i)

            sub_Widget_Each_Files_Information
            sub_Widget_Each_Files_Information.set_Index(i)
            sub_Widget_Each_Files_Information.set_File_Name(file)
            sub_Widget_Each_Files_Information.set_Text_From_Data_Model()
            sub_Widget_Each_Files_Information.update_Title()
            if new_List_File_Names[i] == focused_File_Name:
                self.ui.toolBox.setCurrentIndex(i)
        # self.ui.toolBox.currentWidget().setMinimumHeight(300)
        # self.ui.toolBox.widget(i).setMinimumHeight(500)
        self.data_Model.save_To_Temporary()

    def finish_Experiment(self):
        experiment_ID = self.data_Model.get_Experiment_ID()
        self.messageSender = senderMessageToDiamond(
            self.data_Model.get_URL_Address_Diamond())
        if experiment_ID == "":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please input ID.")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
        else:
            msgBox = QtWidgets.QMessageBox()
            strSetText = ""
            strSetText += "実を終了しますか？\n"
            strSetText += "OKボタンを押すと、共有フォルダのファイルはすべて保存領域に移動します！\n"
            strSetText += "保存が必要な場合は、実験終了前に保存してください！\n\n"
            strSetText += "Are you sure to submit the experiment?\n"
            strSetText += "If OK button is clicked, files in the shared folder is moved and you can't access directory!\n"
            strSetText += "Before finish experiment, please check all files are saved!"
            msgBox.setText(strSetText)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok
                                      | QtWidgets.QMessageBox.Cancel)
            retval = msgBox.exec_()
            if retval == 1024:
                self.setWindowTitle("Please Wait To Uploading.")
                response = self.messageSender.sendRequestFinishExperiment(
                    self.data_Model, isAppendExisting=True)
                # response = self.messageSender.sendRequestFinishExperiment(
                #     experiment_ID,
                #     self.sub_Wid_File_Names,
                #     self.metaDatas,
                #     self.data_Model.get_Share_Directory_In_Storage(),
                #     isAppendExisting=True)
                if response["status"] is True:
                    msgBox.setText(
                        "Data upload have finished.\nThis program will be closed after click OK button."
                    )
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    retval = msgBox.exec_()
                    os.remove("./temporary.json")
                    self.close()
                else:
                    msgBox.setText(response["message"])
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    retval = msgBox.exec_()
                # elif response["status"] is True:
                #     msgBox.setText(response["message"])
                #     msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #     retval = msgBox.exec_()
                #     os.remove("./temporary.json")
                #     self.close()
                # else:
                #     msgBox.setText(response["message"])
                #     msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #     retval = msgBox.exec_()
