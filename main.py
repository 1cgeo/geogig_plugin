# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from qgis import core, gui
from geogig_interface.main_dialog import Main_Dialog
import resources

class Main:
    def __init__(self, iface):
        self.iface = iface
        self.geogigAction = None

    def initGui(self):
        self.addActionQgis()

    def unload(self):
        self.removeActionQgis()

    def addActionQgis(self):
        self.geogigAction = QtGui.QAction(
            QtGui.QIcon(":/plugins/geogig_pg/icons/geogig.png"),
            "Geogig", 
            self.iface.mainWindow()
        )
        self.geogigAction.setObjectName("Geogig")
        self.geogigAction.triggered.connect(
            self.showGeogigDialog
        )
        self.iface.pluginToolBar().addAction(self.geogigAction)

    def removeActionQgis(self):
        if self.geogigAction:
            self.iface.pluginToolBar().removeAction(self.geogigAction)
            self.geogigAction = None

    def showGeogigDialog(self):
        self.geogigConfig = Main_Dialog(self.iface)
        self.geogigConfig.run()

   

        
