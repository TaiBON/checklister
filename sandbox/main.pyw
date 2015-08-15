#!/usr/bin/env python3
import sys 
from PyQt4.QtGui import QApplication
from window import Window

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
