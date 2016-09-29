__author__ = 'oupeng'
import threading
from Connector import Connector
from ReadFile import ReadFile

threadLock=threading.Lock()
class ThreadOperation(threading.Thread):

    def __init__(self,eList):
        threading.Thread.__init__(self)
        self.eList=eList

    def run(self):
        print('multi-threading execute starting...')
        threadLock.acquire()
        executer(self.eList)
        threadLock.release()

def executer(oneLine):
    # for oneLine in eList:
    if oneLine.operation=='upload':
        Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
        Conn.sftpUpload(oneLine.restList[1].strip(),oneLine.restList[0].strip())
    elif oneLine.operation=='download':
        Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
        Conn.sftpDownLoad(oneLine.restList[1].strip(),oneLine.restList[0].strip())
    elif oneLine.operation=='execute':
        Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
        Conn.sshExecute(oneLine.restList)
    elif oneLine.operation=='monitor':
        Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
        Conn.sshMonitor(oneLine.restList,oneLine.filePath,oneLine.interval,oneLine.times)

