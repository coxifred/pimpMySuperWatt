# Device protocol getting Pv production of the day/month/year

import json
from communication.abstractCode import *


# Pv production of the year
class QEY(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QEY"+ parameter,9)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"QEY")
        QEY={
               "qey_year_production"      : float(response)
            }
        return QEY

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command returns the year production in watts, last grabbed value " + str(singleton.QEY["qey_year_production"]) + "Wh"]

    def parameterMandatory(self):
        return False

    def parameterFormat(self):
        return []

    def examples(self):
        return ["cmd/QEY"]
