#!/usr/bin/env python3
import dbus

from dbus.service import Object, BusName, method, signal
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib
from modules.scanner import Scanner

DBusGMainLoop(set_as_default=True)

class QRService(Object):
    def __init__(self):
        self.mainloop = GLib.MainLoop()

        self.bus = dbus.SessionBus()
        self.name = BusName("com.github.XtremeTHN.QRScanner", self.bus)

        self.decoded_data = []

        super().__init__(self.bus, "/com/github/XtremeTHN/QRScanner", self.name)
        self.scanner = Scanner(self)

    def run(self):
        self.mainloop.run()

    @method(dbus_interface="com.github.XtremeTHN.QRScanner")
    def StartScan(self):
        ...
        self.scanner.scan()

    @signal(dbus_interface="com.github.XtremeTHN.QRScanner", signature="s")
    def DetectedQR(self, content: str):
        pass

if __name__ == "__main__":
    service = QRService()
    service.run()
