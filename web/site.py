import os
import importlib
import glob
import json
from utils.functions import Functions
from utils.singleton import Singleton
from flask import Flask
from flask_caching import Cache

from flask import render_template



class site():
    def __init__(self):
        self.singleton=Singleton()
        Functions.log("DBG","Site instance created starting site...","site")
        self.create_app()

    def create_app(self):
        # create and configure the app
        template_dir = os.path.abspath('./web/templates')
        static_dir = os.path.abspath('./web/static')
        app = Flask("PimpMySuperWatt", instance_relative_config=True,template_folder=template_dir,static_folder=static_dir)
        # For disabling cache, usefull for online html/css/js script modifications
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['EXPLAIN_TEMPLATE_LOADING'] = True
        cache = Cache(config={'CACHE_TYPE': 'simple'})
        cache.init_app(app)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass



        @app.route('/cmd/<command>')
        @app.route('/cmd/<command>/<parameter>')
        def cmd(command,parameter=""):
           feedback={}
           try:
             if parameter == "":
                feedback=Functions.command(command) 
             else:
                feedback=Functions.command(command,parameter) 
           except Exception as err:
              feedback["error"]="Something wrong in command " + command + " " + parameter + " error was " + str(err)
              Functions.log("ERR","Something wrong in command " + command + " " + parameter + " error was " + str(err),"site.cmd")
              
           return json.dumps(feedback,indent=4)

        @app.route('/ready')
        def ready():
            singleton=Singleton()
            ready={}
            ready["ready"]=singleton.ready
            ready["currentTry"]=singleton.currentTry
            ready["maxTry"]=singleton.maxTry
            ready["communicationStatus"]=singleton.communicationStatus
            ready["lastMessages"]=singleton.lastMessages
            return str(json.dumps(ready,indent=4))

        @app.route('/cmdAvail')
        def cmdAvail():
            cmd=[]
            for file in sorted(glob.glob('communication/*.py')):
               moduleName=os.path.basename(file.replace(".py",""))
               if "init" in moduleName or "abstractCode" in moduleName or "Connector" in moduleName:
                  continue
               try:
                  Functions.log("DBG","Loading communication/" + moduleName,"site.cmdAvail")
                  mod=importlib.import_module("communication." + moduleName)
                  Functions.log("DBG","End loading communication/" + moduleName,"site.cmdAvail")
                  Functions.log("DBG","Trying dynamic instantiation " + moduleName ,"site.cmdAvail")
                  aClass = getattr(mod, moduleName)
                  instanceCommand = aClass()
                  Functions.log("DBG","Command " + moduleName + " instanciated " + str(instanceCommand ),"site.cmdAvail")
                  aCmd={
                        "command"               : moduleName,
                        "help"                  : instanceCommand.help(),
                        "parameterMandatory"    : instanceCommand.parameterMandatory(),
                        "parameterFormat"       : instanceCommand.parameterFormat(),
                        "examples"              : instanceCommand.examples(),
                        "pureQuery"             : instanceCommand.pureQuery(),
                        "internalCommand"       : instanceCommand.internalCommand()
                       }
                  cmd.append(aCmd)
               except Exception as err:
                  Functions.log("ERR","Something wrong in command discovery error was " + str(err) + " from file " + file,"site.cmdAvail")
            Functions.log("DBG","Returning commands list " + str(json.dumps(cmd,indent=4)),"site.cmdAvail")
            return json.dumps(cmd,indent=4)

        @app.route('/')
        @cache.cached(timeout=1)
        def index():
            cache.clear()
            return render_template('index.html')

        @app.route('/parameters')
        def parameters():
            try:
               singleton=Singleton()
               Functions.log("DBG","Parameters content is " + str(singleton.parameters),"site.parameters")
               parameters_plus=self.singleton.parameters.copy()
               Functions.log("DBG","Version is " + str(singleton.version),"site.parameters")
               parameters_plus["version"]=singleton.version
               Functions.log("DBG","hostName is " + str(singleton.hostName),"site.parameters")
               parameters_plus["hostname"]=singleton.hostName
               Functions.log("DBG","Returning " + str(json.dumps(parameters_plus,indent=4)),"site.parameters")
               return json.dumps(parameters_plus,indent=4)
            except Exception as err:
               Functions.log("ERR","Error in parameters query, error was " + str(err),"site.parameters")
               return json.dumps({})

        @app.route('/inverterQuery')
        def inverterQuery(): 
            try:
               singleton=Singleton()
               parameters_plus={}
               if hasattr(singleton,"QET"):
                  Functions.log("DBG","QET content is " + str(json.dumps(singleton.QET,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QET)
               if hasattr(singleton,"QEM"):
                  Functions.log("DBG","QEM content is " + str(json.dumps(singleton.QEM,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QEM)
               if hasattr(singleton,"QEY"):
                  Functions.log("DBG","QEY content is " + str(json.dumps(singleton.QEY,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QEY)
               if hasattr(singleton,"QED"):
                  Functions.log("DBG","QED content is " + str(json.dumps(singleton.QED,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QED)
               if hasattr(singleton,"QT"):
                  Functions.log("DBG","QT content is " + str(json.dumps(singleton.QT,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QT)
               if hasattr(singleton,"QFLAG"):
                  Functions.log("DBG","QFLAG content is " + str(json.dumps(singleton.QFLAG,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QFLAG)
               if hasattr(singleton,"QMOD"):
                  Functions.log("DBG","QMOD content is " + str(json.dumps(singleton.QMOD,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QMOD)
               if hasattr(singleton,"QPIWS"):
                  Functions.log("DBG","QPIWS content is " + str(json.dumps(singleton.QPIWS,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QPIWS)
               if hasattr(singleton,"QPIGS"):
                  Functions.log("DBG","QPIGS content is " + str(json.dumps(singleton.QPIGS,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QPIGS)
               if hasattr(singleton,"QPIGS2"):
                  Functions.log("DBG","QPIGS2 content is " + str(json.dumps(singleton.QPIGS2,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QPIGS2)
               if hasattr(singleton,"QPIRI"):
                  Functions.log("DBG","QPIRI content is " + str(json.dumps(singleton.QPIRI,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QPIRI)
               if hasattr(singleton,"QBMS"):
                  Functions.log("DBG","QBMS content is " + str(json.dumps(singleton.QBMS,indent=4)),"site.inverterQuery")
                  parameters_plus.update(singleton.QBMS)
               if hasattr(singleton,"QPI"):
                  Functions.log("DBG","QPI content is " + str(singleton.QPI),"site.inverterQuery")
                  parameters_plus["qpi"]=singleton.QPI
               if hasattr(singleton,"QID"):
                  Functions.log("DBG","QID content is " + str(singleton.QID),"site.inverterQuery")
                  parameters_plus["qid"]=singleton.QID
               if hasattr(singleton,"QVFW"):
                  Functions.log("DBG","QVFW content is " + str(singleton.QVFW),"site.inverterQuery")
                  parameters_plus["qfw"]=singleton.QVFW
               if hasattr(singleton,"QVFW2"):
                  Functions.log("DBG","QVFW2 content is " + str(singleton.QVFW2),"site.inverterQuery")
                  parameters_plus["qfw2"]=singleton.QVFW2
               if hasattr(singleton,"QVFW2"):
                  Functions.log("DBG","QVFW3 content is " + str(singleton.QVFW3),"site.inverterQuery")
                  parameters_plus["qfw3"]=singleton.QVFW3
               if hasattr(singleton,"QMN"):
                  Functions.log("DBG","QMN content is " + str(singleton.QMN),"site.inverterQuery")
                  parameters_plus["qmn"]=singleton.QMN
               if hasattr(singleton,"QGMN"):
                  Functions.log("DBG","QGMN content is " + str(singleton.QGMN),"site.inverterQuery")
                  parameters_plus["qgmn"]=singleton.QGMN
               if hasattr(singleton,"communicationStatus"):
                  Functions.log("DBG","communicationStatus content is " + str(singleton.communicationStatus),"site.inverterQuery")
                  parameters_plus["communicationStatus"]=singleton.communicationStatus
               if hasattr(singleton,"currentTry"):
                  Functions.log("DBG","currentTry content is " + str(singleton.currentTry),"site.inverterQuery")
                  parameters_plus["currentTry"]=singleton.currentTry
               if hasattr(singleton,"maxTry"):
                  Functions.log("DBG","maxTry content is " + str(singleton.maxTry),"site.inverterQuery")
                  parameters_plus["maxTry"]=singleton.maxTry
               if hasattr(singleton,"GRIDWATTS"):
                  Functions.log("DBG","GRIDWATTS content is " + str(singleton.GRIDWATTS),"site.inverterQuery")
                  parameters_plus["GRIDWATTS"]=singleton.GRIDWATTS
               if hasattr(singleton,"queue"):
                  Functions.log("DBG","Queue content is " + str(singleton.queue),"site.inverterQuery")
                  parameters_plus["queue"]=singleton.queue
               Functions.log("DBG","Returning " + str(json.dumps(parameters_plus,indent=4)),"site.inverterQuery")
               return json.dumps(parameters_plus,indent=4)
            except Exception as err:
               Functions.log("ERR","Error in inverterQuery query, error was " + str(err),"site.inverterQuery")
               return json.dumps({})

        
        self.singleton.scheduler.init_app(app)
        self.singleton.scheduler.start()
        app.run(self.singleton.parameters["httpBind"],self.singleton.parameters["httpPort"])
        Functions.log("DBG","Site instance started","site")

    def runWebApp(self,app):
        try:
            Functions.log("DBG","Trying to start","site")
            app.run(self.singleton.parameters["httpBind"],self.singleton.parameters["httpPort"],self.singleton.parameters["webserverDebug"])

        except E:
            Functions.log("ERR","Error for starting web","site")
