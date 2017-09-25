#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170427
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################
from uiautomator import Selector
from uiobjectaction import *
from deviceaction import DeviceAction
from frameworkkey import *
from devicemanage import *
from dump import *
from log import *
import time
import datetime
import logging
from xmlfile import xmlFileInit
import traceback

def catchexcept(obj):
    def catchexcept_wrapper(self, *arg, **kword):
        try:
            return obj(self, *arg, **kword)
        except KeyboardInterrupt:
            raise
        except BaseException,e:
            if self.info['exce']:
                raise
            else:
                tra = traceback.format_exc()
                if tra != None:
                    self.log.GetLogger().info(" %s ", tra)
                Dump(self.dm.GetRunDevice)(self)
                return False

    return catchexcept_wrapper

class Flow(object):
    '''
    Android Phone Test Engine Framework
    '''
    def __init__(self, que, MDeviceSerial, SDeviceSerial = None, ThreeDeviceSerial=None, FourDeviceSerial=None, runinfo=None):
        '''
        Flow instance
        '''
        self.dm = DeviceManage(MDeviceSerial, SDeviceSerial, ThreeDeviceSerial, FourDeviceSerial)
        self.info = runinfo
        self.log = Logger(self.info)
        self.log.LogAdapter(devname=self.dm.GetRunDeviceName)
        self.xmlfile = self.info.get('xmlfile')
        self.share_que = que

    def __GetFields__(self,dict):
        '''
        Get some fields From a dict
        '''
        sel_dict = {}
        uio_dict = UIObjectAction()
        uio_fin_dict = UIObjectFinishAction()
        dev_dict = DeviceAction()
        for key in dict:
            if key in Selector._Selector__fields.keys():
                sel_dict[key] = dict[key]
                continue
            try:
                uio_dict[key] = dict[key]
            except:
                try:
                    uio_fin_dict[key] = dict[key]
                except:
                    dev_dict[key] = dict[key]
        return (sel_dict,uio_dict,uio_fin_dict,dev_dict)


    def __RunFlow__(self, kwargs, device = None):
        '''
        Run a list or tuple flow
        '''
        #self.log.GetLogger().debug("Run Flow")
        result = True
        #if device == None:
        #    device = self.dm.rundevice()
        for item in kwargs:
            result = self.Run(item)
            #self.log.GetLogger().debug("run %s cost time: %.4fs" % (item ,time.time()-starttime))
            if not result:
                break
        return result

    @catchexcept
    def Run(self, item, device = None):
        '''
        '''
        result = True
        if item == None or item == [] or item == {} or item == '':
            pass
        elif isinstance(item,list) or isinstance(item, tuple):
            result = self.__RunFlow__(item)
        elif isinstance(item, SWITCHWrapper):
            result = self.__SwitchFlow__(item(self))
        elif callable(item):
            #print("start time: %.5f" % time.time())
            result = item(self)
            time.sleep(0.2)
            result = self.Run(result)
        elif hasattr(item, "next"):
            result = self.__ForFlow__(item)
            #print("Finish time: %.5f" % time.time())
        elif isinstance(item, dict):
            #print("Start time: %.5f" % time.time())
            result = self.__RunStep__(item, self.dm.GetRunDevice)
            time.sleep(0.2)
            #print("Finish time: %.5f" % time.time())
        elif isinstance(item, str) or isinstance(item, unicode):
            self.log.GetLogger().info(item)
        elif isinstance(item, NOT):
            result = self.__NotFlow__(item)
        else:
            if not item:
                result = False
        return result

    def __RunStep__(self, kwargs, device = None):
        '''
        Execute a Step
        '''
        selector_field, uiobjectaction_field , uiobjectaction_finish_field, deviceaction_field = self.__GetFields__(kwargs)
        if selector_field:
            self.log.GetLogger().debug("operate %s " % selector_field)
            uiobject = device(**selector_field)
            return self.__OperateUIObject__(uiobject, selector_field, uiobjectaction_field,uiobjectaction_finish_field)
        elif deviceaction_field.IsHasAction():
            return self.__OperateDevice__(device, deviceaction_field)
        else:
            raise Exception, "UIObject %s isn't exists!!!" % selector_field
        return False
        

    def __OperateUIObject__(self, uiobject, selector_field, uio_field, uio_finish_field):
        '''
        Operate a UIObject
        '''
        single_oper_flag = True
        for per_oper in uio_field.GetAction():
                result = per_oper(self, uiobject, uio_field.get(per_oper),selector_field = selector_field)
                if result:
                    break
        if not result:
            return False
        if not uio_finish_field.IsHasAction():
            pass
        else:
            for per_oper in uio_finish_field.GetAction():
                result = per_oper(self, uiobject, uio_finish_field[per_oper])
                if not result:
                    return False
        return True

    def __OperateDevice__(self, device, dev_field):
        '''
        Operate a UIObject
        '''
        self.log.GetLogger().debug("Operate Device Action")
        if not dev_field.IsHasAction():
            pass
        else:
            for per_oper in dev_field.GetAction():
                result = per_oper(self, device, dev_field[per_oper])
                self.log.GetLogger().debug("Device operate: %s " % dev_field[per_oper])
                if not result:
                    return False
        return True

    def __ForFlow__(self, gene):
        '''
        Operate for circulation with generator
        '''
        result = False
        for item in gene:
            result = self.Run(item)
            if not result:
                break
        return result

    def __SwitchFlow__(self, gene):
        '''
        '''
        result = True
        for item in gene:
            if self.Run(item[0]):
                result = self.Run(item[1:])
                break
        return result

    def __NotFlow__(self, gene):
        '''
        '''
        for item in gene.args:
            result = self.Run(item)
            if not result:
                return True
        return False