# Another CPU Firmware version inquiry

import json
from communication.abstractCode import *



class QVFW3(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QVFW3",15)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + response,"QVFW3")
        
        return response

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command returns the inverter #2 Display Firmware version, last grabbed value " + singleton.QVFW3]

    def examples(self):
        return ["cmd/QVFW3"]
