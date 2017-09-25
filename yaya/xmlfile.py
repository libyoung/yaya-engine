#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import datetime
from xml.dom.minidom import Document 
import xml
class xmlFileInit(object):

    def __init__(self, path):
        self.path = path

    def _logPath(self):
        return self.path + '/scriptlog'

    def _getNowTime(self):
        ISOTIMEFORMAT = '%Y%m%d%H%M%S'
        now_time = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        return now_time

    def createXMLfile(self,modules):
        doc = Document()
        root = doc.createElement('RESULTS')
        doc.appendChild(root)
        planType = doc.createElement('PLANTYPE')
        planType.appendChild(doc.createTextNode('STABILITY UIAUTOMATOR'))
        playName = doc.createElement('PLAYNAME')
        playName.appendChild(doc.createTextNode('Android_Stationl'))
        swVersion = doc.createElement('SWVersion')
        swVersion.appendChild(doc.createTextNode("Andoid Version"))
        wStatus = doc.createElement('wStatus')
        wStatus.appendChild(doc.createTextNode('Finished'))
        debugLog = doc.createElement('DebugLOG')
        debugLog.appendChild(doc.createTextNode((self._logPath())))
        androidLog = doc.createElement('AndroidLOG')
        androidLog.appendChild(doc.createTextNode((self._logPath())))
        timeStamp = doc.createElement('TimeStamp')
        timeStamp.appendChild(doc.createTextNode(str(self._getNowTime())))
        cases = doc.createElement('CASES')

        nameList = modules.split(',')

        caselist = []
        caseNamelist = []
        totTimelist = []
        succTimelist = []
        datalist = []
        listNum = 0
        for index,i in enumerate(nameList):
            caselist.append(doc.createElement('Case'))
            caseNamelist.append(doc.createElement('NAME'))
            caseNamelist[listNum].appendChild(doc.createTextNode('5.1.' + str(index+1) + '_' + i))
            totTimelist.append(doc.createElement('TOTALTIMES'))
            totTimelist[listNum].appendChild(doc.createTextNode('0'))
            succTimelist.append(doc.createElement('SuccessRate'))
            succTimelist[listNum].appendChild(doc.createTextNode('0'))
            datalist.append(doc.createElement('DATA'))

            caselist[listNum].appendChild(caseNamelist[listNum])
            caselist[listNum].appendChild(caseNamelist[listNum])
            caselist[listNum].appendChild(totTimelist[listNum])
            caselist[listNum].appendChild(succTimelist[listNum])
            caselist[listNum].appendChild(datalist[listNum])

            cases.appendChild(caselist[listNum])

            listNum +=1

        rootChild = [planType,playName,swVersion,wStatus,debugLog,androidLog,timeStamp,cases]
        for i in rootChild:
            root.appendChild(i)
        fb = open(self.path + '/TestData.xml','w')
        doc.writexml(fb,indent = '\t',addindent = '\t',newl = '\n', encoding = 'utf-8')
        fb.close()


class StrAnalysis(object):

    def __init__(self, moduleName, index, timeDiff, totalTimes, successTimes, xmlfile):
        self.moduleName = moduleName
        self.index = index
        self.timeDiff = timeDiff
        self.totalTimes = totalTimes
        self.successTimes = successTimes
        self.successRate = 0
        self.xmlfile = xmlfile


    def _getCaseTypeByName(self,NameStr, modules):
        nameList = modules.split(',')
        for index, item in enumerate(nameList):
            if item.lower() in NameStr.lower():
                return index


    def _updata_SuccessRate(self,beforeSuccRate):
        if self.index == 1:
            nowData = float(self.successTimes)
        elif self.index >= 2:
            beforeData = float(beforeSuccRate)*(self.index-1)*float(self.totalTimes)
            nowData = beforeData + float(self.successTimes)
        nowTimeRate = nowData/float(self.totalTimes)/self.index
        nowRateStr = '%.2f'%nowTimeRate
        return nowRateStr

    def _updata_DATA(self):
        doc = Document()
        loop = doc.createElement('LOOP')
        loopIndex = doc.createElement('INDEX')
        loopIndex.appendChild(doc.createTextNode(str(self.index)))
        loopTime = doc.createElement('TIME')
        loopTime.appendChild(doc.createTextNode(self.timeDiff))
        loopSuccessTimes = doc.createElement('SUCCESSTIMES')
        loopSuccessTimes.appendChild(doc.createTextNode(self.successTimes))
        loop.appendChild(loopIndex)
        loop.appendChild(loopTime)
        loop.appendChild(loopSuccessTimes)
        return loop

    def _resetXMLfile(self,filepath):
        emptyline = '\t\n'
        fb_r = open(filepath,'r')
        result = list()
        for line in fb_r.readlines():
            if emptyline in line:
                continue
            elif len(line) == 1:
                continue
            result.append(line)
        finResult = ''.join(result)
        fb_r.close()
        fb_w = open(filepath,'w')
        fb_w.write(finResult)
        fb_w .close()

    def addDataToXML(self, modules):
        #print 'clay put data to xml\n'
        theNum = self._getCaseTypeByName(self.moduleName, modules)
        xmlPath = self.xmlfile.path + '/TestData.xml'
        if os.path.exists(xmlPath):
            DOMTree = xml.dom.minidom.parse(xmlPath)
            rootTree = DOMTree.documentElement
            nameByStr = rootTree.getElementsByTagName('NAME')
            totaltimesByStr = rootTree.getElementsByTagName('TOTALTIMES')
            successrateByStr = rootTree.getElementsByTagName('SuccessRate')
            dataByStr = rootTree.getElementsByTagName('DATA')
            totaltimesByStr[theNum].firstChild.data = self.totalTimes
            beforeSuccRate = successrateByStr[theNum].firstChild.data
            successrateByStr[theNum].firstChild.data = self._updata_SuccessRate(beforeSuccRate)
            dataByStr[theNum].appendChild(self._updata_DATA())
            fb = open(xmlPath,'w')
            DOMTree.writexml(fb,addindent = '\t',newl = '\n',encoding = 'utf-8')
            fb.close()
            self._resetXMLfile(xmlPath)

if __name__ == '__main__':
    print sys.path[0]
    a = xmlFileInit(sys.path[0])
    a.createXMLfile()
    StrAnalysis('Telephony', 1, "51:12:00", '200', '199', a).addDataToXML()