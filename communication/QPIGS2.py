# Device general status parameters inquiry
# GridVoltage, GridFrequency, OutputVoltage, OutputFrequency, OutputApparentPower, OutputActivePower, OutputLoadPercent, BusVoltage, BatteryVoltage, BatteryChargingCurrent, BatteryCapacity, InverterHeatSinkTemperature, PV-InputCurrentForBattery, PV-InputVoltage, BatteryVoltageFromSCC, BatteryDischargeCurrent, DeviceStatus,

import json
from communication.abstractCode import *



class QPIGS2(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending QPIGS2 command","QPIGS2")
        response=""
        try:
            response=self.singleton.connector.write("QPIGS2",106)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"QPIGS2")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"QPIGS2")
            pv_amps,pv_volts,pv_watts,garb=str(response).split(" ")
            QPIGS2={
               "qpigs2_pv2_amps"             : float(pv_amps),
               "qpigs2_pv2_volts"            : float(pv_volts),
               "qpigs2_pv2_watts"            : float(pv_watts)
                  }
            Functions.log("DBG","Response for a QPIGS2 command " + json.dumps(QPIGS2,indent=4),"QPIGS2")
        except Exception as err:
            Functions.log("ERR","Can't parse QPIGS2 response " + str(response),"QPIGS2")
            return {}
           
        return QPIGS2

    def pureQuery(self):
        return True

    def help(self):
        anHelp=[]
        anHelp.append("This command returns solar energy metrics from solar array #2")
        anHelp.append("pv2_amps")
        anHelp.append("pv2_volts")
        anHelp.append("pv2_watts")
        return anHelp

    def examples(self):
        return ["cmd/QPIGS2"]
