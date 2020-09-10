import usb.core
import usb.util
import serial
import time
from struct import pack
from crc16 import crc16xmodem
from serial import Serial

from communication.abstractConnector import *


 

class usbConnector(AbstractConnector):

    def populateDevices(self):
        if not self.singleton.parameters["portPath"] == "":
            Functions.log("INF","Port path " + self.singleton.parameters["portPath"] + " will be used","usbConnector")
            self.device=self.singleton.parameters["portPath"]
        # Find the usb superwatt
        self.ser = serial.Serial()
        self.ser.port = self.device
        self.ser.baudrate = 2400
        self.ser.bytesize = serial.EIGHTBITS     #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE     #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  #number of stop bits
        self.ser.timeout = 2                     #non-block read
        #self.ser.timeout = None                     #non-block read
        self.ser.xonxoff = False                 #disable software flow control
        self.ser.rtscts = False                  #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False                  #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 1                #timeout for write

    def connect(self):
        Functions.log("INF","Connecting to device " + self.device,"usbConnector")
        self.ser.open()
        time.sleep(1)
        Functions.log("INF","Connecting to device " + self.device,"usbConnector")
            
    def disconnect(self):
        Functions.log("INF","Disconnecting from device " + self.device,"usbConnector")
        self.dev.close()

    def write(self,data,size):
        if self.ser.isOpen:
           Functions.log("DBG","Writing " + data + " to device " + self.device,"usbConnector")
           self.ser.reset_input_buffer()
           self.ser.reset_output_buffer()
           encoded_cmd = data.encode()
           checksum = crc16xmodem(encoded_cmd)
           request = encoded_cmd + pack('>H', checksum) + b'\r'
           self.ser.write(request[:8])
           if len(request) > 8:
              self.ser.write(request[8:])
           response = self.ser.read(size)
           Functions.log("DBG","Raw device response: " + str(response),"usbConnector")
           response=response.decode("ISO-8859-1")
           response=response.encode("ascii","ignore")
           return response.decode()
        else:
           self.connect()
           return ''

