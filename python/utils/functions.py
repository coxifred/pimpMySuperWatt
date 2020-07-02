import datetime
import subprocess
import re
import sys
import threading
import hashlib
import requests
import warnings
import json
from utils.singleton import Singleton
 
 
 
class Functions:
 
        @staticmethod
        def log(level, message, source):
                date = str(datetime.datetime.now())
                singleton=Singleton()
                aLog=date + " " + "[" + threading.current_thread().name + "] " + level + " " + source + " " + message
                if ( level == "DBG" ):
                        if singleton.debug:
                                Functions.logdebug()
                                print(aLog)
                elif ( level == "ERR" or level == "WNG" or level == "DEAD" ):
                        Functions.logred()
                        print(aLog,end='')
                        Functions.lognormal()
                elif ( level == "ASK" ):
                        Functions.logyellow()
                        print(aLog)
                else:
                        Functions.lognormal()
                        print(aLog)
                if ( level == "DEAD" ):
                        sys.exit(1)
                singleton.logs.append(aLog)
 
        @staticmethod
        def logred():
                sys.stdout.write("\033[1;37;41m")
 
        @staticmethod
        def logyellow():
                sys.stdout.write("\033[1;33;40m")
 
        @staticmethod
        def lognormal():
                sys.stdout.write("\033[1;37;40m")
 
        @staticmethod
        def logdebug():
                sys.stdout.write("\033[1;36;40m")
 
        @staticmethod
        def requestHttp(request):
                Functions.log("DBG","HttpRequest: " + request,"Functions")
                requests.packages.urllib3.disable_warnings()
                r = requests.get(request, verify=False)
                Functions.log("DBG","Response code: " + str(r.status_code),"Functions")
                if r.status_code is 200:
                        body = r.content
                        array=body.split("\n")
                        while '' in array:
                                array.pop(array.index(''))
                        return array
                else:
                        Functions.log("ERR","Error while request " + str(r.text),"Functions")
                        raise Exception('Error while request')
 
        @staticmethod
        def getFieldFromString(string,delimiter,fieldNumber):
                return re.split(delimiter,string)[fieldNumber]
 
        @staticmethod
        def getFromFieldFromString(string,delimiter,fieldNumber):
                tab=re.split(delimiter,string);
                return tab[fieldNumber:]
 
        @staticmethod
        def getFirstMatchInAFile(string,file):
                with open(file, "r") as f:
                        for line in f.readlines():
                                if string in line:
                                        f.close()
                                        return(line.rstrip('\n'))
 
        @staticmethod
        def getFirstMatchInArray(string,array):
                for line in array:
                        if string in line:
                                return(line.rstrip('\n'))
        @staticmethod
        def getLastMatchInArray(string,array):
                returnLine=""
                for line in array:
                        if string in line:
                                returnLine=line
                return returnLine
 
        @staticmethod
        def getLastMatchReInArray(regexp,array):
                returnLine=""
                for line in array:
                        if re.match(regexp, line) is not None:
                                returnLine=line
                return returnLine
 
        @staticmethod
        def getFirstMatchInLine(string,line):
                array=line.split("\n")
                return Functions.getFirstMatchInArray(string,array).rstrip('\n')
 
        @staticmethod
        def displayFromLastSeenPatternFromArray(string,array):
                returnArray=[]
                for line in array:
                        if string in line:
                                del returnArray[:]
                                returnArray.append(line)
                        else:
                                returnArray.append(line)
                return returnArray
 
        @staticmethod
        def getLastMatchInLine(string,line):
                array=line.split("\n")
                return Functions.getLastMatchInArray(string,array).rstrip('\n')
 
        @staticmethod
        def kommandShell(aKommand):
                return_output=subprocess.check_output(aKommand,shell=True).decode('utf-8').rstrip('\n')
                return return_output
 
        @staticmethod
        def kommandShellInArray(aKommand):
                return_output=Functions.kommandShell(aKommand).split('\n')
                return return_output
 
        @staticmethod
        def getDateFormat(format):
                if format == "default":
                        format='%Y%m%d%H%M%S'
                return datetime.datetime.now().strftime(format)
 
        @staticmethod
        def getDateFormatFromDate(date,format):
                if format == "default":
                        format='%Y%m%d%H%M%S'
                return date.datetime.strftime(format)
 
        @staticmethod
        def getDateFormatFromString(stringDate,format):
                if format == "default":
                        format='%Y%m%d%H%M%S'
                return datetime.datetime.strptime(stringDate,format)
 
        @staticmethod
        def loadFileInALine(file):
                lines=""
                with open(file, "r") as f:
                        for line in f.readlines():
                                lines += line +"\n"
                        f.close()
                return(lines.rstrip('\n+'))
 
        @staticmethod
        def writeArrayInAFile(file,array):
                Functions.log("DBG","Writing " + str(len(array)) + " line(s) in " + file,"Functions")
                aFile = open(file, "w")
                for line in array:
                        aFile.write(line + "\n");
 
        @staticmethod
        def loadFileInArray(file):
                lines=[]
                with open(file, "r") as f:
                        for line in f.readlines():
                                lines.append(line.rstrip('\n+'))
                        f.close()
                return(lines)
