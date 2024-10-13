# Another CPU Firmware version inquiry

import json
from communication.abstractCode import *



class QVFW2(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QVFW2",6)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + response,"QVFW2")
        
        return response

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command returns the inverter #2 CPU Firmware version, last grabbed value " + singleton.QVFW2]

    def examples(self):
        return ["cmd/QVFW2"]
