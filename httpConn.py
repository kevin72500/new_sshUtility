__author__ = 'oupeng'
# -*- encoding:utf-8 -*-

import httplib
import time
import random


def send_user_json_with_headerKey(cloudCode):
    if cloudCode=="":
        cloudCode=78507
    else:
        conn = httplib.HTTPConnection("183.230.40.34:80")
        headers = {"api-key":"aijVmFZpgnW3ip8uuLbDBGLEb3oA"}#application/x-www-form-urlencoded  "Content-type":"application/json",
        curTime=time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()))
        params='''{"datastreams" : [{"id" : "GPS", "datapoints" : [{"at" : "'''+str(curTime)+'''", "value" : {"lon" : ",'''+\
               str(random.uniform(73,135))+''',", "speed" : "'''+str(random.randint(0,100))+'''", "direction" : "'''+\
               str(random.randint(1,8))+'''", "lat" : "'''+str(random.uniform(3,53))+'''", "ele" : 270 } } ] } ] }'''
        print params
        url="/devices/"+str(cloudCode)+"/datapoints"
        print url
        conn.request('POST', url, params, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            print 'success'
            print data
        else:
            print 'fail'
            print data
        conn.close()

code=raw_input("please input cloud code :")
while True:
    send_user_json_with_headerKey(code)
    time.sleep(5)
