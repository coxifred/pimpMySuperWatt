# Device protocol getting Pv production of the day/month/year

import json
from communication.abstractCode import *


# Pv production since reset of begining of time
class QET(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QET"+ parameter,9)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"QET")
        QET={
               "qet_firstStart_production"      : float(response)
            }
        return QET

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command returns the production since reset in watts, last grabbed value " + str(singleton.QET["qet_firstStart_production"]) + "Wh"]

    def parameterMandatory(self):
        return False

    def parameterFormat(self):
        return []

    def examples(self):
        return ["cmd/QET"]
