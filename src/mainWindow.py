#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
.. module:: MainWindow
   :synopsis: checklister main window
.. moduleauthor:: Cheng-Tao Lin
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QDesktopServices
from PyQt5.QtWidgets import *
from ui_main import Ui_MainWindow
from ui_about import Ui_AboutDialog
from ui_combine import Ui_CombineDialog
from ui_compare import Ui_CompareDialog
from ui_format import Ui_FormatDialog
from ui_databases import Ui_DBMainWindow
from platform import uname
from subprocess import Popen
from datetime import datetime # datetime
import codecs
import csv
import genlist_api
import os
import pycurl
import re
import shutil
import speech_recognition as sr # speech recognition
import sqlite3
import sys
import tempfile
import traceback
import uuid     # Python UUID, for generate a checklist id
import yaml     # Python YAML



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        try:
            super().__init__(parent)
            g = genlist_api.Genlist()
            self.g = genlist_api.Genlist()

            self.home = os.path.expanduser("~")
            # checking database status
            self.checklist_db_dir = self.g.resource_path(os.path.join(self.home, 'checklist_db'))
            self.checklist_db = self.g.resource_path(os.path.join(self.checklist_db_dir, 'twnamelist.db'))
            self.latest_db = self.g.resource_path(os.path.join(self.checklist_db_dir, 'twnamelist_latest.db'))
            self.orig_db = self.g.resource_path(os.path.join(self.checklist_db_dir, 'twnamelist_orig.db'))
            self.sqlite_db = self.checkLocalDB()

            self.setupUi(self)

            #add icon
            self.setWindowIcon(QIcon('icons/checklister_small.png'))

            # set up variables
            self.tempDir = tempfile.gettempdir()
            self.tempExpFile = os.path.join(self.tempDir, 'checklister_exp_filename.txt')
            # Clear temp files
            self.clearOutputFilename()

            #self.butGenerateSp.clicked.connect(self.genChecklist)
            # self.comboDBselect.activated.connect(self.spCompleter)
            # self.butUpdateDB.clicked.connect(self.updateDB)

            ### COMPLETER
            # enable completer to show matched species list
            self.spCompleter()

            # DBViewer
            # self.dbViewer()
            # self.butViewTable.clicked.connect(self.viewTable)

            ### MENUBARS
            # load menubar
            self.statusBar().showMessage(self.tr('Ready'))
            # Menubar::File
            self.actionNewProject.triggered.connect(self.newProj)
            self.actionSelectExport.triggered.connect(self.browOutput)
            self.actionBatch.triggered.connect(self.browSlist)
            self.actionExportChecklist.triggered.connect(self.genChecklist)
            self.actionQuit.triggered.connect(self.closeApp)
            # Menubar::Edit
            self.actionDeleteSel.triggered.connect(self.delSelectedItems)
            self.actionDeleteAll.triggered.connect(self.delAllTreeItems)
            self.actionDeselectAll.triggered.connect(self.deselectTreeItmes)
            self.actionSelectAll.triggered.connect(self.selectAllTreeItmes)
            self.actionClearSp.triggered.connect(self.lineSpecies.clear)

            # Menubar::Databases
            self.actionTaiwanVascularPlants.triggered.connect(self.checkDB)
            self.actionTaiwanFlora.triggered.connect(self.checkDB)
            self.actionTaiwanRedList2017.triggered.connect(self.checkDB)
            self.actionJapanYlist.triggered.connect(self.checkDB)
            self.actionUpdateDB.triggered.connect(self.updateDB)
            self.actionDatabaseInfo.triggered.connect(self.openDBMainWindow)

            # Menubar::View
            self.actionShowToolbarText.triggered.connect(self.setToolBarText)

            # Menubar::Help
            self.actionHomepage.triggered.connect(self.urlHomepage)
            self.actionReportIssues.triggered.connect(self.urlIssue)
            self.actionAbout.triggered.connect(self.openAboutDialog)

            # Menubar::Window
            self.actionShowEdit.triggered.connect(self.showEdit)
            self.actionShowSearch.triggered.connect(self.showSearch)
            self.actionShowTaxonInfo.triggered.connect(self.showTaxonInfo)

            # Only in Toolbar actions
            self.actionSaveTxt.triggered.connect(self.saveChecklistTxt)
            self.actionTropicos.triggered.connect(self.searchTropicos)
            self.actionNomenMatch.triggered.connect(self.searchNomenMatch)
            self.actionAddSpecies.triggered.connect(self.addToTree)

            self.actionMerge.triggered.connect(self.selMergedList)
            self.actionCombine.triggered.connect(self.openCombDialog)
            self.actionCompare.triggered.connect(self.openCompareDialog)
            self.actionFormat.triggered.connect(self.openFormatDialog)

            # actionGroups
            self.setPlantDBActionGroup()

            # Taxon TreeWidget
            self.treeWidget.itemPressed.connect(self.getTaxonInfo)
            self.treeWidget.itemPressed.connect(self.getWebInfo)
            self.treeWidget.currentItemChanged.connect(self.getTaxonInfo)
            self.treeWidget.currentItemChanged.connect(self.getWebInfo)
            self.buttonReload.clicked.connect(self.butLoadWeb)
            self.backwardButton.clicked.connect(self.webBackward)
            self.forwardButton.clicked.connect(self.webForward)
            self.stopButton.clicked.connect(self.webStop)

            #self.webDBSelectButton.connect(self.checkWebDB)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
    def newProj(self):
        """
        newProj
        =======
        Synopsis: initiating a new project

        Args:
        ----------
        None

        Returns:
        --------
        None
        """
        try:
            self.clearOutputFilename()
            self.lineSpecies.clear()
            self.textBrowserInfo.clear()
            self.delAllTreeItems()
            self.statusBar().showMessage(self.tr(u'Ready'))

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def setPlantDBActionGroup(self):
        try:
            actionGroupP = QActionGroup(self.menuPlants, exclusive = True)
            actionGroupP.addAction(self.actionTaiwanVascularPlants)
            actionGroupP.addAction(self.actionTaiwanRedList2017)
            actionGroupP.addAction(self.actionTaiwanFlora)
            actionGroupP.addAction(self.actionJapanYlist)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def showEdit(self):
        try:
            if self.actionShowEdit.isChecked():
                self.toolBarEdit.setVisible(True)
            else:
                self.toolBarEdit.setVisible(False)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def showSearch(self):
        try:
            if self.actionShowSearch.isChecked():
                self.toolBarSearch.setVisible(True)
            else:
                self.toolBarSearch.setVisible(False)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def showTaxonInfo(self):
        try:
            if self.actionShowTaxonInfo.isChecked():
                self.dockWidgetTaxonInfo.setVisible(True)
            else:
                self.dockWidgetTaxonInfo.setVisible(False)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def setToolBarText(self):
        try:
            if self.actionShowToolbarText.isChecked():
                self.toolBarEdit.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                self.toolBarSearch.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            else:
                self.toolBarEdit.setToolButtonStyle(Qt.ToolButtonIconOnly)
                self.toolBarSearch.setToolButtonStyle(Qt.ToolButtonIconOnly)
        except BaseException as e:
           QMessageBox.information(self, "Warning", str(e))

    def openCombDialog(self):
        try:
            self.CombineDialog = CombineDialog(self)
            self.CombineDialog.setWindowFlags(self.CombineDialog.windowFlags() | Qt.WindowStaysOnTopHint)
            self.CombineDialog.show()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def openCompareDialog(self):
        try:
            self.CompareDialog = CompareDialog(self)
            self.CompareDialog.setWindowFlags(self.CompareDialog.windowFlags() | Qt.WindowStaysOnTopHint)
            self.CompareDialog.show()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def openFormatDialog(self):
        try:
            self.FormatDialog = FormatDialog(self)
            self.FormatDialog.setWindowFlags(self.FormatDialog.windowFlags() | Qt.WindowStaysOnTopHint)
            self.FormatDialog.show()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def openAboutDialog(self):
        try:
            self.AboutDialog = AboutDialog(self)
            self.AboutDialog.setWindowFlags(self.AboutDialog.windowFlags() | Qt.WindowStaysOnTopHint)
            self.AboutDialog.show()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def openDBMainWindow(self):
        try:
            self.DBMainWindow = checklistDB(self)
            #self.DBMainWindow.setWindowFlags(self.DBMainWindow.windowFlags() | Qt.WindowStaysOnTopHint)
            self.DBMainWindow.show()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))


    def urlHomepage(self):
        try:
            url = 'https://github.com/TaiBON/checklister'
            QDesktopServices.openUrl(QUrl(url))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def urlIssue(self):
        try:
            url = 'https://github.com/TaiBON/checklister/issues'
            QDesktopServices.openUrl(QUrl(url))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def closeApp(self):
        self.close()

    def keyPressEvent(self, qKeyEvent):
        '''
        shortcut key events
        '''
        try:

            if qKeyEvent.key() == Qt.Key_Return or qKeyEvent.key() == Qt.Key_Enter:
                if self.lineSpecies.text() is not None:
                    self.addToTree()
                self.lineSpecies.clear()
            if qKeyEvent.key() == Qt.Key_Escape:
                self.lineSpecies.clear()
            if qKeyEvent.key() == Qt.Key_Delete or qKeyEvent.key() == Qt.Key_Backspace:
                self.delSelectedItems()
           # ctrl/command + s: save txt files
            if qKeyEvent.key() == Qt.Key_S and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.saveChecklistTxt()
            # ctrl/command + e: export checklist 輸出名錄
            if qKeyEvent.key() == Qt.Key_E and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.genChecklist()
            # ctrl/command + o: save export file
            if qKeyEvent.key() == Qt.Key_O and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.browOutput()
            # ctrl/command + b: open batch file
            if qKeyEvent.key() == Qt.Key_B and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.browSlist()
            if qKeyEvent.key() == Qt.Key_S and (qKeyEvent.modifiers() & Qt.AltModifier):
                self.tabWidget.setCurrentIndex(0)
            elif qKeyEvent.key() == Qt.Key_D and (qKeyEvent.modifiers() & Qt.AltModifier):
                self.tabWidget.setCurrentIndex(1)
            elif qKeyEvent.key() == Qt.Key_A and (qKeyEvent.modifiers() & Qt.AltModifier):
                self.tabWidget.setCurrentIndex(2)
            if qKeyEvent.key() == Qt.Key_G and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.speechAddToTree()
                self.statusBar().showMessage(self.tr('Speech recognizing...please say plant common name'))
            # websearch
            if qKeyEvent.key() == Qt.Key_T and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.searchTropicos()
            if qKeyEvent.key() == Qt.Key_J and (qKeyEvent.modifiers() & Qt.ControlModifier):
                self.searchNomenMatch()


        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def butCheckPath(self, text_edit_path):
        """
        butCheckPath(text_edit)
        ==========================
        Synopsis: check if the "Text Edit" field exists. If the "Text Edit" exists, then let 
        it become a global variable.

        text_edit: Qt Text Edit 

        """
        try:
            if text_edit_path is None or text_edit_path is '':
                text_edit_path = QDir.homePath()
            else:
                if os.path.isdir(text_edit_path) == True:
                    pass
                else:
                    text_edit_path = os.path.split(text_edit_path)[0]
                    if os.path.exists(text_edit_path) == True:
                        pass 
                    else:
                        text_edit_path = QDir.homePath()
            return(text_edit_path)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
            self.statusBar().showMessage(self.tr('Debug: butCheckPath error!'))

   # load to be merged list 
    def selMergedList(self):
        try:
            tobe_merged_lists = QFileDialog.getOpenFileNames(self, self.tr(u"Select checklist text files to merge"), \
                '', self.tr("Text files (*.txt)"))[0]
            if tobe_merged_lists is None or tobe_merged_lists == '':
                return
            tobe_merged_files = ', '.join(tobe_merged_lists)
            # load data into QTreeWidget
            m_lists = []
            for files in range(0,len(tobe_merged_lists)):
                with codecs.open(tobe_merged_lists[files], 'r', 'utf-8') as f:
                     m_lists += f.read().splitlines()
                f.close()
            m_lists_uniq = list(set(m_lists))
            if len(m_lists_uniq) >= 1:
                self.bulkLoadToTree(m_lists_uniq)
            else:
                QMessageBox.information(self, "Warning", \
                        self.tr("There is nothing to load into the tree view of checklist. Maybe the files are empty"))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def getTaxonInfo(self):
        '''
        getTaxonInfo
        ============

        '''
        try:
            item = self.treeWidget.currentItem()
            if item:
                fullname = self.g.fmtname(str(item.text(1)), doformat=True, format_type='html', split=False)
                family_cname = str(item.text(0))
                cname = str(item.text(2))
                # check database
                db_table = self.selectDB()
                # get full information from data tables
                QUERYSPINFO = '''
                    SELECT
                        n.family,
                        n.cname,
                        n.endemic,
                        n.iucn_category,
                        n.source,
                        n.id
                    FROM %s n
                    WHERE n.cname = '%s';
                ''' % (db_table, cname)
                conn = sqlite3.connect(self.sqlite_db)
                curs = conn.cursor()
                curs.execute(QUERYSPINFO)
                taxonRes = curs.fetchall()
                family = taxonRes[0][0]
                endemic = taxonRes[0][2]
                taxonID = taxonRes[0][5]
                taxonAttr = []
                if endemic == 1:
                    endemic = self.tr(u'<font color="#aaaaaa">(Endemic)</font>')
                else:
                    endemic = ''
                iucn = taxonRes[0][3]
                if len(iucn) > 0:
                    taxonAttr.append('(' + iucn + ')')
                source = taxonRes[0][4]
                if source != '未知' and source !='原生':
                    taxonAttr.append(source)
                taxonAttr = ' '.join(taxonAttr)
                if len(taxonAttr) > 0:
                    taxonInfo = '''<b>Info</b>:<br/>%s<br/>''' % taxonAttr
                else:
                    taxonInfo = '<br/>'
                ## get synonyms

                # get all of the table name first
                queryTableList = '''SELECT name FROM sqlite_master WHERE type = "table"'''
                curs.execute(queryTableList)
                allTables = curs.fetchall()
                tabList = []
                for tab in allTables:
                    tabList.append(tab[0])
                # if the synonym table exists, list all the synonyms
                synonymTab = db_table + '_synonym'
                if synonymTab in tabList:
                    querySynonyms = '''
                    SELECT
                        namecode,
                        synonyms
                    FROM
                        %s
                    WHERE id=%i
                    ''' % (synonymTab, int(taxonID))
                    curs.execute(querySynonyms)
                    synonymList = []
                    synonyms = curs.fetchall()
                    if len(synonyms) > 0:
                        for syn in range(0, len(synonyms)):
                            synonymsFmt = self.g.fmtname(synonyms[syn][1], \
                                    doformat=True, format_type='html', split=False)
                            synonymList.append(synonymsFmt)
                        synonymList = '<br/>\n'.join(synonymList)
                        synonymHtml = '''
                        <p class="synonyms">
                        <b>Synonyms</b>: <br/>
                        %s
                        </p>
                        ''' % synonymList
                        synonymList + '''</p>'''
                    else:
                        synonymHtml = '<br/>'
                else:
                    synonymHtml = '<br/>'
                # export
                taxonInfo = '''
                <p class="info">
                <h3>%s %s %s</h3>
                <br/>
                <b>Family</b>:<br/> %s (%s)<br/>
                </p>
                %s
                %s
                ''' % (fullname, cname, endemic, \
                        family_cname, family, \
                        taxonInfo, synonymHtml)

                self.textBrowserInfo.setText(taxonInfo)
                self.statusBar().showMessage(cname)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def getWebInfo(self):
        '''
        getWebInfo
        ============
        Obtain
        '''
        try:
            item = self.treeWidget.currentItem()
            if item:
                fullname = self.g.fmtname(str(item.text(1)), doformat=False, split=True)
                fullnameNoAuthors = fullname[0]
                cname = ' '.join([item.text(1), fullnameNoAuthors])
                queryUrl = self.checkWebDB(fullnameNoAuthors)
                self.loadUrl(queryUrl)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))
    
    def checkWebDB(self, species):
        '''
        search for species on taxoninfo widget
        '''
        try:
            webDBIdx = self.webDBSelectButton.currentIndex()
            if webDBIdx == 0:
                queryUrl = '''http://www.eol.org/search?q=%s&search=Go''' % species
            elif webDBIdx == 1:
                # tropicos
                queryUrl = '''http://tropicos.org/NameSearch.aspx?name=%s&commonname=''' % species
            elif webDBIdx == 2:
                # theplantlist
                queryUrl = '''http://www.theplantlist.org/tpl1.1/search?q=%s''' % species
                pass
            elif webDBIdx == 3:
                # TaiBNET
                queryUrl = '''http://taibnet.sinica.edu.tw/chi/taibnet_species_list.php?T2=%s&T2_new_value=true&fr=y''' % species
            elif webDBIdx == 4:
                # IPNI
                spSplitted = species.split(' ')
                if len(spSplitted) == 2:
                    queryUrl = '''http://www.ipni.org/ipni/advPlantNameSearch.do?find_genus=%s&find_species=%s&find_rankToReturn=spec''' % (spSplitted[0], spSplitted[1])
                elif len(spSplitted) >= 4:
                    queryUrl = '''http://www.ipni.org/ipni/advPlantNameSearch.do?find_genus=%s&find_species=%s&find_infraspecies=%s''' % (spSplitted[0], spSplitted[1], spSplitted[3])
                else:
                    queryUrl = '''http://www.ipni.org/ipni/advPlantNameSearch.do?find_genus=%s&find_species=%s&find_rankToReturn=spec''' % (spSplitted[0], spSplitted[1])
            elif webDBIdx == 5:
                # tai2
                # http://tai2.ntu.edu.tw/PlantInfo/SearchResult.php?search=%s&rgkeyword=2&recrodnum=20&enter2=送出
                queryUrl = '''http://tai2.ntu.edu.tw/PlantInfo/SearchResult.php?search=%s&rgkeyword=2&recrodnum=20&enter2=送出''' % species
            elif webDBIdx == 6:
                queryUrl = '''http://www.plantsoftheworldonline.org/?q=%s''' % species
            else:
                queryUrl = '''http://tropicos.org/NameSearch.aspx?name=%s&commonname=''' % species
            return(queryUrl)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def loadUrl(self, URL):
        try:
            self.urlLine.setText(URL)
            self.webEngineView.setUrl(QUrl(URL))
            self.statusBar().showMessage('Loading %s' % URL)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def webBackward(self):
        try:
            self.webEngineView.back()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def webForward(self):
        try:
            self.webEngineView.forward()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def webStop(self):
        try:
            self.webEngineView.stop()
            self.webEngineView.load('about:blank')
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def speechRecognition(self):
        try:
            db_table = self.selectDB() 
            if db_table == 'dao_jp_ylist':
                speechLanguage = 'ja-JP'
            else:
                speechLanguage = 'zh-TW'

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                results = recognizer.recognize_google(audio, language=speechLanguage)
                self.statusBar().showMessage(self.tr('Google recognized the plant name as: %s' %s))
            return(results)
        except sr.RequestError as e:
            QMessageBox.information(self, "Warning","Could not request results from Google Speech Recognition service; {0}".format(e))
        except sr.UnknownValueError:
            QMessageBox.information(self, "Warning","Google Speech Recognition does not undertand your speech")
        except IndexError: 
            QMessageBox.information(self, "Warning","No internet connection")
        except KeyError:
            QMessageBox.information(self, "Warning", "Invalid API key or quota maxed out")

    def speechAddToTree(self):
        try:
            speechResult = self.speechRecognition()
            db_table = self.selectDB()
            retrieved = self.g.dbGetsp(db_table, self.sqlite_db)
            names = []
            for i in range(len(retrieved)):
                names.append(retrieved[i][3] +  "|" + retrieved[i][5] + "|" + retrieved[i][2])
            matches = filter(lambda x: re.match(speechResult, x), names)
            res = []
            for p in matches:
                res.append(p)
            if len(res) == 0:
                self.lineSpecies.setText(speechResult)
            else:
                self.lineSpecies.setText(res[0])
                self.addToTree()
        except BaseException as e:
            QMessageBox.information(self, "Warning speechAddToTree()", str(e))

    def butLoadWeb(self):
        try:
            item = self.treeWidget.currentItem()
            if item:
                fullname = self.g.fmtname(str(item.text(1)), doformat=False, split=True)
                fullnameNoAuthors = fullname[0]
                queryUrl = self.checkWebDB(fullnameNoAuthors)
                self.urlLine.setText(queryUrl)
                self.loadUrl(queryUrl)
            else:
                pass
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def spCompleter(self):
        try:
            def setHighlighted(self, text):
                self.lastSelected = text
            g = genlist_api.Genlist()
            completer = QCompleter()
            model = QStringListModel()
            completer.setModel(model)
            # PopupCompletion
            # QCompleter setFilterMode Qt>5.2
            # http://doc.qt.io/qt-5/qcompleter.html#filterMode-prop
            completer.setFilterMode(Qt.MatchContains)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.lineSpecies.setCompleter(completer)
            db_table = self.selectDB()
            retrieved = self.g.dbGetsp(db_table, self.sqlite_db)
            b_container=[]
            for i in range(len(retrieved)):
                b_container.append(retrieved[i][3] +  "|" + retrieved[i][5] + "|" + retrieved[i][2])
            model.setStringList(b_container)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def selectDB(self):
        try:
            if self.actionTaiwanVascularPlants.isChecked():
                db_table = 'dao_pnamelist_pg'
                self.dblabel.setText(self.tr('Current DB: Vascular Plants of Taiwan'))
            elif self.actionTaiwanRedList2017.isChecked():
                db_table = 'dao_twredlist2017'
                self.dblabel.setText(self.tr('Current DB: the Red List of Taiwan Vascular Plants (2017)'))
            elif self.actionTaiwanFlora.isChecked():
                db_table = 'dao_pnamelist'
                self.dblabel.setText(self.tr('Current DB: Flora of Taiwan'))
            elif self.actionJapanYlist.isChecked():
                db_table = 'dao_jp_ylist'
                self.dblabel.setText(self.tr('Current DB: Ylist'))
            else:
                db_table = 'dao_pnamelist_pg'
                self.dblabel.setText(self.tr('Current DB: Vascular Plants of Taiwan'))
            return(db_table)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def checkDB(self):
        try:
            db_table = self.selectDB()
            # after changing the database, clear all the tree items
            # and browser taxon info
            self.delAllTreeItems()
            self.textBrowserInfo.clear()
            # update status bar
            self.statusBar().showMessage(self.tr('Current database table is %s' % db_table))
            self.spCompleter()
            return(db_table)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def checkLocalDB(self):
        try:
            self.g = genlist_api.Genlist()
            db_filename = 'twnamelist.db'
            builtin_sqlite_db = self.g.resource_path(os.path.join('db', db_filename))
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
            dburl = 'https://raw.github.com/TaiBON/checklister/master/src/db/twnamelist.db'
            curl.setopt(pycurl.URL, dburl)
            curl.setopt(pycurl.FOLLOWLOCATION, True)
            #curl.perform()
            #if curl.getinfo(curl.HTTP_CODE) == 200:
            with open(self.latest_db, 'wb+') as f:
                curl.setopt(curl.WRITEDATA, f)
                curl.perform()
            # update to latest
            shutil.copy(self.latest_db, self.checklist_db)
            self.statusBar().showMessage(self.tr('Updating database, please wait for a while ...')) 
            QMessageBox.information(self, self.tr('Checklist generator'), self.tr('Update DB done!'))
            self.statusBar().showMessage(self.tr('Database updated!')) 
            curl.close()
            # update completer
            self.spCompleter()
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def browSlist(self):
        try:
            #self.lineSlist.clear()
            Slist = QFileDialog.getOpenFileName(self, self.tr(u"Open file"), \
                    self.home, self.tr("Text files (*.txt *.yml *.yaml)"))[0]
            if Slist is None or Slist is '':
                return
            info_message = self.tr(u'''When you load species file (only common names) to generate checklist, the "checklist generator" will save a temporary file (filename_temp.txt/csv) within the same directory, and load this species file into checklist below. You can add/remove species to generate checklist.''')
            QMessageBox.information(self, "Info", self.tr(info_message))
            Slist_str = str.split(str(Slist), '.')
            Slist_modified = Slist_str[0] + '_temp.' + Slist_str[1]
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
            db_table = self.selectDB()
            query_list = '''
            SELECT n.family_cname,n.fullname,n.cname FROM %s n, sample s
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
            nspList = []
            for i in no_sp:
                nspList.append(i[0])
            nspStr = ', '.join(nspList)
            if len(nspList) > 0:
                # save unmatched name to nomatch.txt
                sDir = os.path.dirname(Slist)
                noMatchFile = os.path.join(sDir, 'nomatch.txt')
                with codecs.open(noMatchFile, 'w+', 'utf-8') as f:
                    f.write(u'\n'.join(nspList))
                QMessageBox.information(self, "Warning", \
                        self.tr(u'''The following species did not exist in our database,and I stored it at %s. Please check again: %s''' % (noMatchFile, nspStr)))
            # clean the tree first
            self.delAllTreeItems()
            for i in range(0, len(fetched_results)):
                item = QTreeWidgetItem()
                item.setText(0, fetched_results[i][0])
                item.setText(1, fetched_results[i][1])
                item.setText(2, fetched_results[i][2])
                self.treeWidget.addTopLevelItem(item)
        except BaseException as e:
            QMessageBox.information(self, "Warning! [BrowSlist]", str(e))

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
            db_table = self.selectDB()
            query_list = '''
            SELECT n.family_cname,n.fullname,n.cname FROM %s n, compare_sample s
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
            nspList = []
            for i in no_sp:
                nspList.append(i[0])
            nspStr = ', '.join(nspList)
            if len(nspList) > 0:
                # save unmatched name to nomatch.txt
                noMatchFile = os.path.join(self.home, 'nomatch.txt')
                with codecs.open(noMatchFile, 'w+', 'utf-8') as f:
                    f.write(u'\n'.join(nspList))
                QMessageBox.information(self, "Warning", \
                        self.tr(u"The following species did not exist in our database. I store it at %s. Please check again: %s" % (noMatchFile, nspStr)))
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
        '''
        browOutput
        ==========

        選擇輸出名錄的檔名(.docx/.odt/.xlsx)

        選擇之後會把要儲存的檔案路徑存在 ${TMP}/checklister_exp_filename.txt 中

        Return
        ------
        str tempExpFile: 輸出的暫存檔案，內容為選擇的輸出檔案
        '''
        try:
            self.clearOutputFilename()
            saveOutputFile = QFileDialog.getSaveFileName(self, self.tr(u"Save file as:"), \
                    self.home, self.tr("Text files (*.docx *.odt *.xlsx)"))[0]
            if saveOutputFile is None or saveOutputFile is '':
                return
            with codecs.open(self.tempExpFile, 'w+', 'utf-8') as f:
                f.write(saveOutputFile)
            self.statusBar().showMessage(self.tr(u'Export file is: %s' % saveOutputFile))
            return(self.tempExpFile)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def outputFilename(self):
        '''
        outputFilename
        ==============
        輸出名錄的檔名
        '''
        try:
            if not os.path.exists(self.tempExpFile):
                self.browOutput()
                with codecs.open(self.tempExpFile, 'r', 'utf-8') as f:
                    outputFile = f.read()
                return(outputFile)
            else:
                with codecs.open(self.tempExpFile, 'r', 'utf-8') as f:
                    outputFile = f.read()
                return(outputFile)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def clearOutputFilename(self):
        '''
        clearOutputFilename
        ===================
        清掉輸出名錄檔名暫存檔

        '''
        try:
            if os.path.exists(self.tempExpFile):
                os.remove(self.tempExpFile)
            else:
                pass
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def checklistTextFile(self, saveOutputFile):
        '''
        Get txt file according to the output *.docx/*.odt filename
        '''
        try:
            if saveOutputFile is None or saveOutputFile is '':
                return
            outputFilePath = os.path.splitext(self.g.resource_path(saveOutputFile))
            checklistTxtFile = outputFilePath[0] + '.yml'
            return(checklistTxtFile)
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
            self.g = genlist_api.Genlist()
            db_table = self.selectDB()
            retrieved = self.g.dbGetsp(db_table, self.sqlite_db)
            b_container = []
            for i in range(len(retrieved)):
                    b_container.append([retrieved[i][2], retrieved[i][3], retrieved[i][5]])
            # returnlist
            return(b_container)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def deselectTreeItmes(self):
        try:
            self.treeWidget.clearSelection()
            pass
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def selectAllTreeItmes(self):
        try:
            self.treeWidget.selectAll()
            pass
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def addToTree(self):
        try:
            if self.lineSpecies.text() is '':
                QMessageBox.information(self, "Warning", self.tr("Please input the species name!"))
                return
            else:
                # check for species items
                #root = QTreeWidgetItem() 
                species_item = str.split(str(self.lineSpecies.text()), '|')
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
                    item = QTreeWidgetItem()
                    # if selected item exists in our tree widget, ignore it
                    # match pattern: family and fullname
                    if self.treeWidget.findItems(species_item[1], Qt.MatchExactly, 1) and \
                        self.treeWidget.findItems(species_item[0], Qt.MatchExactly, 1):
                        pass
                    else:
                        item.setText(0, species_item[2])
                        item.setText(1, species_item[1])
                        item.setText(2, species_item[0])
                        self.treeWidget.addTopLevelItem(item)
                    self.lineSpecies.clear()
                else:
                    item = QTreeWidgetItem()
                    if '|' in str(self.lineSpecies.text()):
                        species_item = str.split(str(self.lineSpecies.text()), '|')
                        item.setText(0, species_item[0])
                        item.setText(1, species_item[1])
                        item.setText(2, species_item[2])
                        self.treeWidget.addTopLevelItem(item)
                    else:
                        QMessageBox.information(self, "Warning", self.tr('''The species %s did not exist in our database!
                        You can add it manually by "family|fullname with authors|common name" ''') % species_item[0])
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
                all_items.append([item.text(0), item.text(1), item.text(2)])
            return all_items
        except BaseException as e:
            QMessageBox.information(self, "Warning [getTreeItems]", str(e))

    def searchTropicos(self):
        try:
            item = self.treeWidget.currentItem()
            if item:
                fullnameNoAuthors = self.g.fmtname(str(item.text(1)), doformat=False, split=True)[0]
                fullnameNoAuthors = fullnameNoAuthors.replace(' ','+')
                queryUrl = '''http://tropicos.org/NameSearch.aspx?name=%s&commonname=''' % fullnameNoAuthors
                QDesktopServices.openUrl(QUrl(queryUrl))
            else:
                pass
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def searchNomenMatch(self):
        try:
            item = self.treeWidget.selectedItems()
            if item:
                itemCat = []
                for item in self.treeWidget.selectedItems():
                    fullnameNoAuthors = self.g.fmtname(str(item.text(1)), doformat=False, split=True)[0]
                    fullnameNoAuthors = fullnameNoAuthors.replace(' ','+')
                    itemCat.append(fullnameNoAuthors)
                queryItems = '|'.join(itemCat)
                queryUrl = '''http://match.taibif.tw/api.php?names=%s''' % queryItems
                QDesktopServices.openUrl(QUrl(queryUrl))
            else:
                pass
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

    def initMetadata(self):
        '''
        Initiating metadata of a checklist
        '''
        try:
            # get create time
            checklistTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            checklistUUID = str(uuid.uuid4())
            checklistMetadata = [{'eventID': checklistUUID}, {'eventDate': checklistTime}]
            return(checklistMetadata)
            #
        except BaseException as e:
            QMessageBox.information(self, "Warning [savedMetadata]", str(e))


    # 儲存批次的文字檔
    def saveChecklistTxt(self):
        '''
        saveChecklistTxt
        ================
        save checklist (vernacular names)


        Returns
        =======
        None

        '''
        try:
            # 取得既有的名錄
            tree_item = self.getTreeItems(self.treeWidget)
            # 先確認看一下有沒有輸出的檔名
            tempDir = tempfile.gettempdir()
            if not os.path.exists(self.tempExpFile):
                self.browOutput()
            with codecs.open(self.tempExpFile, 'r', 'utf-8') as f:
                expFile = f.read()
            # 儲存的文字檔案
            savedTxtList = self.checklistTextFile(expFile)
            # 檢查有沒有同檔名存在，如果有的話另外存成 $filename.bak
            if os.path.exists(savedTxtList) == True:
                ofile_abspath = self.g.resource_path(savedTxtList)
                # open yaml file to check if the metadata exists
                with codecs.open(ofile_abspath, 'r') as f:
                    ymldata = yaml.load(f)
                    # clear the taxa list
                    ymldata['taxa'] = []
                shutil.copyfile(ofile_abspath, ofile_abspath + '.bak')
                os.remove(ofile_abspath)
            else:
                checklistMetadata = self.initMetadata()
                ymldata = {'taxa': [], 'metadata': checklistMetadata}
            with codecs.open(savedTxtList, 'w', 'utf-8') as f:
                # save

                for sp in range(0, len(tree_item)):
                    family = tree_item[sp][0]
                    scientificName = tree_item[sp][1]
                    vernacularName = tree_item[sp][2]
                    ymldata['taxa'].append({'family': '%s' % family,
                        'scientificName':'%s' % scientificName, 
                        'vernacularName':'%s' % vernacularName})
                yaml.dump(ymldata, f, allow_unicode=True)
            f.close()
            return(savedTxtList)
            self.statusBar().showMessage(self.tr("Saving checklist to %s " % savedTxtList)) 

        except BaseException as e:
            QMessageBox.information(self, "Warning [saveCheckListTxt]:", str(e))


    # 產生名錄
    def genChecklist(self):
        try:
            ## TODO: 
            self.g = genlist_api.Genlist()
            tree_item = self.getTreeItems(self.treeWidget)
            # getdbtable
            db_table = self.selectDB()
            ofile = self.outputFilename()
            if ofile:
                # 儲存成文字檔
                savedTxtList = self.saveChecklistTxt()

                if os.path.exists(ofile) == True:
                    ofile_abspath = self.g.resource_path(ofile)
                    shutil.copyfile(ofile_abspath, ofile_abspath+'.bak')
                    os.remove(ofile_abspath)
                output_flist = str.split(ofile, '.')
                # before generate namelist, clean up the sample table in sqlite db
                conn = sqlite3.connect(self.sqlite_db)
                curs = conn.cursor()
                curs.execute('DROP TABLE IF EXISTS sample;')
                conn.commit()
                # export outputfile
                self.g.genEngine(self.sqlite_db, db_table, savedTxtList, output_flist[1], output_flist[0])
                QMessageBox.information(self, self.tr('Checklist generator'), \
                        self.tr("Export checklist to '%s' done!" % ofile))

                # 輸出後清除暫存檔
                self.clearOutputFilename()

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

class AboutDialog(QDialog, Ui_AboutDialog):

     def __init__(self, mainWindow):
         super().__init__()
         self.setupUi(self)
         self.okButton.clicked.connect(self.destroy)

     def destroy(self):
         self.close()

#### Combine Dialog 
class CombineDialog(QDialog, Ui_CombineDialog):

    def __init__(self, MainWindow):
        try:
            super().__init__()
            self.setupUi(self)

            self.home = os.path.expanduser("~")
            self.g = genlist_api.Genlist()
            self.dbTable = MainWindow.selectDB()
            self.sqlite_db = MainWindow.checkLocalDB()

            self.butSelCombList.clicked.connect(self.selTobeCombFiles)
            self.butSelExcelFile.clicked.connect(self.selExportExcel)
            self.butCombine.clicked.connect(self.execCombine)
            self.butClose.clicked.connect(self.destroy)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))


    def selTobeCombFiles(self):
        # 待組合的名錄
        try:
            tobe_combined_lists = QFileDialog.getOpenFileNames(self, self.tr(u"Select checklist text files to combine"), \
                self.home, self.tr("Text files (*.txt)"))[0]
            if tobe_combined_lists is None or tobe_combined_lists is '':
                return
            else:
                self.textChecklists.setText(','.join(tobe_combined_lists))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def selExportExcel(self):
        try:
            combExcelFile = QFileDialog.getSaveFileName(self, self.tr(u"Save combined list as:"), \
                self.home, self.tr("Excel files (*.xlsx)"))[0]
            if combExcelFile is None or combExcelFile is '':
                return
            else:
                self.textExpExcel.setText(combExcelFile)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def execCombine(self):
        try:
            combChecklists = str(self.textChecklists.text()).split(',')
            combExcelFile = str(self.textExpExcel.text())
            if combChecklists is None or combExcelFile is None:
                QMessageBox.information(self, "Warning", self.tr(u'Checklists and excel file should not be empty!'))
                return
            else:
                self.g.expCombList(sqlite_db = self.sqlite_db , current_db_table = self.dbTable, \
                    tobe_combined_lists = combChecklists, exportExcel = combExcelFile)
                QMessageBox.information(self, "Warning", self.tr(u'Combing checklists done!'))
                self.textChecklists.clear()
                self.textExpExcel.clear()
                self.destroy()

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def destroy(self):
        self.close()

class CompareDialog(QDialog, Ui_CompareDialog):

    def __init__(self, MainWindow):
        try:
            super().__init__()
            self.setupUi(self)

            self.home = os.path.expanduser("~")
            self.bulkLoadToTree = MainWindow.bulkLoadToTree
            self.delAllTreeItems = MainWindow.delAllTreeItems
            self.butCheckASelect.clicked.connect(self.selChecklistA)
            self.butCheckBSelect.clicked.connect(self.selChecklistB)
            self.butCompare.clicked.connect(self.execCompare)
            self.butClose.clicked.connect(self.destroy)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def selChecklistA(self):
        try:
            checklist_A = QFileDialog.getOpenFileName(self, self.tr(u"Open file"), \
                    self.home, self.tr("Text files (*.txt)"))[0]
            if checklist_A is None or checklist_A is '':
                return
            self.lineChecklistA.setText(checklist_A)
            #status_bar = "Loading " + checklist_A 
            #self.statusBar().showMessage(self.tr(status_bar))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def selChecklistB(self):
        try:
            checklist_B = QFileDialog.getOpenFileName(self, self.tr(u"Open file"), \
                    self.home, self.tr("Text files (*.txt)"))[0]
            if checklist_B is None or checklist_B is '':
                return
            self.lineChecklistB.setText(checklist_B)
            #status_bar = "Loading " + checklist_B 
            #self.statusBar().showMessage(self.tr(status_bar))
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def execCompare(self):
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
                    #self.lineTempFile.setText(os.path.join(a_path, tmp_filename))
                    compare_result = list(compare_result)
                    self.delAllTreeItems()
                    # load compared list into QTreeWidget
                    if len(compare_result) >= 1:
                        self.bulkLoadToTree(compare_result)
                        self.destroy()
                    else:
                        QMessageBox.information(self, "Warning", self.tr("There is no common species between checklist A and B"))
                        MainWindow.delAllTreeItems()

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))


    def destroy(self):
        self.close()

class FormatDialog(QDialog, Ui_FormatDialog):

    def __init__(self, MainWindow):
        try:
            super().__init__()
            self.setupUi(self)
            self.home = os.path.expanduser("~")
            self.g = genlist_api.Genlist()

            self.butSelectExcel.clicked.connect(self.selExcelFile)
            self.butFormatName.clicked.connect(self.formatName)
            self.butClose.clicked.connect(self.destroy)

        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def selExcelFile(self):
        try:
            #self.lineExcelFilePath.clear()
            orig_excel_file = QFileDialog.getOpenFileName(self, self.tr(u"Select excel files"), \
                    self.home, self.tr("Excel files (*.xls *.xlsx)"))[0]
            if orig_excel_file is None or orig_excel_file is '':
                return
            self.lineExcelFilePath.setText(orig_excel_file)
        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def formatName(self):
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

    def destroy(self):
        self.close()

###### DATABASE class
class checklistDB(QMainWindow, Ui_DBMainWindow):

    def __init__(self, MainWindow):
        try:
            super().__init__()
            self.setupUi(self)


            self.sqlite_db = MainWindow.checkLocalDB()
            self.dbViewer()
            self.butViewTable.clicked.connect(self.viewTable)


        except BaseException as e:
            QMessageBox.information(self, "Warning", str(e))

    def dbViewer(self):
        try:
            conn = sqlite3.connect(self.sqlite_db)
            with conn:
                curs = conn.cursor()
                # 設定 combo text: 列出資料庫內所有資料表
                queryTableList = '''SELECT name FROM sqlite_master WHERE type = "table"'''
                curs.execute(queryTableList)
                allTableList = curs.fetchall()
                for tab in range(0,len(allTableList)):
                    self.comboDBTables.addItem(self.tr("%s" % allTableList[tab]))
            conn.close()
        except BaseException as e:
            QMessageBox.information(self, "Warning: [dbViewer]", str(e))

    def viewTable(self):
        '''
        view table data from sqlite db
        '''
        try:
            # clear all treeWidget items
            self.treeWidgetDB.clear()
            # clear all of the columns (headers)
            self.treeWidgetDB.setColumnCount(0)
            # fetch table columns
            tableName = str(self.comboDBTables.currentText())
            self.treeWidgetDB.header().setVisible(True)
            conn = sqlite3.connect(self.sqlite_db)
            with conn:
                curs = conn.cursor()
                queryTableColNames = '''pragma table_info('%s')''' % tableName
                curs.execute(queryTableColNames)
                columnNamesInfo = curs.fetchall()
                columnNames = []
                for col in range(0, len(columnNamesInfo)):
                    columnNames.append(columnNamesInfo[col][1])
                    self.treeWidgetDB.headerItem().setText(col, self.tr("%s" % columnNamesInfo[col][1]))
                # add item data
                queryTableContents = '''SELECT * FROM %s;''' % tableName
                curs.execute(queryTableContents)
                tableContents = curs.fetchall()
                for i in range(0, len(tableContents)):
                    item = QTreeWidgetItem()
                    for col in range(0, len(columnNames)):
                        # check for species items
                        item.setText(col, str(tableContents[i][col]))
                    self.treeWidgetDB.addTopLevelItem(item)
            conn.close()
        except BaseException as e:
            QMessageBox.information(self, "Warning: [viewTable]", str(e))
