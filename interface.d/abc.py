import abc
import datetime

class WriteFile(object):
    __metaclass__ = abc.ABCMeta
    
    
    @abc.abstractmethod
    def write(self,text):
        """Write to file"""
        print("Should not be here")
        return 

class LogFile(WriteFile):
    def __init__(self, fh):
        self.fh = fh


f = LogFile("log.txt")
f.write("Hello")
