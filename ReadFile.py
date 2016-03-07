__author__ = 'oupeng'
# -*- coding:utf8 -*-
from NewEntities import NewEntities
import os

class ReadFile():
    '''文件读取类，判断路径是否合法，读取配置文件中的数据到内存，并存入实体类'''
    def __init__(self,filePath):
        self.filePath=filePath

    def validatePath(self):

        if os.path.isfile(self.filePath):
            return True
        else:
            print self.filePath+" not a valid file!!!"
            return False


    def parseRow(self):
        operList=[]
        fh=open(self.filePath,'r+')
        for line in fh:
            if not line.startswith('#'):
                one=NewEntities(line.strip())
                print one
                operList.append(one)
        return operList