import cv2

class Scanner():
    def __init__(self, dbus):
        self.dbus = dbus
        self.decoder = cv2.QRCodeDetector()

    def scan(self):
        cam = cv2.VideoCapture(0)

        while True:
            _, frame = cam.read()
            ret, points = self.decoder.detect(frame)

            if ret is True:
                try:
                    content, _ = self.decoder.decode(frame, points)
                except Exception as e:
                    print("WARN: Error when detecting qr code from camera:", e, "\nINFO: Ignoring...")
                    continue

                if content != "":
                    return content

        cam.release()
