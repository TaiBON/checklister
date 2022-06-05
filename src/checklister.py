#!/usr/bin/env python3
import genlist_api
import locale
import os
import sys
import platform
from PyQt6.QtCore import Qt, QLocale, QTranslator, QDir
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import *
from mainWindow import MainWindow


def minimizeWindow(self):
    try:
        window.showMinimized()
    except BaseException as e:
        QMessageBox.information(self, "Warning", str(e))

def normalWindow(self):
    try:
        window.showNormal()
    except BaseException as e:
        QMessageBox.information(self, "Warning", str(e))

def maximizeWindow(self):
    try:
        window.showMaximized()
    except BaseException as e:
        QMessageBox.information(self, "Warning", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if platform.system() == 'Windows':
        app.setStyle(QStyleFactory.create('WindowsVista'))
    # for retina Only for Qt5
    # if platform.system() == 'Darwin':
    #    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    myLocale = QLocale()
    trans = QTranslator()
    g = genlist_api.Genlist()
    #QDir.addSearchPath('icons', './icons')
    i18nQm = g.resource_path(os.path.join('i18n', 'checklister_' + myLocale.name() + '.qm'))
    trans.load(i18nQm)
    app.installTranslator(trans)
    window = MainWindow()
    window.show()
    # window zoom/min/max
    window.actionMinimize.triggered.connect(minimizeWindow)
    window.actionZoom.triggered.connect(normalWindow)
    window.actionMaximize.triggered.connect(maximizeWindow)
    sys.exit(app.exec())
