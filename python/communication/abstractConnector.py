import os
import math
import datetime
from datetime import timedelta
from abc import ABCMeta, abstractmethod
from utils.functions import Functions
from utils.singleton import Singleton
 

 

class AbstractConnector():

        __metaclass__ = ABCMeta

        def __init__(self):
            self.starttime=datetime.datetime.now()
            self.endtime=""
            self.singleton=Singleton()
            Functions.log("DBG","Instanciation of a Connector Class on "  + self.singleton.hostName + " start=" + str(self.starttime),"CORE")
            self.populateDevices()
            self.connect()

        def populateDevices(self):
            Functions.log("DBG","populateDevices not implemented in AbstractConnector","AbstractConnector")

        def connect(self):
            Functions.log("DBG","connect not implemented in AbstractConnector","AbstractConnector")

        def disconnect(self):
            Functions.log("DBG","disconnect not implemented in AbstractConnector","AbstractConnector")

        def read(self):
            Functions.log("DBG","read not implemented in AbstractConnector","AbstractConnector")

