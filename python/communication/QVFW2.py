# Another CPU Firmware version inquiry

import json
from communication.abstractCode import *



class QVFW2(AbstractCode):

    def send(self):
        response=self.singleton.connector.write("QVFW2",20)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + response,"QVFW2")
        
        return response
