import RPi.GPIO as GPIO
import time
import datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

channel = 17

GPIO.setup(channel, GPIO.IN)

while True:
  print("Water sensor: ", GPIO.input(channel))

  time.sleep(1)
