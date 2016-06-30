import sys

import soco
from PySide.QtGui import *
from PySide.QtCore import *
from dialogsandwindows import showMainWindow
import connectWidget
import urllib

class MainWindow(QMainWindow, showMainWindow.Ui_Sonos_Controller):

    class DialogDidNotOpen(Exception):
        """Raise when dialog did not open"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        timer = QTimer(self)
        self.setupUi(self)
        dialog = connectWidget.MainDialog(self)
        if dialog.exec_():
            self.sonos = dialog.sonostoworkwith
            self.volumeBar.setValue(self.sonos.volume)
        else:
            raise self.DialogDidNotOpen("connect dialog did not open")
        self.playPauseButton.clicked.connect(self.playpause)
        self.playing = self.sonos.get_current_transport_info()['current_transport_state'] == 'PLAYING'
        if self.playing:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/pause.png"), QIcon.Normal, QIcon.Off)
            self.playPauseButton.setIcon(icon)
            self.playPauseButton.setIconSize(QSize(32, 32))
        self.volumeBar.valueChanged.connect(self.setVolume)
        self.albumUpdaterThread = None
        self.prevtrackinfo = None
        self.updateanyway = True
        timer.timeout.connect(self.updateValues)
        timer.start(1000)

    def playpause(self):
        try:
            if self.sonos.get_current_transport_info()['current_transport_state'] == 'PLAYING':
               self.sonos.pause()
               self.playing = False
               icon = QIcon()
               icon.addPixmap(QPixmap(":/icons/play.png"), QIcon.Normal, QIcon.Off)
               self.playPauseButton.setIcon(icon)
               self.playPauseButton.setIconSize(QSize(32, 32))
            else:
                self.sonos.play()
                self.playing = True
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/pause.png"), QIcon.Normal, QIcon.Off)
                self.playPauseButton.setIcon(icon)
                self.playPauseButton.setIconSize(QSize(32, 32))
            self.updateValues()
        except soco.SoCoException:
            QMessageBox.warning(self, "connection lost", "connection to sonos device lost")

    def setVolume(self):
        self.sonos.volume = self.volumeBar.sliderPosition()

    def getPercentageofTimeString(self, position, total):
        """converts the position and total to seconds and divides that, after that it does it times 100"""

        ftr = [3600, 60, 1]
        percent = (sum([a * b for a, b in zip(ftr, map(int, position.split(':')))]) /
                   sum([a * b for a, b in zip(ftr, map(int, total.split(':')))])) * 100
        return percent

    def updateValues(self):
        playing = self.sonos.get_current_transport_info()['current_transport_state'] == 'PLAYING'
        if playing != self.playing:
            self.playing = playing
            icon = QIcon()
            if playing:
                icon.addPixmap(QPixmap(":/icons/pause.png"), QIcon.Normal, QIcon.Off)
            else:
                icon.addPixmap(QPixmap(":/icons/play.png"), QIcon.Normal, QIcon.Off)
            self.playPauseButton.setIcon(icon)

        curtrackinfo = self.sonos.get_current_track_info()
        if curtrackinfo['title'] != self.prevtrackinfo or self.updateanyway:
            if curtrackinfo['album_art'] != '':
                if self.albumUpdaterThread is None:
                    self.albumUpdaterThread = albumUpdaterThread(curtrackinfo['album_art'])
                    self.albumUpdaterThread.threadDone.connect(self.updateAlbum)
                    self.albumUpdaterThread.start()
            else:
                self.albumArt.setPixmap(QPixmap(":/icons/album.png"))

            self.nowPlayingLabel.setText(curtrackinfo['artist'] + " : " + curtrackinfo['title'])
            self.prevtrackinfo = curtrackinfo['title']
        if self.playing or self.updateanyway:
            if curtrackinfo['duration'] != '0:00:00':
                self.trackSlider.setDisabled(False)
                self.trackSlider.setValue(self.getPercentageofTimeString(curtrackinfo['position'], curtrackinfo['duration']))
                self.timeInSongLabel.setText(curtrackinfo['position'] + "/" + curtrackinfo['duration'])
            else:
                self.trackSlider.setDisabled(True)
                self.trackSlider.setValue(0)
                self.timeInSongLabel.setText(str(curtrackinfo['position']))
            self.updateanyway = False

    def updateAlbum(self, album):
        img = QPixmap()
        img.loadFromData(album)
        self.albumArt.setPixmap(img)
        self.albumUpdaterThread = None


class albumUpdaterThread(QThread):
        threadDone = Signal(bytes)

        def __init__(self, album):
            super(albumUpdaterThread, self).__init__(None)
            self.album = album

        def run(self):
            album = urllib.request.urlopen(self.album).read()
            self.threadDone.emit(album)


app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()