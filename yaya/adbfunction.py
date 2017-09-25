#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170427
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################
from uiautomator.adb import Adb
import configparser
import time
import subprocess
import os

def OpenAPP(appname, *arg, **kwargs):
    if appname == None:
        return None
    def OpenAPP_wrapper(flow):
        adb = ADBFunction()
        flow.log.GetLogger().debug("Launch %s APP" % appname)
        for _ in xrange(2):
            if flow.dm.GetRunDevice.info['currentPackageName'] in adb.__GetAppPackageandActivity__(appname):
                return True
            time.sleep(1)
        return adb.__StartActivity__(flow.dm.GetRunDeviceSerial, adb.__GetAppPackageandActivity__(appname))
    return OpenAPP_wrapper

def IsInCall(timeout=5, *arg, **kwargs):
    '''
    '''
    def IsInCall_wraper(flow):
        flow.log.GetLogger().debug("Check if the phone is incall status")
        adb = ADBFunction()
        return adb.__CallState__(flow.dm.GetRunDeviceSerial,'InCall', timeout)
    return IsInCall_wraper

def IsNoCall(timeout=5, *arg, **kwargs):
    '''
    '''
    def IsNoCall_wraper(flow):
        flow.log.GetLogger().debug("Check if the phone is Idle status")
        adb = ADBFunction()
        return not adb.__CallState__(flow.dm.GetRunDeviceSerial,'Idle', timeout)
    return IsNoCall_wraper

def InCallStay(timeout=5):
    '''
    '''
    def InCallStay_wrapper(flow):
        flow.log.GetLogger().debug("Check if the phone stay %ss in incall status" ,timeout)
        adb = ADBFunction()
        for _ in xrange(timeout):
            if not adb.__CallState__(flow.dm.GetRunDeviceSerial,'InCall', 1):
                return False
            time.sleep(0.9)
        return True
    return InCallStay_wrapper

def CallNumber(number):
    '''

    :param number:
    :return:
    '''
    def CallNumber_wrapper(flow):
        flow.log.GetLogger().debug("Dial %s" ,number)
        adb = ADBFunction()
        adb.__AdbCallNumber__(flow.dm.GetRunDeviceSerial, number)
        return adb
    return CallNumber_wrapper

def IsRinging(timeout=5, *arg, **kwargs):
    '''
    '''
    def IsRinging_wrapper(flow):
        flow.log.GetLogger().debug("Check if the phone is ringing status")
        adb = ADBFunction()
        return adb.__CallState__(flow.dm.GetRunDeviceSerial,'Ringing', timeout)
    return IsRinging_wrapper

def CallAnswer(*arg, **kwargs):
    '''
    '''
    def CallAnswer_wrapper(flow):
        flow.log.GetLogger().debug("Input KEYCODE_CALL to answer Call")
        adb = ADBFunction()
        return adb.__AdbInputKey__(flow.dm.GetRunDeviceSerial,'KEYCODE_CALL')
    return CallAnswer_wrapper

def EndCall(*arg, **kwargs):
    '''
    '''
    def EndCall_wrapper(flow):
        flow.log.GetLogger().debug("Input KEYCODE_ENDCALL to end Call")
        adb = ADBFunction()
        return adb.__AdbInputKey__(flow.dm.GetRunDeviceSerial,'KEYCODE_ENDCALL')
    return EndCall_wrapper

def Reboot(deviceid):
    '''
    '''
    def Reboot_wrapper(flow):
        flow.log.GetLogger().debug("reboot %s" ,deviceid)
        adb = ADBFunction()
        return adb.__Adbreboot__(flow.dm.GetRunDeviceSerial,deviceid)
    return Reboot_wrapper

def InstallAPK(deviceid):
    '''
    '''
    def Reboot_wrapper(flow):
        flow.log.GetLogger().debug("InstallAPK %s" ,deviceid)
        adb = ADBFunction()
        return adb.__InstallAPK__(flow.dm.GetRunDeviceSerial,deviceid)
    return Reboot_wrapper

def PushMedia(media, path, *arg, **kwargs):
    '''
    '''
    def Push(flow):
        if path == 'sdcard0' :
            storage = 'Internal storage'
        else :
            storage = 'SD card'
        flow.log.GetLogger().debug("Push %s to %s"%(media , storage))
        libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cmd = ' push %s/pre-cfg/%s/* /storage/%s' % (libpath ,media ,path)
        Adb(serial = flow.dm.GetRunDeviceSerial).cmd(cmd)
        time.sleep(2)
        return True
    return Push

def rotation_screen(value):
    '''value == 0 , not ratation screen ;
       value == 1 , ratation screen'''
    def rotation(flow):
        flow.log.GetLogger().debug("rotation screen")
        cmd = ' shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:%s'%(value)
        Adb(serial = flow.dm.GetRunDeviceSerial).cmd(cmd)
        time.sleep(3)
        return True
    return rotation

class ADBFunction(object):
    '''
    '''
    def __StartActivity__(self, serial, pkgact):
        """Start an app.

        Args:
            pkg (str): Package name of the app.
            act (str): Activity name.
        """
        """启动包名为pkg类名为act的activity"""
        cmd = ' shell am start -n %s' % pkgact
        Adb(serial=serial).cmd(cmd)
        time.sleep(1)
        return True

    def __GetAppPackageandActivity__(self, appname='call'):
        return configparser.Get("apps.ini","App List", appname)
    
    def __CallState__(self, serial ,status, timeout):
        '''`
        Check the phone call status.
        '''
        cmd = ' shell dumpsys telephony.registry'
        for _ in xrange(timeout):
            res = Adb(serial=serial).cmd(*cmd.split()).communicate()[0]
            ret = None
            if 'mCallState=0' in res:
                ret = 'Idle'
            elif 'mCallState=1' in res:
                ret = 'Ringing'
            elif 'mCallState=2' in res:
                ret = 'InCall'
            if ret.lower() in status.lower():
                return True
            time.sleep(0.9)
        return False

    def __AdbInputKey__(self, serial, key):
        """
        input all kinds of KEY
        """
        cmd = ' shell input keyevent ' + key
        Adb(serial=serial).cmd(*cmd.split()).communicate()
        return True

    def __AdbCallNumber__(self, serial, number):

        cmd = ' shell am start -a android.intent.action.CALL -d tel:%s ' % number
        Adb(serial=serial).cmd(*cmd.split()).communicate()
        return True

    def __Adbreboot__(self, serial,deviceid):

        cmd = '-s %s reboot ' % deviceid
        Adb(serial=serial).cmd(*cmd.split()).communicate()
        return True

    def __InstallAPK__(self, serial,deviceid):
        libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cmd = '-s %s install %s/pre-cfg/APKtest.apk ' % (deviceid,libpath)
        Adb(serial=serial).cmd(*cmd.split()).communicate()
        return True

if __name__ == '__main__':
    OpenAPP("Call")("GEZPWKJ78SZPCUIV")

