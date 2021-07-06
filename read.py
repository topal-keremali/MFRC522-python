from time import sleep
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
import RPi.GPIO as GPIO

try:
    print("Hold a tag near the reader")
    len = len(reader.BLOCK_ADDRS)
    id, text = reader.read()
    print(text)
    cut_text = text[0:(len*4)]
    print("ID: %s\nText: %s" % (id,cut_text))
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
