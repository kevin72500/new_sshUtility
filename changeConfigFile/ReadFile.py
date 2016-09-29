# -*- coding: utf-8 -*-
__author__ = 'oupeng'

from NewEntities import NewEntities
import os

class ReadFile():
    '''read file and check if it's exist or not, and put it into the entity class'''
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