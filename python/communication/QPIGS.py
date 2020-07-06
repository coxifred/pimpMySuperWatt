# Device general status parameters inquiry
# GridVoltage, GridFrequency, OutputVoltage, OutputFrequency, OutputApparentPower, OutputActivePower, OutputLoadPercent, BusVoltage, BatteryVoltage, BatteryChargingCurrent, BatteryCapacity, InverterHeatSinkTemperature, PV-InputCurrentForBattery, PV-InputVoltage, BatteryVoltageFromSCC, BatteryDischargeCurrent, DeviceStatus,

import json
from communication.abstractCode import *



class QPIGS(AbstractCode):

    def send(self):
        response=self.singleton.connector.write("QPIGS",106)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QPIGS")
        grid_volt,grid_freq,ac_volt,ac_freq,ac_va,ac_watt,load_percent,bus_volt,batt_volt,batt_charge_amps,batt_capacity,temp,pv_amps,pv_volts,batt_volt_scc,batt_discharge_amps,raw_status,mask_b,mask_c,pv_watts,mask_d=str(response).split(" ")
        QPIGS={
               "grid_volt"           : float(grid_volt),
               "grid_freq"           : float(grid_freq),
               "ac_volt"             : float(ac_volt),
               "ac_freq"             : float(ac_freq),
               "ac_va"               : float(ac_va),
               "ac_watt"             : float(ac_watt),
               "load_percent"        : float(load_percent),
               "bus_volt"            : float(bus_volt),
               "batt_volt"           : float(batt_volt),
               "batt_charge_amps"    : float(batt_charge_amps),
               "batt_capacity"       : float(batt_capacity),
               "temp"                : float(temp),
               "pv_amps"             : float(pv_amps),
               "pv_volts"            : float(pv_volts),
               "batt_volt_scc"       : float(batt_volt_scc),
               "batt_discharge_amps" : float(batt_discharge_amps),
               "raw_status"          : float(raw_status),
               "mask_b"              : float(mask_b),
               "mask_c"              : float(mask_c),
               "pv_watts"            : float(pv_watts),
               "mask_d"              : float(mask_d)
              }
        Functions.log("DBG","Response for a QPIGS command " + json.dumps(QPIGS,indent=4),"QPIGS")
        return QPIGS
