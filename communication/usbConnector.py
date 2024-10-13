import usb.core
import usb.util
import serial
import time
from threading import Thread, Lock
from struct import pack
from crc16 import crc16xmodem
from serial import Serial
from usb_resetter.usb_resetter import main

from communication.abstractConnector import *




 

class usbConnector(AbstractConnector):
 
    queue={}

 

    def cleanUp(self):
        self.connected=False
        self.stop=True
        self.lock.release()
        self.disconnect()

    def populateDevices(self):
        if not self.singleton.parameters["portPath"] == "":
            Functions.log("DBG","Port path " + self.singleton.parameters["portPath"] + " will be used","usbConnector")
            self.device=self.singleton.parameters["portPath"]
        # Find the usb superwatt
        self.stop=False
        self.lock=Lock()
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
        #self.ser.exclusive = True
        self.ser.dsrdtr = False                  #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 1                #timeout for write

    def connect(self):
        singleton=Singleton()
        singleton.ready=False
        Functions.log("INF","Connecting to device " + self.device + " ...","usbConnector")
        if self.stop:
           return
        if not self.ser.is_open:
           try:
               singleton.communicationStatus="CONNECTING"
               Functions.log("INF"," - Open device","usbConnector")
               self.ser.open()
               Functions.log("INF"," - Reset device","usbConnector")
               self.ser.reset_input_buffer()
               self.ser.reset_output_buffer()
               self.connected=True
               singleton.communicationStatus="CONNECTED"
           except Exception as err:
               singleton.communicationStatus="DOWN"
               self.connected=False
               Functions.log("ERR", "Can't connect to device " + self.device + " error was " + str(err),"usbConnector")
        else:
           Functions.log("INF",self.device + " Already open, make some reset","usbConnector")
           self.ser.reset_input_buffer()
           self.ser.reset_output_buffer()
           Functions.log("INF",self.device + " Already open, make some flush","usbConnector")
           self.ser.flush()
           self.connected=True
           singleton.communicationStatus="CONNECTED"
           self.lastCommand=""
        if self.connected:
           Functions.log("ACK","Successfully connected to device " + self.device,"usbConnector")
           singleton.communicationStatus="CONNECTED"
           time.sleep(10)
            
    def disconnect(self):
        try:
            if self.ser.is_open:
               self.ser.reset_input_buffer()
               self.ser.reset_output_buffer()
               self.ser.flush()
               Functions.log("INF","Disconnecting from device " + self.device,"usbConnector")
               self.ser.close()
               self.connected=False
               singleton.communicationStatus="DOWN"
        except Exception as err:
            Functions.log("ERR","Can't disconnect properly " + self.device + " error was " + str(err) ,"usbConnector")

    def write(self,data,size):
        timeout=20
        self.lock.acquire(timeout=timeout)
        singleton=Singleton()
        singleton.queue=usbConnector.queue
        # Protection 
        Functions.log("DBG","connector queue size=" + str(len(usbConnector.queue)) ,"usbConnector")
        while len(usbConnector.queue) > 0 and timeout > 0:
          Functions.log("DBG","Waiting lastCommand to finish " + self.lastCommand + " timeout=" + str(timeout) + " connector queue size=" + str(len(usbConnector.queue)) ,"usbConnector")
          time.sleep(1)
          singleton.queue=usbConnector.queue
          timeout-=1

        usbConnector.queue[str(data)]=str(size)
        if self.connected and self.ser.is_open:
           try:
               Functions.log("DBG","Writing " + data + " to device " + self.device + " connector queue size=" + str(len(usbConnector.queue)) ,"usbConnector")
               self.lastCommand=data 
               encoded_cmd = data.encode()
               checksum = crc16xmodem(encoded_cmd)
               request = encoded_cmd + pack('>H', checksum) + b'\r'
               self.ser.flush()
               self.ser.reset_input_buffer()
               self.ser.reset_output_buffer()
               self.ser.write(request[:8])
               if len(request) > 8:
                  self.ser.write(request[8:])
               self.ser.flush()
               response = self.ser.read(size)
               Functions.log("DBG","Raw device response for " + data + " : " + str(response),"usbConnector")
               response=response.decode("ISO-8859-1")
               response=response.encode("ascii","ignore")
               self.lock.release()
               decoded=response.decode()
               time.sleep(1)
               usbConnector.queue.pop(str(data))
               singleton.queue=usbConnector.queue
               return decoded
           except Exception as err:
               Functions.log("ERR", "Can't write to device " + self.device + " error was " + str(err),"usbConnector")
               self.disconnect()
               usbConnector.queue.pop(str(data))
               singleton.queue=usbConnector.queue
               self.connected=False
               self.lock.release()
               raise err
        else:
           usbConnector.pop(str(data))
           singleton.queue=usbConnector.queue
           self.lock.release()
           raise Exception()

