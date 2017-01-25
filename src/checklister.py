#!/usr/bin/env python3
import genlist_api
import locale
import os
import sys
from PyQt5.QtCore import Qt, QLocale, QTranslator
from PyQt5.QtWidgets import *
from mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # for retina
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    current_locale = QLocale()
    trans = QTranslator()
    g = genlist_api.Genlist()
    i18n_ui_window_trans = g.resource_path(os.path.join('i18n', 'ui_main_' + current_locale.name() + '.qm'))
    print(i18n_ui_window_trans)
    trans.load(i18n_ui_window_trans)
    app.installTranslator(trans)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
