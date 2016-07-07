#!/usr/bin/python
import sys


import soco
from PySide.QtGui import *
from PySide.QtCore import *
from dialogsandwindows import showMainWindow
import connectWidget
import urllib
import dataCollector
import time


class MainWindow(QMainWindow, showMainWindow.Ui_Sonos_Controller):

    class DialogDidNotOpen(Exception):
        """Raise when dialog did not open"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        dialog = connectWidget.MainDialog(self)
        if dialog.exec_():
            self.sonos = dialog.sonostoworkwith
            self.volumeBar.setValue(self.sonos.volume)
        else:
            raise self.DialogDidNotOpen("connect dialog did not open")
        self.eventGetter = dataCollector.getEvents(self.sonos)
        self.albumUpdaterThread = None
        self.prevtrackinfo = None
        self.updateanyway = True
        self.duration = None
        self.volumeBar.valueChanged.connect(self.setVolume)
        self.volumeBar.setTracking(False)
        self.trackSlider.valueChanged.connect(self.seek)
        self.trackSlider.setTracking(False)
        self.playPauseButton.toggled.connect(self.playpause)
        self.eventGetter.updateValues.connect(self.updateValues, Qt.DirectConnection)
        self.eventGetter.start()
        self.position = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatetimer)
        self.playing = self.sonos.get_current_transport_info()['current_transport_state'] == 'PLAYING'
        if self.playing:
            self.setPlaying(True)
        else:
            self.setPlaying(False)

    def updateValues(self, event, event2):
        if event is not None:
            playing = event['transport_state']
            if playing == 'PLAYING':
                self.setPlaying(True)
            elif playing == 'PAUSED_PLAYBACK':
                self.setPlaying(False)
            self.duration = event['current_track_duration']
        if event2 is not None:
            self.volumeBar.blockSignals(True)
            self.volumeBar.setValue(int(event2['volume']['Master']))
            self.volumeBar.blockSignals(False)

    def updatetimer(self):
        self.position += 1
        self.timeInSongLabel.setText(str(self.position))

    def playpause(self):
        self.eventGetter.pausethread = True
        if self.playing:
            self.sonos.pause()
            self.setPlaying(False)
            self.playing = False
        else:
            self.sonos.play()
            self.setPlaying(True)
            self.playing = True
        self.eventGetter.pausethread = False

    def setPlaying(self, playing):
        if playing is False:
            self.playPauseButton.blockSignals(True)
            self.playing = False
            self.playPauseButton.setChecked(False)
            self.playPauseButton.blockSignals(False)
            self.timer.stop()
        else:
            self.playPauseButton.blockSignals(True)
            self.playing = True
            self.playPauseButton.setChecked(True)
            self.playPauseButton.blockSignals(False)
            self.timer.start(1000)
        pos = self.sonos.get_current_track_info()['position']
        self.position = self.converttoseconds(pos)

    def setVolume(self):
        self.sonos.volume = self.volumeBar.sliderPosition()

    def converttoseconds(self, timestring):
        ftr = [3600, 60, 1]
        seconds = sum([a * b for a, b in zip(ftr, map(int, timestring.split(':')))])
        return seconds


    def converttotime(self, percentage, duration):
        ftr = [3600, 60, 1]
        seconds = ((sum([a * b for a, b in zip(ftr, map(int, duration.split(':')))]) /
                   100) * percentage)
        hours, minutes = divmod(seconds, 3600)
        minutes, seconds = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def seek(self):
        timestring = self.converttotime(self.trackSlider.value(), self.duration)
        self.sonos.seek(timestring)

    def exitHandler(self):
        self.eventGetter.abortThread = True
        if not self.eventGetter.wait(5000):
            self.eventGetter.terminate()
            self.eventGetter.wait()

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
app.aboutToQuit.connect(form.exitHandler)
form.show()
app.exec_()
