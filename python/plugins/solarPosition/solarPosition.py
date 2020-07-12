from datetime import datetime, timedelta
import os,json
from plugins.abstractPlugin import *
from pathlib import Path


class solarPosition(abstractPlugin):

    def runPlugin(self):
        self.generateFile()
        self.extract()
 
    def extract(self):
        day=int(Functions.getDateFormat("%d"))
        month=int(Functions.getDateFormat("%m"))
        hour=int(Functions.getDateFormat("%H"))
        minute=self.roundMinute(Functions.getDateFormat("%M"))
        Functions.log("DBG","Today we are " + str(day) + "/" + str(month) + " " + str(hour) + ":" + str(minute) + " looking inside data file to retrieve zenith and azimuth","solarPosition")
        line=Functions.getFirstMatchReInArray("^" + str(day) +"/" + str(month) + ".*" + str(hour) + ":" + str(minute) +".*",self.data)
        Functions.log("DBG","Line retrieved: " + line,"solarPosition")
        self.zenith=float(Functions.getFieldFromString(line,";",1))
        self.azimuth=float(Functions.getFieldFromString(line,";",2))
        Functions.log("DBG","For today, zenith is " + str(self.zenith) + " azimuth is " + str(self.azimuth),"solarPosition")

    def roundMinute(self,minute):
        minute=int(float(minute)/15)
        minute=15*minute
        return minute

    def influxData(self):
        return self.result()

    def mqttData(self):
        return self.result()

    def result(self):
        return [
                        {
                         "measurement": "pimpMySuperWatt_plugin_solarPosition",
                         "tags": {
                                  "hostname": self.singleton.hostName,
                                  "version" : self.singleton.version,
                                  "qpi"     : self.singleton.QPI,
                                  "qid"     : self.singleton.QID,
                                  "qfw"     : self.singleton.QVFW,
                                  "qfw2"    : self.singleton.QVFW2,
                                  "url"     : "http://" + self.singleton.ip + ":" + str(self.singleton.parameters["httpPort"]),
                                  "instance": self.singleton.parameters["instance"],
                                  "latitude" : self.parameters["latitude"],
                                  "longitude" : self.parameters["longitude"],
                                 },
                         "fields":
                                  {
                                   "latitude" : self.parameters["latitude"],
                                   "longitude" : self.parameters["longitude"],
                                   "zenith" : self.zenith,
                                   "azimuth" : self.azimuth
                                  }
                        }
               ]

    def generateFile(self):
        configFile="plugins/solarPosition/solarPosition.json"
        dataFile="plugins/solarPosition/solarPosition.dat"
        if not Path(configFile).is_file():
            Functions.log("ERR","Config file " + configFile + " doesn't exist please create","solarPosition")
        else:
        
            # Parsing the configFile
            Functions.log("DBG","Parsing configFile " + configFile,"solarPosition")
            try:
                jsonLine=Functions.loadFileInALine(configFile)
                self.parameters=json.loads(jsonLine)
                Functions.log("DBG","Json config file successfully loaded " +  json.dumps(self.parameters,indent=4),"solarPosition")
            except Exception as err:
                Functions.log("DEAD","Can't parse file " + configFile + " is it a json file ? details " + str(err),"solarPosition")

            Functions.log("DBG","Retrieve latitude : " + str(self.parameters["latitude"]),"solarPosition")
            Functions.log("DBG","Retrieve longitude : " + str(self.parameters["longitude"]),"solarPosition")
            Functions.log("DBG","Retrieve dst : " + str(self.parameters["dst"]),"solarPosition")

            if not Path(dataFile).is_file():
                Functions.log("INF","Data file " + dataFile + " doesn't exist,trying to create...","solarPosition")
                solartopo="http://www.solartopo.com/services/solarOrbit.php?lat=" + str(self.parameters["latitude"]) + "&long=" + str(self.parameters["longitude"]) + "&dst=" + str(self.parameters["dst"]) 
            
                date=Functions.getDateFormatFromString("20200101000000","default")
                for i in range(0,364):
                    Functions.log("DBG","Date is : " + str(date),"solarPosition")
                    aDay=int(Functions.getDateFormatFromDate(date,"%d"))
                    aMonth=int(Functions.getDateFormatFromDate(date,"%m"))
                    aYear=int(Functions.getDateFormatFromDate(date,"%Y"))
                    aDate=str(aDay) + "-" + str(aMonth) + "-" + str(aYear)
                    Functions.log("DBG","Retrieve informations from " + solartopo + "&date=" + aDate,"solarPosition")
                    data=Functions.requestHttp(solartopo + "&date=" + aDate)
                    fixData=[]
                    for line in data:
                        fixData.append(str(aDay) +"/" + str(aMonth) + " " + line)
                    Functions.writeArrayInAFileAppend("plugins/solarPosition/solarPosition.dat",fixData)
                    date=date + datetime.timedelta(1)
                    i=i+1
            Functions.log("DBG","Loading file " + "plugins/solarPosition/solarPosition.dat","solarPosition")
            self.data=Functions.loadFileInArray("plugins/solarPosition/solarPosition.dat")
