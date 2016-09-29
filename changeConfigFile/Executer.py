# -*- coding: utf-8 -*-
__author__ = 'oupeng'

from ReadFile import ReadFile
from ThreadOperation import ThreadOperation


if __name__=='__main__':

    rf=ReadFile("newUtilityRecords.txt")
    if rf.validatePath()==True:
        eList=rf.parseRow()
        NumOfThread=len(eList)
    # for one in eList:
    #     executer(one)


    threads=[]
    for i in range(0,NumOfThread):
        threads.append(ThreadOperation(eList[i]).start())
    for t in threads:
        t.join()
    answer=raw_input("please input y to exit")
    while(answer!='y'):
        answer=raw_input("please input y to exit")