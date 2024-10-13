# Device reset parameters to default
# no parameter needed

import json
from communication.abstractCode import *



class PF(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending PF command","PF")
        response=""
        PF={}
        try:
            response=self.singleton.connector.write("PF" + str(parameter),10)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PF")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PF")
            
            PF={
               "pf"               : str(response)
                  }
            Functions.log("DBG","Response for a PF command " + json.dumps(PF,indent=4),"PF")
        except Exception as err:
            Functions.log("ERR","Can't parse PF response " + str(response),"PF")
            return {}
           
        return PF

    def pureQuery(self):
        return False
   
    def help(self):
        return ["This command will reset to default parameters"]

    def parameterMandatory(self):
        return False

    def parameterFormat(self):
        return [""]

    def examples(self):
        return ["cmd/PF"]
