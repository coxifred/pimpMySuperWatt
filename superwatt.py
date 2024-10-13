import time, sys, socket, argparse, os.path, json, threading, glob
import importlib
import atexit
import signal
import netifaces
import requests
import paho.mqtt.publish as publish
from utils.functions import Functions
from os import listdir
from utils.singleton import Singleton
from influxdb import InfluxDBClient
from netifaces import interfaces, ifaddresses, AF_INET
from plugins.abstractPlugin import *

externalFile="/tmp/PimpMySuperWatt_EXTCOMMAND.dat"
format="COMMAND:PARAM"


## Parameter reader (from file) and args
def checkParameter(args):
    singleton=Singleton()
    # If debug
    if args.debug:
        Functions.log("INF","Debug activated","CORE.checkParameter")
        singleton.debug=True

    # Populate version
    singleton.version=Functions.kommandShell("git log | head -6")

    # Read configuration file json
    configFile=os.path.abspath(args.configFile)
    if not os.path.isfile(configFile):
        Functions.log("DEAD","File " + str(configFile) + " doesn't exist","CORE.checkParameter")
    Functions.log("INF","Config file exist " + configFile,"CORE.checkParameter")
    singleton.configFile=configFile

    # Setting current hostname & ip
    singleton.hostName=socket.gethostname()
    for ifaceName in interfaces():
          addrs=ifaddresses(ifaceName)
          try:
              for subAdress in addrs[netifaces.AF_INET]:
                  if subAdress["addr"] != "127.0.0.1":
                      Functions.log("DBG","Local ip detected " + str(subAdress["addr"]),"CORE.checkParameter")
                      singleton.ip=str(subAdress["addr"])
          except Exception as err:
              pass

    # Parsing the configFile
    Functions.log("DBG","Parsing configFile " + configFile,"CORE.checkParameter")
    try:
        jsonLine=Functions.loadFileInALine(configFile)
        singleton.parameters=json.loads(jsonLine)
        if "debug" in singleton.parameters:
            singleton.debug=singleton.parameters["debug"]
        Functions.log("DBG","Json config file successfully loaded " +  json.dumps(singleton.parameters,indent=4),"CORE.checkParameter")
    except Exception as err:
        Functions.log("DEAD","Can't parse file " + configFile + " is it a json file ? details " + str(err),"CORE.checkParameter")

    if "queryPoolingInterval" not in singleton.parameters:
        Functions.log("WNG","queryPoolingInterval not set in " + configFile + " using default 60s","CORE.checkParameter")
        singleton.parameters["queryPoolingInterval"]=60

    if "logsPoolingInterval" not in singleton.parameters: 
        Functions.log("WNG","logsPoolingInterval not set in " + configFile + " using default 300s","CORE.checkParameter")
        singleton.parameters["logsPoolingInterval"]=300

    # initialize externalCommand structure
    initExternalCommand()

    # Instanciate plugin
    intanciatePlugins()


def intanciatePlugins():
    singleton=Singleton()
    singleton.plugins=[]
    for file in sorted(glob.glob('plugins/*/*.py')):
        moduleName=os.path.basename(file.replace(".py",""))
        try:
            Functions.log("DBG","Loading plugins/" + moduleName + "/" + moduleName,"CORE.intanciatePlugins")
            mod=importlib.import_module("plugins." + moduleName + "." + moduleName)
            Functions.log("DBG","End loading plugins/" + moduleName + "/" + moduleName ,"CORE.intanciatePlugins")
            Functions.log("DBG","Trying dynamic instantiation " + moduleName ,"CORE.intanciatePlugins")
            aClass = getattr(mod, moduleName)
            instancePlugin = aClass()

            if isinstance(instancePlugin,abstractPlugin):
                Functions.log("DBG","Plugin " + str(instancePlugin.__class__.__name__.upper()) + " is an instance of AbstractPlugin, populating array","CORE.intanciatePlugins")
                singleton.plugins.append(instancePlugin)
            else:
                Functions.log("ERR","Plugin " + moduleName + " isn't an instance of AbstractPlugin did u extend abstractPlugin ?","CORE.intanciatePlugins")
        except Exception as err:
         Functions.log("ERR","Couldn't instantiate " + moduleName + " error " + str(err),"CORE.intanciatePlugins")

def startDaemons():
    Functions.log("DBG","Start daemons now","CORE.startDaemons")
    singleton=Singleton()
    ## Pooling for query power values
    try:
        time.sleep(10)
        Functions.log("DBG","Add poolingRequest job for Energy query to scheduler with " + str(singleton.parameters["queryPoolingInterval"]) + " sec(s) interval","CORE.startDaemons")
        # At least one time for init
        poolingRequest()
        singleton.internalScheduler.add_job(poolingRequest, 'interval', seconds=singleton.parameters["queryPoolingInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE.startDaemons")

    ## Pooling for query logs and 
    try:
        Functions.log("DBG","Add poolingRequest job for Logs/Default/Parameters to scheduler with " + str(singleton.parameters["logsPoolingInterval"]) + " sec(s) interval","CORE.startDaemons")
        # At least one time for init
        logsPoolingRequest()
        singleton.internalScheduler.add_job(logsPoolingRequest, 'interval', seconds=singleton.parameters["logsPoolingInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE.startDaemons")

def startExternalCommands():
    Functions.log("DBG","Start external command now","CORE.startExternalCommands")
    singleton=Singleton()
    try:
        Functions.log("DBG","Add externalCommand job to scheduler with 5 sec(s) interval","CORE.startExternalCommands")
        singleton.internalScheduler.add_job(externalCommand, 'interval', seconds=5)
    except Exception as err:      
        Functions.log("ERR","Error with scheduler " + str(err),"CORE.startExternalCommands")

def startPlugins():
    Functions.log("DBG","Start plugins now","CORE.startPlugins")
    singleton=Singleton()
    try:
        singleton.internalScheduler.add_job(pluginRequest, 'interval', seconds=singleton.parameters["queryPluginInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE.startPlugins")

def startDayStats():
    Functions.log("DBG","Start days stats now","CORE.startDayStats")
    singleton=Singleton()
    try: 
        # Init at least once
        getStatsD()
        getStatsM()
        getStatsY()
        singleton.internalScheduler.add_job(getStatsD, trigger='cron', hour='23', minute='55')
        singleton.internalScheduler.add_job(getStatsM, trigger='cron', month='*', day='last',hour='23', minute='55')
        singleton.internalScheduler.add_job(getStatsY, trigger='cron', month='12', day='last',hour='23', minute='55')
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE.startDayStats")

def getStatsSince():
    singleton=Singleton()
    Functions.log("DBG","Start getStats by querying PV production since started or last reset","CORE.getStatsSince")
    singleton.QET=Functions.command("QET")
    sendStats("qet_since","1970",singleton.QET)


def getStatsM():
    singleton=Singleton()
    dtStr=Functions.getDateFormat('%Y%m')
    Functions.log("DBG","Start getStats by querying month's PV production at month of " + dtStr,"CORE.getStatsM")
    singleton.QEM=Functions.command("QEM",dtStr)
    sendStats("qed_month",dtStr,singleton.QEM)
    

def getStatsY():
    singleton=Singleton()
    dtStr=Functions.getDateFormat('%Y')
    Functions.log("DBG","Start getStats by querying year's PV production at year of " + dtStr,"CORE.getStatsY")
    singleton.QEY=Functions.command("QEY",dtStr)
    sendStats("qed_year",dtStr,singleton.QEY)

def getStatsD():
    singleton=Singleton()
    dtStr=Functions.getDateFormat('%Y%m%d')
    Functions.log("DBG","Start getStats by querying day's PV production at day of " + dtStr,"CORE.getStatsD")
    singleton.QED=Functions.command("QED",dtStr)
    sendStats("qed_day",dtStr,singleton.QED)
    getStatsSince()

def sendStats(tagName,tagValue,fieldValue):
    singleton=Singleton()
    json_body=[
                {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  tagName   : tagValue,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": fieldValue
                }
              ]
    
    Functions.log("DBG",tagName + "(" + tagValue + ") production is " + str(fieldValue) + " sending to influxDb .." , "CORE.sendStats")
    try:
        Functions.timeoutF(sendToInflux(json_body),10)
    except Exception as err:
        Functions.log("ERR","Error when sending json_body to influxdb " + str(err),"CORE.sendStats")

    Functions.log("DBG",tagName + "(" + tagValue + ") production is " + str(fieldValue) + " sending to mqtt .." , "CORE.sendStats")
    try:
        Functions.timeoutF(sendToMqtt(json_body),10)
    except Exception as err:
        Functions.log("ERR","Error when sending json_body to mqtt " + str(err),"CORE.sendStats")

    


def pluginRequest():
    try:
        Functions.log("DBG","Start plugin request","CORE.pluginRequest")
        singleton=Singleton()
        for plugin in singleton.plugins:
           plugin.runPlugin() 
           influxData=plugin.influxData()
           if influxData is not None:
              Functions.timeoutF(sendToInflux(influxData),2)
              Functions.timeoutF(sendToMqtt(influxData),2)
    except Exception as err:
       Functions.log("ERR","Error while requesting pluginRequest error was " + str(err),"CORE.pluginRequest")

def logsPoolingRequest():
    try:
       Functions.log("DBG","Start pooling request for logs/parameters/defaults","CORE.logsPoolingRequest")
       singleton=Singleton()
       singleton.QFLAG=Functions.command("QFLAG","")
       singleton.QMOD=Functions.command("QMOD","")
       print(str(singleton.QMOD))
       singleton.QPIWS=Functions.command("QPIWS","")
    except Exception as err:
       Functions.log("ERR","Error while requesting ogs/parameters/defaults error was " + str(err),"CORE.logsPoolingRequest")

def poolingRequest():
    try:
        json_body=[]
        json_body_parameters=[]
        Functions.log("DBG","Start pooling request for inverter values","CORE.poolingRequest")
        singleton=Singleton()
        singleton.GRIDWATTS={}
        Functions.timeoutF(queryExternalPower(),5)
        singleton.QPIGS=Functions.command("QPIGS","")
        singleton.QPIGS2=Functions.command("QPIGS2","")
        singleton.QPIRI=Functions.command("QPIRI","")
        singleton.QBMS=Functions.command("QBMS","")
        json_body=[
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "array"   : 1,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qmn"     : singleton.QMN,
                                  "qgmn"    : singleton.QGMN,
                                  "qmod"    : singleton.QMOD["qmod_label"],
                                  "qflag"   : singleton.QFLAG["qflag"],
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "qfw3"    : singleton.QVFW3,
                                  "connectionRetry"      : singleton.currentTry,
                                  "maxTry"      : singleton.maxTry,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.QPIGS
                        },
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "array"   : 1,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qmn"     : singleton.QMN,
                                  "qgmn"    : singleton.QGMN,
                                  "qmod"    : singleton.QMOD["qmod_label"],
                                  "qflag"   : singleton.QFLAG["qflag"],
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "qfw3"    : singleton.QVFW3,
                                  "connectionRetry"      : singleton.currentTry,
                                  "maxTry"      : singleton.maxTry,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.GRIDWATTS
                        },
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "array"   : 2,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qmn"     : singleton.QMN,
                                  "qgmn"    : singleton.QGMN,
                                  "qmod"    : singleton.QMOD["qmod_label"],
                                  "qflag"   : singleton.QFLAG["qflag"],
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "qfw3"    : singleton.QVFW3,
                                  "connectionRetry"      : singleton.currentTry,
                                  "maxTry"      : singleton.maxTry,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.QPIGS2
                        },
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "array"   : 2,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qmn"     : singleton.QMN,
                                  "qgmn"    : singleton.QGMN,
                                  "qmod"    : singleton.QMOD["qmod_label"],
                                  "qflag"   : singleton.QFLAG["qflag"],
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "qfw3"    : singleton.QVFW3,
                                  "connectionRetry"      : singleton.currentTry,
                                  "maxTry"      : singleton.maxTry,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.QPIRI
                        },
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "array"   : 2,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qmn"     : singleton.QMN,
                                  "qgmn"    : singleton.QGMN,
                                  "qmod"    : singleton.QMOD["qmod_label"],
                                  "qflag"   : singleton.QFLAG["qflag"],
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "qfw3"    : singleton.QVFW3,
                                  "connectionRetry"      : singleton.currentTry,
                                  "maxTry"      : singleton.maxTry,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.QBMS
                        },
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "array"   : 2,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qmn"     : singleton.QMN,
                                  "qgmn"    : singleton.QGMN,
                                  "qmod"    : singleton.QMOD["qmod_label"],
                                  "qflag"   : singleton.QFLAG["qflag"],
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "qfw3"    : singleton.QVFW3,
                                  "connectionRetry"      : singleton.currentTry,
                                  "maxTry"      : singleton.maxTry,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.QPIWS
                        }

               ]
        json_body_parameters=[
                        {
                         "measurement": "pimpMySuperWatt_Parameters",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                 },
                         "fields": {
                                    "qpi"                  : singleton.QPI,
                                    "qid"                  : singleton.QID,
                                    "qmn"                  : singleton.QMN,
                                    "qgmn"                 : singleton.QGMN,
                                    "qmod"                 : singleton.QMOD["qmod_label"],
                                    "qflag"                : singleton.QFLAG["qflag"],
                                    "qfw"                  : singleton.QVFW,
                                    "qfw2"                 : singleton.QVFW2,
                                    "qfw3"                 : singleton.QVFW3,
                                    "url"                  : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                    "connectionRetry"      : singleton.currentTry,
                                    "maxTry"               : singleton.maxTry,
                                    "instance"             : singleton.parameters["instance"],
                                    "debug"                : singleton.parameters["debug"],
                                    "communicationClass"   : singleton.parameters["communicationClass"],
                                    "portPath"             : singleton.parameters["portPath"],
                                    "webserver"            : singleton.parameters["webserver"],
                                    "webserverDebug"       : singleton.parameters["webserverDebug"],
                                    "webClass"             : singleton.parameters["webClass"],
                                    "httpBind"             : singleton.parameters["httpBind"],
                                    "queryPoolingInterval" : singleton.parameters["queryPoolingInterval"],
                                    "logsPoolingInterval"  : singleton.parameters["logsPoolingInterval"]
                                   }
                        }
               ]
    except Exception as err:
        Functions.log("ERR","Error when requesting or building values " + str(err),"CORE.poolingRequest")

    singleton=Singleton()
    singleton.ready=True
    try:
        Functions.timeoutF(sendToInflux(json_body),5)
    except Exception as err:
        Functions.log("ERR","Error when sending json_body to influxdb " + str(err),"CORE.poolingRequest")

    try:
        Functions.timeoutF(sendToInflux(json_body_parameters),5)
    except Exception as err:
        Functions.log("ERR","Error when sending json_body_parameters to influxdb " + str(err),"CORE.poolingRequest")

    try:
        Functions.timeoutF(sendToMqtt(json_body),5)
    except Exception as err:
        Functions.log("ERR","Error when sending json_body to mqtt " + str(err),"CORE.poolingRequest")

    try:
        Functions.timeoutF(sendToMqtt(json_body_parameters),5)
    except Exception as err:
        Functions.log("ERR","Error when sending json_body_parameters to mqtt " + str(err),"CORE.poolingRequest")

def queryExternalPower():
    singleton=Singleton()
    if "gridWattUrl" in singleton.parameters and singleton.parameters["gridWattUrl"] != "":
       if "gridWattField" in singleton.parameters and singleton.parameters["gridWattField"] != "":
          try:
             Functions.log("DBG","Querying now external to grab watts from GRID " + str(singleton.parameters["gridWattUrl"]),"CORE.queryExternalPower")
             r = requests.get(singleton.parameters["gridWattUrl"])
             try:
                jsonResult=json.loads(r.text)
                try:
                  watts=float(jsonResult[singleton.parameters["gridWattField"]])
                  singleton.GRIDWATTS={
                                        "gridWattUrl"    : singleton.parameters["gridWattUrl"],
                                        "gridWattField"  : singleton.parameters["gridWattField"],
                                        "gridwatts"      : watts
                                      }
                  Functions.log("DBG","Successfully grabbed external GRID watts " + json.dumps(singleton.GRIDWATTS, indent=4),"CORE.queryExternalPower")
                except Exception as err:
                  Functions.log("WNG","When requesting " + str(singleton.parameters["gridWattUrl"]) + " can't extract watt field " + str(singleton.parameters["gridWattField"]) + " error was " + str(err),"CORE.queryExternalPower")
                  Functions.log("WNG","Raw result was  " + str(err),"CORE.queryExternalPower")
             except Exception as err:
               Functions.log("WNG","When requesting " + str(singleton.parameters["gridWattUrl"]) + " can't parse result as json format error was " + str(err),"CORE.queryExternalPower")
               Functions.log("WNG","Raw result was  " + str(err),"CORE.queryExternalPower")
          except Exception as err:
             Functions.log("WNG","Cant' reach " + str(singleton.parameters["gridWattField"]) + " error was " + str(err),"CORE.queryExternalPower")
   
       else:
          Functions.log("WNG","Can't find field gridWattField in superwatt.json","CORE.queryExternalPower")

def sendToMqtt(json_body):
    singleton=Singleton()
    if not singleton.parameters["mqttServers"] == "":
        Functions.log("DBG","Sending now to mqtts","CORE")
        for mqtt in singleton.parameters["mqttServers"]:
            mqttUser=""
            mqttPassword=""
            if "mqttUser" in mqtt:
                mqttUser=mqtt["mqttUser"]
            if "mqttPassword" in mqtt:
                mqttPassword=mqtt["mqttPassword"]
            Functions.log("DBG","Sending now to " + mqtt["mqttServer"] + ":" + str(mqtt["mqttServerPort"]) + " server now","CORE")
            if mqttUser == "":
                publish.single(topic=mqtt["mqttTopic"],payload=json.dumps(json_body), hostname=mqtt["mqttServer"], port=mqtt["mqttServerPort"])
            else:
                publish.single(topic=mqtt["mqttTopic"],payload=json.dumps(json_body), hostname=mqtt["mqttServer"], port=mqtt["mqttServerPort"],auth={'username': mqttUser, 'password': mqttPassword})
    else:
        Functions.log("DBG","No mqtt target specified","CORE")
    Functions.log("DBG","End sending now to mqtts","CORE")

def sendToInflux(json_body):
    singleton=Singleton()
    if not singleton.parameters["influxDbUrls"] == "":
        Functions.log("DBG","Sending now to influxdbs","CORE.sendToInflux")
        for db in singleton.parameters["influxDbUrls"]:
            Functions.log("DBG","Sending now to " + db["dbHost"] + " database now","CORE.sendToInflux")
            dbUser=db["username"]
            dbPassword=db["password"]
            dbHost=db["dbHost"]
            dbPort=db["dbPort"]
            dbName=db["dbName"]
            Functions.log("DBG","Sending data to " + dbHost + ":" + dbPort + " user: " + dbUser + " password: " + dbPassword + " database: " + dbName,"CORE.sendToInflux")
            client = InfluxDBClient(dbHost, dbPort, dbUser, dbPassword, dbName)
            try:
               client.create_database(dbName)
            except:
               pass
            # Transforming json to line format (more performance)
            #linePoints=Functions.make_lines(data=json_body[0],precision="s")
            #client.write_points(data, database=dbName, time_precision='ms', batch_size=10000, protocol='line')
            try:
                Functions.log("DBG","Sending : " + str(json_body) + " to influxdb", "CORE.sendToInflux")
                client.write_points(json_body)
                Functions.log("DBG","Data successfully sent to influxdb " + dbHost + ":" + dbPort + " user: " + dbUser + " password: " + dbPassword + " database: " + dbName,"CORE.sendToInflux")
            except Exception as err:
                Functions.log("ERR","Can't send correctly to influxDb, error was " + str(err),"CORE.sendToInflux")
            finally:
                client.close()

            
    else:
        Functions.log("DBG","No influxdb target specified","CORE")
     
    Functions.log("DBG","End sending now to influx","CORE")

def startConnector():
    singleton=Singleton()
    Functions.log("DBG","Start connector now","CORE")
    # Ok let's start with connector checking
    importlib.import_module('communication')
    singleton.maxTry=40
    singleton.currentTry=1
    singleton.communicationStatus="DOWN"
    
    while singleton.currentTry <= singleton.maxTry:
        singleton.communicationStatus="CONNECTING"
        Functions.log("DBG","Trying instanciation of " + str(singleton.parameters["communicationClass"]),"CORE")
        if not singleton.parameters["communicationClass"] == "":
            try:
                Functions.log("DBG","Importing module communicationClass " + str(singleton.parameters["communicationClass"]),"CORE")
                modCom=importlib.import_module('.' + singleton.parameters["communicationClass"],package="communication")
                Functions.log("DBG","Retrieving class object " + str(singleton.parameters["communicationClass"]),"CORE")
                aConnectorClass = getattr(modCom, singleton.parameters["communicationClass"])
                #if singleton.connector is None:
                singleton.connector=aConnectorClass()
                #else:
                    #if singleton.connector.stop:
                    #    break
                if singleton.connector.connected:
                    singleton.communicationStatus="CONNECTED"
                    Functions.log("DBG","Launching QPI command","CORE")
                    singleton.QPI=Functions.command("QPI","")
                    Functions.log("DBG","Launching QID command","CORE")
                    singleton.QID=Functions.command("QID","")
                    Functions.log("DBG","Launching QMN command","CORE")
                    singleton.QMN=Functions.command("QMN","")
                    Functions.log("DBG","Launching QGMN command","CORE")
                    singleton.QGMN=Functions.command("QGMN","")
                    Functions.log("DBG","Launching QVFW command","CORE")
                    singleton.QVFW=Functions.command("QVFW","")
                    Functions.log("DBG","Launching QVFW2 command","CORE")
                    singleton.QVFW2=Functions.command("QVFW2","")
                    Functions.log("DBG","Launching QVFW3 command","CORE")
                    singleton.QVFW3=Functions.command("QVFW3","")
                    Functions.log("DBG","Launching QT command","CORE")
                    singleton.QT=Functions.command("QT","")
                    Functions.log("DBG","Serial connector started.","CORE")
                    break
                countSec=singleton.currentTry * 10
            except Exception as err:
                Functions.log("ERR","Connector exception " + str(err),"CORE")
            countSec=singleton.currentTry * 2
            Functions.log("ERR","Try " + str(singleton.currentTry) + "/" + str(singleton.maxTry) +" will retry in " + str(countSec) + " secs","CORE")
            singleton.currentTry=singleton.currentTry + 1
            time.sleep(countSec)
    else:
        Functions.log("DBG","No serial connector defined.","CORE")

def startWeb():
    singleton=Singleton()
    # Ok now check if we webserver is asked
    if singleton.parameters["webserver"] :
        Functions.log("DBG","Webserver is asked, starting it","CORE")
        importlib.import_module('web')
        Functions.log("DBG","Trying instanciation of " + str(singleton.parameters["webClass"]),"CORE")
        mod=importlib.import_module('.' + singleton.parameters["webClass"],package="web")
        aSiteClass = getattr(mod, singleton.parameters["webClass"])
        singleton.instanceWebApp=aSiteClass()
    else:
        Functions.log("DBG","Webserver not asked","CORE")

def initExternalCommand():
    singleton=Singleton()
    singleton.lastExternalCommand={}
    singleton.lastExternalCommand["command"]=""
    singleton.lastExternalCommand["parameter"]=""
    singleton.lastExternalCommand["result"]=""
    singleton.lastExternalCommand["returnCode"]=0
    singleton.lastExternalCommand["info"]="External Command can be dropped into " + externalFile + " file with format " + format

def externalCommand():
    global externalFile
    global format
    if os.path.isfile(externalFile):
       Functions.log("DBG","External command file [" + externalFile + "] is present, trying to read it..","CORE")
       try:
          initExternalCommand()
          fileLines=Functions.loadFileInArray(externalFile)
          Functions.log("DBG","Deleting file " + externalFile + " now","CORE")
          try:
             os.remove(externalFile)
             if os.path.isfile(externalFile):
                singleton.lastExternalCommand["result"]="Can't delete file " + externalFile
                singleton.lastExternalCommand["returnCode"]=1
                Functions.log("ERR","Can't delete file " + externalFile,"CORE")
                return
          except Exception as err:
             singleton.lastExternalCommand["result"]="Can't delete file " + externalFile
             singleton.lastExternalCommand["returnCode"]=1
             Functions.log("ERR","Can't delete file " + externalFile + " error was " + str(err),"CORE")
             return

          if len(fileLines) > 0:
             Functions.log("DBG",str(len(fileLines)) + " command(s) loaded from " + externalFile,"CORE")
             for fileContent in fileLines:
                Functions.log("DBG","Analysing line " + fileContent,"CORE")
                try:
                   command=Functions.getFieldFromString(fileContent,":",0)
                   singleton.lastExternalCommand["command"]=command
                   if command != "":
                      Functions.log("DBG","Detected command is " + str(command),"CORE")
                      try:
                         parameter=Functions.getFieldFromString(fileContent,":",1)
                         singleton.lastExternalCommand=command + ":" + str(parameter)  + " (External Command can be dropped into " + externalFile + " with format " + format + ")"
                         Functions.log("DBG","Detected parameter is " + str(parameter),"CORE")
                         Functions.log("DBG","Running command " + command + parameter,"CORE")
                         result=Functions.command(command,parameter)
                         Functions.log("DBG","Result of command " + command + parameter + " is " + str(result) ,"CORE")
                         singleton.lastExternalCommand=command + ":" + str(parameter)  + " (External Command can be dropped into " + externalFile + " with format " + format + ")"
                         singleton.lastExternalCommandResult=str(result)
                         singleton.lastExternalCommand["returnCode"]=0
                      except Exception as err:
                         singleton.lastExternalCommand["returnCode"]=1
                         singleton.lastExternalCommand["result"]="Can't extract PARAM, remember format " + format  + " error was " + str(err)
                         Functions.log("ERR","Can't extract PARAM, remember format " + format,"CORE")
                   else:
                       singleton.lastExternalCommand["result"]="Can't extract PARAM, remember format " + format 
                       singleton.lastExternalCommand["returnCode"]=1
                       Functions.log("ERR","Can't extract COMMAND, remember format " + format,"CORE")
                except Exception as err:
                   singleton.lastExternalCommand["result"]="Can't extract PARAM, remember format " + format + " error was " + str(err)
                   singleton.lastExternalCommand["returnCode"]=1
                   Functions.log("ERR","Can't extract COMMAND, remember format " + format,"CORE")
          else:
              singleton.lastExternalCommand["result"]="File content is empty, remember format " + format + " error was " + str(err)
              singleton.lastExternalCommand["returnCode"]=1
              Functions.log("ERR","File content is empty, remember format " + format,"CORE")
       except Exception as err:
          singleton.lastExternalCommand["result"]="Can't read file correctly,"  + " error was " + str(err)
          singleton.lastExternalCommand["returnCode"]=1
          Functions.log("ERR","Can't read file correctly, error was : " + str(err),"CORE")
    else:
       Functions.log("DBG","No command file to execute : " + str(externalFile) + " remember format " + format,"CORE")
        

def waitEnd():
    while True:
         Functions.log("INF","PimpMySuperWatt still alive (Activate debug in configuration file for more verbosity)","CORE")
         time.sleep(120)
         global stop_threads
         if stop_threads:
            break


## start
def pimpMySuperWatt():
    Functions.log("DBG","Instanciate Singleton","CORE")
    singleton=Singleton()
    Functions.log("INF","Starting PimpMySuperWatts on " + socket.gethostname(),"CORE")
    Functions.log("INF","Analysing arguments","CORE")
    parser = argparse.ArgumentParser()
    parser.add_argument("--configFile",help="The absolute path to the configuration file (pimpMySuperWatt.py)")
    parser.add_argument("--debug",help="Debug mode, more verbosity",action="store_true")
    args = parser.parse_args()
    
    checkParameter(args)

    # Connector communication starting
    waitConnector=threading.Thread(target=startConnector,name="connector")
    waitConnector.start()
    singleton.waitConnector=waitConnector

    # Web starting
    waitServer=threading.Thread(target=startWeb,name="webServer")
    waitServer.start()
    singleton.waitServer=waitServer

    waitThread=threading.Thread(target=waitEnd,name="heartbeat")
    waitThread.start() 
    singleton.waitThread=waitThread

    Functions.log("INF","","CORE")
    Functions.log("INF","********************************************************************","CORE")
    Functions.log("INF","*                                                                  *","CORE")
    Functions.log("INF","*              WAIT AT LEAST 1MN FOR USB CONNECTION                *","CORE")
    Functions.log("INF","*                                                                  *","CORE")
    Functions.log("INF","********************************************************************","CORE")
    Functions.log("INF","","CORE")
    global externalFile
    global format
    Functions.log("INF"," o You can submit a command externally by creating a file " + externalFile + " format is " + str(format) + "(1 line per command)","CORE")
    Functions.log("INF","","CORE")


    while True:
        try:
            if not singleton.connector.connected: 
               Functions.log("DBG","Waiting for connector " + singleton.connector.device + " initialization... recheck in 2secs","CORE")
            else:
               Functions.log("DBG","Connector " + singleton.connector.device + " seems ready, let's go.","CORE")
               break
        except Exception as err:
            pass
        time.sleep(2)

    startDaemons()
    startExternalCommands()
    startPlugins()
    startDayStats()
    waitServer.join()


def kill_handler(*args):
    Functions.log("INF","Kill_handler call " + str(args),"CORE.kill_handler")
    #exit_handler()

def exit_handler():
    Functions.log("INF","Cleaning stuff..","CORE")
    singleton=Singleton()
    try:
       Functions.log("INF","Cleanup internal scheduler","CORE")
       singleton.internalScheduler.shutdown(wait=False)
    except Exception as err:
       pass
    try:
       Functions.log("INF","Cleanup internal connector","CORE")
       if singleton.connector is not None:
           singleton.connector.stop=True
           singleton.connector.cleanUp()
    except Exception as err:
       print(str(err))
       pass
    try:
       Functions.log("INF","Cleanup internal waitThread","CORE")
       stop_threads=True
    except Exception as err:
       print(str(err))
       pass
    Functions.log("INF","Cleaning done, exit now","CORE")

    sys.exit(1)

if __name__ == '__main__':
    # Exit handlers
    #atexit.register(exit_handler)
    signal.signal(signal.SIGINT, kill_handler)
    signal.signal(signal.SIGTERM, kill_handler)
    stop_threads=False
    pimpMySuperWatt()
