__author__ = 'oupeng'
#-*- coding:utf8 -*-

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

