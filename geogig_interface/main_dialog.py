# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))  
sys.path.append(os.path.dirname(__file__))

from PyQt4 import QtCore, QtGui, uic
from config_dialog import Config_Dialog
from merge_dialog import Merge_Dialog
from conflicts_dialog import Conflicts_Dialog
from geogig_lib.geogig import Repository

GUI, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),
    'ui',
    'main_dialog.ui'), 
    resource_suffix=''
)

class Main_Dialog(QtGui.QDialog, GUI):
    def __init__(self, iface):
        super(Main_Dialog, self).__init__() 
        self.setupUi(self)
        self.iface = iface
        self.geogig_conf = Config_Dialog(self.iface)
        self.repositoryData = {}
        self.repo = None
        self.solve_conflicts = None
        self.geogig_merge = None
        
    def run(self):
        self.configRepoBtn.clicked.connect(
            self.showConfigRepository
        )
        self.mergeBtn.clicked.connect(
            self.showMergeDialog
        )
        self.exec_()

    def setCurrentRepositoryData(self, repoData):
        self.repositoryData = repoData

    def showConfigRepository(self):
        self.geogig_conf.addReposiory.connect(
            self.setCurrentRepositoryData
        )
        self.geogig_conf.exec_()

    def showMergeDialog(self):
        repoData = self.geogig_conf.getRepositoryDataOnQSettings()
        print u"LOG: {0}".format(repoData)
        if (repoData and not('' in repoData.values())):
            host = repoData["host"]
            port = repoData["port"]
            geogigPath = repoData["geogigPath"]
            repositoryName = repoData["repositoryName"]
            user = repoData["user"]
            password = repoData["password"]
            schema = repoData["schema"]
            database = repoData["database"]
            self.repo = Repository(host,port,database,schema,repositoryName,user,password, geogigPath)
            branches = self.repo.branches.keys()           
            self.geogig_merge = Merge_Dialog(self.iface)
            self.geogig_merge.loadCombo(branches)
            self.geogig_merge.pushButton_merge.clicked.connect(self.merge)
            self.geogig_merge.exec_()
    
    def merge(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        selectedBranches = self.geogig_merge.getSelectedBranches()
        result = self.repo.branches[selectedBranches['head']].merge(selectedBranches['mergeHead'])
        if(result!='Success'):
            self.solve_conflicts = Conflicts_Dialog(self.iface)
            self.solve_conflicts.processSolveConflictsData(result)
            QtGui.QApplication.restoreOverrideCursor()
            conflictResult = self.solve_conflicts.exec_()
            if conflictResult:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                decisionDict = self.solve_conflicts.decisionDict
                self.repo.branches[selectedBranches['head']].merge_features(decisionDict)
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.information(
            self.geogig_merge,
            u"Aviso :", 
            u"Merge realizado com sucesso !"
        )