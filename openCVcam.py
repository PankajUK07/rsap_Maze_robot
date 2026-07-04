from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.start()

while True:
    frame = picam2.capture_array()

    # Convert RGB → BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()