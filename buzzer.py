import RPi.GPIO as GPIO   #import the GPIO library
import time               #import the time library


class Buzzer(object):
    def __init__(self, buzzer_pin):
        GPIO.setmode(GPIO.BCM)
        self.buzzer_pin = buzzer_pin
        GPIO.setup(self.buzzer_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        print("Buzzer is ready to work")

    def __del__(self):
        class_name = self.__class__.__name__
        print (class_name, "finished")

    def buzz(self, pitch, duration):
        if pitch==0:
            time.sleep(duration)
            return
        period = 1.0 / pitch     # The period (sec/cyc) is the inverse of the frequency (cyc/sec)
        delay = period / 2     # Calcuate the time for half of the wave
        cycles = int(duration * pitch)   # The number of waves to produce is the duration times the frequency

        for i in range(cycles):
            GPIO.output(self.buzzer_pin, True)   # Set buzzer_pin to high
            time.sleep(delay)    # Wait with buzzer_pin high
            GPIO.output(self.buzzer_pin, False)  # Set buzzer_pin to low
            time.sleep(delay)    # Wait with buzzer_pin low

    def play(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        print("Playing tune for the kitties")
        pitches = [262,294,330,349,392,440,494,523,587,659,698,784,880,988,1047]
        duration = 0.1
        for p in pitches:
            self.buzz(p, duration)
            time.sleep(duration*0.5)
        for p in reversed(pitches):
            self.buzz(p, duration)
            time.sleep(duration*0.5)

        GPIO.setup(self.buzzer_pin, GPIO.IN)
