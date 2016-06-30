# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectWidget.ui'
#
# Created: Thu Jun 23 23:06:02 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_sonosConnect(object):
    def setupUi(self, sonosConnect):
        sonosConnect.setObjectName("sonosConnect")
        self.gridLayout = QtGui.QGridLayout(sonosConnect)
        self.connectList = QtGui.QListWidget(sonosConnect)
        QtGui.QListWidgetItem(self.connectList)
        self.gridLayout.addWidget(self.connectList, 0, 0, 1, 3)
        self.checkBox = QtGui.QCheckBox(sonosConnect)
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)
        self.connectButton = QtGui.QPushButton(sonosConnect)
        self.gridLayout.addWidget(self.connectButton, 2, 2, 1, 1)
        self.rescanButton = QtGui.QPushButton(sonosConnect)
        self.gridLayout.addWidget(self.rescanButton, 2, 1, 1, 1)

        self.retranslateUi(sonosConnect)
        QtCore.QMetaObject.connectSlotsByName(sonosConnect)

    def retranslateUi(self, sonosConnect):
        sonosConnect.setWindowTitle(QtGui.QApplication.translate("sonosConnect", "Sonos Picker", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.connectList.isSortingEnabled()
        self.connectList.setSortingEnabled(False)
        self.connectList.setSortingEnabled(__sortingEnabled)
        self.checkBox.setText(QtGui.QApplication.translate("sonosConnect", "Party Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("sonosConnect", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.rescanButton.setText(QtGui.QApplication.translate("sonosConnect", "Rescan", None, QtGui.QApplication.UnicodeUTF8))



