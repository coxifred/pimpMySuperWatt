import os
import math
import datetime
from datetime import timedelta
from abc import ABCMeta, abstractmethod
from utils.functions import Functions
from utils.singleton import Singleton

class AbstractClassRule():
        __metaclass__ = ABCMeta
 
        def __init__(self,singleton):
 
                self.error=0
                self.accept=-1
                self.singleton=singleton
 
        def run(self):
                try:
                       self.filter()
                       return self.accept
                except Exception as err:
                        self.error=1
                        self.errorText=str(err).replace(" ", "_")
                        raise
                finally:
                        self.endtime=datetime.datetime.now()
 
        def filter(self):
                Functions.log("DBG","Abstract filter, you should not see this message","CORE")
                return -1
