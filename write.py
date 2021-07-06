#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        id,text = reader.write(text)
        print("Written"+text)
finally:
        GPIO.cleanup()
