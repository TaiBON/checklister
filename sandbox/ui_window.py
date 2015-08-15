# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/namegen.ui'
#
# Created: Sun Aug 16 02:24:22 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName(_fromUtf8("Window"))
        Window.resize(709, 548)
        self.horizontalLayoutWidget = QtGui.QWidget(Window)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(260, 490, 441, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.butGenerate = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.butGenerate.setObjectName(_fromUtf8("butGenerate"))
        self.horizontalLayout.addWidget(self.butGenerate)
        self.butClose = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.butClose.setObjectName(_fromUtf8("butClose"))
        self.horizontalLayout.addWidget(self.butClose)
        self.tabWidget = QtGui.QTabWidget(Window)
        self.tabWidget.setGeometry(QtCore.QRect(10, 110, 681, 371))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabSelect = QtGui.QWidget()
        self.tabSelect.setObjectName(_fromUtf8("tabSelect"))
        self.treeWidget = QtGui.QTreeWidget(self.tabSelect)
        self.treeWidget.setGeometry(QtCore.QRect(10, 110, 651, 211))
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.tabWidget.addTab(self.tabSelect, _fromUtf8(""))
        self.tabBatch = QtGui.QWidget()
        self.tabBatch.setObjectName(_fromUtf8("tabBatch"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.tabBatch)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 30, 571, 80))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineSlist = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineSlist.setObjectName(_fromUtf8("lineSlist"))
        self.horizontalLayout_2.addWidget(self.lineSlist)
        self.butSlist = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.butSlist.setObjectName(_fromUtf8("butSlist"))
        self.horizontalLayout_2.addWidget(self.butSlist)
        self.tabWidget.addTab(self.tabBatch, _fromUtf8(""))
        self.gridLayoutWidget_2 = QtGui.QWidget(Window)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 481, 81))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineBlist = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.lineBlist.setObjectName(_fromUtf8("lineBlist"))
        self.gridLayout_2.addWidget(self.lineBlist, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.butBlist = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.butBlist.setObjectName(_fromUtf8("butBlist"))
        self.gridLayout_2.addWidget(self.butBlist, 0, 2, 1, 1)
        self.lineOutputFilename = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.lineOutputFilename.setObjectName(_fromUtf8("lineOutputFilename"))
        self.gridLayout_2.addWidget(self.lineOutputFilename, 1, 1, 1, 1)
        self.comboOutputFormat = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboOutputFormat.setObjectName(_fromUtf8("comboOutputFormat"))
        self.comboOutputFormat.addItem(_fromUtf8(""))
        self.comboOutputFormat.addItem(_fromUtf8(""))
        self.comboOutputFormat.addItem(_fromUtf8(""))
        self.comboOutputFormat.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboOutputFormat, 2, 1, 1, 1)

        self.retranslateUi(Window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.butClose, QtCore.SIGNAL(_fromUtf8("clicked()")), Window.close)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        Window.setWindowTitle(_translate("Window", "物種名錄產生器 namelist generator", None))
        self.butGenerate.setText(_translate("Window", "產生名錄", None))
        self.butClose.setText(_translate("Window", "關閉", None))
        self.treeWidget.headerItem().setText(0, _translate("Window", "Family", None))
        self.treeWidget.headerItem().setText(1, _translate("Window", "Name", None))
        self.treeWidget.headerItem().setText(2, _translate("Window", "Localname", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSelect), _translate("Window", "選擇物種", None))
        self.label_4.setText(_translate("Window", "產生名錄之物種csv檔案", None))
        self.butSlist.setText(_translate("Window", "Select Files ...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBatch), _translate("Window", "批次匯入", None))
        self.label_3.setText(_translate("Window", "輸出格式", None))
        self.label_2.setText(_translate("Window", "輸出檔名", None))
        self.label.setText(_translate("Window", "物種清單資料表", None))
        self.butBlist.setText(_translate("Window", "Select Files ...", None))
        self.lineOutputFilename.setText(_translate("Window", "output", None))
        self.comboOutputFormat.setItemText(0, _translate("Window", "docx", None))
        self.comboOutputFormat.setItemText(1, _translate("Window", "odt", None))
        self.comboOutputFormat.setItemText(2, _translate("Window", "txt", None))
        self.comboOutputFormat.setItemText(3, _translate("Window", "rtf", None))

