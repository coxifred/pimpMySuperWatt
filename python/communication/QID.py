# The device serial number inquiry

import json
from communication.abstractCode import *



class QID(AbstractCode):

    def send(self):
        response=self.singleton.connector.write("QID",106)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QID")
        return str(response)
