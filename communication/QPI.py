# Device protocol ID inquiry

import json
from communication.abstractCode import *



class QPI(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QPI",5)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","")
        Functions.log("DBG","Raw response: " + str(response),"QPI")
        return str(response)

    def pureQuery(self):
        return True
     
    def help(self):
        singleton=Singleton()
        return ["Will return the inverter protocol ID, last grabbed value " + singleton.QPI ]

    def examples(self):
        return ["cmd/QPI"]
