import os
import math
import datetime
from datetime import timedelta
from abc import ABCMeta, abstractmethod
from utils.functions import Functions
from utils.singleton import Singleton
 

 

class AbstractConnector():

        __metaclass__ = ABCMeta

        def __init__(self,singleton):
             self.singleton=singleton
             self.starttime=datetime.datetime.now()
             self.endtime=""
             Functions.log("DBG","Instanciation of a Connector Class on "  + self.singleton.hostName + " start=" + str(self.starttime),"CORE")

        def populateDevices(self):

        def connect(self):
  
        def disconnect(self):

        def read(self):

        def write(self,data):
 
