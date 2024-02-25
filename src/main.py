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

        super().__init__(self.bus, "/com/github/XtremeTHN/QRScanner", self.name)
        
        self.scanner = Scanner(self)


    def run(self):
        self.mainloop.run()
    
    @method(dbus_interface="com.github.XtremeTHN.QRScanner")
    def start_scan(self):
        self.scanner.scan_from_webcam()

    @method(dbus_interface="com.github.XtremeTHN.QRScanner", out_signature="s")
    def get_data(self):
        return self.scanner.get_result()
    
    @method(dbus_interface="com.github.XtremeTHN.QRScanner")
    def stop_scan(self):
        self.scanner.stop_scan_from_webcam()
    
    @signal(dbus_interface="com.github.XtremeTHN.QRScanner")
    def detected_qr(self):
        print("Detected qr")
    
if __name__ == "__main__":
    QRService().run()