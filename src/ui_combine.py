# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_combine.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CombineDialog(object):
    def setupUi(self, CombineDialog):
        CombineDialog.setObjectName("CombineDialog")
        CombineDialog.resize(559, 257)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CombineDialog.sizePolicy().hasHeightForWidth())
        CombineDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(CombineDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(CombineDialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 535, 233))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 511, 177))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 3, 1, 2)
        self.butSelCombList = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butSelCombList.sizePolicy().hasHeightForWidth())
        self.butSelCombList.setSizePolicy(sizePolicy)
        self.butSelCombList.setObjectName("butSelCombList")
        self.gridLayout_2.addWidget(self.butSelCombList, 0, 5, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.textChecklists = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textChecklists.sizePolicy().hasHeightForWidth())
        self.textChecklists.setSizePolicy(sizePolicy)
        self.textChecklists.setMinimumSize(QtCore.QSize(0, 21))
        self.textChecklists.setObjectName("textChecklists")
        self.gridLayout_2.addWidget(self.textChecklists, 1, 1, 1, 6)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(52, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 3, 1, 2)
        self.butSelExcelFile = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butSelExcelFile.sizePolicy().hasHeightForWidth())
        self.butSelExcelFile.setSizePolicy(sizePolicy)
        self.butSelExcelFile.setObjectName("butSelExcelFile")
        self.gridLayout_2.addWidget(self.butSelExcelFile, 2, 5, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.textExpExcel = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textExpExcel.sizePolicy().hasHeightForWidth())
        self.textExpExcel.setSizePolicy(sizePolicy)
        self.textExpExcel.setMinimumSize(QtCore.QSize(0, 21))
        self.textExpExcel.setObjectName("textExpExcel")
        self.gridLayout_2.addWidget(self.textExpExcel, 3, 1, 1, 6)
        spacerItem3 = QtWidgets.QSpacerItem(318, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 4, 0, 1, 4)
        self.butClose = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butClose.sizePolicy().hasHeightForWidth())
        self.butClose.setSizePolicy(sizePolicy)
        self.butClose.setObjectName("butClose")
        self.gridLayout_2.addWidget(self.butClose, 4, 4, 1, 2)
        self.butCombine = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butCombine.sizePolicy().hasHeightForWidth())
        self.butCombine.setSizePolicy(sizePolicy)
        self.butCombine.setDefault(True)
        self.butCombine.setObjectName("butCombine")
        self.gridLayout_2.addWidget(self.butCombine, 4, 6, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.addWidget(self.scrollArea_2, 1, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(CombineDialog)
        QtCore.QMetaObject.connectSlotsByName(CombineDialog)

    def retranslateUi(self, CombineDialog):
        _translate = QtCore.QCoreApplication.translate
        CombineDialog.setWindowTitle(_translate("CombineDialog", "Dialog"))
        self.label_2.setText(_translate("CombineDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Step 1</span>: Select checklist to be combined (*.txt)</p></body></html>"))
        self.butSelCombList.setText(_translate("CombineDialog", "Select file(s) ..."))
        self.label_4.setText(_translate("CombineDialog", "Checklists"))
        self.label_3.setText(_translate("CombineDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Step 2</span>: Select export Excel file:</p></body></html>"))
        self.butSelExcelFile.setText(_translate("CombineDialog", "Select file ..."))
        self.label_5.setText(_translate("CombineDialog", "Excel file"))
        self.butClose.setText(_translate("CombineDialog", "Close"))
        self.butCombine.setText(_translate("CombineDialog", "Combine"))
        self.label.setText(_translate("CombineDialog", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Combine multiple checklists</span></p></body></html>"))
