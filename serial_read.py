#!/usr/bin/env python
import time
import serial
import base64 as b64
ser = serial.Serial(
        port='/dev/serial0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

latestByte = []

while 1:


       x=ser.read(1)
       try:
          x = int.from_bytes(x, byteorder='big')
          if(x == 170):
             print("Got it",x)

       except ValueError:
          print("failed")

