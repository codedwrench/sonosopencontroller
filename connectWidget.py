import sys

import soco
from PySide.QtGui import *

from dialogsandwindows import connectDialog


class MainDialog(QDialog, connectDialog.Ui_sonosConnect):
    class NotASonosSelected(Exception):
        """Raise when no Sonos devices were selected"""

    def __init__(self, parent):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.rescanButton.clicked.connect(self.rescan)
        self.connectButton.clicked.connect(self.connect)
        self.rescan()
        self.sonostoworkwith = None

    def rescan(self):
        try:
            setofinstances = list(soco.discovery.discover())
            self.connectList.clear()
            for sonos in setofinstances:
                listwitem = QListWidgetItem(sonos.ip_address + " [" + sonos.player_name + "]", self.connectList,
                                            QListWidgetItem.Type)
                # The third data "role" is free to use, so we'll just dump our object in there
                listwitem.setData(3, sonos)

            # Select the first item for convenience
            self.connectList.setCurrentRow(0)
        except OSError:
            # I noticed that the program died when there was no internet connection, this allows the program to continue
            QMessageBox.critical(self, "No internet connection", "Network unreachable!")

    def connect(self):
        # For now you can only select one sonos device, i don't have multiple sonos devices to test with :/
        first = True
        for item in self.connectList.selectedItems():
            if first:
                self.sonostoworkwith = item.data(3)
                first = False
            else:
                item.data(3).join(self.sonostoworkwith)
        self.accept()

    def accept(self):
        if self.checkBox.checkState():
            self.sonostoworkwith.partymode()
        try:
            if not isinstance(self.sonostoworkwith, soco.SoCo):
                raise self.NotASonosSelected("No Sonos device was selected")
            else:
                QDialog.accept(self)
        except self.NotASonosSelected:
            # This should actually never happen, QListWidget should always at least have something selected
            QMessageBox.warning(self, "No selection made", "No Sonos device selected!")
            return
