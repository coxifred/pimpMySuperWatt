# Device protocol getting Pv production of the day/month/year

import json
from communication.abstractCode import *


# Pv production of the month
class QEM(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QEM"+ parameter,9)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"QEM")
        QEM={
               "qem_month_production"      : float(response)
            }
        return QEM

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command return the monthly production in watts, last grabbed value " + str(singleton.QEM["qem_month_production"]) + "Wh"]

    def parameterMandatory(self):
        return False

    def parameterFormat(self):
        return []

    def examples(self):
        return ["cmd/QEM"]
