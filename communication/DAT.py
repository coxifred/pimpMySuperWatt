# Device protocol setting Date inside inverter

import json
from communication.abstractCode import *


# Time inquiry
class DAT(AbstractCode):

    def send(self,parameter):
        response=self.singleton.connector.write("DAT"+ parameter,5)
        response=Functions.getFieldFromString(str(response),"\(",1).replace("'","").replace("\r","").replace("?","")[:14]
        Functions.log("DBG","Raw response: " + str(response),"DAT")
        dat={
             "inverterDate" : str(response)
            }
        return dat


    def pureQuery(self):
        return False

    def help(self):
        return ["This command will setup the internal inverter date"]

    def parameterMandatory(self):
        return True

    def parameterFormat(self):
        return ["%y%m%d%H%M%S"]

    def examples(self):
        now=datetime.datetime.now()
        nowStr=Functions.getDateFormatFromDate(now,"%y%m%d%H%M%S")
        return ["cmd/DAT/" + nowStr]
