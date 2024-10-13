# Device Device flag status inquiry
# QFLAG<cr>: Device flag status inquiry

# ExxxDxxx is the flag status. E means enable, D means disable x
#
# a Enable/disable silence buzzer or open buzzer
# b Enable/Disable overload bypass function
# d Enable/Disable solar feed to grid (reserved)
# k Enable/Disable LCD display escape to default page after 1min timeout
# u Enable/Disable overload restart
# v Enable/Disable over temperature restart
# x Enable/Disable backlight on
# y Enable/Disable alarm on when primary source interrupt
# z Enable/Disable fault code record


import json
import traceback
from communication.abstractCode import *



class QFLAG(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending QFLAG command","QFLAG")
        response=""
        QFLAG={}
        try:
            response=self.singleton.connector.write("QFLAG",12)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"QFLAG")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"QFLAG")
            enabledOnes=Functions.getFieldFromString(str(response),"D",0).replace("E","")
            disabledOnes=Functions.getFieldFromString(str(response),"D",1).replace("D","")
            Functions.log("DBG","EnabledOnes: " + str(enabledOnes),"QFLAG")
            Functions.log("DBG","DisabledOnes: " + str(disabledOnes),"QFLAG")
            
            buzzerEnable=False
            overloadBypassEnable=False
            solarFeedToGridEnable=False
            lcdDisplayEscapeEnable=False
            overloadRestartEnable=False
            overTemperatureRestartEnable=False
            backlightEnable=False
            alarmOnPrimarySourceGoneEnable=False
            faultCodeRecordEnable=False

            for aFlag in enabledOnes:
                if aFlag == "a":
                   buzzerEnable=True
                if aFlag == "b":
                   overloadBypassEnable=True
                if aFlag == "d":
                   solarFeedToGridEnable=True
                if aFlag == "k":
                   lcdDisplayEscapeEnable=True
                if aFlag == "u":
                   overloadRestartEnable=True
                if aFlag == "v":
                   overTemperatureRestartEnable=True
                if aFlag == "x":
                   backlightEnable=True
                if aFlag == "y":
                   alarmOnPrimarySourceGoneEnable=True
                if aFlag == "z":
                   alarmOnPrimarySourceGoneEnable=True
                   
       
                 
            
            QFLAG={
                    "qflag"                                  : str(response),
                    "qflag_buzzerEnable"                     : buzzerEnable,
                    "qflag_overloadBypassEnable"             : overloadBypassEnable,
                    "qflag_solarFeedToGridEnable"            : solarFeedToGridEnable,
                    "qflag_lcdDisplayEscapeEnable"           : lcdDisplayEscapeEnable,
                    "qflag_overloadRestartEnable"            : overloadRestartEnable,
                    "qflag_overTemperatureRestartEnable"     : overTemperatureRestartEnable,
                    "qflag_backlightEnable"                  : backlightEnable,
                    "qflag_alarmOnPrimarySourceGoneEnable"   : alarmOnPrimarySourceGoneEnable,
                    "qflag_faultCodeRecordEnable"            : faultCodeRecordEnable
                  }
            Functions.log("DBG","Response for a QFLAG command " + json.dumps(QFLAG,indent=4),"QFLAG")
        except Exception as err:
            Functions.log("ERR",str(traceback.print_exc()),"QFLAG")
            Functions.log("ERR","Can't parse QFLAG response " + str(response) + " error was " + str(err) ,"QFLAG")
            return {}
           
        return QFLAG
 
    def pureQuery(self):
        return True

    def help(self):
        anHelp=[]

        anHelp.append("Display bascic inverter settings (LCD, Buzzer,...)")
        anHelp.append("Display silence buzzer or open buzzer settings")
        anHelp.append("Display overload bypass function settings")
        anHelp.append("Display solar feed to grid (reserved) settings")
        anHelp.append("Display LCD display escape to default page after 1min timeout settings")
        anHelp.append("Display overload restart settings")
        anHelp.append("Display over temperature restart settings")
        anHelp.append("Display backlight on settings")
        anHelp.append("Display alarm on when primary source interrupt settings")
        anHelp.append("Display fault code record settings")

        return anHelp

    def examples(self):
        return ["cmd/QFLAG"]

