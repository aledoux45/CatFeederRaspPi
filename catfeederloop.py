from time import sleep
import datetime
import smtplib
import RPi.GPIO as GPIO
from buzzer import *
import picamera
from emails_settings import * # To be modified for different user
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


def send_text_and_image(image_name):
    from_email = gmail_user
    to_phone = ', '.join(phone_to_text)
    to_email = ', '.join(email_to_send)
    body = "Message notification kitties have been fed"

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Kitten picture eating'
    msgRoot['From'] = from_email
    msgRoot['To'] = to_email
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText(body)
    msgAlternative.attach(msgText)
    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('Picture of the cats.<br><img src="cid:image1"><br>', 'html')
    msgAlternative.attach(msgText)
    # This example assumes the image is in the current directory
    fp = open(image_name, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the image and text via smtp
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.login(gmail_user, gmail_pwd)
    s.sendmail(from_email, to_email, msgRoot.as_string())
    # s.sendmail(from_email, to_phone, body)
    print(">>> Text sent to Yozhiks!")
    s.quit()


def feed_cat():
    # Set servo on Servo1Pin to 1200us (1.2ms)
    servo = GPIO.PWM(servo_pin, 50)
    servo.start(10.5)
    time.sleep(3.5)
    servo.stop()
    time.sleep(.05)


def take_cat_picture(file_name):
    video_taken = False
    i = 0
    while i < 100 and not video_taken:
        time.sleep(0.1)
        current_state = GPIO.input(motion_pin)
        if current_state:
            print(">>> Kitten has been detected")
            camera.start_recording(file_name + '.h264')
            sleep(5)
            camera.stop_recording()
            video_taken = True
        i += 1
    camera.capture(file_name + '.jpg')

# Pin connections
servo_pin = 18
buzzer_pin = 5
motion_pin = 4

# Tell the GPIO who is what
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(motion_pin, GPIO.IN, GPIO.PUD_DOWN)

# Initiate buzzer and camera and time_of_day
buzzer = Buzzer(buzzer_pin)
camera = picamera.PiCamera()
time_of_day = "DAY"


### Test for first run
now = datetime.datetime.now().time()
buzzer.play()
feed_cat()
print(">>> Cats have been fed (first run) at " + now.strftime("%H:%M:%S"))
file_name = '/home/pi/camera/kitten' + now.strftime("%H:%M:%S")
take_cat_picture(file_name)
send_text_and_image(file_name + '.jpg')
###


while True:
    # What time is it?
    now = datetime.datetime.now().time()
    print(now)
    print(time_of_day)

    if feedtime_morning < now < feedtime_evening and time_of_day != "DAY":
        time_of_day = "DAY"
        buzzer.play()
        feed_cat()
        print(">>> Cats have been fed in the morning at " + now.strftime("%H:%M:%S"))
        file_name = '/home/pi/camera/kitten' + now.strftime("%H:%M:%S")
        take_cat_picture(file_name)
        send_text_and_image(file_name + '.jpg')

    elif (now > feedtime_evening or now < feedtime_morning) and time_of_day != "NIGHT":
        time_of_day = "NIGHT"
        buzzer.play()
        feed_cat()
        print(">>> Cats have been fed in the evening at " + now.strftime("%H:%M:%S"))
        image_name = '/home/pi/camera/kitten' + now.strftime("%H:%M:%S") + '.jpg'
        file_name = '/home/pi/camera/kitten' + now.strftime("%H:%M:%S")
        take_cat_picture(file_name)
        send_text_and_image(file_name + '.jpg')

    #  Wait another 5min
    time.sleep(300)
