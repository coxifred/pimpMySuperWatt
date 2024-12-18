import re
import datetime
import subprocess
import sys
import threading
import hashlib
import requests
import warnings
import importlib
import json
import time
from utils.singleton import Singleton
from utils.timeout import TimeoutFunction
 
 
 
class Functions:
 
        @staticmethod
        def log(level, message, source):
                date = str(datetime.datetime.now())
                singleton=Singleton()
                aLog=date + " " + "[" + threading.current_thread().name + "] " + level + " " + source + " " + message
                singleton.lastMessages.append(aLog)
                if len(singleton.lastMessages) > 10:
                   singleton.lastMessages.pop(0)
                if ( level == "DBG" ):
                        if singleton.debug:
                           if "debugClass" in singleton.parameters:
                              if len(singleton.parameters["debugClass"]) == 0:
                                Functions.logdebug()
                                print(aLog, flush=True)
                              elif source in singleton.parameters["debugClass"]:
                                Functions.logdebug()
                                print(aLog, flush=True)
                           else:
                                Functions.logdebug()
                                print(aLog, flush=True)
                elif ( level == "ERR" or level == "DEAD" ):
                        Functions.logred()
                        print(aLog,end='', flush=True)
                        print("")
                        time.sleep(0.5)
                        Functions.lognormal()
                elif ( level == "ASK" or level == "WNG" ):
                        Functions.logyellow()
                        print(aLog, flush=True)
                elif ( level == "ACK" ):
                        Functions.loggreen()
                        print(aLog, flush=True)
                else:
                        Functions.lognormal()
                        print(aLog, flush=True)
                if ( level == "DEAD" ):
                        sys.exit(1)
                singleton.logs.append(aLog)
                f= open("/tmp/pimpMySuperWatt.log","a+")
                f.write(aLog + "\r\n")
                sys.stdout.flush()
       
        @staticmethod
        def command(aCommand,aParameter=""):
            Functions.log("DBG","Running a command " + aCommand + " with parameter " + aParameter,"CORE")
            importlib.import_module('communication')
            Functions.log("DBG","Trying instanciation of " + aCommand,"CORE")
            mod=importlib.import_module('.' + aCommand,package="communication")
            aRealCommand = getattr(mod, aCommand)
            return aRealCommand().send(parameter=aParameter)

                 
        @staticmethod
        def timeoutF(function,timeout):
            try:
                Functions.log("DBG","Running a timeout function " + str(function) + " with " + str(timeout) + " timeout second(s)","CORE")
                TimeoutFunction(function, timeout) 
            except TimeoutFunctionException: 
                Functions.log("WNG","Too slow, function is running over "  + str(timeout) + " sec(s)","CORE")


        @staticmethod
        def loggreen():
                sys.stdout.write("\033[1;37;32m")
                sys.stdout.flush()
 
        @staticmethod
        def logred():
                sys.stdout.write("\033[1;37;41m")
                sys.stdout.flush()
 
        @staticmethod
        def logyellow():
                sys.stdout.write("\033[1;33;33m")
                sys.stdout.flush()
 
        @staticmethod
        def lognormal():
                sys.stdout.write("\033[1;37;40m")
                sys.stdout.flush()
 
        @staticmethod
        def logdebug():
                sys.stdout.write("\033[1;36;35m")
                sys.stdout.flush()
 
        @staticmethod
        def requestHttp(request):
                Functions.log("DBG","HttpRequest: " + request,"Functions")
                requests.packages.urllib3.disable_warnings()
                r = requests.get(request, verify=False)
                Functions.log("DBG","Response code: " + str(r.status_code),"Functions")
                if r.status_code == 200:
                        body = r.content.decode()
                        Functions.log("DBG","Response : " + str(body),"Functions")
                        array=body.split("\n")
                        while '' in array:
                                array.pop(array.index(''))
                        return array
                else:
                        Functions.log("ERR","Error while request " + str(r.text),"Functions")
                        raise Exception('Error while request')
 
        @staticmethod
        def getFieldFromString(string,delimiter,fieldNumber):
                try:
                    return re.split(delimiter,string)[fieldNumber]
                except Exception as err:
                    Functions.log("WNG","Error while trying to use getFieldFromString on " + string + ", perhaps no separator " + delimiter + ", default behavior is to return the full string, error was "+ str(err),"Functions.getFieldFromString")
                    return string
 
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
        def getFirstMatchReInArray(regexp,array):
                returnLine=""
                for line in array:
                        #Functions.log("DBG","Looking for " + regexp + " in line " + line,"Functions")
                        if re.match(regexp, line) is not None:
                                #Functions.log("DBG","Match for " + regexp + " in line " + line,"Functions")
                                return line
 
        @staticmethod
        def getLastMatchReInArray(regexp,array):
                returnLine=""
                for line in array:
                        #Functions.log("DBG","Looking for " + regexp + " in line " + line,"Functions")
                        if re.match(regexp, line) is not None:
                                #Functions.log("DBG","Match for " + regexp + " in line " + line,"Functions")
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
                return date.strftime(format)
 
        @staticmethod
        def getDateFormatFromString(stringDate,format="default"):
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
        def writeArrayInAFileAppend(file,array):
                Functions.log("DBG","Writing " + str(len(array)) + " line(s) in " + file,"Functions")
                aFile = open(file, "a+")
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

        @staticmethod
        def make_lines(data, precision=None):
             lines = []
             static_tags = data.get('tags')
             for point in data['points']:
                 elements = []
         
                 # add measurement name
                 measurement = _escape_tag(_get_unicode(
                     point.get('measurement', data.get('measurement'))))
                 key_values = [measurement]
         
                 # add tags
                 if static_tags:
                     tags = dict(static_tags)  # make a copy, since we'll modify
                     tags.update(point.get('tags') or {})
                 else:
                     tags = point.get('tags') or {}
         
                 # tags should be sorted client-side to take load off server
                 for tag_key, tag_value in sorted(iteritems(tags)):
                     key = _escape_tag(tag_key)
                     value = _escape_tag_value(tag_value)
         
                     if key != '' and value != '':
                         key_values.append(key + "=" + value)
         
                 elements.append(','.join(key_values))
         
                 # add fields
                 field_values = []
                 for field_key, field_value in sorted(iteritems(point['fields'])):
                     key = _escape_tag(field_key)
                     value = _escape_value(field_value)
         
                     if key != '' and value != '':
                         field_values.append(key + "=" + value)
         
                 elements.append(','.join(field_values))
         
                 # add timestamp
                 if 'time' in point:
                     timestamp = _get_unicode(str(int(
                         _convert_timestamp(point['time'], precision))))
                     elements.append(timestamp)
         
                 line = ' '.join(elements)
                 lines.append(line)
         
             return '\n'.join(lines) + '\n'
