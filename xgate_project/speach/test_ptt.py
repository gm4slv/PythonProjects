import RPi.GPIO as GPIO
import time

PTT = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PTT,GPIO.OUT)

while True:
    print GPIO.input(PTT)
    time.sleep(1)
