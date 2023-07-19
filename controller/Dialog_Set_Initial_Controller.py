import forms.Dialog_Set_Initial_ui as Dialog_Set_Initial_ui

from controller.SubWidget_Experiment_Information_Controller import Sub_Widget_Experiment_Information
from controller.SubWidget_Sample_Information_Controller import Sub_Widget_Sample_Information
from controller.SubWidget_Equipment_Information_Controller import Sub_Widget_Equipment_Information
from controller.MainWindow_Controller import Window_Main

# from sendMessageToDiamond import senderMessageToDiamond
from Data_Model import DataModel
# from metaDataConverter import MetaDataConverter

from PyQt5 import QtWidgets
from PyQt5 import QtGui


class Dialog_Set_Initial(QtWidgets.QDialog):
    def __init__(self, parent=None, data_Model=None):
        # self.data_Model = DataModel()
        # self.window_Main = Window_Main()

        super().__init__(parent)
        self.ui = Dialog_Set_Initial_ui.Ui_Dialog()
        self.ui.setupUi(self)

        self.set_Signal()
        if data_Model is not None:
            self.data_Model = data_Model
        else:
            self.data_Model = DataModel()
        self.sub_Widget_Experiment_Information = Sub_Widget_Experiment_Information(
            data_Model=self.data_Model)
        self.sub_Widget_Sample_Information = Sub_Widget_Sample_Information(
            data_Model=self.data_Model)
        self.sub_Widget_Equipment_Information = Sub_Widget_Equipment_Information(
            data_Model=self.data_Model)

        self.ui.HL_Page1.addWidget(self.sub_Widget_Experiment_Information)
        self.ui.HL_Page2.addWidget(self.sub_Widget_Sample_Information)
        self.ui.HL_Page3.addWidget(self.sub_Widget_Equipment_Information)

        self.initialize_From_Data_Model()

        self.ui.stackedWidget.setCurrentIndex(0)
        self.setWindowTitle("Set Initial Information 1/3")

    def set_Icon(self):
        icon_next = QtGui.QIcon()
        icon_next.addPixmap(QtGui.QPixmap("./icons/GoNext.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_back = QtGui.QIcon()
        icon_back.addPixmap(QtGui.QPixmap("./icons/GoPrevious.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_finish = QtGui.QIcon()
        icon_finish.addPixmap(QtGui.QPixmap("./icons/Start.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.ui.PB_Next_Page1.setIcon(icon_next)
        self.ui.PB_Next_Page2.setIcon(icon_next)
        self.ui.PB_Back_Page2.setIcon(icon_back)
        self.ui.PB_Back_Page3.setIcon(icon_back)
        self.ui.PB_Finish_Page3.setIcon(icon_finish)

    def set_Signal(self):
        self.ui.PB_Next_Page1.clicked.connect(self.go_Next_To_1)
        self.ui.PB_Next_Page2.clicked.connect(self.go_Next_To_2)
        self.ui.PB_Back_Page2.clicked.connect(self.go_Back_To_0)
        self.ui.PB_Back_Page3.clicked.connect(self.go_Back_To_1)
        self.ui.PB_Finish_Page3.clicked.connect(self.finish_Set)

    def set_Data_Model(self, data_model):
        self.data_Model = data_model
        self.sub_Widget_Experiment_Information.set_Data_Model(self.data_Model)
        self.sub_Widget_Sample_Information.set_Data_Model(self.data_Model)
        self.sub_Widget_Equipment_Information.set_Data_Model(self.data_Model)

    def go_Next_To_1(self):
        if self.sub_Widget_Experiment_Information.ui.LE_Title.text() == "":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Experiment Title is empty")
            msgBox.exec_()
        else:
            self.sub_Widget_Experiment_Information.get_All_To_Data_Model()
            self.ui.stackedWidget.setCurrentIndex(1)
            self.setWindowTitle("Set Initial Information 2/3")

    def go_Next_To_2(self):
        if self.sub_Widget_Sample_Information.ui.LE_Sample_Name.text() == "":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Sample Name is empty")
            msgBox.exec_()
        else:
            self.sub_Widget_Sample_Information.get_All_To_Data_Model()
            self.ui.stackedWidget.setCurrentIndex(2)
            self.setWindowTitle("Set Initial Information 3/3")

    def go_Back_To_0(self):
        self.sub_Widget_Sample_Information.get_All_To_Data_Model()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.setWindowTitle("Set Initial Information 1/3")

    def go_Back_To_1(self):
        self.sub_Widget_Equipment_Information.get_All_To_Data_Model()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.setWindowTitle("Set Initial Information 2/3")

    def finish_Set(self):
        self.sub_Widget_Equipment_Information.get_All_To_Data_Model()
        self.data_Model.save_To_Temporary()
        self.window_Main = Window_Main(data_Model=self.data_Model)
        self.window_Main.show()
        self.close()

    def initialize_From_Data_Model(self):
        self.sub_Widget_Experiment_Information.set_All_From_Data_Model()
        self.sub_Widget_Sample_Information.set_All_From_Data_Model()
        self.sub_Widget_Equipment_Information.set_All_From_Data_Model()
