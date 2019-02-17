# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_databases.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DBMainWindow(object):
    def setupUi(self, DBMainWindow):
        DBMainWindow.setObjectName("DBMainWindow")
        DBMainWindow.resize(677, 584)
        self.centralwidget = QtWidgets.QWidget(DBMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 651, 515))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelRawTable = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelRawTable.setObjectName("labelRawTable")
        self.gridLayout_4.addWidget(self.labelRawTable, 0, 0, 1, 1)
        self.comboDBTables = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboDBTables.setObjectName("comboDBTables")
        self.gridLayout_4.addWidget(self.comboDBTables, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(339, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        self.butViewTable = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butViewTable.sizePolicy().hasHeightForWidth())
        self.butViewTable.setSizePolicy(sizePolicy)
        self.butViewTable.setMinimumSize(QtCore.QSize(108, 0))
        self.butViewTable.setObjectName("butViewTable")
        self.gridLayout_4.addWidget(self.butViewTable, 0, 3, 1, 1)
        self.treeWidgetDB = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidgetDB.sizePolicy().hasHeightForWidth())
        self.treeWidgetDB.setSizePolicy(sizePolicy)
        self.treeWidgetDB.setMinimumSize(QtCore.QSize(0, 150))
        self.treeWidgetDB.setMouseTracking(False)
        self.treeWidgetDB.setAlternatingRowColors(True)
        self.treeWidgetDB.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.treeWidgetDB.setIndentation(10)
        self.treeWidgetDB.setRootIsDecorated(True)
        self.treeWidgetDB.setAnimated(True)
        self.treeWidgetDB.setObjectName("treeWidgetDB")
        self.treeWidgetDB.headerItem().setText(0, "1")
        self.treeWidgetDB.header().setVisible(False)
        self.treeWidgetDB.header().setDefaultSectionSize(60)
        self.treeWidgetDB.header().setHighlightSections(True)
        self.treeWidgetDB.header().setMinimumSectionSize(5)
        self.treeWidgetDB.header().setSortIndicatorShown(True)
        self.gridLayout_4.addWidget(self.treeWidgetDB, 1, 0, 1, 4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        DBMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DBMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 677, 22))
        self.menubar.setObjectName("menubar")
        DBMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DBMainWindow)
        self.statusbar.setObjectName("statusbar")
        DBMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DBMainWindow)
        QtCore.QMetaObject.connectSlotsByName(DBMainWindow)

    def retranslateUi(self, DBMainWindow):
        _translate = QtCore.QCoreApplication.translate
        DBMainWindow.setWindowTitle(_translate("DBMainWindow", "MainWindow"))
        self.labelRawTable.setText(_translate("DBMainWindow", "Raw Table"))
        self.butViewTable.setToolTip(_translate("DBMainWindow", "<html><head/><body><p>Update the checklist database</p></body></html>"))
        self.butViewTable.setText(_translate("DBMainWindow", "View"))
        self.treeWidgetDB.setSortingEnabled(True)

