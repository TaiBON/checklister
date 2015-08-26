#!/usr/bin/env python3
import sys 
import genlist_api
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
