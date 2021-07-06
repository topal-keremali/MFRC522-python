#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
        str = input('New data:')
        print("Now place your tag to write")
        n = 4
        chunks = [str[i:i + n] for i in range(0, len(str), n)]
        empty = ""
        for chunk in chunks:
                for i in range(n):
                        empty += chunk
        id,text = reader.write(empty)
        print("Written")
finally:
        GPIO.cleanup()
