# Device protocol ID inquiry

import json
from communication.abstractCode import *



class QPI(AbstractCode):

    def send(self):
        response=self.singleton.connector.write("QPI",16)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","")
        Functions.log("DBG","Raw response: " + str(response),"QPI")
        return str(response)
