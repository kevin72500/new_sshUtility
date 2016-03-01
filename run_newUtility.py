from newUtility import ReadFile,Connector


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