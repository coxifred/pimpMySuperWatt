# Device Set battery dis charge voltage
# Parameter needed
#
import json
from communication.abstractCode import *



class PBDV(AbstractCode):

    def send(self,parameter):
        if '.' not in parameter:
           parameter=str(parameter) + ".0"
        Functions.log("DBG","Sending PBDV" + str(parameter) +" command","PBDV")
        response=""
        PBDV={}
        try:
            response=self.singleton.connector.write("PBDV" + str(parameter),4)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PBDV")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PBDV")
            
            PBDV={
               "pbdv"               : str(response)
                  }
            Functions.log("DBG","Response for a PBDV command " + json.dumps(PBDV,indent=4),"PBDV")
        except Exception as err:
            Functions.log("ERR","Can't parse PBDV response " + str(response),"PBDV")
            return {}
           
        return PBDV
   
    def pureQuery(self):
        return False

    def help(self):
        singleton=Singleton()
        return ["When SBU mode, Discharge on Battery first activated if this battery voltage has been reached. Current setting is " + str(singleton.QPIRI["qpiri_batt_redischarge_voltage"]) + "v, Battery current voltage is " + str(singleton.QPIGS["qpigs_batt_volt"]) +"v"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["xx.x"]

    def examples(self):
        singleton=Singleton()
        return ["cmd/PBDV/" + str(singleton.QPIRI["qpiri_batt_redischarge_voltage"])]

