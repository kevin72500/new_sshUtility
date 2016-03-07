__author__ = 'oupeng'
import threading

threadLock=threading.Lock()
class ThreadOperation(threading.Thread):

    def __init__(self,eList):
        threading.Thread.__init__(self)
        self.eList=eList

    def run(self):
        print 'multi-threading execute starting...'
        threadLock.acquire()
        executer(self.eList)
        threadLock.release()