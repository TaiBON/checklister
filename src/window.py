#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
import genlist_api
from ui_window import Ui_Window
import re
import sqlite3
import codecs
import csv
import sys
import traceback
import os
import pycurl
import shutil

class Window(QWidget, Ui_Window):

    def __init__(self, parent = None):
        try:
            super(Window, self).__init__()
            #self.sqlite_db = g.resource_path('twnamelist.db')
            g = genlist_api.Genlist()
            db_filename = 'twnamelist.db'
            self.sqlite_db = g.resource_path(os.path.join('db', db_filename))
            self.setupUi(self)
            self.butBlist.clicked.connect(self.browBaselist)
            self.butSlist.clicked.connect(self.browSlist)
            self.butAddToTree.clicked.connect(self.addToTree)
            self.lineSpecies.returnPressed.connect(self.addToTree)
            self.butGenerateSp.clicked.connect(self.genNamelist)
            self.butSelectTempFile.clicked.connect(self.browTempfile)
            self.butSelectOutput.clicked.connect(self.browOutput)
            self.butDeleteAll.clicked.connect(self.delAllTreeItems)
            self.butDeleteSelection.clicked.connect(self.delSelectedItems)
            self.comboDBselect.activated.connect(self.spCompleter)
            self.butUpdateDB.clicked.connect(self.updateDB)
            # enable completer to show matched species list
            self.spCompleter()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def spCompleter(self):
        try:
            g = genlist_api.Genlist()
            completer = QCompleter()
            model = QStringListModel()
            completer.setModel(model)
            # QCompleter setFilterMode Qt>5.2
            # http://doc.qt.io/qt-5/qcompleter.html#filterMode-prop
            completer.setFilterMode(Qt.MatchContains)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.lineSpecies.setCompleter(completer)
            db_table = self.checkDB()
            retrieved = g.dbGetsp(db_table, self.sqlite_db)        
            b_container=[]
            for i in range(len(retrieved)):
                b_container.append(retrieved[i][3] +  "," + retrieved[i][4] + "," + retrieved[i][2])
            model.setStringList(b_container)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def browBaselist(self):
        """
        browBaselist: browse the baselist file 
        ======================================
        """
        try:
            self.lineBlist.clear()
            Blist = QFileDialog.getOpenFileName(self, self.tr("Open file:"), \
                    QDir.homePath(), self.tr("Text files (*.txt *.csv)"))[0]
            if Blist is '' or Blist is None:
                return
            else:
                self.lineBlist.setText(Blist) 
                completer = QCompleter()
                self.lineSpecies.setCompleter(completer)
                model = QStringListModel()
                completer.setModel(model)
                self.getCompleteData(model, Blist)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
 
    def checkDB(self):
        try:
            db_idx = self.comboDBselect.currentIndex()
            if db_idx == 0:
                db_table = 'dao_pnamelist_apg3'
            elif db_idx == 1:
                db_table = 'dao_pnamelist'
            elif db_idx == 2:
                db_table = 'dao_bnamelist'
            else:
                db_table = 'dao_pnamelist'
            return(db_table)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def updateDB(self):
        try:
            qApp.setOverrideCursor(Qt.WaitCursor)

            g = genlist_api.Genlist()
            curl = pycurl.Curl()
            orig_sqlite_db = g.resource_path(os.path.join('db', 'twnamelist.db'))
            backup_sqlite_db = g.resource_path(os.path.join('db', 'twnamelist.db.back'))
            latest_sqlite_db = g.resource_path(os.path.join('db', 'latest.db'))
            dburl = 'https://raw.github.com/mutolisp/namelist-generator/master/src/db/twnamelist.db'
            curl.setopt(pycurl.URL, dburl)
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.perform()
            if curl.getinfo(curl.HTTP_CODE) == 200:
                with open(latest_sqlite_db, 'wb') as f:
                    curl.setopt(curl.WRITEDATA, f)
                    curl.perform()
                shutil.copyfile(orig_sqlite_db, backup_sqlite_db)
                shutil.copyfile(latest_sqlite_db, orig_sqlite_db)
                QMessageBox.information(self, self.tr('Checklist generator'), self.tr('Update DB done!'))
                qApp.restoreOverrideCursor()
            else:
                QMessageBox.information(self, self.tr('Checklist generator'), self.tr('Update DB failed!'))
            curl.close()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def browSlist(self):
        try:
            self.lineSlist.clear()
            Slist = QFileDialog.getOpenFileName(self, self.tr(u"Open file"), \
                    QDir.homePath(), self.tr("Text files (*.txt *.csv)"))[0]
            if Slist is None or Slist is '':
                return
            self.lineSlist.setText(Slist)
            info_message = u'''When you load species file (only common names) to \
            generate checklist, the "checklist generator" will save a temporary file (filename_temp.txt/csv) within the same directory, \
            and load this species file into checklist below. You can add/remove species to generate checklist.'''
            QMessageBox.information(self, "Info", self.tr(info_message))
            Slist_str = str.split(str(Slist), '.')
            Slist_modified = Slist_str[0] + '_temp.' + Slist_str[1]
            self.lineTempFile.setText(Slist_modified)
            conn = sqlite3.connect(self.sqlite_db)
            curs = conn.cursor()
            drop_table = '''DROP TABLE IF EXISTS sample;'''
            create_sample = '''CREATE TABLE sample (zh_name varchar);'''
            curs.execute(drop_table)
            curs.execute(create_sample)
            with codecs.open(Slist, 'r', 'utf-8') as f:
                input_container = f.read().splitlines()
                for row in range(len(input_container)):
                    zhname = re.sub(' ', '', input_container[row]) 
                    # substitute zero-width no break-space
                    zhname = re.sub('\ufeff', '', zhname)
                    # substitute 台 to 臺
                    zhname = re.sub(u'台([灣|北|中|西|南|東])',r'臺\1', zhname)
                    # pass the empty lines
                    if zhname != '':
                        insert_db = '''
                        INSERT INTO sample (zh_name) VALUES ("%s");
                        ''' % zhname
                    curs.execute(insert_db)
                conn.commit()
            f.close()
            # check the target database table
            db_table = self.checkDB()
            query_list = '''
            SELECT n.family_zh,n.name,n.zh_name FROM %s n, sample s
            WHERE n.zh_name = s.zh_name order by family,name;
            ''' % db_table
            curs.execute(query_list)
            fetched_results = curs.fetchall() 
            # check phanton species (does not exist in our database)
            query_not_exists_sp = ''' 
                SELECT 
                    distinct s.zh_name 
                FROM 
                    sample s LEFT OUTER JOIN %s n 
                ON s.zh_name=n.zh_name
                WHERE n.zh_name is null;
            ''' % db_table 
            curs.execute(query_not_exists_sp)
            no_sp = curs.fetchall()
            nsp = []
            for i in no_sp:
                nsp.append(i[0])
            nsp = ', '.join(nsp)
            if len(nsp) > 0:
                QMessageBox.information(self, "Warning", \
                        self.tr(u"The following species did not exist in our database, please check again: %s" % nsp))
            # clean the tree first
            self.delAllTreeItems() 
            for i in range(len(fetched_results)):
                item = QTreeWidgetItem()
                item.setText(0, fetched_results[i][0])
                item.setText(1, fetched_results[i][1])
                item.setText(2, fetched_results[i][2])
                self.treeWidget.addTopLevelItem(item)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
 

    def browOutput(self):
        try:
            self.lineOutputFilename.clear()
            saveOutputFile = QFileDialog.getSaveFileName(self, self.tr(u"Save file as:"), \
                    QDir.homePath(), self.tr("Text files (*.docx *.odt)"))[0]
            if saveOutputFile is None or saveOutputFile is '':
                return
            self.lineOutputFilename.setText(saveOutputFile)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
 

    # import data into auto-completion list
    def getCompleteData(self, model, blist):
        try:
            b_container = []
            with open(blist, newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='|')
                for r in reader:
                    # only read common names, name without author and family common name
                    # ex: 松葉蕨, Psilotum nudum, 松葉蕨科
                    b_container.append(r[2] + "," + r[3] + "," + r[1])
            model.setStringList(b_container)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
 

    def getDbIdx(self):
        try:
            g = genlist_api.Genlist()
            db_idx = self.comboDBselect.currentIndex()
            if db_idx == 0:
                # APG III
                retrieved = g.dbGetsp('dao_pnamelist_apg3', self.sqlite_db)        
            elif db_idx == 1:
                # Flora of Taiwan
                retrieved = g.dbGetsp('dao_pnamelist', self.sqlite_db)  
            elif db_idx == 2:
                # Birdlist of Taiwan
                retrieved = g.dbGetsp('dao_bnamelist', self.sqlite_db)
            else:
                retrieved = g.dbGetsp('dao_pnamelist_apg3', self.sqlite_db)        
            b_container = []
            for i in range(len(retrieved)):
                    b_container.append([retrieved[i][2], retrieved[i][3], retrieved[i][4]])
            # returnlist
            return(b_container)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))


    def addToTree(self):
        try:
            if self.lineSpecies.text() is '':
                QMessageBox.information(self, "Warning", self.tr("Please input the species name!"))
                return
            else:
                # check for species items
                item = QTreeWidgetItem()     
                species_item = str.split(str(self.lineSpecies.text()), ',')
                # get species zh_name
                splist = self.getDbIdx()
                splist_zhname = []
                for i in range(len(splist)):
                        splist_zhname.append(splist[i][1])
                exists = 0
                for i, j in enumerate(splist_zhname):
                    if j == species_item[0]:
                        exists = 1
                if exists == 1:
                   item.setText(0, species_item[2])
                   item.setText(1, species_item[1])
                   item.setText(2, species_item[0])
                   self.treeWidget.addTopLevelItem(item)
                   self.lineSpecies.clear()
                else:
                    QMessageBox.information(self, "Warning", self.tr("The species %s did not exist in our database!") % species_item[0])
                    self.lineSpecies.clear()
            self.lineSpecies.clear()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def delFromTree(self):
        #removing the QTreeItemWidget object
        try:
            self.treeWidget.takeTopLevelItem(treeWidget.indexOfTopLevelItem(self))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
 

    def getTreeItems(self, tree_widget):
        try:
            all_items = []
            root = tree_widget.invisibleRootItem()
            child_count = root.childCount()
            for i in range(child_count):
                item = root.child(i)
                all_items.append(item.text(2))
            return all_items
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
 

    def delAllTreeItems(self):
    # TODO: 加入是否確定要全部刪除的確定
        self.treeWidget.clear()

    def delSelectedItems(self):
        try:
            root = self.treeWidget.invisibleRootItem()
            for item in self.treeWidget.selectedItems():
                    (item.parent() or root).removeChild(item)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    # 產生名錄
    def genNamelist(self):
        try:
            g = genlist_api.Genlist()
            tree_item = self.getTreeItems(self.treeWidget)
            # getdbtable
            db_table = self.checkDB()

            if self.lineOutputFilename.text() == '':
                QMessageBox.information(self, "Warning", self.tr("Please input export file name "))
            elif self.lineTempFile.text() == '' or self.lineSlist == '':
                QMessageBox.information(self, "Warning", self.tr("Please input the file to store checklist file"))
            else:
                saved_list = str(self.lineTempFile.text())
                with codecs.open(saved_list, 'w+', 'utf-8') as f:
                    for sp in tree_item:
                        f.write("%s\n" % sp)
                f.close()
                ofile = str(self.lineOutputFilename.text())
                output_flist = str.split(ofile, '.')
                # before generate namelist, clean up the sample table in sqlite db
                conn = sqlite3.connect(self.sqlite_db)
                curs = conn.cursor()
                curs.execute('DROP TABLE IF EXISTS sample;')
                conn.commit()
                # export outputfile
                g.genEngine(self.sqlite_db, db_table, saved_list, output_flist[1], output_flist[0])
                QMessageBox.information(self, self.tr('Checklist generator'), self.tr('Checklist generated!'))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def browTempfile(self):
        try:
            self.lineTempFile.clear()
            saveTempFile = QFileDialog.getSaveFileName(self, self.tr(u"Save File as ... "), QDir.homePath(), \
                    self.tr("Text files (*.txt *.csv)"))[0]
            if saveTempFile is None or saveTempFile is '':
                return
            self.lineTempFile.setText(saveTempFile) 
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
