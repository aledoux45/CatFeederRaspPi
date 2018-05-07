import time
import datetime
import RPi.GPIO as GPIO
from buzzer import *
# import picamera
# import smtplib
# from emails_settings import * # To be modified for different user
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEImage import MIMEImage

# def send_text_and_image(image_name):
#     from_email = gmail_user
#     to_phone = ', '.join(phone_to_text)
#     to_email = ', '.join(email_to_send)
#     body = "Message notification kitties have been fed"

#     # Create the root message and fill in the from, to, and subject headers
#     msgRoot = MIMEMultipart('related')
#     msgRoot['Subject'] = 'Kitten picture eating'
#     msgRoot['From'] = from_email
#     msgRoot['To'] = to_email
#     msgRoot.preamble = 'This is a multi-part message in MIME format.'
#     # Encapsulate the plain and HTML versions of the message body in an
#     # 'alternative' part, so message agents can decide which they want to display.
#     msgAlternative = MIMEMultipart('alternative')
#     msgRoot.attach(msgAlternative)
#     msgText = MIMEText(body)
#     msgAlternative.attach(msgText)
#     # We reference the image in the IMG SRC attribute by the ID we give it below
#     msgText = MIMEText('Picture of the cats.<br><img src="cid:image1"><br>', 'html')
#     msgAlternative.attach(msgText)
#     # This example assumes the image is in the current directory
#     fp = open(image_name, 'rb')
#     msgImage = MIMEImage(fp.read())
#     fp.close()
#     # Define the image's ID as referenced above
#     msgImage.add_header('Content-ID', '<image1>')
#     msgRoot.attach(msgImage)

#     # Send the image and text via smtp
#     s = smtplib.SMTP("smtp.gmail.com", 587)
#     s.set_debuglevel(1)
#     s.ehlo()
#     s.starttls()
#     s.login(gmail_user, gmail_pwd)
#     s.sendmail(from_email, to_email, msgRoot.as_string())
#     s.sendmail(from_email, to_phone, body)
#     print(">>> Text sent to Yozhiks!")
#     s.quit()

def feed_cat():
    # Set servo on Servo1Pin to 1200us (1.2ms)
    servo = GPIO.PWM(servo_pin, 50)
    servo.start(10.5)
    time.sleep(3.5)
    servo.stop()
    time.sleep(.05)


# Pin connections
servo_pin = 18
buzzer_pin = 5

# Tell the GPIO who is what
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Initiate buzzer and camera and time_of_day
buzzer = Buzzer(buzzer_pin)
# camera = picamera.PiCamera()

# Test for first run
now = datetime.datetime.now().time()
buzzer.play()
feed_cat()
print(">>> Cats have been fed (first run) at " + now.strftime("%H:%M:%S"))
# image_name = '/home/pi/camera/kitten' + now.strftime("%H:%M:%S") + '.jpg'
# camera.capture(image_name)
# send_text_and_image(image_name)


