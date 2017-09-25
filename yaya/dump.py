#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170627
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Dump Object
##############################
from datetime import datetime
import os
import sys
import glob
import shutil
from uiautomator.adb import Adb

class Dump(object):
    '''
    '''
    def __init__(self, dev, flag=True):
        self.dev = dev
        self.devname = dev.GetDeviceName
        self.flag = flag

    def __call__(self, flow):
        '''
        '''
        self.log = flow.log.TempLogAdapter(devname=self.devname+"Dump")
        self.__screendump(flow.info['name'])
        if self.flag:
            self.__logdump(flow.info['name'])

    def __screendump_path(self):
        """Get the path to the screendump folder."""
        """获取截图的文件夹路径"""
        logpath = os.environ.get('LOG_PATH')
        if logpath is None:
            logpath = sys.path[0]
        dirpath = os.path.join(logpath, 'screendump')
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath


    def __get_logfile_paths(self,opt=None):
        """Get the paths to all the TAT logcat logs."""
        """获取TATlog保存的路径"""
        logpath = os.environ.get('LOG_PATH')
        if logpath is None:
            logpath = sys.path[0]
        logfiles = glob.glob(os.path.join(logpath, '*Device*.txt'))
        logfiles += glob.glob(os.path.join(logpath, '*begin*'))
        logfiles += glob.glob(os.path.join(logpath, '*TestData*'))
        if opt:
            logfiles += glob.glob(os.path.join(logpath, '*%s*' % opt))
        return logfiles


    def __tempdump_path(self):
        """Get the path to the tempdump folder."""
        logpath = os.environ.get('LOG_PATH')
        if logpath is None:
            logpath = sys.path[0]
        dirpath = os.path.join(logpath, 'tempdump')
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath


    def __logdump_path(self):
        """Get the path to the logdump folder."""
        """"""
        logpath = os.environ.get('LOG_PATH')
        if logpath is None:
            logpath = sys.path[0]
        dirpath = os.path.join(logpath, 'logdump')
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath

    def __screendump(self, dirname):
        """Take a screenshot and the UI hierarchy dump of the DUT."""
        """截图和当前界面的xml文件"""
        curtime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        dirpath = self.__screendump_tcdir(dirname)
        ssfile = '%s_%s.png' % (self.devname, curtime)
        sspath = os.path.join(dirpath, ssfile)
        self.dev.GetDevice.screenshot(sspath)
        dpfile = '%s_%s.xml' % (self.devname, curtime)
        dppath = os.path.join(dirpath, dpfile)
        self.dev.GetDevice.dump(filename=dppath, compressed=False, pretty=True)
        self.log.info('[Screen] %s', sspath)
        self.log.info('[Dump] %s', dppath)

    def __logdump(self, dirname):
        """Take various logs at certain point in time."""
        """打log"""
        curtime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        dirpath = self.__logdump_tcdir(dirname)
        logfpath = os.path.join(dirpath, curtime)
        if not os.path.exists(logfpath):
            os.makedirs(logfpath)
        ssfile = '%s_%s.png' % (self.devname, curtime)
        sspath = os.path.join(logfpath, ssfile)
        self.dev.GetDevice.screenshot(sspath)
        dpfile = '%s_%s.xml' % (self.devname, curtime)
        dppath = os.path.join(logfpath, dpfile)
        self.dev.GetDevice.dump(filename=dppath, compressed=False, pretty=True)
        log_cmds = [
            ('shell bugreport', 'bugreport.txt'),
            ('shell dmesg', 'kernel.txt'),
            ('shell ps', 'ps.txt'),
            ('shell dumpsys activity service android.phone.TelephonyDebugService', 'ateldumpsys.txt')
        ]
        for i, (cmd, filename) in enumerate(log_cmds):
            response = Adb(self.dev.GetDeviceSerial).cmd(*cmd.split()).communicate()[0]
            with open(os.path.join(logfpath, filename), 'w') as fd:
                fd.write(response)
        for logfile_path in self.__get_logfile_paths(opt=dirname):
            shutil.copy2(logfile_path, logfpath)
        self.log.info('[LogDump] %s', logfpath)


    def __screendump_tcdir(self , dirname):
        """Create a directory in the screendump folder titled as the TC name.
        """
        """创建截图文件夹"""
        sdpath = self.__screendump_path()
        sdtcdir = os.path.join(sdpath, dirname.lower())
        if not os.path.exists(sdtcdir):
            os.makedirs(sdtcdir)
        return sdtcdir

    def __logdump_tcdir(self, dirname):
        """创建log文件"""
        ldpath = self.__logdump_path()
        ldtcdir = os.path.join(ldpath, dirname.lower())
        if not os.path.exists(ldtcdir):
            os.makedirs(ldtcdir)
        return ldtcdir


    def __screenshot(self, dirname):
        """Take a screenshot of the DUT.

        Returns:
            sspath (str): Path to the screenshot.
        """
        """截图"""
        curtime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        tpddir = self.__tempdump_path()
        ssfile = '%s_%s_%s.png' % (dirname, self.devname, curtime)
        sspath = os.path.join(tpddir, ssfile)
        self.dev.GetDevice.screenshot(sspath)
        for _ in xrange(7):
            if os.path.exists(sspath):
                return sspath
            time.sleep(1)
        return None