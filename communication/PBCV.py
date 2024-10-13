# Device Set battery re charge voltage
# Parameter needed
#
import json
from communication.abstractCode import *



class PBCV(AbstractCode):

    def send(self,parameter):
        if '.' not in parameter:
           parameter=str(parameter) + ".0"
        Functions.log("DBG","Sending PBCV" + str(parameter) +" command","PBCV")
        response=""
        PBCV={}
        try:
            response=self.singleton.connector.write("PBCV" + str(parameter),4)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PBCV")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PBCV")
            
            PBCV={
               "pbcv"               : str(response)
                  }
            Functions.log("DBG","Response for a PBCV command " + json.dumps(PBCV,indent=4),"PBCV")
        except Exception as err:
            Functions.log("ERR","Can't parse PBCV response " + str(response) + " error was=" + str(err),"PBCV")
            return {}
           
        return PBCV
   
    def pureQuery(self):
        return False

    def help(self):
        singleton=Singleton()
        return ["When SBU mode, Charge Battery from Utility activated if this low battery voltage has been reached. Current setting is " + str(singleton.QPIRI["qpiri_batt_recharge_voltage"]) + "v, Battery current voltage is " + str(singleton.QPIGS["qpigs_batt_volt"]) +"v"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["xx.x"]

    def examples(self):
        singleton=Singleton()
        return ["cmd/PBCV/" + str(singleton.QPIRI["qpiri_batt_recharge_voltage"])]

