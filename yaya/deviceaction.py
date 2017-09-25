#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170427
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Action Object
##############################
import uiautomator
import time
from uiobjectaction import *
U = uiautomator.U

__all__ = ["Back","Home","Point","Recent","Enter","Power","Menu","Search","Wait","OpenNotification","OpenQuickSettings","CheckExists","CheckGone","LongClickXY","SelectBackgroundAPP","ClearBackgroundAPP"]


#################################
# Key Action 
#################################
def Back(flow,*arg,**kwargs):
    flow.dm.GetRunDevice.press.back()
    flow.log.GetLogger().debug("Press Back Key")
    return True


def Home(flow,*arg,**kwargs):
    flow.dm.GetRunDevice.press.home()
    flow.dm.GetRunDevice.wait.idle()
    flow.log.GetLogger().debug("Press Home Key")


def Point(x,y,*arg,**kwargs):
    def Point_wrapper(flow):
        flow.dm.GetRunDevice.click(x,y)
        flow.log.GetLogger().debug("CLick (%s, %s) coordinate" % (x, y))
        return True
    return Point_wrapper

def Recent(flow,*arg,**kwargs):
    flow.dm.GetRunDevice.press.recent()
    flow.log.GetLogger().debug("Press Recent Key")
    time.sleep(1.5)
    return True

def Enter(flow,*arg,**kwargs):
    pass

def Power(flow,*arg,**kwargs):
    flow.dm.GetRunDevice.press.power()
    flow.log.GetLogger().debug("Press Power Key")
    return True

def Menu(flow,*arg,**kwargs):
    pass

def Search(flow,*arg,**kwargs):
    pass

class DeviceAction(dict):
    '''
    The class is to build parameters for KeyAction
    '''
    __fields = {
        Home: 0x01,
        Back: 0x02,
        Point: 0x04,
        Enter: 0x08,
        Recent: 0x10,
        Power: 0x20,
        Menu: 0x40,
        Search: 0x80,
    }
    __reverse_fields = {
        0x01: Home,
        0x02: Back,
        0x04: Point,
        0x08: Enter,
        0x10: Recent,
        0x20: Power,
        0x40: Menu,
        0x80: Search,
    }
    __mask = "mask"

    def __init__(self, **kwargs):
        super(DeviceAction, self).__setitem__(self.__mask, 0)
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, k, v):
        if k in self.__fields:
            super(DeviceAction, self).__setitem__(U(k), U(v))
            super(DeviceAction, self).__setitem__(self.__mask, self[self.__mask] | self.__fields[k])
        else:
            raise ReferenceError("%s is not allowed." % k)

    def __delitem__(self, k):
        if k in self.__fields:
            super(DeviceAction, self).__delitem__(k)
            super(DeviceAction, self).__setitem__(self.__mask, self[self.__mask] & ~self.__fields[k])

    def IsHasAction(self):
        return len(self) - 1

    def GetAction(self):
        mask = self[self.__mask]
        for item in range(mask.bit_length()):
            b = 1 << item
            if mask & b == b:
                yield self.__reverse_fields[b]

#################################
# Other Action 
#################################
def CheckExists(**item):
    '''
    '''
    def CheckExists_wrapper(flow):
        if flow.dm.GetRunDevice(**item).wait.exists(timeout=3000):
            return True
        else:
            flow.log.GetLogger().debug("UIObject %s isn't exists!!!" , item)
            return False
        return True
    return CheckExists_wrapper

def CheckGone(**item):
    '''
    '''
    def CheckGone_wrapper(flow):
        if flow.dm.GetRunDevice(**item).wait.Gone(timeout=3000):
            return True
        else:
            flow.log.GetLogger().debug("UIObject %s isn't exists!!!" , item)
            return False
        return True
    return CheckGone_wrapper

def Wait(sec=3):
    def Wait_wrapper(flow):
        time.sleep(sec)
        return True
    return Wait_wrapper

def OpenNotification(flow):
    return flow.dm.GetRunDevice.open.notification()

def OpenQuickSettings(flow):
    return flow.dm.GetRunDevice.open.quick_settings()

def LongClickXY(x,y):
    def LongCLick_warpper(flow):
        return flow.dm.GetRunDevice.long_click(x,y)
    return LongCLick_warpper

def SelectBackgroundAPP(appname):
    def SelectBackgroundAPP_warpper(flow):
        return Recent,{'className':"android.widget.ScrollView", Scroll: {'textContains':appname}},{'textContains':appname}
    return SelectBackgroundAPP_warpper

def ClearBackgroundAPP(appname='all'):
    def ClearBackgroundAPP_warpper(flow):
        if appname == 'all':
            return Recent,Point(365,1072)
        else:
            return Recent,{'className':"android.widget.ScrollView", Scroll: {'textContains':appname}},{'textContains':appname, Swipe:'left'}
    return ClearBackgroundAPP_warpper
def rotation_screen(value):
    '''value == 0 , not ratation screen ;
       value == 1 , ratation screen'''
    def rotation(flow):
        flow.log.GetLogger().debug("rotation screen")
        cmd = ' shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:%s'%(value)
        Adb(serial = flow.dm.GetRunDeviceSerial).cmd(cmd)
        time.sleep(2)
        return True
    return rotation

if __name__ == "__main__":
     #a = UIObjectAction()
     #a[Click]=1
     #b = a.get_action()
     #c = b.next()
     #print c
     pass