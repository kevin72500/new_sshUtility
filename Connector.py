__author__ = 'oupeng'
#-*- coding:utf8 -*-
import paramiko
import os
from progressbar import AnimatedMarker, Bar, BouncingBar,Counter,ETA,FileTransferSpeed, FormatLabel, Percentage,   ProgressBar, ReverseBar, RotatingMarker,   SimpleProgress, Timer
import time


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
        if os.path.isfile(localPath)==False:
            print "upload failed "+localPath+" file not exist!!!"
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
            # answer=raw_input("this is using to pause output, click enter to exit!!")
            # if answer=='y'or answer=="yes":
            #     quit()

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
            # answer=raw_input("this is using to pause output, click enter to exit!!")
            # if answer=='y'or answer=="yes":
            #     quit()

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
            # answer=raw_input("this is using to pause output, click enter to exit!!")
            # if answer=='y'or answer=="yes":
            #     quit()

    def sshMonitor(self,commandList,outFileName="out.txt",exeInterval=0,exeTimes=1):
#         paramiko.util.log_to_file(outFileName)
        outfh=open(outFileName,'a+')
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(self.ip).strip(), int(self.port), str(self.name).strip(), str(self.passwd))
            print 'Executing.....'

            # for command in commandList:
            if len(commandList)>1:
                print "Your command more than one, please make sure your command just have one command!!!"
                command=",".join(commandList)
            else:
                command="".join(commandList).strip()
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
            exit()
        finally:
            ssh.close()
            # answer=raw_input("this is using to pause output, click enter to exit!!")
            # if answer=='y'or answer=="yes":
            #     quit()