# Device: Setting device output source priority
# Parameter needed
#
# Set output source priority
#
# 00 for UtilitySolarBat
# 01 for SolarUtilityBat
# 02 for SolarBatUtility
#

import json
from communication.abstractCode import *
class POP(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending POP" + str(parameter) +" command","POP")
        response=""
        POP={}
        try:
            response=self.singleton.connector.write("POP" + str(parameter),10)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"POP")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"POP")
            POP={
               "pop"               : str(response)
               
                  }
            Functions.log("DBG","Response for a POP command " + json.dumps(POP,indent=4),"POP")
        except Exception as err:
            Functions.log("ERR","Can't parse POP response " + str(response),"POP")
            return {}
           
        return POP

    def pureQuery(self):
        return False

    def help(self):
        singleton=Singleton()
        return ["This command will set the output source priority, last grabbed value is " + singleton.QPIRI["qpiri_output_source_priority"] + "(" + str(singleton.QPIRI["qpiri_output_source_priority_raw"]) + ")"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["00 for UtilitySolarBat aka USB","01 for SolarUtilityBat aka SUB","02 for SolarBatUtility aka SBU"]

    def examples(self):
        return ["cmd/POP/00","cmd/POP/01","cmd/POP/02"]
