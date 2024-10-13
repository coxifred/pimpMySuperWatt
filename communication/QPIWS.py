# Device Device warningsinquiry

# Computer: QPIWS<CRC>
# Device: a0 a1 a 30 a 31 CRC>
# a0… a35 is the warning status. If the warning is happened, the relevant bit will set 1,
# else the relevant bit will set 0. The following table is the warning code.
# bit  Warning                   Description
# a0   PV loss                   Warning
# a1   Inverter fault            Fault
# a2   Bus Over                  Fault
# a3   Bus Under                 Fault
# a4   Bus Soft Fail             Fault
# a5   LINE_FAIL                 Warning
# a6O  PVShort                   Fault
# a7   Inverter voltage too low  Fault
# a8   Inverter voltage too high Fault
# a9   Over temperature          Compile with a1, if a1=1,fault, otherwise warning
# a10  Fan locked                Compile with a1, if a1=1,fault, otherwise warning
# a11  Battery voltage high      Compile with a1, if a1=1,fault, otherwise warning 
# a12  Battery low alarm         Warning
# a13  Reserved
# a14  Battery under shutdown    Warning
# a15  Battery derating          Warning
# a16  Over load                 Compile with a1, if a1=1,fault, otherwise warning
# a17  Eeprom fault              Warning
# a18  Inverter Over Current     Fault
# a19  Inverter                  Soft Fail Fault
# a20  Self Test Fail            Fault
# a21  OP DC Voltage Over        Fault
# a22  Bat Open                    
# a23  Current Sensor Fail       Fault
# a24  Reserved 
# a25  Reserved
# a26  Reserved
# a27  Reserved
# a28  Reserved
# a29  Reserved
# a30  Reserved
# a31  Battery weak              24V model: a31, a32 is fault code|48V model: a32, a33 is fault code
# a32  Reserved
# a33  Reserved
# a34  Reserved
# a35  Battery equalization      Warning


import json
from communication.abstractCode import *



class QPIWS(AbstractCode):

    def getWarningOrOk(self,bitValue):
        if str(bitValue) == "0":
            return 0
        else:
            return 1

    def getFaultOrOk(self,bitValue):
        if str(bitValue) == "0":
            return 0
        else:
            return 2

    def getFaultOrWarningOrOk(self,bitValue,bitValuea1):
        if str(bitValue) == "0":
            return 0
        elif str(bitValuea1) == "1":
            return 2
        else:
            return 1

    def send(self,parameter):
        Functions.log("DBG","Sending QPIWS command","QPIWS")
        response=""
        QPIWS={}
        try:
            response=self.singleton.connector.write("QPIWS",38)
            Functions.log("DBG","Raw response (before cleaning): " + str(response),"QPIWS")
            tempResponse=str(response)
            response=Functions.getFieldFromString(str(response),"\(",1).replace("'","")
            Functions.log("DBG","Raw response (after cleaning): " + str(response),"QPIWS")
            
            
            for aBit in response:
            
               i=0 
               QPIWS={
               "qpiws"                          : str(response),
               "qpiws_pvLoss"                   : self.getWarningOrOk(response[0]),
               "qpiws_inverterFault"            : self.getFaultOrOk(response[1]),
               "qpiws_busOver"                  : self.getFaultOrOk(response[2]),
               "qpiws_busUnder"                 : self.getFaultOrOk(response[3]),
               "qpiws_busSoftFail"              : self.getFaultOrOk(response[4]),
               "qpiws_lineFail"                 : self.getWarningOrOk(response[5]),
               "qpiws_opvShort"                 : self.getFaultOrOk(response[6]),
               "qpiws_inverterVoltageTooLow"    : self.getFaultOrOk(response[7]),
               "qpiws_inverterVoltageTooHigh"   : self.getFaultOrOk(response[8]),
               "qpiws_overTemperature"          : self.getFaultOrWarningOrOk(response[9],response[1]),
               "qpiws_fanLocked"                : self.getFaultOrWarningOrOk(response[10],response[1]),
               "qpiws_batteryVoltageHigh"       : self.getFaultOrWarningOrOk(response[11],response[1]),
               "qpiws_batteryLowAlarm"          : self.getWarningOrOk(response[12]),
               "qpiws_reservedBit_1"            : int(response[13]),
               "qpiws_batteryUnderShutdown"     : self.getWarningOrOk(response[14]),
               "qpiws_batteryDerating"          : self.getWarningOrOk(response[15]),
               "qpiws_overload"                 : self.getFaultOrWarningOrOk(response[16],response[1]),
               "qpiws_eepromFault"              : self.getWarningOrOk(response[17]),
               "qpiws_inverterOverCurrent"      : self.getFaultOrOk(response[18]),
               "qpiws_inverterSoftFail"         : self.getFaultOrOk(response[19]),
               "qpiws_selfTestFail"             : self.getFaultOrOk(response[20]),
               "qpiws_opDcVoltageOver"          : self.getFaultOrOk(response[21]),
               "qpiws_batOpen"                  : int(response[22]),
               "qpiws_currentSensorFail"        : self.getFaultOrOk(response[23]),
               "qpiws_reservedBit_2"            : int(response[24]),
               "qpiws_reservedBit_3"            : int(response[25]),
               "qpiws_reservedBit_4"            : int(response[26]),
               "qpiws_reservedBit_5"            : int(response[27]),
               "qpiws_reservedBit_6"            : int(response[28]),
               "qpiws_reservedBit_7"            : int(response[29]),
               "qpiws_reservedBit_8"            : int(response[30]),
               "qpiws_batteryWeak"              : self.getFaultOrWarningOrOk(response[32],response[33]),
               "qpiws_reservedBit_9"            : int(response[32]),
               "qpiws_reservedBit_10"           : int(response[33]),
               "qpiws_reservedBit_11"           : int(response[34]),
               "qpiws_batteryEqualization"      : self.getWarningOrOk(response[35])
                
               }
            Functions.log("DBG","Response for a QPIWS command " + json.dumps(QPIWS,indent=4),"QPIWS")
        except Exception as err:
            Functions.log("ERR","Can't parse QPIWS response " + str(response),"QPIWS")
            return {}
           
        return QPIWS

    def pureQuery(self):
        return True
        
    def help(self):
        anHelp=[]
        anHelp.append("Will return the inverter alert status")
        anHelp.append("qpiws")
        anHelp.append("pvLoss")
        anHelp.append("inverterFault")
        anHelp.append("busOver")
        anHelp.append("busUnder")
        anHelp.append("busSoftFail")
        anHelp.append("lineFail")
        anHelp.append("opvShort")
        anHelp.append("inverterVoltageTooLow")
        anHelp.append("inverterVoltageTooHigh")
        anHelp.append("overTemperature")
        anHelp.append("fanLocked")
        anHelp.append("batteryVoltageHigh")
        anHelp.append("batteryLowAlarm")
        anHelp.append("reservedBit_1")
        anHelp.append("batteryUnderShutdown")
        anHelp.append("batteryDerating")
        anHelp.append("overload")
        anHelp.append("eepromFault")
        anHelp.append("inverterOverCurrent")
        anHelp.append("inverterSoftFail")
        anHelp.append("selfTestFail")
        anHelp.append("opDcVoltageOver")
        anHelp.append("batOpen")
        anHelp.append("currentSensorFail")
        anHelp.append("reservedBit_2")
        anHelp.append("reservedBit_3")
        anHelp.append("reservedBit_4")
        anHelp.append("reservedBit_5")
        anHelp.append("reservedBit_6")
        anHelp.append("reservedBit_7")
        anHelp.append("reservedBit_8")
        anHelp.append("batteryWeak")
        anHelp.append("reservedBit_9")
        anHelp.append("reservedBit_10")
        anHelp.append("reservedBit_11")
        anHelp.append("batteryEqualization")
        return anHelp


    def examples(self):
        return ["cmd/QPIWS"]

