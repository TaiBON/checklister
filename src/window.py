#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from ui_window import Ui_Window
import codecs
import csv
import genlist_api
import os
import pycurl
import re
import shutil
import sqlite3
import sys
import traceback

class Window(QWidget, Ui_Window):

    def __init__(self, parent = None):
        try:
            super(Window, self).__init__()
            
            #self.sqlite_db = g.resource_path('twnamelist.db')
            g = genlist_api.Genlist()
            self.g = genlist_api.Genlist()
            # only for main window
            #self.main_widget = QWidget(self)
            #self.setCentralWidget(self.main_widget)

            self.home = os.path.expanduser("~")
            self.checklist_db_dir = g.resource_path(os.path.join(self.home, 'checklist_db'))
            self.checklist_db = g.resource_path(os.path.join(self.checklist_db_dir, 'twnamelist.db'))
            self.latest_db = g.resource_path(os.path.join(self.checklist_db_dir, 'twnamelist_latest.db'))
            self.orig_db = g.resource_path(os.path.join(self.checklist_db_dir, 'twnamelist_orig.db'))
            self.sqlite_db = self.checkLocalDB()

            self.setupUi(self)
            #self = Ui_Window()
            #self.setupUi(self)

            #self.butBlist.clicked.connect(self.browBaselist)
            self.butSlist.clicked.connect(self.browSlist)
            self.butAddToTree.clicked.connect(self.addToTree)
            self.lineSpecies.returnPressed.connect(self.addToTree)
            self.butGenerateSp.clicked.connect(self.genChecklist)
            self.butSelectTempFile.clicked.connect(self.browTempfile)
            self.butSelectOutput.clicked.connect(self.browOutput)
            self.butDeleteAll.clicked.connect(self.delAllTreeItems)
            self.butDeleteSelection.clicked.connect(self.delSelectedItems)
            self.comboDBselect.activated.connect(self.spCompleter)
            self.butUpdateDB.clicked.connect(self.updateDB)
            # enable completer to show matched species list
            self.spCompleter()

            # comparison actions
            self.butCheckASelect.clicked.connect(self.selChecklistA)
            self.butCheckBSelect.clicked.connect(self.selChecklistB)
            self.butCompare.clicked.connect(self.checklistCompare)

            # merge checklist actions
            self.butMergeChecklists.clicked.connect(self.selMergedList)

            # combine checklist actions
            self.butCombineChecklists.clicked.connect(self.selCombineList)
            self.combined_checklists = list()

            # format excel scientific names
            self.butSelectExcel.clicked.connect(self.selExcelFile)
            self.butFormatName.clicked.connect(self.formatExcel)
            #self.checkBox.isChecked

            # load menubar
            #menubar = self.menuBar()
            #self.statusBar().showMessage(self.tr('Ready'))
            #self.setWindowTitle(self.tr('Checklist generator'))  


        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    
    def selChecklistA(self):
        try:
            self.lineChecklistA.clear()
            checklist_A = QFileDialog.getOpenFileName(self, self.tr(u"Open file"), \
                    QDir.homePath(), self.tr("Text files (*.txt)"))[0]
            if checklist_A is None or checklist_A is '':
                return
            self.lineChecklistA.setText(checklist_A)
            #status_bar = "Loading " + checklist_A 
            #self.statusBar().showMessage(self.tr(status_bar))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
    

    def selChecklistB(self):
        try:
            self.lineChecklistB.clear()
            checklist_B = QFileDialog.getOpenFileName(self, self.tr(u"Open file"), \
                    QDir.homePath(), self.tr("Text files (*.txt)"))[0]
            if checklist_B is None or checklist_B is '':
                return
            self.lineChecklistB.setText(checklist_B)
            #status_bar = "Loading " + checklist_B 
            #self.statusBar().showMessage(self.tr(status_bar))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    # load to be merged list 
    def selMergedList(self):
        try:
            self.lineMergeChecklists.clear()
            tobe_merged_lists = QFileDialog.getOpenFileNames(self, self.tr(u"Select checklist text files to merge"), \
                    QDir.homePath(), self.tr("Text files (*.txt)"))[0]
            if tobe_merged_lists is None or tobe_merged_lists == '':
                return
            tobe_merged_files = ', '.join(tobe_merged_lists)
            self.lineMergeChecklists.setText(tobe_merged_files)
            # load data into QTreeWidget
            m_lists = []
            for files in range(len(tobe_merged_lists)):
                with codecs.open(tobe_merged_lists[files], 'r', 'utf-8') as f:
                     m_lists += f.read().splitlines()
                f.close()
            m_lists_uniq = list(set(m_lists))
            if self.lineTempFile.text() == '':
                self.lineTempFile.setText(os.path.join(QDir.homePath(), 'merged_checklists.txt'))
            if len(m_lists_uniq) >= 1:
                self.bulkLoadToTree(m_lists_uniq)
            else:
                QMessageBox.information(self, "Warning", \
                        self.tr("There is nothing to load into the tree view of checklist. Maybe the files are empty"))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    # load to be combined list
    def selCombineList(self):
        """
        Combine multiple checklists
        ===========================
        """
        try:
            self.lineCombineChecklists.clear()
            tobe_combined_lists = QFileDialog.getOpenFileNames(self, self.tr(u"Select checklist text files to combine"), \
                    QDir.homePath(), self.tr("Text files (*.txt)"))[0]
            if tobe_combined_lists is None or tobe_combined_lists is '':
                return
            tobe_combined_files = ', '.join(tobe_combined_lists)
            self.lineCombineChecklists.setText(tobe_combined_files)
            g = genlist_api.Genlist()
            g.combineChecklists(self.sqlite_db, tobe_combined_lists) 
            current_db_table = self.checkDB()
            # print(current_db_table)
            if current_db_table == 'dao_bnamelist':
                db_fullname = 'name'
            else:
                db_fullname = 'fullname'
            fetch_combined_sql = '''
            SELECT 
                distinct d.family,d.family_cname,d.%s,u.* 
            FROM 
                tmp_union u, %s d
            WHERE
                u.local_name = d.cname;
            ''' % (db_fullname, current_db_table)
            combined_table = g.dbExecuteSQL(fetch_combined_sql, self.sqlite_db, show_results=True)
            print(combined_table)
            header = ['family', 'family_cname', 'name', 'common name']
            for i in range(len(tobe_combined_lists)):
                fname = str.split(os.path.split(tobe_combined_lists[i])[1], '.')
                header.insert(4+i, fname[0])
            header = tuple(header)
            combined_table.insert(0, header)
            if self.lineOutputFilename.text() is None or self.lineOutputFilename.text() == '':
                export_filename = os.path.join(QDir.homePath(), 'combined_checklists.xlsx')
                self.lineOutputFilename.setText(export_filename)
            else:
                export_filename = self.lineOutputFilename.text()
            self.combined_checklists = combined_table
            print(self.combined_checklists)
            # clear temp file for local names & Slist
            self.lineTempFile.clear()
            self.lineSlist.clear()
            # load data into QTreeWidget
            self.delAllTreeItems() 
            for i in range(1,len(combined_table)):
                item = QTreeWidgetItem()
                # family_cname, name, common name
                item.setText(0, combined_table[i][1])
                item.setText(1, combined_table[i][2])
                item.setText(2, combined_table[i][3])
                self.treeWidget.addTopLevelItem(item)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
    def selExcelFile(self):
        try:
            self.lineExcelFilePath.clear()
            orig_excel_file = QFileDialog.getOpenFileName(self, self.tr(u"Select excel files"), \
                    QDir.homePath(), self.tr("Excel files (*.xls *.xlsx)"))[0]
            if orig_excel_file is None or orig_excel_file is '':
                return
            self.lineExcelFilePath.setText(orig_excel_file)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))


    def formatExcel(self):
        try:
            orig_excel_file = self.lineExcelFilePath.text()
            ncol = self.lineExcelColnum.text()
            if orig_excel_file is None or orig_excel_file is '':
                QMessageBox.information(self, "Warning", self.tr(u"Please input the excel filename"))
            elif ncol is None or ncol is '':
                QMessageBox.information(self, "Warning", self.tr(u"Please input the column number of scientific names"))
            else:
                # get filename and os path
                base_path = os.path.split(orig_excel_file)[0]
                excel_filename = str.split(os.path.split(orig_excel_file)[1], '.')[0]
                formatted_excel_filename = excel_filename + '_formatted.xlsx'
                ncol = int(self.lineExcelColnum.text())
                formatted_filepath = os.path.join(base_path, formatted_excel_filename)
                self.g.fmtExcelNames(original=orig_excel_file, outputfile=formatted_filepath, \
                        name_col_num=ncol)
                QMessageBox.information(self, "Notice", self.tr(u"Formatted excel file:  %s done!" % formatted_filepath))
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

    #def browBaselist(self):
    #    """
    #    browBaselist: browse the baselist file 
    #    ======================================
    #    """
    #    try:
    #        self.lineBlist.clear()
    #        Blist = QFileDialog.getOpenFileName(self, self.tr("Open file:"), \
    #                QDir.homePath(), self.tr("Text files (*.txt *.csv)"))[0]
    #        if Blist is '' or Blist is None:
    #            return
    #        else:
    #            self.lineBlist.setText(Blist) 
    #            completer = QCompleter()
    #            self.lineSpecies.setCompleter(completer)
    #            model = QStringListModel()
    #            completer.setModel(model)
    #            self.getCompleteData(model, Blist)
    #    except BaseException as e:
    #        QMessageBox.information(self, "Warning", str(e))
 
    def checkDB(self):
        try:
            db_idx = self.comboDBselect.currentIndex()
            if db_idx == 0:
                db_table = 'dao_pnamelist_apg3'
            elif db_idx == 1:
                db_table = 'dao_pnamelist'
            elif db_idx == 2:
                db_table = 'dao_bnamelist'
            elif db_idx == 3:
                db_table = 'dao_jp_ylist'
            else:
                db_table = 'dao_pnamelist'
            return(db_table)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def checklistCompare(self):
        try:
            # 1. check for A and B
            checklist_A = self.lineChecklistA.text()
            checklist_B = self.lineChecklistB.text()
            if checklist_A == '':
                QMessageBox.information(self, "Warning", self.tr("Please input checklist A"))
            elif checklist_B == '':
                QMessageBox.information(self, "Warning", self.tr("Please input checklist B"))
            else:
                with codecs.open(checklist_A, 'r', 'utf-8') as f:
                    self.a = f.read().splitlines()
                f.close()
                with codecs.open(checklist_B, 'r', 'utf-8') as f:
                    self.b = f.read().splitlines()
                f.close()
                # get different types (difference, intersection, union)
                ab_idx = self.comboABDifference.currentIndex()
                if self.a == self.b:
                    QMessageBox.information(self, "Warning", self.tr("A and B are identical!"))
                else:
                    if ab_idx == 0:
                        ab_type = ['ab', 'diff']
                        compare_result = set(self.a).difference(self.b)
                    elif ab_idx == 1:
                        ab_type = ['ba', 'diff']
                        compare_result = set(self.b).difference(self.a)
                    elif ab_idx == 2:
                        ab_type = ['ab', 'intersection']
                        compare_result = set(self.a).intersection(self.b)
                    elif ab_idx == 3:
                        ab_type = ['ab', 'union']
                        compare_result = set(self.a).union(self.b)
                    else:
                        ab_type = ['ab', 'diff']
                        compare_result = set(self.a).difference(self.b)
                        compare_result = set(self.a).difference(self.b)
                    # set temporary checklist file
                    a_path = os.path.split(checklist_A)[0]
                    a_filename = os.path.split(checklist_A)[1].split('.')[0]
                    b_filename = os.path.split(checklist_B)[1].split('.')[0]
                    tmp_filename = a_filename + '_' + b_filename + '-' + ab_type[0] + '_' + ab_type[1] + '.txt'
                    self.lineTempFile.setText(os.path.join(a_path, tmp_filename))
                    compare_result = list(compare_result)
                    # load compared list into QTreeWidget
                    if len(compare_result) >= 1:
                        self.bulkLoadToTree(compare_result)
                    else:
                        QMessageBox.information(self, "Warning", self.tr("There is no common species between checklist A and B"))
                        self.delAllTreeItems()

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def checkLocalDB(self):
        try:
            g = genlist_api.Genlist()
            db_filename = 'twnamelist.db'
            builtin_sqlite_db = g.resource_path(os.path.join('db', db_filename))
            if not os.path.exists(self.checklist_db_dir):
                os.mkdir(self.checklist_db_dir)
                # copy db to user directory
                shutil.copy(builtin_sqlite_db, self.checklist_db)
                shutil.copy(builtin_sqlite_db, self.latest_db)
            if not os.path.exists(self.latest_db):
                shutil.copy(builtin_sqlite_db, self.latest_db)
            return(self.checklist_db)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))


    def updateDB(self):
        try:
            self.checkLocalDB()
            # backup original database
            shutil.copy(self.checklist_db, self.orig_db)
            # use pycurl to update database
            curl = pycurl.Curl()
            dburl = 'https://raw.github.com/mutolisp/namelist-generator/master/src/db/twnamelist.db'
            curl.setopt(pycurl.URL, dburl)
            curl.setopt(pycurl.FOLLOWLOCATION, True)
            #curl.perform()
            #if curl.getinfo(curl.HTTP_CODE) == 200:
            with open(self.latest_db, 'wb+') as f:
                curl.setopt(curl.WRITEDATA, f)
                curl.perform()
            # update to latest
            shutil.copy(self.latest_db, self.checklist_db)
            QMessageBox.information(self, self.tr('Checklist generator'), self.tr('Update DB done!'))
            #else:
            #    QMessageBox.information(self, self.tr('Checklist generator'), self.tr('Update DB failed!')
            #qApp.restoreOverrideCursor()
            curl.close()
            # update completer
            self.spCompleter()
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
            create_sample = '''CREATE TABLE sample (cname varchar);'''
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
                        INSERT INTO sample (cname) VALUES ("%s");
                        ''' % zhname
                    curs.execute(insert_db)
                conn.commit()
            f.close()
            # check the target database table
            db_table = self.checkDB()
            query_list = '''
            SELECT n.family_cname,n.name,n.cname FROM %s n, sample s
            WHERE n.cname = s.cname order by family,name;
            ''' % db_table
            curs.execute(query_list)
            fetched_results = curs.fetchall() 
            # check phanton species (does not exist in our database)
            query_not_exists_sp = ''' 
                SELECT 
                    distinct s.cname 
                FROM 
                    sample s LEFT OUTER JOIN %s n 
                ON s.cname=n.cname
                WHERE n.cname is null;
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

    def bulkLoadToTree(self, local_name_list):
        try:
            # QTreeItems
            conn = sqlite3.connect(self.sqlite_db)
            curs = conn.cursor()
            drop_table = '''DROP TABLE IF EXISTS compare_sample;'''
            create_sample = '''CREATE TABLE compare_sample (cname varchar);'''
            curs.execute(drop_table)
            curs.execute(create_sample)
            for row in range(len(local_name_list)):
                zhname = re.sub(' ', '', local_name_list[row]) 
                zhname = re.sub('\ufeff', '', zhname)
                # substitute 台 to 臺
                zhname = re.sub(u'台([灣|北|中|西|南|東])',r'臺\1', zhname)
                # pass the empty lines
                if zhname != '':
                    insert_db = '''
                    INSERT INTO compare_sample (cname) VALUES ("%s");
                    ''' % zhname
                curs.execute(insert_db)
            conn.commit()
            # check the target database table
            db_table = self.checkDB()
            query_list = '''
            SELECT n.family_cname,n.name,n.cname FROM %s n, compare_sample s
            WHERE n.cname = s.cname order by family,name;
            ''' % db_table
            curs.execute(query_list)
            fetched_results = curs.fetchall() 
            # check phanton species (does not exist in our database)
            query_not_exists_sp = ''' 
                SELECT 
                    distinct s.cname 
                FROM 
                    compare_sample s LEFT OUTER JOIN %s n 
                ON s.cname=n.cname
                WHERE n.cname is null;
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
                    QDir.homePath(), self.tr("Text files (*.docx *.odt *.xlsx)"))[0]
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
            elif db_idx == 3:
                # Plant list of Japan (Ylist, cached: 2015-10-15)
                retrieved = g.dbGetsp('dao_jp_ylist', self.sqlite_db)
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
                # get species cname
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
    def genChecklist(self):
        #try:
        g = genlist_api.Genlist()
        tree_item = self.getTreeItems(self.treeWidget)
        # getdbtable
        db_table = self.checkDB()
        export_filename = self.lineOutputFilename.text()
        if self.lineOutputFilename.text() == '':
            QMessageBox.information(self, "Warning", self.tr("Please input export file name "))
        elif self.lineTempFile.text() == '' or self.lineSlist == '':
            if self.lineCombineChecklists.text() != '':
                export_combined_checklist_file = self.lineOutputFilename.text()
                g.listToXls(self.combined_checklists, 2, export_combined_checklist_file)
                QMessageBox.information(self, self.tr('Checklist generator'), \
                    self.tr("Export checklist to '%s' done!" % export_filename))
                self.lineCombineChecklists.clear()
            else:
                QMessageBox.information(self, "Warning", self.tr("Please input the file to store checklist file"))
        else:
            saved_list = str(self.lineTempFile.text())
            with codecs.open(saved_list, 'w+', 'utf-8') as f:
                for sp in tree_item:
                    f.write("%s\n" % sp)
            f.close()
            ofile = str(self.lineOutputFilename.text())
            if os.path.exists(ofile) == True:
                ofile_abspath = g.resource_path(ofile)
                shutil.copyfile(ofile_abspath, ofile_abspath+'.bak')
                os.remove(ofile_abspath)
            output_flist = str.split(ofile, '.')
            # before generate namelist, clean up the sample table in sqlite db
            conn = sqlite3.connect(self.sqlite_db)
            curs = conn.cursor()
            curs.execute('DROP TABLE IF EXISTS sample;')
            conn.commit()
            # export outputfile
            g.genEngine(self.sqlite_db, db_table, saved_list, output_flist[1], output_flist[0])
            QMessageBox.information(self, self.tr('Checklist generator'), \
                    self.tr("Export checklist to '%s' done!" % export_filename))
        #except BaseException as e:
        #    QMessageBox.information(self, "Warning", str(e))

    def browTempfile(self):
        try:
            self.lineTempFile.clear()
            saveTempFile = QFileDialog.getSaveFileName(self, self.tr(u"Save File as ... "), QDir.homePath(), \
                    self.tr("Text files (*.txt *.csv)"))[0]
            if saveTempFile is None or saveTempFile is '':
                return
            self.lineTempFile.setText(saveTempFile) 
        except BaseException as e:
            MessageBox.information(self, "Warning", str(e))
