#!/usr/bin/env python3
import genlist_api
import locale
import os
import sys
import platform
from PyQt5.QtCore import Qt, QLocale, QTranslator
from PyQt5.QtWidgets import *
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
    # for retina
    if platform.system == 'Darwin':
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    myLocale = QLocale()
    trans = QTranslator()
    g = genlist_api.Genlist()
    i18nQm = g.resource_path(os.path.join('i18n',myLocale.name(),'ui_main_' + myLocale.name() + '.qm'))
    trans.load(i18nQm)
    app.installTranslator(trans)
    window = MainWindow()
    window.show()
    # window zoom/min/max
    window.actionMinimize.triggered.connect(minimizeWindow)
    window.actionZoom.triggered.connect(normalWindow)
    window.actionMaximize.triggered.connect(maximizeWindow)

    sys.exit(app.exec_())
