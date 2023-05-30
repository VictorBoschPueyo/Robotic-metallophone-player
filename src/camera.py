from picamera import PiCamera
import time

def take_picture():
    camera = PiCamera()

    camera.resolution = (2000, 1944)
    camera.contrast = 10
    
    time.sleep(2)
    camera.capture(".sheet/img.jpg")
    print("Done.")