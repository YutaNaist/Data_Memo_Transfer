from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer

from controller.TySubWidgetExperimentInformation import (
    TySubWidgetExperimentInformation,
)
from controller.TySubWidgetSampleInformation import (
    TySubWidgetSampleInformation,
)
from controller.TySubWidgetEquipmentInformation import (
    TySubWidgetEquipmentInformation,
)
from controller.TyMainWindow import TyMainWindow


# from metaDataConverter import MetaDataConverter

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic


class TyDialogSetInitial(QtWidgets.QDialog):

    def __init__(self, parent=None, doc: TyDocDataMemoTransfer = None):
        if doc is not None:
            self.doc = doc
        else:
            self.doc = TyDocDataMemoTransfer()
        # self.data_Model = DataModel()
        # self.window_Main = Window_Main()

        super().__init__(parent)
        # self.ui = Dialog_Set_Initial_ui.Ui_Dialog()
        # self.ui.setupUi(self)
        self.__loadUi()
        self.__setSignal()

        self.subWidgetExperimentInformation = TySubWidgetExperimentInformation(
            doc=self.doc
        )
        self.subWidgetSampleInformation = TySubWidgetSampleInformation(doc=self.doc)
        self.subWidgetEquipmentInformation = TySubWidgetEquipmentInformation(
            doc=self.doc
        )
        self.state = "experiment_information"
        self.ui.HL_Page1.addWidget(self.subWidgetExperimentInformation)
        self.ui.HL_Page2.addWidget(self.subWidgetSampleInformation)
        self.ui.HL_Page3.addWidget(self.subWidgetEquipmentInformation)

        self.initializeFromDocument()

        self.ui.stackedWidget.setCurrentIndex(0)
        self.setWindowTitle("Set Initial Information 1/3")

    def __loadUi(self):
        if self.doc.isBuild:
            from views.FormDialogSetInitial import Ui_Dialog

            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
        else:
            uic.loadUi(r"forms/FormDialogSetInitial.ui", self)
            self.ui = self

    def set_Icon(self):
        icon_next = QtGui.QIcon()
        icon_next.addPixmap(
            QtGui.QPixmap("./icons/GoNext.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        icon_back = QtGui.QIcon()
        icon_back.addPixmap(
            QtGui.QPixmap("./icons/GoPrevious.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        icon_finish = QtGui.QIcon()
        icon_finish.addPixmap(
            QtGui.QPixmap("./icons/Start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )

        self.ui.PB_Next_Page1.setIcon(icon_next)
        self.ui.PB_Next_Page2.setIcon(icon_next)
        self.ui.PB_Back_Page2.setIcon(icon_back)
        self.ui.PB_Back_Page3.setIcon(icon_back)
        self.ui.PB_Finish_Page3.setIcon(icon_finish)

    def __setSignal(self):
        self.ui.PB_Next_Page1.clicked.connect(self.changeViewToSampleInformation)
        self.ui.PB_Next_Page2.clicked.connect(self.changeViewToEquipmentInformation)
        self.ui.PB_Back_Page2.clicked.connect(self.changeViewToExperimentInformation)
        self.ui.PB_Back_Page3.clicked.connect(self.changeViewToSampleInformation)
        self.ui.PB_Finish_Page3.clicked.connect(self.changeViewFinishInitialize)

    def changeViewToExperimentInformation(self):
        if self.checkState():
            self.changeView("experiment_information")

    def changeViewToSampleInformation(self):
        if self.checkState():
            self.changeView("sample_information")

    def changeViewToEquipmentInformation(self):
        if self.checkState():
            self.changeView("equipment_information")

    def changeViewFinishInitialize(self):
        if self.checkState():
            self.changeView("finish")

    def changeView(self, newState: str):
        self.state = newState
        if newState == "experiment_information":
            self.ui.stackedWidget.setCurrentIndex(0)
            self.setWindowTitle("Set Initial Information 1/3")
        elif newState == "sample_information":
            self.ui.stackedWidget.setCurrentIndex(1)
            self.setWindowTitle("Set Initial Information 2/3")
        elif newState == "equipment_information":
            self.ui.stackedWidget.setCurrentIndex(2)
            self.setWindowTitle("Set Initial Informationl 3/3")
        elif newState == "finish":
            self.doc.writeToLogger("finish initialization.")
            self.doc.saveToTemporary()
            self.doc.changeView("main_window")
            # self.window_Main = Window_Main(data_Model=self.doc)
            # self.window_Main.show()
            # self.close()

    def checkState(self):
        currentState = self.state
        if currentState == "experiment_information":
            if self.subWidgetExperimentInformation.ui.LE_Title.text() == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Experiment Title is empty")
                msgBox.exec_()
                return False
            else:
                self.subWidgetExperimentInformation.set_To_Data_Model()
                return True
        if currentState == "sample_information":
            if self.subWidgetSampleInformation.ui.LE_Sample_Name.text() == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Sample Name is empty")
                msgBox.exec_()
                return False
            else:
                self.subWidgetSampleInformation.set_To_Data_Model()
                return True
        elif currentState == "equipment_information":
            self.subWidgetEquipmentInformation.set_To_Data_Model()
            return True
        elif currentState == "finish":
            self.doc.writeToLogger("Initialization finished.", "info")

    # def go_Next_To_1(self):
    #     if self.sub_Widget_Experiment_Information.ui.LE_Title.text() == "":
    #         msgBox = QtWidgets.QMessageBox()
    #         msgBox.setText("Experiment Title is empty")
    #         msgBox.exec_()
    #     else:
    #         self.sub_Widget_Experiment_Information.set_To_Data_Model()
    #         self.ui.stackedWidget.setCurrentIndex(1)
    #         self.setWindowTitle("Set Initial Information 2/3")

    # def go_Next_To_2(self):
    #     if self.sub_Widget_Sample_Information.ui.LE_Sample_Name.text() == "":
    #         msgBox = QtWidgets.QMessageBox()
    #         msgBox.setText("Sample Name is empty")
    #         msgBox.exec_()
    #     else:
    #         self.sub_Widget_Sample_Information.set_To_Data_Model()
    #         self.ui.stackedWidget.setCurrentIndex(2)
    #         self.setWindowTitle("Set Initial Information 3/3")

    # def go_Back_To_0(self):
    #     self.sub_Widget_Sample_Information.set_To_Data_Model()
    #     self.ui.stackedWidget.setCurrentIndex(0)
    #     self.setWindowTitle("Set Initial Information 1/3")

    # def go_Back_To_1(self):
    #     self.sub_Widget_Equipment_Information.set_To_Data_Model()
    #     self.ui.stackedWidget.setCurrentIndex(1)
    #     self.setWindowTitle("Set Initial Information 2/3")

    # def finish_Set(self):
    #     self.doc.writeToLogger("finish initialization.")
    #     self.sub_Widget_Equipment_Information.set_To_Data_Model()
    #     self.doc.saveToTemporary()
    #     self.window_Main = Window_Main(data_Model=self.doc)
    #     self.window_Main.show()
    #     self.close()

    def initializeFromDocument(self):
        self.subWidgetExperimentInformation.get_From_Data_Model()
        self.subWidgetSampleInformation.get_From_Data_Model()
        self.subWidgetEquipmentInformation.get_From_Data_Model()
