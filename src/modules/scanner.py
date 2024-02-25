import cv2
import json
import threading
import numpy as np
from pyzbar import pyzbar as zbar

import subprocess

def notify(title: str, msg: str):
    subprocess.Popen(args=["notify-send", title, msg])

class Scanner:
    def __init__(self, dbus):
        self.running = False
        self.result = ""
        self.dbus_object = dbus

    def parse_wifi(self, data):
        base = data.split(";")
        out = {}
        for x in base:
            if x != "":
                if x[0].lower() == "s":
                    out["ssid"] = x[2:]
                elif x[0].lower() == "p":
                    out["password"] = x[2:]
        
        return out

    def encode_json(self, data: dict):
        return json.dumps(data)

    def get_qr_location(self, obj, frame):
        points = obj.polygon
        # If the points do not form a quad, find convex hull
        if len(points) > 4 :
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0,n):
            cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    def scan_from_webcam(self) -> str:
        cap = cv2.VideoCapture(0)

        self.running = True
        threading.Thread(target=self.loop, args=[cap]).start()

    def get_result(self) -> str:
        while self.running:
            if self.result != "":
                output = self.result
                self.result = ""

                return self.encode_json(output)
        return self.encode_json(output) if output != "" else ""

    def loop(self, cap: cv2.VideoCapture):
        notify("QR Scanner", "Finding qr codes on the camera...")
        while self.running:
            _, frame = cap.read()

            obj_decoded = zbar.decode(frame)
            for decodedObject in obj_decoded:
                self.result = self.parse_wifi(decodedObject.data.decode())
                self.dbus_object.detected_qr()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        notify("QR Scanner", "Stoped finding qr codes on camera")
    
    def scan_from_image(self, img):
        frame = cv2.imread(img)
        # print(__import__("os").getcwd(), img)
        obj_decoded = zbar.decode(frame)
        for decodedObject in obj_decoded:
            parsed = self.parse_wifi(decodedObject.data.decode())
            self.running = False
        
        return parsed
    
    def stop_scan_from_webcam(self):
        self.running = False