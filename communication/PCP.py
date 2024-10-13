# Setting device charger priority

import json
from communication.abstractCode import *


# Setting device charger priority
'''
Computer: PCP<NN><CRC><cr>
Device: (ACK<CRC><cr> if device accepts this command, otherwise, responds
(NAK<CRC><cr>
Set output source priority,
01 for solar first, 02 for solar and utility, 03 for only solar charging
'''
class PCP(AbstractCode):

    def send(self,parameter):
        Functions.log("WNG","Sending: PCP" + str(parameter),"PCP")
        response=self.singleton.connector.write("PCP" + parameter,9)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"PCP")
        return str(response)

    def pureQuery(self):
        return False

    def help(self):
        singleton=Singleton()
        return ["This command will setup the device charger priority, last grabbed value is " + singleton.QPIRI["qpiri_charger_source_priority"] + "(" + str(singleton.QPIRI["qpiri_charger_source_priority_raw"]) + ")"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["01 for solar first","02 for solar and utility","03 for only solar charging"]

    def examples(self):
        return ["cmd/PCP/01","cmd/PCP/02","cmd/PCP/03"]
