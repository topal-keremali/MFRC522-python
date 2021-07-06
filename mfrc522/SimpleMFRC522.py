# Code by Simon Monk https://github.com/simonmonk/

from . import MFRC522
import RPi.GPIO as GPIO


class SimpleMFRC522:
    READER = None

    KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    BLOCK_ADDRS = [0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                   0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28,
                   0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
                   0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a,
                   0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x5b,
                   0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x61, 0x62, 0x63]

    def __init__(self):
        self.READER = MFRC522()

    def read(self):
        id, text = self.read_no_block()
        while not id:
            id, text = self.read_no_block()
        return id, text

    def read_id(self):
        id = self.read_id_no_block()
        while not id:
            id = self.read_id_no_block()
        return id

    def read_id_no_block(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None
        return self.uid_to_num(uid)

    def read_no_block(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        # status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
        data = []
        text_read = ''
        if status == self.READER.MI_OK:
            for block_num in self.BLOCK_ADDRS:
                block = self.READER.MFRC522_Read(block_num)
                if block:
                    data += block[0:4]
            if data:
                text_read = ''.join(chr(i) for i in data)
        self.READER.MFRC522_StopCrypto1()
        return id, text_read

    def write(self, text):
        id, text_in = self.write_no_block(text)
        while not id:
            id, text_in = self.write_no_block(text)
        return id, text_in

    def write_no_block(self, text):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        # status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
        self.READER.MFRC522_Read(11)
        if status == self.READER.MI_OK:
            data = bytearray()
            data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
            i = 0
            for block_num in self.BLOCK_ADDRS:
                self.READER.MFRC522_Write(block_num, data[(i * 16):(i + 1) * 16])
                i += 1
        self.READER.MFRC522_StopCrypto1()
        return id, text[0:(len(self.BLOCK_ADDRS) * 16)]

    def uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n
