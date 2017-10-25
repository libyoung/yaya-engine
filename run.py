#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import subprocess
from multiprocessing import Process,Queue
from ConfigParser import SafeConfigParser
import codecs
import signal
import datetime
import importlib
import traceback
from yaya import Flow
from yaya import xmlFileInit
from yaya import LJson
from yaya import write_data_to_xlsx_file
from yaya import FailCaseAgainRun
########################
# ini file Parser
########################
class NewSafeConfigParser(SafeConfigParser):
    def optionxform(self, optionstr):
        return optionstr

def cfg_get(filename, section, key, vtype=None):
    """Retrieve values from common.ini."""
    """检查从config.ini获取的值"""
    cfg = SafeConfigParser()
    cfgpath = os.path.join(sys.path[0], 'cfg', filename)
    if not os.path.isfile(cfgpath):
        raise IOError('%s NOT FOUND.' % cfgpath)
    with codecs.open(cfgpath, 'r', encoding='utf-8') as f:
        cfg.readfp(f)
    if vtype is None:
        return cfg.get(section, key)
    elif vtype == 'bool':
        return cfg.getboolean(section, key)
    elif vtype == 'float':
        return cfg.getfloat(section, key)
    elif vtype == 'int':
        return cfg.getint(section, key)

########################
# command line argv parse
########################
import argparse
from argparse import ArgumentDefaultsHelpFormatter
class CmdLineParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Argument Parser for yaya, you can deploy all argument in common.ini file',
                                              formatter_class=ArgumentDefaultsHelpFormatter)
        self.parser.add_argument('-mdev', help='specify Main test Device serial')
        self.parser.add_argument('-sdev', help='specify Suppplement test Device serial')
        self.parser.add_argument('-3dev', help='specify Third test Device serial')
        self.parser.add_argument('-4dev', help='specify Fourth test Device serial')
        self.parser.add_argument('-circ', help='specify the current test circle')
        self.parser.add_argument('-modu', help='specify test module name: "Telephony" or "PIM ..."')
        self.parser.add_argument('-mode', help='specify test mode: "maxi", "mini"')
        self.parser.add_argument('-exce', help='specify Exception Raise Flag is True or False, if it is True, raise exception in Test Script running, otherwise catch exception and dump to file')
        self.parser.add_argument('-reco', help='specify "circle,modules,jsonfilename" to recover run, example : -reco 3,WiFi,20170817105358_TestData.json')
        self.parser.add_argument('-lsos', help='switch on/off the log stream output to system stdout, example : -lsos False')
        self.parser.add_argument('-estr', help='switch export Stability Test excel report from json file , example : -estr 201708132156465.json')
        self.parser.add_argument('-acmp', help='switch on/off ANR and Crash monitor precess , example : -acmp False')
        self.parser.add_argument('-fcar', help='switch on/off Fail Case Again Run , example : -fcar 20170817105358_TestData.json')

    def parse(self, input):
        return self.parser.parse_args(input)

########################
#
########################
def get_script_file(modu,startmodu = None):
    files = os.listdir(sys.path[0])
    modules = modu.split(',')
    run_script_list = []
    for module in modules:
        for file in files:
            if module in file and file.endswith('.py'):
                run_script_list.append((module,file))
                break
    if startmodu != None:
        ind = modules.index(startmodu)
    else:
        ind=0
    return run_script_list[ind:]


def get_recover_info(info):
    '''
    '''
    recover_str = info.get('reco')

    if recover_str:
        recover_info=recover_str.split(',')
        LJson.JsonLoadFromFile(recover_info[2])
        info['circ'] = LJson.GetPlanData("PlanCricle")
        reco_cricle = int(recover_info[0]) - 1
        if reco_cricle <= 0:
            print "recover cricle is error"
            return None
        reco_modu = recover_info[1]
    else:
        LJson.InitModuleData(info['modu'])
        LJson.SetPlanData("PlanCricle",info['circ'])
        reco_cricle = 0
        reco_modu = None

    return (reco_cricle, reco_modu)


def create_all_deveics_monitor_ANR_Crash_process(info):
    m_ANR_p = None
    s_ANR_p = None
    three_ANR_p = None
    four_ANR_p = None

    if info['acmp']:
        m_ANR_p = create_monitor_ANR_Crash_process(info['mdev'])
        s_ANR_p = create_monitor_ANR_Crash_process(info['sdev'])
        three_ANR_p = create_monitor_ANR_Crash_process(info['3dev'])
        four_ANR_p = create_monitor_ANR_Crash_process(info['4dev'])

    return (m_ANR_p, s_ANR_p, three_ANR_p, four_ANR_p)


def run_script_for_fail_case(info, que=None):
    '''
    '''    
    create_all_deveics_monitor_ANR_Crash_process(info)
    
    files = os.listdir(sys.path[0])

    run_lists = FailCaseAgainRun(files, info.get('fcar')).get_fail_case_again_run_lists()

    LJson.SetJsonFileName("Again_" + info.get('fcar'))
    LJson.InitModuleData(info['modu'])

    info['cuci'] = 1
    for file, mod, moduname, ttim, run_list in run_lists:
        info['name'] = moduname
        info['mode'] = 'mini'
        info['ttim'] = ttim
        print "Run Script:%s, Test Total Times:%s" % (file,info['ttim'])
        LJson.SetCurrRunData(ModuleName=info['name'], TotalTimes=info['ttim'], Cricle=info['cuci'], CaseName='', SucessTimes=0)
        run_f = Flow(que, info['mdev'], info['sdev'], info['3dev'], runinfo = info)
        run_f.Run(run_list)
        if que != None:
            que.put({'modulename':info['name'], 'status':'Finish'})
        time.sleep(5)


def run_script(info, que=None):
    '''
    '''
    create_all_deveics_monitor_ANR_Crash_process(info)
    
    reco_cricle, reco_modu = get_recover_info(info)

    for i in xrange(reco_cricle, int(info['circ'])):
        info['cuci'] = i+1 
        print "Run Circle: %s" % (i+1)
        for item in get_script_file(info['modu'],reco_modu):
            if item[0] in info['modu']:
                info['name'] = item[0]
                mod = importlib.import_module(item[1].replace('.py',''))
                if info['mode'] == 'mini':
                    info['ttim'] = mod.module_mini_total_time
                else:
                    info['ttim'] = mod.module_total_time
                #info['xmlfile'] = xmlfile
                print "Run Script:%s, Test Total Times:%s" % (item[1],info['ttim'])
                #add xmlfile name ttim
                LJson.SetCurrRunData(ModuleName=info['name'], TotalTimes=info['ttim'], Cricle=info['cuci'], CaseName='', SucessTimes=0)
                run_f = Flow(que, info['mdev'], info['sdev'], info['3dev'], runinfo = info)
                run_f.Run(mod.run_list)

                if que != None:
                    que.put({'modulename':info['name'], 'status':'Finish'})
                time.sleep(5)
        reco_modu = None

def monitor_ANR_Crash(deviceSerial):
    '''
    '''
    cmd = ["adb", "-s", deviceSerial, "shell", "am" , "monitor"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print "%s monitor ANR Crash process id: %s" % (deviceSerial, p.pid)
    try:
        while True:
            time.sleep(2)
            s = p.stdout.readline()
            if 'ERROR' in s:
                print "%s have ANR or Crash"
    except KeyboardInterrupt:
            #print "%s catch KeyboardInterrupt" % os.getpid()
            pass

def create_monitor_ANR_Crash_process(deviceSerial):
    if not deviceSerial:
        return "deviceSerial is error"
    pro_p = Process(target = monitor_ANR_Crash, args=(deviceSerial,))
    pro_p.daemon = False
    pro_p.start()
    time.sleep(2)
    print "check %s  ANR Crash process id: %s" % (deviceSerial, pro_p.pid)
    return pro_p


def logcat_system_event_crash(deviceSerial):
    '''
    '''
    cmd = "adb -s " + deviceSerial + " logcat -v threadtime -b system -b events -b crash"
    pid = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pid.communicate()
    time.sleep(3)
    return pid

def logcat_radio(deviceSerial):
    '''
    '''
    cmd = "adb -s " + deviceSerial + " logcat -v time -b radio"
    pid = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return pid

def hander_subprocess(signum, frame):
    '''
    '''
    #for item in process_pid:
    #    item.kill()
    #print signum
    print "Kill all process"
    print "int signal"
    LJson.JsonDumpToFile()
    os.killpg(os.getpid(), signal.SIGKILL)
    sys.exit(0)


def cmd_progress(que):
    bar_length=20
    percent = 0
    q = {}
    while True:
        q = que.get(block=True)
        if q.get('passrate') != None:
            percent= q.get('passrate')
        hashes = u'\u258A' * int( percent/100.0 * bar_length)
        spaces = u' ' * (bar_length - len(hashes))
        status_sym = u'\u279e'
        if q.get('status') == 'Finish':
            status_sym = u'\u2714'
        sys.stdout.write("\r %s [%-14s] : %s %d%%"%(status_sym, q.get('modulename'), hashes + spaces, percent))
        if q.get('status') == 'Finish':
            sys.stdout.write("\n")
            percent = 0
            q = {}
        sys.stdout.flush()

def string_to_bool(string):
    if string in ( 'False', 'false', '假'.decode('utf-8'), 'None', None, 0 , '0'):
        return False
    else:
        return True 


def get_run_info(**custom_info):
    info={}
    #first, run info all data from "common.ini" file
    info['mdev'] = cfg_get('common.ini', 'Run Info', 'mdev')
    info['sdev'] = cfg_get('common.ini', 'Run Info', 'sdev')
    info['3dev'] = cfg_get('common.ini', 'Run Info', '3dev')
    info['4dev'] = cfg_get('common.ini', 'Run Info', '4dev')
    info['mode'] = cfg_get('common.ini', 'Run Info', 'mode')
    info['circ'] = cfg_get('common.ini', 'Run Info', 'circ')
    info['modu'] = cfg_get('common.ini', 'Run Info', 'modu')
    info['exce'] = cfg_get('common.ini', 'Run Info', 'exce')
    info['lsos'] = cfg_get('common.ini', 'Run Info', 'lsos')
    info['acmp'] = cfg_get('common.ini', 'Run Info', 'acmp')

    #then, a part of run info data from commond line
    cmd_info = vars(CmdLineParser().parse(sys.argv[1:]))
    for item in cmd_info:
        if cmd_info[item] != None:
            info[item] = cmd_info[item]

    info['exce'] = string_to_bool(info['exce'])
    info['lsos'] = string_to_bool(info['lsos'])
    info['acmp'] = string_to_bool(info['acmp'])

    #last, a part of run info data from single script custom
    for item in custom_info:
        #for single script run , no allow recover "-reco"
        if item != 'reco':
            info[item] = custom_info[item]

    print "Test Mode:%s" % info['mode']
    return info

def main(**custom_info):
    '''
    '''
    try:
        #print "process group id: %s" % os.getpgrp()
        #print "master process id: %s" % os.getpid()
        #signal.signal(signal.SIGINT, hander_subprocess)

        info = get_run_info(**custom_info)

        if info.get('estr'):
            write_data_to_xlsx_file(*(info['estr'].split(',')))
            return None
        
        share_que = Queue()

        #run_p= Process(target = run_script_2, args=(MD,SD,share_que, loops, mode))
        #run_p.start()

        if not info.get('lsos'):
            probar_p = Process(target = cmd_progress, args=(share_que,))
            probar_p.daemon = True
            probar_p.start()
            time.sleep(1)

        if info.get('fcar'):
            run_script_for_fail_case(info, share_que)
        else:
            run_script(info, share_que)

    except Exception:
        print "main"
        tra = traceback.print_exc()
        if tra != None:
            print tra
    finally:
        print "Save test data to %s file" % LJson.GetJsonFileName()
        LJson.JsonDumpToFile()
        print "Kill all process"
        os.killpg(os.getpid(), signal.SIGKILL)
        sys.exit(0)

if __name__=='__main__':
    main()