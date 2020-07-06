# Main CPU Firmware version inquiry

import json
from communication.abstractCode import *



class QVFW(AbstractCode):

    def send(self):
        response=self.singleton.connector.write("QVFW",15)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QVFW")
        return str(response)
