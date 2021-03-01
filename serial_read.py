#!/usr/bin/env python
import time
import serial
import base64 as b64
import numpy as np


EEG_POWER_BANDS = 8
MAX_PACKET_LENGTH = 32

def parsePacket(packetData):

   hasPower = False
   parseSuccess = True
   rawValue =0

   data = {}
   eeg_power = np.zeros((EEG_POWER_BANDS,))

   #print(packetData)
   i=0
   while i< len(packetData):
      p = packetData[i]
      
      if p ==2:
         data["signal_quality"] = packetData[i+1]
         i+=1
      elif p == 4:
         data["attention"] = packetData[i+1]
         i+=1
      elif p == 5:
         data["meditation"] = packetData[i+1]
         i+=1
      elif p == 131:
         i+=1
         for j in range(EEG_POWER_BANDS):
            a = np.uint32(packetData[i+1])<<16
            i+=1
            b = np.uint32(packetData[i+1])<<8
            i+=1
            c = np.uint32(packetData[i+1])
            i+=1
            eeg_power[j] = a | b | c

         data["power"] = list(eeg_power)
         hasPower = True
      elif p ==128:
         i+=1
         rawValue = int(packetData[i+1])<<8 | int(packetData[i+2])
         i+=2
      else:
         print("bad parse data Error")
         parseSuccess = False
      i+=1
   return parseSuccess,data






if __name__ == "__main__":

   ser = serial.Serial(
         port='/dev/serial0',
         baudrate = 9600,
         parity=serial.PARITY_NONE,
         stopbits=serial.STOPBITS_ONE,
         bytesize=serial.EIGHTBITS,
         timeout=1
   )

   latestByte = None
   lastByte = None

   inPacket = False
   packetIndex = np.uint8(0)
   packetLength = np.uint8(0)
   
   packetData = None
   checksumAccumulator = np.uint8(0)
   freshPacket = False

   parsedData = None
   while 1:


      x=ser.read(1)
      try:
         latestByte = np.uint8(int.from_bytes(x, byteorder='big'))

         
         if inPacket:
            if packetIndex == 0:
               packetLength = latestByte
               packetData = np.zeros((packetLength,))
               print(packetLength)
               if packetLength > MAX_PACKET_LENGTH:
                  print("Packet too long")
                  inPacket = False

            elif packetIndex <= packetLength:
               packetData[packetIndex-1] = latestByte
               checksumAccumulator +=latestByte

            elif packetIndex> packetLength:
               checksum = latestByte
               
               checksumAccumulator = np.uint8(255 - checksumAccumulator)
               
               if checksum == checksumAccumulator:
                  parseSuccess, parsedData = parsePacket(packetData)
                  
                  if parseSuccess:
                     freshPacket= True
                  else:
                     print("Could Not Parse")
               else:
                  print("Checksum Error")
               

               inPacket = False

            packetIndex+=1
         
         if latestByte == 170 and lastByte == 170 and not inPacket:
            inPacket = True
            packetIndex = 0
            checksumAccumulator = 0
         
         lastByte = latestByte
         
         if freshPacket and parsedData is not None:
            print("Signal",parsedData['signal_quality'])
            print("Attention",parsedData['attention'])
            print("Relaxation",parsedData['meditation'])
            print("Power",parsedData['power'])
            parsedData = None
            freshPacket = False
            pass





      except ValueError:
         print("failed")




