# Device general status parameters inquiry
# GridVoltage, GridFrequency, OutputVoltage, OutputFrequency, OutputApparentPower, OutputActivePower, OutputLoadPercent, BusVoltage, BatteryVoltage, BatteryChargingCurrent, BatteryCapacity, InverterHeatSinkTemperature, PV-InputCurrentForBattery, PV-InputVoltage, BatteryVoltageFromSCC, BatteryDischargeCurrent, DeviceStatus,

import json
from communication.abstractCode import *



class QPIGS(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending QPIGS command","QPIGS")
        response=""
        try:
            response=self.singleton.connector.write("QPIGS",106)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"QPIGS")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace(";","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"QPIGS")
            grid_volt,grid_freq,ac_volt,ac_freq,ac_va,ac_watt,load_percent,bus_volt,batt_volt,batt_charge_amps,batt_capacity,temp,pv_amps,pv_volts,batt_volt_scc,batt_discharge_amps,raw_status,mask_b,mask_c,pv_watts,mask_d=str(response).split(" ")
            QPIGS={
               "qpigs_grid_volt"           : float(grid_volt),
               "qpigs_grid_freq"           : float(grid_freq),
               "qpigs_ac_volt"             : float(ac_volt),
               "qpigs_ac_freq"             : float(ac_freq),
               "qpigs_ac_va"               : float(ac_va),
               "qpigs_ac_watt"             : float(ac_watt),
               "qpigs_load_percent"        : float(load_percent),
               "qpigs_bus_volt"            : float(bus_volt),
               "qpigs_batt_volt"           : float(batt_volt),
               "qpigs_batt_charge_amps"    : float(batt_charge_amps),
               "qpigs_batt_capacity"       : float(batt_capacity),
               "qpigs_temp"                : float(temp),
               "qpigs_pv_amps"             : float(pv_amps),
               "qpigs_pv_volts"            : float(pv_volts),
               "qpigs_batt_volt_scc"       : float(batt_volt_scc),
               "qpigs_batt_discharge_amps" : float(batt_discharge_amps),
               "qpigs_raw_status"          : float(raw_status),
               "qpigs_mask_b"              : float(mask_b),
               "qpigs_mask_c"              : float(mask_c),
               "qpigs_pv_watts"            : float(pv_watts),
               "qpigs_mask_d"              : float(mask_d)
                  }
            Functions.log("DBG","Response for a QPIGS command " + json.dumps(QPIGS,indent=4),"QPIGS")
        except Exception as err:
            Functions.log("ERR","Can't parse QPIGS response " + str(response),"QPIGS")
            return {}
           
        return QPIGS

    def pureQuery(self):
        return True

    def help(self):
        anHelp=[]
        anHelp.append("This command returns solar energy metrics from solar array #1 + Internal inverter power values")
        anHelp.append("grid_volt")
        anHelp.append("grid_freq")
        anHelp.append("ac_volt")
        anHelp.append("ac_freq")
        anHelp.append("ac_va")
        anHelp.append("ac_watt")
        anHelp.append("load_percent")
        anHelp.append("bus_volt")
        anHelp.append("batt_volt")
        anHelp.append("batt_charge_amps")
        anHelp.append("batt_capacity")
        anHelp.append("temp")
        anHelp.append("pv_amps")
        anHelp.append("pv_volts")
        anHelp.append("batt_volt_scc")
        anHelp.append("batt_discharge_amps")
        anHelp.append("raw_status")
        anHelp.append("mask_b")
        anHelp.append("mask_c")
        anHelp.append("pv_watts")
        return anHelp 

    def examples(self):
        return ["cmd/QPIGS"]
