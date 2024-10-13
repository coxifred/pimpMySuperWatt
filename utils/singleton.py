from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler




class Singleton(object):
        class __Singleton:
                def __str__(self):
                        return self
 
                def __init__(self):
                        self.hostName=''
                        self.debug=False
                        self.version=''
                        self.parameters={}
                        self.logs=[]
                        self.lastMessages=[]
                        self.connector=None
                        self.webapp=''
                        self.scheduler=APScheduler()
                        self.internalScheduler=BackgroundScheduler()
                        self.internalScheduler.start()
                        self.ip=''
                        self.port=''

                        self.QPIGS={}
                        self.QPIGS2={}
                        self.QPI=""
                        self.QT=""
                        self.QID=""
                        self.QVFW=""
                        self.QVFW2=""
 
        instance = None
 
        def __new__(c):
                if not Singleton.instance:
                        Singleton.instance = Singleton.__Singleton()
                return Singleton.instance
 
        def __getattr__(self, attr):
                return getattr(self.instance, attr)
        def __setattr__(self, attr):
                return setattr(self.instance, attr)
