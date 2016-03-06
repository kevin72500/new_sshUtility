__author__ = 'oupeng'
# -*- coding:gb2312 -*-
import paramiko
import csv
import pexpect
import re
import time

def surootexpect(filename="rootlist.txt"):
    csvReader = csv.reader(open(filename, 'rb'))
    for row in csvReader:
        parameterStr = ','.join(row)
        parameters = parameterStr.split(',')
        listLen=len(parameters)
        # print "start ......."
        # print "List elements are: ", parameters
        loginparams=[]
        executecommands=[]
        for i in range(0,listLen):
            if i < 4:
                loginparams.append(parameters[i])
                # print loginparams
            else:
                executecommands.append(parameters[i])
        try:
            session=pexpect.spawn('ssh %s@%s' % (loginparams[2].strip(),loginparams[0].strip()))
            session.expect('password:')
            session.sendline(loginparams[3].strip())

            session.expect('$')
            session.sendline(executecommands[0].strip())
            session.expect(':')
            session.sendline(executecommands[1].strip())
            session.expect('#')
            session.sendline(executecommands[2].strip())
            session.expect('#')
            session.sendline(executecommands[3].strip())
            session.expect('#')
            session.close()



surootexpect("rootlist")