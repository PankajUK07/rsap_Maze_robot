from picamera2 import Picamera2
import time

picam2 = Picamera2()

config = picam2.create_preview_configuration()
picam2.configure(config)

picam2.start()

time.sleep(2)

picam2.capture_file("image.jpg")

print("Image Saved")

picam2.stop()