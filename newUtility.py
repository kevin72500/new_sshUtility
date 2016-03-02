__author__ = 'oupeng'
# -*- coding:cp936 -*-
import sys
import os
import paramiko
import threading
import time
from progressbar import AnimatedMarker, Bar, BouncingBar,Counter,ETA,FileTransferSpeed, FormatLabel, Percentage,   ProgressBar, ReverseBar, RotatingMarker,   SimpleProgress, Timer
#get num of cpu
from multiprocessing import cpu_count   


class NewEntities():
    '''定义实体类，用来存储配置文件读取
    其中包含操作方式，连接地址，端口号，用户名，密码，root密码，连接方式
    采样频率，采样次数，文件路径，最后一项为命令行用逗号分隔，或者是上传下载路径'''
    def __init__(self,rowLine):
        rowList=rowLine.split(',')
        self.operation=rowList[0]
        self.ip=rowList[1]
        self.port=rowList[2]
        self.userName=rowList[3]
        self.passWord=rowList[4]
        self.rootPassWord=rowList[5]
        self.connWay=rowList[6]
        self.interval=rowList[7]
        self.times=rowList[8]
        self.filePath=rowList[9]
        self.restList=rowList[10:]
        
    def __str__(self):
        return 'Current "%s" will perform, "%s" on the %s using port %s thru %s, execute %s times with interval %s, store in %s... rest list are: %s'  % (self.operation, self.userName, self.ip, self.port, self.connWay, self.times, self.interval, self.filePath,self.restList)


class ReadFile():
    '''文件读取类，判断路径是否合法，读取配置文件中的数据到内存，并存入实体类'''
    def __init__(self,filePath):
        self.filePath=filePath
        
    def validatePath(self):
        f=open(self.filePath)
        if type(f)!=file:
            print filePath, " not a valid file!!!"
            return False
        else:
            return True
        
    def parseRow(self):
        operList=[]
        fh=open(self.filePath,'r+')
        for line in fh:
            if not line.startswith('#'):
                one=NewEntities(unicode(line.strip(),'utf8'))
                print one
                operList.append(one)
        return operList


class Connector():
    '''连接器类，利用paramiko模块，ssh sftp登录远程linux服务器，执行命令或者上传下载'''
    def __init__(self,ip,port,name,passwd,connWay):
        self.ip=ip
        self.port=int(port)
        self.name=name
        self.passwd=passwd
        self.connWay=connWay
#         print self.ip,type(self.ip),self.port,type(self.port),self.name,type(self.name),self.passwd,type(self.passwd)


    def sftpUpload(self,localPath,remotePath):
        try:
            t = paramiko.Transport((self.ip, self.port))
            t.connect(username=self.name, password=self.passwd)
#             print 'upload'
            sftp = paramiko.SFTPClient.from_transport(t)
            # print 'Uploading.....'
            widgets = ['Uploading ',localPath,' : ', Percentage(), ' ',Bar(marker='#',left='[',right=']'),' ', ETA(), ' ', FileTransferSpeed()]
            file_size = os.path.getsize(localPath)
            pbar = ProgressBar(widgets=widgets, maxval=file_size)
            pbar.start()
            progress_bar = lambda transferred, toBeTransferred: pbar.update(transferred)
            sftp.put(localPath, remotePath,callback=progress_bar)
            pbar.finish()
        except Exception, e:
            print 'upload failed: ', e
            t.close()
        finally:
            t.close()
            print 'Upload done!!!'
            answer=raw_input("this is using to pause output, click enter to exit!!")
            if answer=='y'or answer=="yes":
                quit()

    def sftpDownLoad(self,localPath,remotePath):
        print localPath
        print remotePath
        try:
            t = paramiko.Transport((self.ip, int(self.port)))
            t.connect(username=self.name, password=self.passwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            print 'Downloading.....'
            # widgets = ['Test: ', Percentage(), ' ',Bar(marker='#',left='[',right=']'),' ', ETA(), ' ', FileTransferSpeed()]
            # file_size = os.path.getsize(localPath)
            # pbar = ProgressBar(widgets=widgets, maxval=file_size)
            # pbar.start()
            # progress_bar = lambda transferred, toBeTransferred: pbar.update(transferred)
            sftp.get(remotePath, localPath)
            # pbar.finish()
        except Exception, e:
            print 'Download failed: ', e
            t.close()
        finally:
            t.close()
            print remotePath, ' -->  Download done!!!'
            answer=raw_input("this is using to pause output, click enter to exit!!")
            if answer=='y'or answer=="yes":
                quit()
            
    def sshExecute(self,commandList):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(self.ip).strip(), int(self.port), str(self.name).strip(), str(self.passwd))
            print 'Executing.....'
            for command in commandList:
                # print command
                command=command.strip()
                stdin, stdout, stderr = ssh.exec_command(command)
                outValue=stdout.read()
                outError=stderr.read()
                if outValue=="" and outError=="":#len(stdout.readlines())==0:
                    print "command: ",command, " ,execute Success",outValue, outError
                else:
                    print "command: ", command, " ,execute Failed",outValue, outError
        except Exception, e:
            print 'remote execute error: ', e
            ssh.close()
        finally:
            ssh.close()
            answer=raw_input("this is using to pause output, click enter to exit!!")
            if answer=='y'or answer=="yes":
                quit()
            
    def sshMonitor(self,commandList,outFileName="out.txt",exeInterval=0,exeTimes=1):
#         paramiko.util.log_to_file(outFileName) 
        outfh=open(outFileName,'a+')
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(self.ip).strip(), int(self.port), str(self.name).strip(), str(self.passwd)) 
            print 'Executing.....'
            for command in commandList:
                # print command
                if len(commandList)>1:
                    print "Your command more than one, please shrank it"
                    quit()
                else:
#                     command=command.strip()
                    for i in range(0,int(exeTimes)):
        
                        stdin, stdout, stderr = ssh.exec_command(command)
                        outValue=stdout.read()
                        print outValue
                        if outValue=="":
                            print "command: ",command, " ,execute Failed and no output"
                        else:
                            print "command: ", command, " ,execute Success, output is: ",outValue
                        curTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        outfh.writelines(curTime+"    "+outValue)
                        time.sleep(int(exeInterval))
                    outfh.close()
        except Exception, e:
            print 'remote execute error: ', e
            ssh.close()
        finally:
            ssh.close()
            answer=raw_input("this is using to pause output, click enter to exit!!")
            if answer=='y'or answer=="yes":
                quit()
            
# class ThreadOperation(threading.Thread):
#     
#     def __init__(self,ip,port,name,passwd,connWay):
#         threading.Thread.__init__(self)
#         self.ip=ip
#         self.port=port
#         self.name=name
#         self.passwd=passwd
#         self.connWay=connWay
#     
#     def run(self):
#         print 'multi-threading execute starting...'
        
    
    
    
    
        
# if __name__=='__main__':
#     rf=ReadFile("newUtilityRecords.txt")
#     if rf.validatePath()==True:
#         eList=rf.parseRow()
#
#     for oneLine in eList:
#         if oneLine.operation=='upload':
#             Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
#             Conn.sftpUpload(oneLine.restList[1].strip(),oneLine.restList[0].strip())
#         elif oneLine.operation=='download':
#             Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
#             Conn.sftpDownLoad(oneLine.restList[1].strip(),oneLine.restList[0].strip())
#         elif oneLine.operation=='execute':
#             Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
#             Conn.sshExecute(oneLine.restList)
#         elif oneLine.operation=='monitor':
#             Conn=Connector(oneLine.ip,oneLine.port,oneLine.userName,oneLine.passWord,oneLine.connWay)
#             Conn.sshMonitor(oneLine.restList,oneLine.filePath,oneLine.interval,oneLine.times)
#
    
    
    
rf=ReadFile("newUtilityRecords.txt")
if rf.validatePath()==True:
    eList=rf.parseRow()

for oneLine in eList:
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
