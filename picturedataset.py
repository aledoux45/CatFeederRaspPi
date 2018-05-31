from time import sleep
import RPi.GPIO as GPIO
import picamera

# This file take cpitures of cats when the motion sensors detects the presence of a cat

# Pin connections
motion_pin = 4

# Tell the GPIO who is what
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin, GPIO.IN, GPIO.PUD_DOWN)

i = 0
while True:
    current_state = GPIO.input(motion_pin)
    if current_state:
        print('>>> Kitten has been detected: ' + str(i))
        file_name = '/home/pi/Pictures/kittens/kitten' + str(i) + '.png'
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.CAPTURE_TIMEOUT = 60
            camera.capture(file_name)
        i += 1
    sleep(1)
