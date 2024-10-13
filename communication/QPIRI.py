# Device rating information parameters inquiry

import json
from communication.abstractCode import *



class QPIRI(AbstractCode):

    def send(self,parameter):
        Functions.log("DBG","Sending QPIRI command","QPIRI")
        response=""
        try:
            response=self.singleton.connector.write("QPIRI",105)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"QPIRI")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("k","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"QPIRI")
            grid_rating_voltage,grid_rating_current,ac_output_rating_voltage,ac_output_rating_freq,ac_output_rating_current,ac_output_rating_apparent_power,ac_output_rating_active_power,batt_rating_voltage,batt_recharge_voltage,batt_under_voltage,batt_bulk_voltage,batt_float_voltage,batt_type,max_ac_charging_current,max_charging_current,input_voltage_range,output_source_priority,charger_source_priority,parallel_max_num,machine_type,topology,output_mode,batt_redischarge_voltage,pv_ok_condition_for_parallel,pv_power_balance,max_charging_time_at_cv_stage,operation_logic,max_discharging_current=str(response).split(" ")

            batt_type_raw=int(batt_type)
            if batt_type == "0": batt_type="AGM"
            if batt_type == "1": batt_type="Flooded"
            if batt_type == "2": batt_type="User"
            if batt_type == "3": batt_type="Pylontech"
            if batt_type == "5": batt_type="Weco"
            if batt_type == "6": batt_type="Soltaro"
            if batt_type == "8": batt_type="Lib"
            if batt_type == "9": batt_type="Lic"

            input_voltage_range_raw=int(input_voltage_range)
            if input_voltage_range == "0": input_voltage_range="Appliance"
            if input_voltage_range == "1": input_voltage_range="Ups"

            output_source_priority_raw=int(output_source_priority)
            if output_source_priority == "0": output_source_priority="Utility then Solar then Battery USB"
            if output_source_priority == "1": output_source_priority="Solar then Utility then Battery SUB"
            if output_source_priority == "2": output_source_priority="Solar then Battery then Utility SBU"

            charger_source_priority_raw=int(charger_source_priority)
            if charger_source_priority == "1": charger_source_priority="Solar first"
            if charger_source_priority == "2": charger_source_priority="Solar + Utility"
            if charger_source_priority == "3": charger_source_priority="Only solar permitted"

         
            machine_type_raw=int(machine_type)
            if machine_type == "00": machine_type="Grid tie"
            if machine_type == "01": machine_type="Off grid"
            if machine_type == "10": machine_type="Hybrid"

            topology_raw=int(topology)
            if topology == "0": topology="Transformless"
            if topology == "1": topology="Transformer"

            output_mode_raw=int(output_mode)
            if output_mode == "00": output_mode="Single machine output"
            if output_mode == "01": output_mode="Parallel output"
            if output_mode == "02": output_mode="Phase 1 of 3 output"
            if output_mode == "03": output_mode="Phase 2 of 3 output"
            if output_mode == "04": output_mode="Phase 3 of 3 output"
            if output_mode == "05": output_mode="Phase 1 of 2 output"
            if output_mode == "06": output_mode="Phase 2 of 2 output (120°)"
            if output_mode == "07": output_mode="Phase 2 of 2 output (180°)"

            operation_logic_raw=int(operation_logic)
            if operation_logic_raw == 0: operation_logic=="Automatically"
            if operation_logic_raw == 1: operation_logic=="On-line mode"
            if operation_logic_raw == 2: operation_logic=="ECO mode"
               

            QPIRI={
               "qpiri_grid_rating_voltage"                             : float(grid_rating_voltage),
               "qpiri_grid_rating_current"                             : float(grid_rating_current),
               "qpiri_ac_output_rating_voltage"                        : float(ac_output_rating_voltage),
               "qpiri_ac_output_rating_freq"                           : float(ac_output_rating_freq),
               "qpiri_ac_output_rating_current"                        : float(ac_output_rating_current),
               "qpiri_ac_output_rating_apparent_power"                 : int(ac_output_rating_apparent_power),
               "qpiri_ac_output_rating_active_power"                   : float(ac_output_rating_active_power),
               "qpiri_batt_rating_voltage"                             : float(batt_rating_voltage),
               "qpiri_batt_recharge_voltage"                           : float(batt_recharge_voltage),
               "qpiri_batt_under_voltage"                              : float(batt_under_voltage),
               "qpiri_batt_bulk_voltage"                               : float(batt_bulk_voltage),
               "qpiri_batt_float_voltage"                              : float(batt_float_voltage),
               "qpiri_batt_type_raw"                                   : batt_type_raw,
               "qpiri_batt_type"                                       : batt_type,
               "qpiri_max_ac_charging_current"                         : int(max_ac_charging_current),
               "qpiri_max_charging_current"                            : int(max_charging_current),
               "qpiri_input_voltage_range_raw"                         : input_voltage_range_raw,
               "qpiri_input_voltage_range"                             : input_voltage_range,
               "qpiri_output_source_priority_raw"                      : output_source_priority_raw,
               "qpiri_output_source_priority"                          : output_source_priority,
               "qpiri_charger_source_priority_raw"                     : charger_source_priority_raw,
               "qpiri_charger_source_priority"                         : charger_source_priority,
               "qpiri_parallel_max_num"                                : int(parallel_max_num),
               "qpiri_machine_type_raw"                                : machine_type_raw,
               "qpiri_machine_type"                                    : machine_type,
               "qpiri_topology_raw"                                    : topology_raw,
               "qpiri_topology"                                        : topology,
               "qpiri_output_mode_raw"                                 : output_mode_raw,
               "qpiri_output_mode"                                     : output_mode,
               "qpiri_batt_redischarge_voltage"                        : float(batt_redischarge_voltage),
               "qpiri_pv_ok_condition_for_parallel"                    : int(pv_ok_condition_for_parallel),
               "qpiri_pv_power_balance"                                : int(pv_power_balance),
               "qpiri_max_charging_time_at_cv_stage"                   : int(max_charging_time_at_cv_stage),
               "qpiri_operation_logic_raw"                             : operation_logic_raw,
               "qpiri_operation_logic"                                 : operation_logic,
               "qpiri_max_discharging_current"                         : int(max_discharging_current)
                 }
        except Exception as err:
            Functions.log("ERR","Can't parse QPIRI response " + str(response) + " error was " + str(err),"QPIRI")
            return { 
                      "error" : "Can't parse QPIRI response " + str(response) + " error was " + str(err),
                      "raw_response" : str(response)
                   }
           
        return QPIRI

    def pureQuery(self):
        return True

    def help(self):
        anHelp=[]
        anHelp.append("This command returns rating informations values")
        return anHelp 

    def examples(self):
        return ["cmd/QPIRI"]
