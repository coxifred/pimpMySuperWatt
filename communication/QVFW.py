# Main CPU Firmware version inquiry

import json
from communication.abstractCode import *



class QVFW(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QVFW",15)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QVFW")
        return str(response)

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command returns the inverter #1 CPU Firmware version, last grabbed value " + singleton.QVFW]

    def examples(self):
        return ["cmd/QVFW"]
