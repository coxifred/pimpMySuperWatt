import time, sys, socket, argparse, os.path, json, threading, glob
import importlib
import netifaces
import paho.mqtt.publish as publish
from utils.functions import Functions
from os import listdir
from utils.singleton import Singleton
from influxdb import InfluxDBClient
from netifaces import interfaces, ifaddresses, AF_INET
from plugins.abstractPlugin import *



## Parameter reader (from file) and args
def checkParameter(args):
    singleton=Singleton()
    # If debug
    if args.debug:
        Functions.log("INF","Debug activated","CORE")
        singleton.debug=True

    # Populate version
    singleton.version=Functions.kommandShell("git log | head -6")

    # Read configuration file json
    configFile=os.path.abspath(args.configFile)
    if not os.path.isfile(configFile):
        Functions.log("DEAD","File " + str(configFile) + " doesn't exist","CORE")
    Functions.log("INF","Config file exist " + configFile,"CORE")
    singleton.configFile=configFile

    # Setting current hostname & ip
    singleton.hostName=socket.gethostname()
    for ifaceName in interfaces():
          addrs=ifaddresses(ifaceName)
          try:
              for subAdress in addrs[netifaces.AF_INET]:
                  if subAdress["addr"] != "127.0.0.1":
                      Functions.log("INF","Local ip detected " + str(subAdress["addr"]),"CORE")
                      singleton.ip=str(subAdress["addr"])
          except Exception as err:
              Functions.log("WNG","Error while trying to detect local ip " + str(err),"CORE")
              pass

    # Parsing the configFile
    Functions.log("DBG","Parsing configFile " + configFile,"CORE")
    try:
        jsonLine=Functions.loadFileInALine(configFile)
        singleton.parameters=json.loads(jsonLine)
        Functions.log("DBG","Json config file successfully loaded " +  json.dumps(singleton.parameters,indent=4),"CORE")
    except Exception as err:
        Functions.log("DEAD","Can't parse file " + configFile + " is it a json file ? details " + str(err),"CORE")

    # Instanciate plugin
    intanciatePlugins()


def intanciatePlugins():
    singleton=Singleton()
    singleton.plugins=[]
    for file in sorted(glob.glob('plugins/*/*.py')):
        moduleName=os.path.basename(file.replace(".py",""))
        try:
            Functions.log("DBG","Loading plugins/" + moduleName + "/" + moduleName,"CORE")
            mod=importlib.import_module("plugins." + moduleName + "." + moduleName)
            Functions.log("DBG","End loading plugins/" + moduleName + "/" + moduleName ,"CORE")
            Functions.log("DBG","Trying dynamic instantiation " + moduleName ,"CORE")
            aClass = getattr(mod, moduleName)
            instancePlugin = aClass()

            if isinstance(instancePlugin,abstractPlugin):
                Functions.log("DBG","Plugin " + str(instancePlugin.__class__.__name__.upper()) + " is an instance of AbstractPlugin, populating array","CORE")
                singleton.plugins.append(instancePlugin)
            else:
                Functions.log("ERR","Plugin " + moduleName + " isn't an instance of AbstractPlugin did u extend abstractPlugin ?","CORE")
        except Exception as err:
         Functions.log("ERR","Couldn't instantiate " + moduleName + " error " + str(err),"CORE")

def startDaemons():
    Functions.log("DBG","Start daemons now","CORE")
    singleton=Singleton()
    try:
        singleton.internalScheduler.add_job(poolingRequest, 'interval', seconds=singleton.parameters["queryPoolingInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE")

def startPlugins():
    Functions.log("DBG","Start plugins now","CORE")
    singleton=Singleton()
    try:
        singleton.internalScheduler.add_job(pluginRequest, 'interval', seconds=singleton.parameters["queryPluginInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE")

def pluginRequest():
    Functions.log("DBG","Start plugin request","CORE")
    singleton=Singleton()
    for plugin in singleton.plugins:
        plugin.runPlugin() 
        influxData=plugin.influxData()
        sendToInflux(influxData)
        sendToMqtt(influxData)

def poolingRequest():
    Functions.log("DBG","Start pooling request","CORE")
    singleton=Singleton()
    singleton.QPIGS=Functions.command("QPIGS","")
    json_body=[
                        {
                         "measurement": "pimpMySuperWatt",
                         "tags": {
                                  "hostname": singleton.hostName,
                                  "version" : singleton.version,
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                                  "url"     : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                  "instance": singleton.parameters["instance"]
                                 },
                         "fields": singleton.QPIGS
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
                                    "qfw"                  : singleton.QVFW,
                                    "qfw2"                 : singleton.QVFW2,
                                    "url"                  : "http://" + singleton.ip + ":" + str(singleton.parameters["httpPort"]),
                                    "instance"             : singleton.parameters["instance"],
                                    "debug"                : singleton.parameters["debug"],
                                    "communicationClass"   : singleton.parameters["communicationClass"],
                                    "portPath"             : singleton.parameters["portPath"],
                                    "webserver"            : singleton.parameters["webserver"],
                                    "webserverDebug"       : singleton.parameters["webserverDebug"],
                                    "webClass"             : singleton.parameters["webClass"],
                                    "httpBind"             : singleton.parameters["httpBind"],
                                    "queryPoolingInterval" : singleton.parameters["queryPoolingInterval"]
                                   }
                        }
               ]
    sendToInflux(json_body)
    sendToInflux(json_body_parameters)

    sendToMqtt(json_body)
    sendToMqtt(json_body_parameters)


def sendToMqtt(json_body):
    singleton=Singleton()
    if not singleton.parameters["mqttServers"] == "":
        Functions.log("DBG","Sending now to mqtts","CORE")
        for mqtt in singleton.parameters["mqttServers"]:
            Functions.log("DBG","Sending now to " + mqtt["mqttServer"] + ":" + str(mqtt["mqttServerPort"]) + " server now","CORE")
            publish.single(topic=mqtt["mqttTopic"],payload=json.dumps(json_body), hostname=mqtt["mqttServer"], port=mqtt["mqttServerPort"])
    else:
        Functions.log("DBG","No mqtt target specified","CORE")

def sendToInflux(json_body):
    singleton=Singleton()
    if not singleton.parameters["influxDbUrls"] == "":
        Functions.log("DBG","Sending now to influxdbs","CORE")
        for db in singleton.parameters["influxDbUrls"]:
            Functions.log("DBG","Sending now to " + db["dbHost"] + " database now","CORE")
            dbUser=db["username"]
            dbPassword=db["password"]
            dbHost=db["dbHost"]
            dbPort=db["dbPort"]
            dbName=db["dbName"]
            Functions.log("DBG","Sending data to " + dbHost + ":" + dbPort + " user: " + dbUser + " password: " + dbPassword + " database: " + dbName,"CORE")
            client = InfluxDBClient(dbHost, dbPort, dbUser, dbPassword, dbName)
            client.create_database(dbName)
            client.write_points(json_body)
    else:
        Functions.log("DBG","No influxdb target specified","CORE")
     

def startConnector():
    singleton=Singleton()
    Functions.log("DBG","Start connector now","CORE")
    # Ok let's start with connector checking
    importlib.import_module('communication')
    Functions.log("DBG","Trying instanciation of " + str(singleton.parameters["communicationClass"]),"CORE")
    if not singleton.parameters["communicationClass"] == "":
        try:
            Functions.log("DBG","Importing module communicationClass " + str(singleton.parameters["communicationClass"]),"CORE")
            modCom=importlib.import_module('.' + singleton.parameters["communicationClass"],package="communication")
            Functions.log("DBG","Retrieving class object " + str(singleton.parameters["communicationClass"]),"CORE")
            aConnectorClass = getattr(modCom, singleton.parameters["communicationClass"])
            singleton.connector=aConnectorClass()
            Functions.log("DBG","Launching QPI command","CORE")
            singleton.QPI=Functions.command("QPI","")
            Functions.log("DBG","Launching QID command","CORE")
            singleton.QID=Functions.command("QID","")
            Functions.log("DBG","Launching QVFW command","CORE")
            singleton.QVFW=Functions.command("QVFW","")
            Functions.log("DBG","Launching QVFW2 command","CORE")
            singleton.QVFW2=Functions.command("QVFW2","")
        except Exception as err:
            Functions.log("ERR","Connector exception " + str(err),"CORE")
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


def waitEnd():
    while True:
         Functions.log("DBG","PimpMySuperWatt still alive","CORE")
         time.sleep(2)


## start
def pimpMySuperWatt():
    Functions.log("INF","Instanciate Singleton","CORE")
    singleton=Singleton()
    Functions.log("INF","Starting PimpMySuperWatts on " + socket.gethostname(),"CORE")
    Functions.log("INF","Analysing arguments","CORE")
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile",help="The absolute path to the configuration file (pimpMySuperWatt.py)")
    parser.add_argument("--debug",help="Debug mode, more verbosity",action="store_true")
    args = parser.parse_args()
    
    checkParameter(args)

    # Web starting
    waitServer=threading.Thread(target=startWeb)
    waitServer.start()

    # Connector communication starting
    waitConnector=threading.Thread(target=startConnector)
    waitConnector.start()
    
    waitThread=threading.Thread(target=waitEnd)
    waitThread.start()

    startDaemons()
    startPlugins()
    waitServer.join()

if __name__ == '__main__':
    pimpMySuperWatt()
