# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.dirname(__file__))

from PyQt4 import QtCore, QtGui, uic

GUI, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),
    'ui',
    'config_dialog.ui'), 
    resource_suffix=''
) 

class Config_Dialog(QtGui.QDialog, GUI):
    
    addReposiory = QtCore.pyqtSignal(dict)

    def __init__(self, iface):
        super(Config_Dialog, self).__init__()
        self.setupUi(self)
        self.iface = iface
        self.repositoryData = {}
        self.connectWidgets()
        self.loadDataForm()
    
    def connectWidgets(self):
        self.okBtn.clicked.connect(
            self.saveRepository
        )
        self.cancelBtn.clicked.connect(
            self.close
        )

    def loadDataForm(self):
        repoData = self.getRepositoryDataOnQSettings()
        self.serverIPLineEdit.setText(repoData["host"])
        self.passwordLineEdit.setText(repoData["password"])
        self.portLineEdit.setText(repoData["port"])
        self.repositoryNameLineEdit.setText(repoData["repositoryName"])
        self.schemaLineEdit.setText(repoData["schema"])
        self.userLineEdit.setText(repoData["user"])
        self.localDbNameLineEdit.setText(repoData["database"])
        self.geogigPathLineEdit.setText(repoData["geogigPath"])
        self.branchNameLineEdit.setText(repoData["branchName"])

    def getRepositoryDataOnQSettings(self):
        s = QtCore.QSettings()
        repoData = {
            "host" : s.value("Geogig/host"),
            "password" : s.value("Geogig/password"),
            "port" : s.value("Geogig/port"),
            "repositoryName" : s.value("Geogig/repositoryName"),
            "schema" : s.value("Geogig/schema"),
            "user" : s.value("Geogig/user"),
            "database" : s.value("Geogig/database"),
            "geogigPath" : s.value("Geogig/geogigPath"),
            "branchName" : s.value("Geogig/branchName")
        }  
        return repoData

    def setRepositoryDataOnQSettings(self, repoData):
        s = QtCore.QSettings()
        s.setValue("Geogig/host", repoData["host"])
        s.setValue("Geogig/password", repoData["password"])
        s.setValue("Geogig/port", repoData["port"])
        s.setValue("Geogig/repositoryName", repoData["repositoryName"])
        s.setValue("Geogig/schema", repoData["schema"])
        s.setValue("Geogig/user", repoData["user"])
        s.setValue("Geogig/database", repoData["database"])
        s.setValue("Geogig/geogigPath", repoData["geogigPath"])
        s.setValue("Geogig/branchName", repoData["branchName"])

    def saveRepository(self):
        repoData = {
            "host" : self.serverIPLineEdit.text(),
            "password" : self.passwordLineEdit.text(),
            "port" : self.portLineEdit.text(),
            "repositoryName" : self.repositoryNameLineEdit.text(),
            "schema" : self.schemaLineEdit.text(),
            "user" : self.userLineEdit.text(),
            "database" : self.localDbNameLineEdit.text(),
            "geogigPath" : self.geogigPathLineEdit.text(),
            "branchName" : self.branchNameLineEdit.text()
        }
        self.setRepositoryDataOnQSettings(repoData)
        self.addReposiory.emit(repoData)
        self.accept()
        

    
