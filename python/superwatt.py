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



def startConnector():
    singleton=Singleton()
    Functions.log("DBG","Start connector now","CORE")
    # Ok let's start with connector checking
    importlib.import_module('communication')
    Functions.log("DBG","Trying instanciation of " + str(singleton.parameters["communicationClass"]),"CORE")
    if not singleton.parameters["communicationClass"] == "":
        modCom=importlib.import_module('.' + singleton.parameters["communicationClass"],package="communication")
        aConnectorClass = getattr(modCom, singleton.parameters["communicationClass"])
        singleton.connector=aConnectorClass()
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
    waitServer.join()

if __name__ == '__main__':
    pimpMySuperWatt()
