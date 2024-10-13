# Device Device mode inquiry

# Computer: QMOD <CRC>
# Device : (M<CRC>)
# MODE                CODE(M) Notes
# Power on mode         P     Power on mode
# Standby mode          S     Standby mode
# Line mode             L     Line mode
# Battery mode          B     Battery mode
# Fault mode            F     Fault mode
# Shutdown mode         D     Shutdown mode
# Example:
#
# Computer: QMOD<CRC>
#

import json
from communication.abstractCode import *



class QMOD(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending QMOD command","QMOD")
        response=""
        QMOD={}
        try:
            response=self.singleton.connector.write("QMOD",2)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"QMOD")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"QMOD")
            qmod_label="Unknown"
            if str(response) == "P":
               qmod_label="Power on mode"
            if str(response) == "S":
               qmod_label="Standby mode"
            if str(response) == "L":
               qmod_label="Line mode"
            if str(response) == "B":
               qmod_label="Battery mode"
            if str(response) == "F":
               qmod_label="Fault mode"
            if str(response) == "D":
               qmod_label="Shutdown mode"
            
            Functions.log("DBG","QMOD label " + str(qmod_label),"QMOD")
            QMOD={
                   "qmod"               : str(response),
                   "qmod_label"         : str(qmod_label)
                  }
            Functions.log("DBG","Response for a QMOD command " + json.dumps(QMOD,indent=4),"QMOD")
        except Exception as err:
            Functions.log("ERR","Can't parse QMOD response " + str(response),"QMOD")
            return {}
           
        return QMOD


    def pureQuery(self):
        return True
 
    def help(self):
        anHelp=[]
        singleton=Singleton()
        anHelp.append("Will return the inverter current mode, last grabbed mode is " + singleton.QMOD["qmod_label"] + "(" + str(singleton.QMOD["qmod"]) + ")")
        anHelp.append("Power on mode")
        anHelp.append("Standby mode")
        anHelp.append("Line mode")
        anHelp.append("Battery mode")
        anHelp.append("Fault mode")
        anHelp.append("Shutdown mode")
        return anHelp


    def examples(self):
        return ["cmd/QMOD"]
        
