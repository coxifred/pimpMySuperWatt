# Device protocol getting Pv production of the day/month/year

import json
from communication.abstractCode import *


# Pv production since reset of begining of time
class QBMS(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QBMS",34)
        Functions.log("DBG","Raw response (before cleaning): " + str(response),"QBMS")
        tempResponse=str(response)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace(",","").replace(";","").replace("?","")
        Functions.log("DBG","Raw response (after cleaning): " + str(response),"QBMS")
        battery_connect_status,battery_percentage,force_ac_charge_battery,battery_stop_discharge_flag,battery_stop_charge_flag,battery_cv_charging_voltage,battery_floating_charging_voltage,battery_cutoff_voltage,battery_max_charging_current,battery_max_discharging_current=str(response).split(" ")

        battery_connect_status_raw=int(battery_connect_status)
        if battery_connect_status_raw == 0:
           battery_connect_status="connected"
        else:
           battery_connect_status="disconnected"

        force_ac_charge_battery_raw=int(force_ac_charge_battery)
        if force_ac_charge_battery_raw == 0:
           force_ac_charge_battery="Do not force"
        else:
           force_ac_charge_battery="Force"
 
        battery_stop_discharge_flag_raw=int(battery_stop_discharge_flag)
        if battery_stop_discharge_flag_raw == 0:
           battery_stop_discharge_flag="Enable discharge"
        else: 
           battery_stop_discharge_flag="Disable discharging"

        battery_stop_charge_flag_raw=int(battery_stop_charge_flag)
        if battery_stop_charge_flag_raw == 0:
           battery_stop_charge_flag="Enable charge"
        else:
           battery_stop_charge_flag="Disable charging"

        Functions.log("DBG","Raw response: " + str(tempResponse),"QBMS")
        QBMS={
               "qbms"      : str(response),
               "qbms_battery_connect_status_raw"           : battery_connect_status_raw,
               "qbms_battery_connect_status"               : battery_connect_status_raw, 
               "qbms_battery_percentage"                   : int(battery_percentage),
               "qbms_force_ac_charge_battery_raw"          : force_ac_charge_battery_raw,
               "qbms_force_ac_charge_battery"              : force_ac_charge_battery,
               "qbms_battery_stop_discharge_flag_raw"      : battery_stop_discharge_flag_raw,
               "qbms_battery_stop_discharge_flag"          : battery_stop_discharge_flag,
               "qbms_battery_stop_charge_flag_raw"         : battery_stop_charge_flag_raw,
               "qbms_battery_stop_charge_flag"             : battery_stop_charge_flag,
               "qbms_battery_cv_charging_voltage"          : int(battery_cv_charging_voltage),
               "qbms_battery_floating_charging_voltage"    : int(battery_floating_charging_voltage),
               "qbms_battery_cutoff_voltage"               : int(battery_cutoff_voltage),
               "qbms_battery_max_charging_current"         : int(battery_max_charging_current),
               "qbms_battery_max_discharging_current"      : int(battery_max_discharging_current)
            }
        return QBMS

    def pureQuery(self):
        return True

    def help(self):
        singleton=Singleton()
        return ["This command returns BMS values" ]

    def parameterMandatory(self):
        return False

    def parameterFormat(self):
        return []

    def examples(self):
        return ["cmd/QBMS"]
