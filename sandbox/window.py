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
        self.connect(self.butAddToTree, SIGNAL("clicked()"), self.addToTree)
        self.connect(self.butGenerateSp, SIGNAL("clicked()"), self.generateSp)
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
        completer = QCompleter()
        self.lineSpecies.setCompleter(completer)
        model = QStringListModel()
        completer.setModel(model)
        self.getCompleteData(model, str(self.lineBlist.text()))

    def browSlist(self):
        self.lineSlist.clear()
        Slist = QFileDialog.getOpenFileName(self, "Open File 開啟物種清單檔案:", "./data/", "Text files (*.txt *.csv)")
        if Slist is None:
            return
        self.lineSlist.setText(Slist) 

    # import data into auto-completion list
    def getCompleteData(self, model, blist):
        b_container = []
        with open(blist, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for r in reader:
                # only read common names, name without author and family common name
                # ex: 松葉蕨, Psilotum nudum, 松葉蕨科
                b_container.append(r[2] + "," + r[3] + "," + r[1])
        model.setStringList(b_container)

    def addToTree(self):
        item = QTreeWidgetItem()     
        species_item = str.split(str(self.lineSpecies.text()), ',')
        item.setText(0, species_item[2])
        item.setText(1, species_item[1])
        item.setText(2, species_item[0])
        self.treeWidget.addTopLevelItem(item)
        self.lineSpecies.clear()

    def delFromTree(self):
        #removing the QTreeItemWidget object
        self.treeWidget.takeTopLevelItem(treeWidget.indexOfTopLevelItem(self))


    def get_all_items(self, tree_widget):
        all_items = []
        root = tree_widget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            all_items.append(item.text(2))
        return all_items

    def generateSp(self):
        temp_container = []
        print(self.treeWidget.items)
        tree_item = self.get_all_items(self.treeWidget)
        f = open('/tmp/log', 'a')
        for row in range(len(tree_item)):
            f.write(tree_item[row]+'\n')
        f.close()

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
