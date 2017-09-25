#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170815
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     LogJson Object
##############################
import json
import datetime
##############################
#   Date Struct
#   {
#       "PlanType" : "Stability UIautomator",
#       "PlanName" : "Android Stationl",
#       "SWVersion" : "Phone SW version",
#       "PlanCricle" ：10,
#       "RunStatus" : "Finished",   #Suspend Ready
#       "TimeStamp" : "2017893475902345",
#       "CurrRunData": {
#                           "ModuleName": "Telephony",
#                           "TotalTimes": 300,
#                           "SucessTimes" :100,
#                           "CaseName" : ""
#                           "Cricle": 2,
#                           }
#       "ModuleData" : [
#                           {
#                               "ModuleName": "Telephony",
#                               "TotalTimes" : 300,
#                               "SuccessRate" : "90.00%",
#                               "PerCricleSucessTimes" : [299,300,300,280],
#                               "PerCricleRunTime" : ["2:35:34", "2:40:45","2:39:56","2:50:12"],
#                           },
#                           {
#                               "ModuleName": "Telephony",
#                               "TotalTimes" : 300,
#                               "SuccessRate" : 90.00%",
#                               "PerCricleSucessTimes" : [299,300,300,280],
#                               "PerCricleRunTime" : ["2:35:34", "2:40:45","2:39:56","2:50:12"],
#                           },
#                           {
#                               "ModuleName": "Telephony",
#                               "TotalTimes" : 300,
#                               "SuccessRate" : 90.00%",
#                               "PerCricleSucessTimes" : [299,300,300,280],
#                               "PerCricleRunTime" : ["2:35:34", "2:40:45","2:39:56","2:50:12"],
#                           }, 
#                           .
#                           .
#                           .
#                       ]
#   }
##############################
class LogDataToJson(object):

    def __init__(self):
        self.data = {}
        self.data["PlanType"] = "Stability UIautomator"
        self.data["PlanName"] = "Android Stationl"
        self.data["SWVersion"] = "Phone SW version"
        self.data["PlanCricle"] = 10
        self.data["RunStatus"] = "Ready"
        self.data["TimeStamp"] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.data["CurrRunData"] = {}
        self.data["ModuleData"] = []
        self._fields = ["PlanType","PlanName","SWVersion","PlanCricle","TimeStamp","CurrCricle","CurrModule","ModuleData"]
        self.jsonfilename = self.data["TimeStamp"] + "_" + "TestData.json"

    def InitModuleData(self, modules):
        for item in modules.split(','):
            self.data["ModuleData"].append({"ModuleName":item,"PerCricleSucessTimes":[],"PerCricleRunTime":[]})

    def GetModuleData(self, modulename):
        for item in self.data["ModuleData"]:
            if modulename == item["ModuleName"]:
                return item
        return None

    def AddModuleData(self, modulename, totaltimes, sucesstimes, runtime, cricle=1):
        for item in self.data["ModuleData"]:
            if modulename == item["ModuleName"]:
                item["TotalTimes"] = totaltimes
                if len(item["PerCricleSucessTimes"]) < cricle:
                    item["PerCricleSucessTimes"].append(sucesstimes)
                else:
                    item["PerCricleSucessTimes"][cricle-1] = sucesstimes
                if len(item["PerCricleRunTime"]) < cricle:
                    item["PerCricleRunTime"].append(runtime)
                else:
                    item["PerCricleRunTime"][cricle-1] = runtime
                item["SuccessRate"] = "%0.2f%%" % (sum(item["PerCricleSucessTimes"]) / (len(item["PerCricleSucessTimes"]) * item["TotalTimes"]) * 100 )

    def SetPlanData(self, key, value):
        self.data[key] = value

    def GetPlanData(self, key):
        return self.data[key]

    def SetCurrRunData(self, **value):
        curr_data= self.data["CurrRunData"]
        for item in value:
            if item in ("ModuleName", "TotalTimes" ,"SucessTimes", "CaseName", "Cricle"):
                curr_data[item] = value[item]

    def GetCurrRunData(self, key):
        curr_data= self.data["CurrRunData"]
        if key in ("ModuleName", "TotalTimes" ,"SucessTimes", "CaseName", "Cricle"):
            return curr_data[key]

    def SetCurrRunDataInFlow(self , **value):
        def SetCurrRunDataInFlow_wrapper(flow):
            self.SetCurrRunData(**value)
            return True
        return SetCurrRunDataInFlow_wrapper

    def ToJson(self):
        return self.data

    def JsonDumpToFile(self):
        with open(self.jsonfilename , "wb") as fb:
            json.dump(self.ToJson(), fb , indent=4, separators=(',', ':'))

    def JsonLoadFromFile(self, filename):
        with open(filename , "rb") as fb:
            self.data = json.load(fb)
        self.jsonfilename = filename

    def GetJsonFileName(self):
        return self.jsonfilename

LJson = LogDataToJson()
