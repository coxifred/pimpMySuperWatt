# Device Parameter Disable settings
# Parameter needed
#
# Control setting
# a Disable silence buzzer or open buzzer
# b Disable overload bypass
# d Disable solar feed to grid (reserved feature)
# k Disable LCD display escape to default page after 1min timeout
# u Disable overload restart and battery over discharge restart
# v Disable over temperature restart
# x Disable backlight on
# y Disable alarm on when primary source interrupt
# z Disable fault code record

import json
from communication.abstractCode import *



class PD(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending PD" + str(parameter) +" command","PD")
        response=""
        PD={}
        try:
            response=self.singleton.connector.write("PD" + str(parameter),10)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"PD")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"PD")
            
            PD={
               "pd"               : str(response)
                  }
            Functions.log("DBG","Response for a PD command " + json.dumps(PD,indent=4),"PD")
        except Exception as err:
            Functions.log("ERR","Can't parse PD response " + str(response),"PD")
            return {}
           
        return PD
   
    def pureQuery(self):
        return False

    def help(self):
        return ["This command will disable specified parameter"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["a disable silence buzzer or open buzzer","b disable overload bypass","k disable LCD display escape to default page after 1min timeout","u disable overload restart and battery over discharge restart","v disable over temperature restart","x disable backlight on","y disable alarm on when primary source interrupt","z disable fault code record"]

    def examples(self):
        return ["cmd/PD/a","cmd/PD/b","cmd/PD/k","cmd/PD/u","cmd/PD/v","cmd/PD/x","cmd/PD/y","cmd/PD/z"]

