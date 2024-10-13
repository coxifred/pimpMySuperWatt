# The device general model inquiry

import json
from communication.abstractCode import *



class QGMN(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QGMN",3)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QGMN")
        return str(response)

    def pureQuery(self):
        return True
 
    def help(self):
        singleton=Singleton()
        return ["Will return inverter general model, last grabbed value " + singleton.QGMN ]

    def examples(self):
        return ["cmd/QGMN"]
