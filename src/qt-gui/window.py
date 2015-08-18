from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#(QApplication, QWidget, QDialog, QFileDialog, QCompleter)
from genlist_api import *

from ui_window import Ui_Window
import genlist_api
Blist = ''
class Window(QWidget, Ui_Window):
    
    def __init__(self, parent = None):
        super(Window, self).__init__()
        #QWidget.__init__(self, parent)
        self.setupUi(self)
        self.butBlist.clicked.connect(self.browBaselist)
        self.butSlist.clicked.connect(self.browSlist)
        self.butGenerate.clicked.connect(self.genList)
        self.butAddToTree.clicked.connect(self.addToTree)
        self.butGenerateSp.clicked.connect(self.generateSp)
        self.butSelectTempFile.clicked.connect(self.browTempfile)
        self.butSelectOutput.clicked.connect(self.browOutput)
        self.butDeleteAll.clicked.connect(self.delAllTreeItems)
        self.butDeleteSelection.clicked.connect(self.delSelectedItems)

        #self.connect(self.butBlist, SIGNAL("clicked()"), self.browBaselist)
        #self.connect(self.butSlist, SIGNAL("clicked()"), self.browSlist)
        #self.connect(self.butGenerate, SIGNAL("clicked()"), self.genList)
        #self.connect(self.butAddToTree, SIGNAL("clicked()"), self.addToTree)
        #self.connect(self.butGenerateSp, SIGNAL("clicked()"), self.generateSp)
        #self.connect(self.butSelectTempFile, SIGNAL("clicked()"), self.browTempfile)
        #self.connect(self.butSelectOutput, SIGNAL("clicked()"), self.browOutput)
        #self.connect(self.butDeleteAll, SIGNAL("clicked()"), self.delAllTreeItems)
        #self.connect(self.butDeleteSelection, SIGNAL("clicked()"), self.delSelectedItems)

    def browBaselist(self):
        """
        browBaselist: browse the baselist file 
        ======================================
        """
        self.lineBlist.clear()
        Blist = QFileDialog.getOpenFileName(self, self.tr("Open File 開啟物種資料檔案:"), QDir.homePath(), self.tr("Text files (*.txt *.csv)"))[0]
        if Blist is None:
            return
        self.lineBlist.setText(Blist) 
        completer = QCompleter()
        self.lineSpecies.setCompleter(completer)
        model = QStringListModel()
        completer.setModel(model)
        self.getCompleteData(model, Blist)

    def browSlist(self):
        self.lineSlist.clear()
        Slist = QFileDialog.getOpenFileName(self, self.tr("Open File 開啟物種清單檔案:"), QDir.homePath(), self.tr("Text files (*.txt *.csv)"))[0]
        if Slist is None:
            return
        self.lineSlist.setText(Slist) 

    def browOutput(self):
        self.lineOutputFilename.clear()
        saveOutputFile = QFileDialog.getSaveFileName(self, self.tr("Save File as 儲存輸出的名錄檔案:"), \
                QDir.homePath(), self.tr("Text files (*.docx *.odt *.txt)"))[0]
        if saveOutputFile is None:
            return
        self.lineOutputFilename.setText(saveOutputFile)

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

    def getTreeItems(self, tree_widget):
        all_items = []
        root = tree_widget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            all_items.append(item.text(2))
        return all_items

    def delAllTreeItems(self):
    # TODO: 加入是否確定要全部刪除的確定
        self.treeWidget.clear()

    def delSelectedItems(self):
        root = self.treeWidget.invisibleRootItem()
        for item in self.treeWidget.selectedItems():
                (item.parent() or root).removeChild(item)

    # 產生單一物種的清單檔案
    def generateSp(self):
        g = genlist_api.Genlist()
        tree_item = self.getTreeItems(self.treeWidget)
        if self.lineBlist.text() == '':
            QMessageBox.information(self, "Warning", "請指定物種資料檔案")
        elif self.lineOutputFilename.text() == '':
            QMessageBox.information(self, "Warning", "請指定輸出檔案名稱")
        elif self.lineTempFile.text() == '':
            QMessageBox.information(self, "Warning", "請指定要存物種清單之檔案")
        else:
            saved_list = str(self.lineTempFile.text())
            f = open(saved_list, 'w')
            for sp in tree_item:
                f.write("%s\n" % sp)
            f.close()
            dbfile = str(self.lineBlist.text())
            ofile = str(self.lineOutputFilename.text())
            output_flist = str.split(ofile, '.')
            g.generator(dbfile, saved_list, output_flist[1], output_flist[0])
            QMessageBox.information(self, "名錄產生器", "名錄已產生完畢")

    def browTempfile(self):
        self.lineTempFile.clear()
        saveTempFile = QFileDialog.getSaveFileName(self, self.tr("Save File as 開啟物種清單檔案:"), QDir.homePath(), \
                self.tr("Text files (*.txt *.csv)"))[0]
        if saveTempFile is None:
            return
        self.lineTempFile.setText(saveTempFile) 

    def genList(self):
        g = genlist_api.Genlist()
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
            output_flist = str.split(ofile, '.')
            g.generator(dbfile, sample_file, output_flist[1], output_flist[0])
            QMessageBox.information(self, "名錄產生器", "名錄已產生完畢")
