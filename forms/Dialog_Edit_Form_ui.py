# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './forms/Dialog_Edit_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 295)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LAB_Title = QtWidgets.QLabel(Dialog)
        self.LAB_Title.setObjectName("LAB_Title")
        self.verticalLayout.addWidget(self.LAB_Title)
        self.HL_Add_Widget = QtWidgets.QHBoxLayout()
        self.HL_Add_Widget.setObjectName("HL_Add_Widget")
        self.verticalLayout.addLayout(self.HL_Add_Widget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.PB_Copy_From_Clipboard = QtWidgets.QPushButton(Dialog)
        self.PB_Copy_From_Clipboard.setObjectName("PB_Copy_From_Clipboard")
        self.horizontalLayout_3.addWidget(self.PB_Copy_From_Clipboard)
        self.PB_Paste_To_Clipboard = QtWidgets.QPushButton(Dialog)
        self.PB_Paste_To_Clipboard.setObjectName("PB_Paste_To_Clipboard")
        self.horizontalLayout_3.addWidget(self.PB_Paste_To_Clipboard)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.PB_OK = QtWidgets.QPushButton(Dialog)
        self.PB_OK.setObjectName("PB_OK")
        self.horizontalLayout_2.addWidget(self.PB_OK)
        self.PB_Cancel = QtWidgets.QPushButton(Dialog)
        self.PB_Cancel.setObjectName("PB_Cancel")
        self.horizontalLayout_2.addWidget(self.PB_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.LAB_Title.setText(_translate("Dialog", "Title"))
        self.PB_Copy_From_Clipboard.setText(_translate("Dialog", "Copy from clipboard"))
        self.PB_Paste_To_Clipboard.setText(_translate("Dialog", "Paste to clipboard"))
        self.PB_OK.setText(_translate("Dialog", "OK"))
        self.PB_Cancel.setText(_translate("Dialog", "Cancel"))
