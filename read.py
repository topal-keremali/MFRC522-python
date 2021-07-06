from time import sleep
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
import RPi.GPIO as GPIO

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
