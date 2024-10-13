# Device Parameter Enable settings
# Parameter needed
#
# Control setting
# a Enable silence buzzer or open buzzer
# b Enable overload bypass
# d Enable solar feed to grid (reserved feature)
# k Enable LCD display escape to default page after 1min timeout
# u Enable overload restart and battery over discharge restart
# v Enable over temperature restart
# x Enable backlight on
# y Enable alarm on when primary source interrupt
# z Enable fault code record

import json
from communication.abstractCode import *



class PE(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending PE" + str(parameter) +" command","PE")
        response=""
        PE={}
        try:
            response=self.singleton.connector.write("PE" + str(parameter),10)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PE")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PE")
            
            PE={
               "pe"               : str(response)
                  }
            Functions.log("DBG","Response for a PE command " + json.dumps(PE,indent=4),"PE")
        except Exception as err:
            Functions.log("ERR","Can't parse PE response " + str(response),"PE")
            return {}
           
        return PE

    def pureQuery(self):
        return False
   
    def help(self):
        return ["This command will enable specified parameter"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["a enable silence buzzer or open buzzer","b enable overload bypass","k enable LCD display escape to default page after 1min timeout","u enable overload restart and battery over discharge restart","v enable over temperature restart","x enable backlight on","y enable alarm on when primary source interrupt","z enable fault code record"]

    def examples(self):
        return ["cmd/PE/a","cmd/PE/b","cmd/PE/k","cmd/PE/u","cmd/PE/v","cmd/PE/x","cmd/PE/y","cmd/PE/z"]
