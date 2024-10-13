# Device protocol getting Pv production of the day/month/year

import json
from communication.abstractCode import *


# Pv production of the day
class QED(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QED"+ parameter,9)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"QED")
        QED={
               "qed_day_production"      : float(response)
            }
        return QED

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command return the dayly production in watts, last grabbed value " + str(singleton.QED["qed_day_production"]) + "Wh"]

    def parameterMandatory(self):
        return False

    def parameterFormat(self):
        return []

    def examples(self):
        return ["cmd/QED"]
