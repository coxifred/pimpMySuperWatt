import os
import math
import datetime
from datetime import timedelta
from abc import ABCMeta, abstractmethod
from utils.functions import Functions
from utils.singleton import Singleton

class abstractPlugin():
        __metaclass__ = ABCMeta

        def runPlugin(self):
            Functions.log("DBG","runPlugin not implemented in AbstractPlugin","AbstractPlugin")

        def influxData(self):
            Functions.log("DBG","influxData not implemented in AbstractPlugin","AbstractPlugin")

        def mqttData(self):
            Functions.log("DBG","mqttData not implemented in AbstractPlugin","AbstractPlugin")

        def __init__(self):
                self.error=0
                self.singleton=Singleton()
