# Device Setting Battery type
# Parameter needed
#
# Control setting
# 00 for AGM
# 01 for Flooded battery
# 02 for User defined
# 03 for Pylontech

import json
from communication.abstractCode import *



class PBT(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending PBT" + str(parameter) +" command","PBT")
        response=""
        PBT={}
        try:
            response=self.singleton.connector.write("PBT" + str(parameter),10)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PBT")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PBT")
            
            PBT={
               "pbt"               : str(response)
                  }
            Functions.log("DBG","Response for a PBT command " + json.dumps(PBT,indent=4),"PBT")
        except Exception as err:
            Functions.log("ERR","Can't parse PBT response " + str(response),"PBT")
            return {}
           
        return PBT

    def pureQuery(self):
        return False
   
    def help(self):
        return ["This command will setup battery type"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["00 for AGM Battery type","01 for Flooded battery","02 for user defined","03 for Pylontech"]

    def examples(self):
        return ["cmd/PBT/00","cmd/PBT/01","cmd/PBT/02","cmd/PBT/03"]
