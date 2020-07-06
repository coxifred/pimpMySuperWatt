import time, sys, socket, argparse, os.path, json, threading
import importlib
from utils.functions import Functions
from os import listdir
from utils.singleton import Singleton



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

    # Setting current hostname
    singleton.hostName=socket.gethostname()

    # Parsing the configFile
    Functions.log("DBG","Parsing configFile " + configFile,"CORE")
    try:
        jsonLine=Functions.loadFileInALine(configFile)
        Functions.log("DBG","Json config reader " + jsonLine,"CORE")
        singleton.parameters=json.loads(jsonLine)
        Functions.log("DBG","Json config file successfully loaded " + str(singleton.parameters),"CORE")
    except Exception as err:
        Functions.log("DEAD","Can't parse file " + configFile + " is it a json file ? details " + str(err),"CORE")

def startDaemons():
    Functions.log("DBG","Start daemons now","CORE")
    singleton=Singleton()
    try:
        singleton.internalScheduler.add_job(poolingRequest, 'interval', seconds=singleton.parameters["queryPoolingInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE")

def poolingRequest():
    Functions.log("DBG","Start pooling request","CORE")
    singleton=Singleton()
    singleton.QPIGS=Functions.command("QPIGS","")
    if not singleton.parameters["influxDbUrls"] == "":
        Functions.log("DBG","Sending now to influxdbs","CORE")
        for db in singleton.parameters["influxDbUrls"]:
            Functions.log("DBG","Sending now to " + db + " database now","CORE")
   
    else:
        Functions.log("DBG","No influxdb target specified","CORE")

    if not singleton.parameters["mqttServers"] == "":
        Functions.log("DBG","Sending now to mqtts","CORE")
        for mqtt in singleton.parameters["mqttServers"]:
            Functions.log("DBG","Sending now to " + mqtt + " server now","CORE")
 
    else:
        Functions.log("DBG","No mqtt target specified","CORE")
     

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
    waitServer.join()

if __name__ == '__main__':
    pimpMySuperWatt()
