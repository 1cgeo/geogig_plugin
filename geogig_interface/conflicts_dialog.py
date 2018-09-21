# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.dirname(__file__))

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot

GUI, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),
    'ui',
    'conflicts_dialog.ui'), 
    resource_suffix=''
)

class Conflicts_Dialog(QtGui.QDialog, GUI):
    def __init__(self, iface):
        super(Conflicts_Dialog, self).__init__()
        self.setupUi(self)
        self.conflictsData = None
        self.currentFeature = 0
        self.decisionDict = dict()
    
    def processSolveConflictsData(self, conflicts):
        self.conflictsData = conflicts
        self.conflicsDecisionList = ['']*len(self.conflictsData)
        self.showValues(self.currentFeature)

    def diffJson(self, a, b):
        diff_att = []
        for key in a.keys():
            if key in b and b[key] != a[key]:
                diff_att.append(key)
        return diff_att

    def showValues(self, featureId):
        self.setWindowTitle('Conflito {0}/{1}'.format(featureId+1, len(self.conflictsData)))
        headerDict = {'':None, 'ancestor':None, 'ours':1, 'theirs':2}
        feature = self.conflictsData[featureId]
        ancestorKeys = feature['ancestor'].keys()
        oursKeys = feature['ours'].keys()
        theirsKeys = feature['theirs'].keys()
        self.label_feature.setText(feature['camada'])
        self.tableWidget.clear()
        for i in reversed(range(len(ancestorKeys))):
            self.tableWidget.removeRow(i)
        self.tableWidget.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Ancestor'))
        self.tableWidget.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Ours'))
        self.tableWidget.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem('Theirs'))
        for i in range(len(ancestorKeys)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(ancestorKeys[i]))
            self.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(feature['ancestor'][ancestorKeys[i]]))
            self.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(feature['ours'][oursKeys[i]]))
            self.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(feature['theirs'][theirsKeys[i]]))
        if headerDict[self.conflicsDecisionList[featureId]]:
            self.tableWidget.selectColumn(headerDict[self.conflicsDecisionList[featureId]])
    
    @pyqtSlot(bool, name = 'on_pushButton_next_clicked')
    @pyqtSlot(bool, name = 'on_pushButton_previous_clicked')
    def iterateValue(self):
        """
        1. Validate selection
        2. Store current value
        3. Get next value
        4. Go to next value
        """
        selectedType = self.validateSelection()
        if not selectedType or selectedType == 'ancestor':
            QtGui.QMessageBox.critical(self, 'Crítico','Selecione ou a coluna ours ou theirs!')
            return
        self.conflicsDecisionList[self.currentFeature] = selectedType
        self.decisionDict[self.label_feature.text()] = selectedType
        sender = self.sender()
        unit = 1 if sender.text() == '>>>' else  -1
        self.currentFeature = (self.currentFeature + unit) % (len(self.conflicsDecisionList))
        self.showValues(self.currentFeature)
    
    def validateSelection(self):
        selectedItems = self.tableWidget.selectedItems()
        if selectedItems == []:
            return None
        if selectedItems[0].column() == 0:
            return 'ancestor'
        elif selectedItems[0].column() == 1:
            return 'ours'
        elif selectedItems[0].column() == 2:
            return 'theirs'
        else:
            return None
    
    @pyqtSlot(bool)
    def on_pushButton_finalizar_clicked(self):
        if '' in self.conflicsDecisionList:
            QtGui.QMessageBox.critical(self, 'Crítico','Resolva todos os conflitos antes de finalizar!')
            return
        self.done(1)
        self.close()
