# The device serial number inquiry

import json
from communication.abstractCode import *



class QID(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QID",17)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QID")
        return str(response)

    def pureQuery(self):
        return True
 
    def help(self):
        singleton=Singleton()
        return ["Will return the inverter serial number, last grabbed value " + str(singleton.QID)]

    def examples(self):
        return ["cmd/QID"]
