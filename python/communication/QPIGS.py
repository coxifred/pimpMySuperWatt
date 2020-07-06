# Device general status parameters inquiry
# GridVoltage, GridFrequency, OutputVoltage, OutputFrequency, OutputApparentPower, OutputActivePower, OutputLoadPercent, BusVoltage, BatteryVoltage, BatteryChargingCurrent, BatteryCapacity, InverterHeatSinkTemperature, PV-InputCurrentForBattery, PV-InputVoltage, BatteryVoltageFromSCC, BatteryDischargeCurrent, DeviceStatus,

import json
from communication.abstractCode import *



class QPIGS(AbstractCode):

    def send(self):
        response=self.singleton.connector.write("QPIGS",106)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
        Functions.log("DBG","Raw response: " + str(response),"QPIGS")
        grid_vold,grid_freq,ac_volt,ac_freq,ac_va,ac_watt,load_percent,bus_volt,batt_volt,batt_charge_amps,batt_capacity,temp,pv_amps,pv_volts,batt_volt_scc,batt_discharge_amps,raw_status,mask_b,mask_c,pv_watts,mask_d=str(response).split(" ")
        QPIGS={
               "grid_vold"           : grid_vold,
               "grid_freq"           : grid_freq,
               "ac_volt"             : ac_volt,
               "ac_freq"             : ac_freq,
               "ac_va"               : ac_va,
               "ac_watt"             : ac_watt,
               "load_percent"        : load_percent,
               "bus_volt"            : bus_volt,
               "batt_volt"           : batt_volt,
               "batt_charge_amps"    : batt_charge_amps,
               "batt_capacity"       : batt_capacity,
               "temp"                : temp,
               "pv_amps"             : pv_amps,
               "pv_volts"            : pv_volts,
               "batt_volt_scc"       : batt_volt_scc,
               "batt_discharge_amps" : batt_discharge_amps,
               "raw_status"          : raw_status,
               "mask_b"              : mask_b,
               "mask_c"              : mask_c,
               "pv_watts"            : pv_watts,
               "mask_d"              : mask_d
              }
        Functions.log("DBG","Response for a QPIGS command " + json.dumps(QPIGS,indent=4),"QPIGS")
        return QPIGS
