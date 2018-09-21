# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.dirname(__file__))

from PyQt4 import QtCore, QtGui, uic

GUI, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),
    'ui',
    'merge_dialog.ui'), 
    resource_suffix=''
)

class Merge_Dialog(QtGui.QDialog, GUI):
    def __init__(self, iface):
        super(Merge_Dialog, self).__init__()
        self.setupUi(self)
    
    def loadCombo(self,itens):
        self.comboBox_branchAtivo.addItems(itens)
        self.comboBox_branch2Merge.addItems(itens) 

    def getSelectedBranches(self):
        selectedBranches = {
            "head":self.comboBox_branchAtivo.currentText(),
            "mergeHead":self.comboBox_branch2Merge.currentText()
        }
        return selectedBranches
        


    
