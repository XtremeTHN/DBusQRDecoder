import cv2

class Scanner():
    def __init__(self, dbus):
        self.dbus = dbus
        self.cam = cv2.VideoCapture(0)
        self.decoder = cv2.QRCodeDetector()

    def scan(self):
        while True:
            _, frame = self.cam.read()
            ret, points = self.decoder.detect(frame)

            if ret is True:
                try:
                    content, _ = self.decoder.decode(frame, points)
                except cv2.Error as e:
                    print("WARN: Error when detecting qr code from camera:", e, "\nINFO: Ignoring...")
                    continue

                if content != "":
                    return content

    def release(self):
        self.cam.release()
