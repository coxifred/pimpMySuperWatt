import time, sys, socket, argparse, os.path, json
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
        Functions.log("DBG","Json config file successfully loaded","CORE")
    except Exception as err:
        Functions.log("DEAD","Can't parse file " + configFile + " is it a json file ? details " + str(err),"CORE")
	

	
	

	

## Main start
def main():
    Functions.log("INF","Instanciate Singleton","CORE")
    singleton=Singleton()
    Functions.log("INF","Starting PimpMySuperWatts on " + socket.gethostname(),"CORE")
    Functions.log("INF","Analysing arguments","CORE")
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile",help="The absolute path to the configuration file (pimpMySuperWatt.py)")
    parser.add_argument("--debug",help="Debug mode, more verbosity",action="store_true")
    args = parser.parse_args()
    checkParameter(args)


if __name__ == '__main__':
    main()
