# Device Battery charge/discharge controlling command
# Parameter needed
#
# Control setting
# 111 - Enable Charger
#     Enable discharger
# 011 - Enabled charger, depends on Prog16 setting if AC source valid, charge 2A from AC, even if prog. 16 is “only solar”. 
#       If prog. 16 is any other setting, ignore and let charging from AC source continue normally.
#     - Disabled discharger and shut down unit completely when insufficient PV or Grid is present
# 101 - Enabled charger, depends on Prog16 setting if AC source valid, charge 2A from AC, even if prog. 16 is “only solar”.
#       If prog. 16 is any other setting, ignore and let charging from AC source continue normally.
#     - Disabled discharger but keep unit stay at standby mode
# 110 - Disabled charger
#     - Enabled discharger
# 010 - Disabled charger
#     - Disabled discharger and shut down unit completely when no PV or Grid is present
# 100 - Disabled charger
#     - Disabled discharger but keep unit stay at standby mode
# 001 - N/A
#     - N/A
# 000 - Cleaned the enable/disable charger flags and return to previous charger status
#     - Cleaned the enable/disable discharger flags and return to previous discharger status.

import json
from communication.abstractCode import *



class PBATCD(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending PBATCD" + str(parameter) +" command","PBATCD")
        response=""
        PBATCD={}
        try:
            response=self.singleton.connector.write("PBATCD" + str(parameter),10)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PBATCD")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PBATCD")
            
            PBATCD={
               "pbatcd"               : str(response)
                  }
            Functions.log("DBG","Response for a PBATCD command " + json.dumps(PBATCD,indent=4),"PBATCD")
        except Exception as err:
            Functions.log("ERR","Can't parse PBATCD response " + str(response),"PBATCD")
            return {}
           
        return PBATCD
   
    def pureQuery(self):
        return False

    def help(self):
        return ["This command will control the battery charge/discharge system"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["111","011","101","110","010","100","001","000"]

    def examples(self):
        return ["cmd/PBATCD/111","cmd/PBATCD/110"]

