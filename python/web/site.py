import os
from utils.functions import Functions
from utils.singleton import Singleton
from flask import Flask


class site():
    def __init__(self):
        self.singleton=Singleton()
        Functions.log("DBG","Site instance created starting site...","site")
        self.create_app()

    def create_app(self):
        # create and configure the app
        app = Flask("PimpMySuperWatt", instance_relative_config=True)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # a simple page that says hello
        @app.route('/hello')
        def hello():
            return 'Hello, World!'
        
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
