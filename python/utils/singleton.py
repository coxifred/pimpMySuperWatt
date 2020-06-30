class Singleton(object):
        class __Singleton:
                def __str__(self):
                        return self
 
                def __init__(self):
                        self.hostName=''
                        self.debug=False
                        self.version=''
                        self.params={}
                        self.logs=[]
 
        instance = None
 
        def __new__(c):
                if not Singleton.instance:
                        Singleton.instance = Singleton.__Singleton()
                return Singleton.instance
 
        def __getattr__(self, attr):
                return getattr(self.instance, attr)
        def __setattr__(self, attr):
                return setattr(self.instance, attr)
