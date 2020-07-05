import hidraw
from communication.abstractConnector import *

 

class usbConnector(AbstractConnector):

    def populateDevices(self):
        if not self.singleton.parameters["portPath"] == "":
            Functions.log("INF","Port path " + self.singleton.parameters["portPath"] + " will be used","usbConnector")
            self.device=self.singleton.parameters["portPath"]
        Functions.log("INF","Discovering serial devices","usbConnector")

    def connect(self):
        Functions.log("INF","Connecting to device " + self.device,"usbConnector")
        try:
            self.dev = hidraw.device()
            #self.dev.open_path(self.device.encode())
        except Exception as e:
            Functions.log("ERR","Error while connecting to " + self.device + " " + str(e),"usbConnector")
            
    def disconnect(self):
        Functions.log("INF","Disconnecting from device " + self.device,"usbConnector")
        self.dev.close()

    def read(self):
        Functions.log("INF","Reading to device","usbConnector")

    def write(self,data):
        Functions.log("INF","Writing to device","usbConnector")

