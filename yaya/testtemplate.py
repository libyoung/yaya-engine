#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170515
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################
from adbfunction import *
from deviceaction import *
from frameworkkey import *
from dump import Dump
from devicemanage import *
from log import *
from logdatatojson import LJson
from uiobjectaction import PRE_CHECK_UIOBJECT_TIME_MSEC
import json
import importlib

def Setup(flow):
    """Setup"""
    LogStart(flow)
    if flow.share_que != None:
        flow.share_que.put({'modulename':flow.info['name'], 'status':'Start'})
    return ReadyAll
    #mtel.switch_enhance_lte('off')


def Teardown(flow):
    """Teardown"""
    LogFinish(flow)
    #mtel = util.tcget(tcname, 'MDEVICE')
    #mtel.switch_enhance_lte('on')


class StabilityTestTemplate(object):
    '''
    '''
    def __init__(self, caselist, setup=None, teardown=None, callback=None):
        self.setup = setup
        self.teardown = teardown
        self.caselist = caselist
        self.callback = callback

    def __run_case__(self, flow, caseName, maxitimes, minitimes, caseflow, notsuccess_handler):
        if flow.info['mode'] == 'maxi':
            times = maxitimes
        else:
            times = minitimes

        return LJson.SetCurrRunDataInFlow(CaseName=caseName), FOR(times)(
                    SWITCH()[
                        NOT(*caseflow), 
                        Failes(caseName),
                        Dump(flow.dm.runde), 
                        notsuccess_handler,
                    ]
                    [
                        Passes, Wait(5)
                    ]
                ), SwitchMDevice

    def __call__(self, flow):
        '''
        '''
        runflow = [Setup, self.setup]
        for case in self.caselist:
            runflow.append(self.__run_case__(flow, *case))
        runflow.append(self.teardown)
        runflow.append(Teardown)
        return runflow


class FailCaseAgainRun(object):

    def __init__(self, script_files, json_file):
        self.script_files = script_files
        self.json_file = json_file
        self.fail_case_list = self.__load_fail_case_from_json()
       

    def __get_script_file_mod(self, moduname):
        for file in self.script_files:
            if moduname in file and file.endswith('.py'):
                return file, importlib.import_module(file.replace('.py',''))


    def __load_fail_case_from_json(self):
        fail_case_list = []
        with open(self.json_file , "rb") as fb:
            self.data = json.load(fb)

        for item in self.data['ModuleData']:
            if item['FailCase']:
                fail_case_list.append((item['ModuleName'],item['FailCase']))
        return fail_case_list

    def get_fail_case_again_run_lists(self):
        '''
        '''
        run_lists = []
        for moduname, fail_cases in self.fail_case_list:
            case_list = []
            file, mod = self.__get_script_file_mod(moduname)
            for item in mod.case_list:
                if item[0] in fail_cases:
                    case_list.append((item[0],item[1],fail_cases[item[0]],item[3],item[4]))
            ttim = sum([item[2] for item in case_list])
            run_list = StabilityTestTemplate(case_list, mod.setup, mod.teardown)
            run_lists.append((file, mod, moduname, ttim, run_list))

        return run_lists


class CompareUIObjectInfo(object):
    '''
    '''
    def __init__(self, fliter = 'text',**select):
        self.select = select
        self.info_fliter = fliter
        self.value_dict = {}

    def __DiffValue__(self):
        '''
        '''
        if not (self.value_dict.get('old') and self.value_dict.get('new')):
            return False
        if self.value_dict['old'] <= self.value_dict['new']:
            return True
        else:
            return False
    
    def __call__(self,*arg):
        '''
        '''
        def run_wrapper(flow):
            uiobject = flow.dm.GetRunDevice(**self.select)
            if uiobject.wait.exists(timeout=PRE_CHECK_UIOBJECT_TIME_MSEC):
                self.value_dict['old'] = uiobject.info[self.info_fliter]
            else:
                flow.log.GetLogger().debug("UIObject %s isn't exists!!!" , self.select)
                return False
            flow.Run(arg)
            if uiobject.wait.exists(timeout=PRE_CHECK_UIOBJECT_TIME_MSEC):
                self.value_dict['new'] = uiobject.info[self.info_fliter]
            else:
                flow.log.GetLogger().debug("UIObject %s isn't exists!!!" , self.select)
                return False
            return self.__DiffValue__()
        return run_wrapper

class SaveValue_Wrapper(dict):
    '''
    '''
    def __init__(self):
        self.value_dict = {}

    def DiffValue(self, flow):
        '''
        '''
        if not (self.value_dict.get('old') and self.value_dict.get('new')):
            return False
        if self.value_dict['old'] < self.value_dict['new']:
            return True
        else:
            return False

SaveValue = SaveValue_Wrapper()

def ReadyAll(flow):
    '''
    '''
    re_li = []
    for item in flow.dm.GetDeviceList:
        if item.GetDevice != None:
            re_li += [SwitchDevice(item.GetDeviceName),ClearBackgroundAPP()]
    re_li.append(SwitchMDevice)
    return re_li
