from PySide.QtCore import *
import soco
try:
    from queue import Empty
except:  # Py2.7
    from Queue import Empty
from pprint import pprint
import time
from soco.events import event_listener


class getEvents(QThread):
    updateValues = Signal(dict, dict)

    def __init__(self, sonos, parent=None):
        super(getEvents, self).__init__(parent)
        self.avSubscription = sonos.avTransport.subscribe(auto_renew=True)
        self.renderingSubscription = sonos.renderingControl.subscribe(auto_renew=True)
        self.abortThread = False
        self.event = None
        self.event2 = None
        self.pausethread = False

    def run(self):
        while not self.abortThread:
            #self.msleep(100)
            variablesone = None
            variablestwo = None
            if not self.pausethread:
                try:
                    while True:
                        self.event = self.avSubscription.events.get(timeout=0.1)
                except Empty:
                    pass
                try:
                    while True:
                        self.event2 = self.renderingSubscription.events.get(timeout=0.1)
                except Empty:
                    pass
                if self.event2 is not None or self.event is not None:
                    if self.event is not None:
                        print("event")
                        variablesone = self.event.variables
                        print("meta")
                        print(self.event.variables['enqueued_transport_uri_meta_data'].to_dict())
                        pprint(self.event.variables)
                    if self.event2 is not None:
                        print("event2")
                        pprint(self.event2.variables)
                        variablestwo = self.event2.variables

                    self.updateValues.emit(variablesone, variablestwo)
                    self.event = None
                    self.event2 = None

        self.avSubscription.unsubscribe()
        self.renderingSubscription.unsubscribe()
        event_listener.stop()

