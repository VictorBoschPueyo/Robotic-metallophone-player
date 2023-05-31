from picamera import PiCamera
import time

def take_picture():
    camera = PiCamera()

    camera.resolution = (2000, 1944)
    camera.contrast = 40
    camera.saturation = -100
    
    time.sleep(2)
    camera.capture("photo_sheet.jpg")