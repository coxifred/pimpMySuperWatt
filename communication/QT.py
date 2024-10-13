# Device protocol ID inquiry

import json
from communication.abstractCode import *


# Time inquiry
class QT(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("QT",17)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"QT")
        now=datetime.datetime.now()
        nowStr=Functions.getDateFormatFromDate(now,"%Y%m%d%H%M%S")

        minutes=99999999
        inverterDate=""
        if len(str(response)) == 12:
            inverterDate = Functions.getDateFormatFromString(str(response),format="%Y%m%d%H%M")
            c = now - inverterDate
            minutes = int(abs(c.total_seconds() / 60))
        elif len(str(response)) == 14:
            inverterDate = Functions.getDateFormatFromString(str(response),format="%Y%m%d%H%M%S")
            c = now - inverterDate
            minutes = int(abs(c.total_seconds() / 60))
        else:
            Functions.log("WNG","Unrecognized date format, bypass","QT")

        Functions.log("DBG","Time setup inside inverter is " + str(inverterDate),"QT")
        Functions.log("DBG","Time now is " + str(now),"QT")
        Functions.log("DBG","Drift in minutes is " + str(minutes),"QT")
        qt={
            "qt_inverterDate"   : str(response),
            "qt_currentDate"    : nowStr,
            "qt_driftInMinutes" : minutes
           }
        return qt

    def pureQuery(self):
        return True

    def help(self):
        return ["This command returns the inverter internal date + potential minutes drift against current date"]

    def examples(self):
        return ["cmd/QT"]
