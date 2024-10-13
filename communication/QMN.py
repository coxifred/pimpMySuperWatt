# The device model inquiry

import json
from communication.abstractCode import *



class QMN(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QMN",10)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QMN")
        return str(response)

    def pureQuery(self):
        return True
 
    def help(self):
        singleton=Singleton()
        return ["Will return inverter model, last grabbed value " + singleton.QMN ]

    def examples(self):
        return ["cmd/QMN"]
