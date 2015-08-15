from PyQt4.QtCore import *
from PyQt4.QtGui import *
from genlist_api import *

from ui_window import Ui_Window
import genlist_api

class Window(QWidget, Ui_Window):
    
    oformat_list = ["docx", "odt", "txt", "rtf"]

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.butBlist, SIGNAL("clicked()"), self.browBaselist)
        self.connect(self.butSlist, SIGNAL("clicked()"), self.browSlist)
        self.connect(self.butGenerate, SIGNAL("clicked()"), self.generate)
#        self.connect(self.
#        f = open('/tmp/log', 'w')
#        f.write(ofile + '\n')
#        f.write(oformat + '\n')
#        f.close()

    def browBaselist(self):
        self.lineBlist.clear()
        Blist = QFileDialog.getOpenFileName(self, "Open File 開啟物種資料檔案:", "./data/", "Text files (*.txt *.csv)")
        if Blist is None:
            return
        self.lineBlist.setText(Blist) 

    def browSlist(self):
        self.lineSlist.clear()
        Slist = QFileDialog.getOpenFileName(self, "Open File 開啟物種清單檔案:", "./data/", "Text files (*.txt *.csv)")
        if Slist is None:
            return
        self.lineSlist.setText(Slist) 

    def generate(self):
        g = genlist_api.genlist()
        if self.lineBlist.text() == '':
            QMessageBox.information(self, "Warning", "請指定物種資料檔案")
        elif self.lineSlist.text() == '':
            QMessageBox.information(self, "Warning", "請指定物種清單檔案")
        elif self.lineOutputFilename.text() == '':
            QMessageBox.information(self, "Warning", "請指定輸出檔案名稱")
        else:
            dbfile = str(self.lineBlist.text())
            sample_file = str(self.lineSlist.text())
            ofile = str(self.lineOutputFilename.text())
            oformat = self.oformat_list[self.comboOutputFormat.currentIndex()]
            output = ofile + '.' + oformat
            g.generator(dbfile, sample_file, oformat, ofile)
            f = open('/tmp/log', 'w')
            f.write(dbfile + ' ' + sample_file + ' ' + oformat + ' ' +ofile + '\n')
            f.close()
            QMessageBox.information(self, "名錄產生器", "名錄已產生完畢")
