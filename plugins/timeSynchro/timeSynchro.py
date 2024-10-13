from datetime import datetime, timedelta
import os,json
from plugins.abstractPlugin import *
from pathlib import Path
from utils.singleton import Singleton
import math


class timeSynchro(abstractPlugin):

    def runPlugin(self):
        self.checkDrift()
 
    def checkDrift(self):
        singleton=Singleton()
        now=datetime.datetime.now()
        Functions.log("DBG","Date/Hour/Minute now is " + Functions.getDateFormatFromDate(now,"%Y%m%d%H%M"),"timeSynchro")
        Functions.log("DBG","Checking time on inverter","timeSynchro")
        singleton.QT=Functions.command("QT")
        if len(singleton.QT["qt_inverterDate"]) == 12:
            inverterDate = Functions.getDateFormatFromString(singleton.QT["qt_inverterDate"],format="%Y%m%d%H%M")
        elif len(singleton.QT["qt_inverterDate"]) == 14:
            inverterDate = Functions.getDateFormatFromString(singleton.QT["qt_inverterDate"],format="%Y%m%d%H%M%S")
        else:
            Functions.log("WNG","Unrecognized date format, bypass","timeSynchro")
            return
            
        Functions.log("DBG","Time setup inside inverter is " + str(inverterDate),"timeSynchro")
        Functions.log("DBG","Time now is " + str(now),"timeSynchro")
        c = now - inverterDate
        minutes = int(abs(c.total_seconds() / 60))
        Functions.log("DBG","Drift in minutes is " + str(minutes),"timeSynchro")
        # Load conf file
        configFile="plugins/timeSynchro/timeSynchro.json"
        if not Path(configFile).is_file():
            Functions.log("ERR","Config file " + configFile + " doesn't exist please create","timeSynchro")
        else:
            # Parsing the configFile
            Functions.log("DBG","Parsing configFile " + configFile,"timeSynchro")
            try:
                jsonLine=Functions.loadFileInALine(configFile)
                self.parameters=json.loads(jsonLine)
                Functions.log("DBG","Json config file successfully loaded " +  json.dumps(self.parameters,indent=4),"timeSynchro")
                if "enable" in self.parameters and self.parameters["enable"]:
                   maxDriftMinutes=5
                   if "maxDriftMinutes" in self.parameters:
                       maxDriftMinutes=int(self.parameters["maxDriftMinutes"])
                       Functions.log("DBG","Using maxDriftMinutes from config file: " + str(maxDriftMinutes) + "mn","timeSynchro")
                   else:
                       Functions.log("DBG","Using default maxDriftMinutes: " + str(maxDriftMinutes) + "mn","timeSynchro")
                   if minutes > maxDriftMinutes:
                       Functions.log("INF","Drift[" + str(minutes) + "mn] is more than maxDriftMinutes[" + str(maxDriftMinutes) + "mn]" ,"timeSynchro")
                       Functions.log("INF","Setting new date inside inverter" ,"timeSynchro")
                       now=datetime.datetime.now()
                       nowStr=Functions.getDateFormatFromDate(now,"%y%m%d%H%M%S")
                       Functions.command("DAT",aParameter=nowStr)
                   else:
                       Functions.log("DBG","Drift[" + str(minutes) + "mn] is under maxDriftMinutes[" + str(maxDriftMinutes) + "mn]" ,"timeSynchro")
                else:
                   Functions.log("DBG","enable property not found in " + configFile + " or value is false","timeSynchro")
            except Exception as err:
                Functions.log("ERR","Can't parse file " + configFile + " is it a json file ? details " + str(err),"timeSynchro")
        
        

    def influxData(self):
        return None

    def mqttData(self):
        return self.result()

    def result(self):
        return None
