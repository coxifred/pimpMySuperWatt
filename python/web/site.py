import os
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
        cache = Cache(config={'CACHE_TYPE': 'null'})
        cache.init_app(app)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        @app.route('/')
        @cache.cached(timeout=1)
        def index():
            cache.clear()
            return render_template('index.html')

        @app.route('/parameters')
        def parameters():
            return json.dumps(self.singleton.parameters,indent=4)

        @app.route('/inverterParameters')
        def inverterParameters(): 
            singleton=Singleton()
            return {
                                  "qpi"     : singleton.QPI,
                                  "qid"     : singleton.QID,
                                  "qfw"     : singleton.QVFW,
                                  "qfw2"    : singleton.QVFW2,
                   }

        @app.route('/inverterQuery')
        def inverterQuery():
            singleton=Singleton()
            return singleton.QPIGS

        
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
