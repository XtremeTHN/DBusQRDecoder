import cv2

cam = cv2.VideoCapture(0)
decoder = cv2.QRCodeDetector()
while True:
    _, frame = cam.read()
    ret, points = decoder.detect(frame)

    if ret is True:
        try:
            content, _ = decoder.decode(frame, points)
        except cv2.Error as e:
            print("WARN: Error when detecting qr code from camera:", e, "\nINFO: Ignoring...")
            continue
        if content != "":
            print(content)
        points = points[0].astype(int)
        for i in range(4):
            start = tuple(points[i])
            end = tuple(points[(i + 1) % 4])
            cv2.line(frame, start, end, (0,0,255), 3)

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
