#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170629
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Log Object
##############################
import logging
from configparser import *
from xmlfile import StrAnalysis
import time
import datetime
from logdatatojson import LJson

def LogStart(flow):
    log = flow.log
    log.Start()
    log.GetLogger().info('Trace Total Times %s', flow.info['ttim'])

def LogFinish(flow):
    """Teardown"""
    log = flow.log.GetLogger()
    total = flow.info['ttim']
    fails = total - flow.log.success_times
    passing_rate = flow.log.success_times*1.0 / total
    if passing_rate < 0.95:
        log.warning('FAILED (passes = %d, failures = %d)', flow.log.success_times, fails)
        log.warning('Result Fail Success Rate Is %.2f%%', passing_rate * 100)
    else:
        log.info('PASSED (passes = %d, failures = %d)', flow.log.success_times, fails)
        log.info('Result Pass Success Rate Is %.2f%%', passing_rate * 100)
    log.info('Finished %s Test Case', 'Telephony')
    flow.log.Finish(flow, total)

def Passes(flow):
    '''
    '''
    t = flow.log.Pass()
    LJson.SetCurrRunData(SucessTimes=t)
    flow.log.GetLogger().info('#####################################')
    flow.log.GetLogger().info('Trace Success Loop %s', t)
    flow.log.GetLogger().info('#####################################')
    rate = (t*100)/flow.info['ttim']
    if flow.share_que != None:
        flow.share_que.put({'modulename':flow.info['name'], 'suc_time': t, 'total':flow.info['ttim'], 'passrate': rate})

def Failes(caseName):
    '''
    '''
    def FailesWarpper(flow):
        t = flow.log.Fail(caseName)
        flow.log.GetLogger().info('#####################################')
        flow.log.GetLogger().info('Trace Fail Loop %s', t)
        flow.log.GetLogger().info('#####################################')
    return FailesWarpper

class Logger(object):
    '''
    '''
    def __init__(self, info):
        self.modulename = info['name']
        if info['cuci'] == None:
            self.curr_loop = (1, "mini")
        else:
            self.curr_loop = (info['cuci'], 'Circle'+str(info['cuci']))
        self.log = self._GetLogInstace(info.get('lsos'))
        self.logadapter = logging.LoggerAdapter(self.log, {'devname':'MainFra'})
        self.success_times = 0
        self.fail_times = 0
        self.fail_cases = {}

    def _GetLogDir(self):
        """Get the path to the log folder."""
        """获取截图的文件夹路径"""
        logpath = os.environ.get('LOG_PATH')
        if logpath is None:
            logpath = sys.path[0]
        dirpath = os.path.join(logpath, 'scriptlog')
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath

    def _GetLogPath(self):
        """Take a screenshot and the UI hierarchy dump of the DUT."""
        """截图和当前界面的xml文件"""
        dirpath = self._GetLogDir()
        ISOTIMEFORMAT = '%Y%m%d%H%M%S'
        now_time = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        ssfile = '%s_%s_%s.txt' % (now_time, self.curr_loop[1], self.modulename)
        sspath = os.path.join(dirpath, ssfile)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return sspath


    def _GetLogInstace(self, logtostdout):
        """Retrieve Python logger."""
        """得到脚本中的log"""
        log = logging.getLogger(self.modulename)
        log.handlers = []
        if not len(log.handlers):
            log.setLevel(logging.DEBUG)
            log_format = ' '.join(['%(asctime)s', ':', '[%(levelname)-5s]',
                                '[%(name)s]', '[%(devname)s]',
                                '[%(funcName)s]', '%(message)s'])
            log_formatter = logging.Formatter(log_format)
            if logtostdout:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.DEBUG)
                stream_handler.setFormatter(log_formatter)
                log.addHandler(stream_handler)
            file_handler = logging.FileHandler(self._GetLogPath(), 'w')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(log_formatter)
            log.addHandler(file_handler)
        return log

    def LogAdapter(self,**kword):
        self.logadapter = logging.LoggerAdapter(self.log, kword)
        return self.logadapter

    def TempLogAdapter(self,**kword):
        return logging.LoggerAdapter(self.log, kword)

    def GetLogger(self):
        return self.logadapter

    def _datetime(self):
        t = time.time()
        msecs = (t - long(t)) * 1000
        strt = time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime(t))
        return (t, "%s,%03d" % (strt , msecs))

    def _timediff(self,time):
        t = int(time)
        h = t/3600
        m = (t%3600)/60
        s = t- 3600*h - m*60
        return "%s:%s:%s" % (h,m,s)

    def Pass(self):
        self.success_times += 1
        return  self.success_times

    def Fail(self, CaseName):
        self.fail_times += 1
        if self.fail_cases.get(CaseName):
            self.fail_cases[CaseName] += 1 
        else:
            self.fail_cases[CaseName] = 1
        return  self.fail_times

    def Start(self):
        self.starttime = self._datetime()
        self.TempLogAdapter(devname='MainFra').info("Start Run")

    def Finish(self, flow, total):
        self.finishtime = self._datetime()
        self.TempLogAdapter(devname='MainFra').info("Finish Run")
        circle_time = self.finishtime[0] - self.starttime[0]
        #StrAnalysis(self.modulename, self.curr_loop[0], self._timediff(circle_time), str(total), str(self.success_times), flow.xmlfile).addDataToXML(flow.info['modu'])
        LJson.AddModuleData(self.modulename, total, self.success_times, self._timediff(circle_time),   self.fail_cases, self.curr_loop[0])
        LJson.JsonDumpToFile()
