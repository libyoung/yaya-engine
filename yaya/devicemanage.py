#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170427
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################
from uiautomator import Device
from watcher import Watcher
from log import *

__all__ = ["SwitchSDevice","SwitchMDevice","SwitchThreeDevice","SwitchFourDevice","SDevice","MDevice","ThreeDevice","FourDevice","SDevice2","MDevice2","ThreeDevice2","FourDevice2","SwitchDevice","DeviceManage"]

def SwitchSDevice(flow):
    flow.log.GetLogger().debug("Switch SDevice")
    flow.dm.SwitchRunDevice("SDevice")
    flow.log.LogAdapter(devname=flow.dm.GetRunDeviceName)
    return True

def SwitchMDevice(flow):
    flow.log.GetLogger().debug("Switch MDevice")
    flow.dm.SwitchRunDevice("MDevice")
    flow.log.LogAdapter(devname=flow.dm.GetRunDeviceName)
    return True


def SwitchThreeDevice(flow):
    flow.log.GetLogger().debug("Switch Three Device")
    flow.dm.SwitchRunDevice("ThreeDevice")
    flow.log.LogAdapter(devname=flow.dm.GetRunDeviceName)
    return True

def SwitchFourDevice(flow):
    flow.log.GetLogger().debug("Switch Four Device")
    flow.dm.SwitchRunDevice("FourDevice")
    flow.log.LogAdapter(devname=flow.dm.GetRunDeviceName)
    return True


def SwitchDevice(name):
    '''
    '''
    def SwitchDeviceWarpper(flow):
        flow.log.GetLogger().debug("Switch %s" ,name)
        flow.dm.SwitchRunDevice(name)
        flow.log.LogAdapter(devname=flow.dm.GetRunDeviceName)
        return True
    return SwitchDeviceWarpper

class SwitchDeviceWrapper(object):
    '''
    Switch Device
    '''
    def __init__(self, *args):
        self.args = list(args)

    def __call__(self, flow):
        name = flow.dm.GetRunDeviceName
        if name == self.name:
            return flow.Run(self.args)
        else:
            return flow.Run((SwitchDevice(self.name), self.args, SwitchDevice(name)))

class SwitchDeviceWrapper2(object):
    '''
    Switch Device
    '''
    def __init__(self, deviceclass):
        self.deviceclass = deviceclass

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.deviceclass(*key)
        else:
            return self.deviceclass(key)

MDevice = type("MDevice", (SwitchDeviceWrapper,), {"name": "MDevice"})
SDevice = type("SDevice", (SwitchDeviceWrapper,), {"name": "SDevice"})
ThreeDevice = type("ThreeDevice", (SwitchDeviceWrapper,), {"name": "ThreeDevice"})
FourDevice = type("FourDevice", (SwitchDeviceWrapper,), {"name": "FourDevice"})

MDevice2 = SwitchDeviceWrapper2(MDevice)
SDevice2 = SwitchDeviceWrapper2(SDevice)
ThreeDevice2 = SwitchDeviceWrapper2(ThreeDevice)
FourDevice2 = SwitchDeviceWrapper2(FourDevice)

class DeviceInfo(object):
    '''
    '''
    def __init__(self, serial, name):
        self._serial = serial
        self.name = name
        if self._serial != None and self._serial != '':
            self._device = Device(self._serial)
            self._watcher = Watcher(self._device)
        else:
            self._device = None
            self._watcher = None
    
    @property
    def GetDevice(self):
        '''
        '''
        return self._device

    @property
    def GetDeviceName(self):
        '''
        '''
        return self.name

    @property
    def GetDeviceSerial(self):
        '''
        '''
        return self._serial

    @property
    def GetDeviceWatcher(self):
        '''
        '''
        return self._watcher

class DeviceManage(object):
    '''
    '''
    def __init__(self, MDeviceSerial, SDeviceSerial = None, ThreeDeviceSerial = None, FourDeviceSerial = None):
        self.devlist= []
        self.devlist.append(DeviceInfo(MDeviceSerial, 'MDevice'))
        self.devlist.append(DeviceInfo(SDeviceSerial, 'SDevice'))
        self.devlist.append(DeviceInfo(ThreeDeviceSerial, 'ThreeDevice'))
        self.devlist.append(DeviceInfo(FourDeviceSerial, 'FourDevice'))
        self.runde = self.devlist[0]

    @property
    def GetRunDeviceName(self):
        '''
        '''
        return self.runde.GetDeviceName

    @property
    def GetRunDevice(self):
        '''
        '''
        return self.runde.GetDevice

    @property
    def GetRunDeviceSerial(self):
        '''
        '''
        return self.runde.GetDeviceSerial

    @property
    def GetRunDeviceWatcher(self):
        '''
        '''
        return self.runde.GetDeviceWatcher

    @property
    def GetRunDeviceInfo(self):
        '''
        '''
        return self.runde.GetDeviceName, self.runde.GetDeviceSerial, self.runde.GetDevice, self.runde.GetDeviceWatcher

    @property
    def GetMDevice(self):
        '''
        '''
        return self.devlist[0]

    @property
    def GetSDevice(self):
        '''
        '''
        return self.devlist[1]

    @property
    def GetThreeDevice(self):
        '''
        '''
        return self.devlist[2]

    @property
    def GetFourDevice(self):
        '''
        '''
        return self.evlist[3]

    @property
    def GetDeviceList(self):
        '''
        '''
        return self.devlist

    def SwitchRunDevice(self, devicename):
        '''
        '''
        if devicename == "MDevice":
            if not (self.devlist[0].GetDeviceSerial and self.devlist[0].GetDevice and self.devlist[0].GetDeviceWatcher):
                raise Exception("Mdevices isn't exists!")
            self.runde = self.devlist[0]
        elif devicename == "SDevice":
            if not (self.devlist[1].GetDeviceSerial and self.devlist[1].GetDevice and self.devlist[1].GetDeviceWatcher):
                raise Exception("Sdevices isn't exists!")
            self.runde = self.devlist[1]
        elif devicename == "ThreeDevice":
            if not (self.devlist[2].GetDeviceSerial and self.devlist[2].GetDevice and self.devlist[2].GetDeviceWatcher):
                raise Exception("Three devices isn't exists!")
            self.runde = self.devlist[2]
        elif devicename == "FourDevice":
            if not (self.devlist[3].GetDeviceSerial and self.devlist[3].GetDevice and self.devlist[3].GetDeviceWatcher):
                raise Exception("Four devices isn't exists!")
            self.runde = self.devlist[3]
        