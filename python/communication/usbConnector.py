rom communication.abstractConnector import *

 

class usbConnector(AbstractConnector):

    def populateDevices(self):
        Functions.log("INF","Discovering serial devices","serialConnector")

    def connect(self):
        Functions.log("INF","Connecting to device","serialConnector")
            
    def disconnect(self):
        Functions.log("INF","Disconnecting to device","serialConnector")

    def read(self):
        Functions.log("INF","Reading to device","serialConnector")

    def write(self,data):
        Functions.log("INF","Writing to device","serialConnector")

